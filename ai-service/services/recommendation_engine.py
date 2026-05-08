import os
from knowledge.sector_benchmarks import format_benchmark_for_prompt
from knowledge.regulations import format_regulations_for_prompt
from knowledge.best_practices import format_best_practices_for_prompt
from knowledge.technologies import format_technologies_for_prompt
from services.mistral_client import call_mistral, extract_json

# Map axis scores to maturity level labels
def _score_to_level(score: float) -> str:
    if score <= 20: return "INITIAL"
    if score <= 40: return "BASIQUE"
    if score <= 60: return "INTERMEDIAIRE"
    if score <= 80: return "AVANCE"
    return "OPTIMISE"


class RecommendationEngine:
    def __init__(self):
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    async def generate(self, request) -> dict:
        knowledge_context = self._build_knowledge_context(request)
        prompt = self._build_prompt(request, knowledge_context)

        raw = await call_mistral(
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            model=self.model,
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

Réponds UNIQUEMENT en JSON valide.
"""

    def _build_prompt(self, req, knowledge_context: str) -> str:
        sub_axis_summary = ""
        if req.sub_axis_scores:
            weak = [s for s in req.sub_axis_scores if s.get("score", 100) < 50]
            if weak:
                sub_axis_summary = "\nSous-axes faibles (<50) : " + ", ".join(
                    f"{s['subAxis']} ({s['score']:.0f}/100)" for s in weak[:5]
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
{sub_axis_summary}

BASE DE CONNAISSANCES CONTEXTUALISÉE :
{knowledge_context}
{consultant_section}
INSTRUCTIONS :
- Génère 2 à 4 recommandations par axe selon les scores (plus le score est bas, plus de recommandations HAUTE priorité)
- Pour les scores > 75, génère 1 recommandation BASSE priorité (maintien de l'excellence)
- Ignore les axes dont le score est 0 (non évalués)
- Cite des outils concrets (Salesforce, Power BI, UiPath, Azure AD, etc.) dans best_practice
- Mentionne les réglementations applicables dans les recommandations SI et Processus
- Inclue les benchmarks sectoriels pour contextualiser l'écart de performance
- Adapte les recommandations au secteur {req.sector} et au contexte de {req.country}

Réponds avec ce JSON exact :
{{
  "recommendations": [
    {{
      "axis": "METIER",
      "priority": "HAUTE",
      "title": "...",
      "description": "...",
      "best_practice": "..."
    }}
  ]
}}

Les valeurs possibles pour axis : METIER, PROCESSUS, SI, CANAUX, MARKETING, RH, OFFRES
Les valeurs possibles pour priority : HAUTE, MOYENNE, BASSE
"""

    def _normalize(self, items: list) -> list:
        valid_axes = {"METIER", "PROCESSUS", "SI", "CANAUX", "MARKETING", "RH", "OFFRES"}
        valid_priorities = {"HAUTE", "MOYENNE", "BASSE"}
        result = []
        for item in items:
            axis = item.get("axis", "METIER").upper()
            priority = item.get("priority", "MOYENNE").upper()
            result.append({
                "axis": axis if axis in valid_axes else "METIER",
                "priority": priority if priority in valid_priorities else "MOYENNE",
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "best_practice": item.get("best_practice", "")
            })
        return result
