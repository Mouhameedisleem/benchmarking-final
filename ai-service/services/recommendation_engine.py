import os
from knowledge.sector_benchmarks import format_benchmark_for_prompt
from knowledge.regulations import format_regulations_for_prompt
from knowledge.best_practices import format_best_practices_for_prompt
from knowledge.technologies import format_technologies_for_prompt
from services.llm_client import call_llm as call_groq, extract_json, TaskType

# Only research firms, regulators and international bodies whose homepage
# is itself a credible reference. Technology vendors (Google, Microsoft, SAP…)
# are intentionally excluded — their homepages are not useful source pages.
_ORG_URLS: dict[str, str] = {
    # ── Cabinets conseil & analyse ───────────────────────────────────────────
    "mckinsey":             "https://www.mckinsey.com",
    "gartner":              "https://www.gartner.com",
    "bcg":                  "https://www.bcg.com",
    "boston consulting":    "https://www.bcg.com",
    "deloitte":             "https://www.deloitte.com",
    "pwc":                  "https://www.pwc.com",
    "kpmg":                 "https://www.kpmg.com",
    "ey ":                  "https://www.ey.com",
    "ernst & young":        "https://www.ey.com",
    "forrester":            "https://www.forrester.com",
    "idc":                  "https://www.idc.com",
    "accenture":            "https://www.accenture.com",
    "capgemini":            "https://www.capgemini.com",
    # ── Forums & organisations internationales ───────────────────────────────
    "wef":                  "https://www.weforum.org",
    "world economic forum": "https://www.weforum.org",
    "world bank":           "https://www.worldbank.org",
    "banque mondiale":      "https://www.worldbank.org",
    "imf":                  "https://www.imf.org",
    "ifc":                  "https://www.ifc.org",
    "gsma":                 "https://www.gsma.com",
    "itu":                  "https://www.itu.int",
    "union internationale des télécommunications": "https://www.itu.int",
    "ocde":                 "https://www.oecd.org",
    "oecd":                 "https://www.oecd.org",
    "african development":  "https://www.afdb.org",
    "afdb":                 "https://www.afdb.org",
    "union africaine":      "https://au.int",
    "african union":        "https://au.int",
    "uemoa":                "https://www.uemoa.int",
    "cedeao":               "https://www.ecowas.int",
    "ecowas":               "https://www.ecowas.int",
    # ── Régulateurs & normes ────────────────────────────────────────────────
    "anssi":                "https://www.ssi.gouv.fr",
    "iso":                  "https://www.iso.org",
    "cnil":                 "https://www.cnil.fr",
    "bceao":                "https://www.bceao.int",
    "european commission":  "https://ec.europa.eu",
    "commission européenne": "https://ec.europa.eu",
}

def _get_source_url(source: str) -> str:
    if not source:
        return ""
    s = source.lower()
    for key, url in _ORG_URLS.items():
        if key in s:
            return url
    return ""

# Map axis scores to maturity level labels
def _score_to_level(score: float) -> str:
    if score <= 20: return "INITIAL"
    if score <= 40: return "BASIQUE"
    if score <= 60: return "INTERMEDIAIRE"
    if score <= 80: return "AVANCE"
    return "OPTIMISE"


class RecommendationEngine:
    def __init__(self):
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def generate(self, request) -> dict:
        knowledge_context = self._build_knowledge_context(request)
        prompt = self._build_prompt(request, knowledge_context)

        # Use CONSULTANT_REVIEW chain (DeepSeek V3 priority) when the consultant
        # has provided custom directives — better instruction following matters more there.
        task = (
            TaskType.CONSULTANT_REVIEW
            if getattr(request, "consultant_prompt", None)
            else TaskType.RECOMMENDATIONS
        )

        has_directive = bool(getattr(request, "consultant_prompt", None))
        raw = await call_groq(
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.75 if has_directive else 0.6,
            model=self.model,
            task=task,
            use_cache=not has_directive,
        )
        data = extract_json(raw)
        return {
            "evaluation_id": request.evaluation_id,
            "recommendations": self._normalize(data.get("recommendations", []))
        }

    def _build_knowledge_context(self, req) -> str:
        """Assemble all knowledge base context for this evaluation."""
        blocks = []

        # 1. Sector benchmark (with company score for positioning)
        bench = format_benchmark_for_prompt(req.sector, req.country, req.global_score)
        if bench:
            blocks.append(bench)

        # 2. Applicable regulations
        regs = format_regulations_for_prompt(req.sector, req.country)
        if regs:
            blocks.append(regs)

        # 3. Best practices per axis (based on current maturity level)
        for axis_key, score in [
            ("BUSINESS", req.business_score),
            ("PROCESS", req.process_score),
            ("INFORMATION_SYSTEM", req.si_score),
            ("CANAUX_DISTRIBUTION", req.canaux_score),
            ("MARKETING_COMMUNICATION", req.marketing_score),
            ("RH_CULTURE_DIGITALE", req.rh_score),
            ("OFFRES_DIGITALES", req.offres_score),
            ("MODELE_OPERATIONNEL_INNOVATION", getattr(req, "modele_operationnel_score", 0.0)),
            ("IT_DATA", getattr(req, "it_data_score", 0.0)),
        ]:
            level = _score_to_level(score)
            bp = format_best_practices_for_prompt(axis_key, level, req.sector)
            if bp:
                blocks.append(bp)

        # 4. Recommended technologies per axis
        for axis_key, score in [
            ("BUSINESS", req.business_score),
            ("PROCESS", req.process_score),
            ("INFORMATION_SYSTEM", req.si_score),
            ("CANAUX_DISTRIBUTION", req.canaux_score),
            ("MARKETING_COMMUNICATION", req.marketing_score),
            ("RH_CULTURE_DIGITALE", req.rh_score),
            ("OFFRES_DIGITALES", req.offres_score),
            ("MODELE_OPERATIONNEL_INNOVATION", getattr(req, "modele_operationnel_score", 0.0)),
            ("IT_DATA", getattr(req, "it_data_score", 0.0)),
        ]:
            level = _score_to_level(score)
            tech = format_technologies_for_prompt(axis_key, level)
            if tech:
                blocks.append(tech)

        return "\n".join(blocks)

    def _system_prompt(self) -> str:
        return """Tu es un consultant expert en transformation digitale et en stratégie IA,
spécialisé dans les benchmarks de maturité digitale pour les entreprises africaines et européennes.

Tu génères des recommandations d'amélioration personnalisées, concrètes et actionnables,
en t'appuyant sur la base de connaissances fournie : benchmarks sectoriels, réglementations applicables,
meilleures pratiques par axe, et technologies de référence recommandées par Gartner, McKinsey, ANSSI et l'ISO.

Chaque recommandation doit être :
- Spécifique au score, au secteur et au pays de l'entreprise
- Fondée sur des meilleures pratiques et technologies concrètes (citées dans la base de connaissance)
- Priorisée (HAUTE / MOYENNE / BASSE) selon l'urgence et l'impact
- Actionnable à court ou moyen terme avec des technologies nommées
- Conforme aux réglementations applicables identifiées
- Accompagnée d'une source crédible : organisation reconnue + année

RÈGLE ABSOLUE : Si le message utilisateur contient une section "⚠️ DIRECTIVES PRIORITAIRES DU CONSULTANT",
ces directives ont PRIORITÉ ABSOLUE sur toutes les autres instructions.
Tu DOIS les appliquer immédiatement et de manière visible dans les recommandations générées.
Elles prévalent sur tout le reste — ignore tout conflit avec les instructions génériques.

Pour le champ source, cite UNIQUEMENT des organisations reconnues parmi :
McKinsey, Gartner, BCG, Deloitte, PwC, KPMG, EY, Forrester, IDC, Accenture, Capgemini,
WEF, World Bank, IMF, GSMA, ITU, OCDE, AFDB, UEMOA, CEDEAO,
ANSSI, ISO, CNIL, BCEAO, Commission Européenne.
N'invente JAMAIS une source fictive (ex: "Hsys Digital Benchmark", "Digital Africa Report").
Pour le champ source_url, mets toujours une chaîne vide "" — l'URL est gérée côté serveur.

Réponds UNIQUEMENT en JSON valide.
"""

    def _build_prompt(self, req, knowledge_context: str) -> str:
        sub_axis_summary = ""
        if req.sub_axis_scores:
            weak = [s for s in req.sub_axis_scores if s.get("score", 100) < 50]
            if weak:
                sub_axis_summary = "\nSous-axes faibles (<50) : " + ", ".join(
                    f"{s.get('sub_axis', s.get('subAxis', '?'))} ({s['score']:.0f}/100)" for s in weak[:5]
                )

        consultant_section = ""
        if getattr(req, "consultant_prompt", None):
            consultant_section = f"""
⚠️ DIRECTIVES PRIORITAIRES DU CONSULTANT (PRIORITÉ ABSOLUE) :
{req.consultant_prompt}

Ces directives définissent un contexte stratégique spécifique fourni par le consultant.
Tu DOIS adapter, reformuler et prioriser les recommandations en tenant compte de ces directives.
Elles prévalent sur toute instruction générique ci-dessus.
"""

        return f"""Génère des recommandations d'amélioration pour cette entreprise :

⚠️ CONTRAINTE CRITIQUE : Cette entreprise opère dans le secteur {req.sector.upper()}.
Toutes les recommandations, technologies et exemples DOIVENT être adaptés au secteur {req.sector}.
N'utilise JAMAIS de terminologie ou de solutions appartenant à d'autres secteurs
(ex: ne mentionne PAS de solutions bancaires, d'assurance ou de retail pour une entreprise Education).

CONTEXTE :
- Entreprise : {req.company_name}
- Secteur : {req.sector}
- Pays : {req.country}
- Niveau de maturité : {req.maturity_level}

SCORES :
- Score global : {req.global_score:.1f}/100
- Axe Métier (METIER) : {req.business_score:.1f}/100
- Axe Processus (PROCESSUS) : {req.process_score:.1f}/100
- Axe SI (SI) : {req.si_score:.1f}/100
- Axe Canaux & UX (CANAUX) : {req.canaux_score:.1f}/100
- Axe Marketing & Communication (MARKETING) : {req.marketing_score:.1f}/100
- Axe RH & Culture Digitale (RH) : {req.rh_score:.1f}/100
- Axe Offres Digitales (OFFRES) : {req.offres_score:.1f}/100
- Axe Modèle Opérationnel & Innovation (MODELE_OPERATIONNEL) : {getattr(req, 'modele_operationnel_score', 0.0):.1f}/100
- Axe IT & Data (IT_DATA) : {getattr(req, 'it_data_score', 0.0):.1f}/100
{sub_axis_summary}

BASE DE CONNAISSANCES CONTEXTUALISÉE :
{knowledge_context}

INSTRUCTIONS :
- Génère 2 à 4 recommandations par axe selon les scores (plus le score est bas, plus de recommandations HAUTE priorité)
- Pour les scores > 75, génère 1 recommandation BASSE priorité (maintien de l'excellence)
- Ignore les axes dont le score est 0 (non évalués)
- Cite des outils concrets (Salesforce, Power BI, UiPath, Azure AD, etc.) dans best_practice
- Mentionne les réglementations applicables dans les recommandations SI et Processus
- Inclue les benchmarks sectoriels pour contextualiser l'écart de performance
- Adapte les recommandations au secteur {req.sector} et au contexte de {req.country}
- Pour chaque recommandation, ajoute source (organisation + année) et source_url (URL officielle du domaine)
{consultant_section}
Réponds avec ce JSON exact :
{{
  "recommendations": [
    {{
      "axis": "METIER",
      "priority": "HAUTE",
      "title": "...",
      "description": "...",
      "best_practice": "...",
      "source": "<Organisation Année — ex: Gartner 2024, McKinsey Digital 2023, ANSSI 2024>",
      "source_url": "<https://url-officielle-domaine — ex: https://www.gartner.com>"
    }}
  ]
}}

Les valeurs possibles pour axis : METIER, PROCESSUS, SI, CANAUX, MARKETING, RH, OFFRES, MODELE_OPERATIONNEL, IT_DATA
Les valeurs possibles pour priority : HAUTE, MOYENNE, BASSE
"""

    def _normalize(self, items: list) -> list:
        valid_axes = {"METIER", "PROCESSUS", "SI", "CANAUX", "MARKETING", "RH", "OFFRES", "MODELE_OPERATIONNEL", "IT_DATA"}
        valid_priorities = {"HAUTE", "MOYENNE", "BASSE"}
        result = []
        for item in items:
            axis = item.get("axis", "METIER").upper()
            priority = item.get("priority", "MOYENNE").upper()
            source = item.get("source", "")
            # Always use the whitelist homepage URL — never trust LLM-generated paths
            source_url = _get_source_url(source)
            result.append({
                "axis": axis if axis in valid_axes else "METIER",
                "priority": priority if priority in valid_priorities else "MOYENNE",
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "best_practice": item.get("best_practice", ""),
                "source": source,
                "source_url": source_url,
            })
        return result
