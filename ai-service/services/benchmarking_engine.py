"""
Benchmarking Engine
Positions the company against national and international sector benchmarks.
Primary path: LLM-grounded analysis via Mistral (Gartner, McKinsey, WEF, OECD, BCG).
Fallback path: deterministic rule-based benchmark when the LLM is unavailable.
"""
import json
import os
from services.mistral_client import call_mistral, extract_json


# ── Sector reference data (Gartner DTI / McKinsey Digital Index 2023-2024) ────

_SECTOR_DATA = {
    "banking":     {"nat": 57, "intl": 68, "top": 83, "source": "McKinsey Global Banking Report 2024"},
    "insurance":   {"nat": 50, "intl": 62, "top": 78, "source": "Gartner Insurance Digital Maturity 2024"},
    "industry":    {"nat": 44, "intl": 57, "top": 74, "source": "WEF Advanced Manufacturing 2024"},
    "retail":      {"nat": 53, "intl": 66, "top": 81, "source": "McKinsey Retail Digital Index 2024"},
    "healthcare":  {"nat": 42, "intl": 55, "top": 72, "source": "Gartner Healthcare IT Maturity 2024"},
    "tech":        {"nat": 66, "intl": 76, "top": 89, "source": "IDC Digital Transformation Survey 2024"},
    "education":   {"nat": 38, "intl": 50, "top": 68, "source": "OECD Education Digital Readiness 2024"},
    "transport":   {"nat": 47, "intl": 60, "top": 76, "source": "WEF Mobility Futures Report 2024"},
    "energy":      {"nat": 49, "intl": 63, "top": 79, "source": "IEA Digital Energy Transformation 2024"},
    "construction":{"nat": 35, "intl": 48, "top": 66, "source": "McKinsey Construction Productivity 2024"},
}
_DEFAULT_DATA = {"nat": 50, "intl": 63, "top": 78, "source": "Gartner Digital Business Survey 2024"}

_SECTOR_TRENDS = {
    "banking": [
        {"title": "IA Générative dans les services financiers",
         "description": "Les banques intègrent ChatGPT et Claude pour l'analyse de risque, le KYC automatisé et le conseil client. 68% des grandes banques mondiales pilotent des cas d'usage IA générative.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "68% des grandes banques", "source": "McKinsey 2024"},
        {"title": "Open Banking & API Economy",
         "description": "La directive DSP2 et son évolution DSP3 accélèrent l'ouverture des systèmes bancaires. Les API banking permettent de nouveaux modèles de revenus en partenariat avec les fintechs.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "55% des banques européennes", "source": "Gartner 2024"},
        {"title": "Instant Payment généralisé",
         "description": "Le virement instantané devient la norme en Europe (règlement UE 2024). Les banques doivent adapter leurs systèmes de paiement en temps réel 24/7.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "72% des banques UE", "source": "BCE 2024"},
        {"title": "Cloud hybride bancaire",
         "description": "Migration progressive vers le cloud souverain pour les workloads critiques. Réduction des coûts d'infrastructure et flexibilité accrue pour les nouvelles offres.",
         "impact_level": "MOYEN", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "42% des banques", "source": "IDC 2024"},
    ],
    "insurance": [
        {"title": "InsurTech & tarification dynamique",
         "description": "L'utilisation de l'IA et de la télématique permet une tarification en temps réel basée sur les comportements réels des assurés.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "45% des assureurs", "source": "Gartner 2024"},
        {"title": "Automatisation des sinistres",
         "description": "Les processus de déclaration et d'indemnisation sont automatisés grâce à l'IA, réduisant les délais de traitement de 60%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "38% des assureurs", "source": "McKinsey 2024"},
    ],
    "default": [
        {"title": "IA Générative et automatisation cognitive",
         "description": "L'adoption de l'IA générative transforme les processus métier, de la relation client à l'analyse décisionnelle. Les entreprises leaders réduisent leurs coûts opérationnels de 25-35%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "52% des entreprises", "source": "McKinsey 2024"},
        {"title": "Cloud & Architecture microservices",
         "description": "La migration vers le cloud hybride et les architectures microservices devient un impératif compétitif. Elle permet l'agilité nécessaire pour lancer de nouveaux produits en semaines plutôt qu'en mois.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "61% des entreprises", "source": "Gartner 2024"},
        {"title": "Cybersécurité Zero Trust",
         "description": "La généralisation du télétravail et la multiplication des cyberattaques poussent les entreprises à adopter le modèle Zero Trust. Les budgets cybersécurité croissent de 15% par an.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "44% des entreprises", "source": "IDC 2024"},
        {"title": "Expérience client omnicanale",
         "description": "Les clients exigent une expérience fluide et personnalisée sur tous les canaux. Les entreprises leaders investissent dans le CRM unifié et l'analyse comportementale temps réel.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "67% des entreprises", "source": "Salesforce 2024"},
        {"title": "Data Mesh & gouvernance des données",
         "description": "La gouvernance décentralisée des données avec une architecture Data Mesh permet une exploitation plus agile des actifs données tout en garantissant conformité et qualité.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "28% des entreprises", "source": "Gartner 2024"},
    ]
}

_SECTOR_LEADERS = {
    "banking": [
        {"company": "DBS Bank", "country": "Singapour", "estimated_score": 91, "key_practice": "Banque 100% cloud-native avec IA embarquée dans tous les processus", "differentiator": "Digital bank of the year 5 années consécutives (Euromoney)", "source": "Gartner 2024"},
        {"company": "ING Group", "country": "Pays-Bas", "estimated_score": 86, "key_practice": "Plateforme de banking-as-a-service et API ouverte à 200+ fintechs", "differentiator": "Architecture agile Spotify transformée en modèle bancaire", "source": "McKinsey 2024"},
        {"company": "Capitec Bank", "country": "Afrique du Sud", "estimated_score": 83, "key_practice": "Digitalisation complète avec 8M+ clients actifs sur mobile", "differentiator": "Leader en inclusion financière digitale sur marchés émergents", "source": "BCG 2024"},
    ],
    "default": [
        {"company": "Amazon", "country": "USA", "estimated_score": 93, "key_practice": "Plateforme cloud AWS et culture data-driven à toutes les strates", "differentiator": "Pionnier du cloud computing et de l'IA appliquée à grande échelle", "source": "Gartner 2024"},
        {"company": "Siemens AG", "country": "Allemagne", "estimated_score": 87, "key_practice": "Jumeau numérique industriel et usine 4.0 intégralement connectée", "differentiator": "Leader mondial de la transformation digitale industrielle", "source": "WEF 2024"},
        {"company": "Ping An Group", "country": "Chine", "estimated_score": 89, "key_practice": "IA et big data intégrés dans tous les produits financiers et santé", "differentiator": "2 000+ chercheurs en IA — plus grand investisseur FinTech mondial", "source": "McKinsey 2024"},
    ]
}

_MATURITY_ROADMAP = {
    "INITIAL": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Établir les fondations digitales", "actions": ["Cartographier les processus manuels prioritaires à automatiser", "Déployer un ERP/CRM cloud de base", "Former les équipes aux outils numériques essentiels"], "gain": "+10 à +15 points", "target": "BASIQUE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Digitaliser les processus cœur de métier", "actions": ["Mettre en place une architecture data centralisée", "Lancer la migration cloud des applications critiques", "Créer un portail client digital avec self-service"], "gain": "+15 à +20 points", "target": "INTERMEDIAIRE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Intégrer l'IA dans les décisions métier", "actions": ["Déployer des modèles prédictifs pour l'analyse de risque", "Automatiser 60% des processus de back-office", "Mettre en place une gouvernance données mature"], "gain": "+20 à +25 points", "target": "AVANCE", "investment": "Élevé"},
    ],
    "BASIQUE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Consolider la base digitale et éliminer les silos", "actions": ["Unifier les sources de données dans un data lake centralisé", "Déployer des APIs pour l'intégration inter-systèmes", "Automatiser les reportings et tableaux de bord"], "gain": "+8 à +12 points", "target": "INTERMEDIAIRE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Développer les capacités analytiques avancées", "actions": ["Implémenter une plateforme BI self-service pour tous les métiers", "Lancer des pilotes IA/ML sur les cas d'usage à fort ROI", "Transformer l'expérience client en omnicanal seamless"], "gain": "+12 à +18 points", "target": "AVANCE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Atteindre l'excellence opérationnelle digitale", "actions": ["Industrialiser les modèles IA validés en production", "Déployer une architecture microservices full cloud", "Certifier la gouvernance des données (ISO 27001, RGPD)"], "gain": "+15 à +20 points", "target": "OPTIMISE", "investment": "Élevé"},
    ],
    "INTERMEDIAIRE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Optimiser et automatiser les processus clés", "actions": ["Déployer l'automatisation RPA sur les tâches répétitives", "Renforcer la cybersécurité (Zero Trust, SOC)", "Lancer un programme d'innovation interne (lab digital)"], "gain": "+5 à +10 points", "target": "AVANCE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Intégrer l'IA générative dans les produits/services", "actions": ["Pilotes IA générative pour support client et production de contenu", "Moderniser le SI legacy vers une architecture API-first", "Mettre en place un programme de data literacy pour les managers"], "gain": "+10 à +15 points", "target": "AVANCE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Devenir leader digital du secteur", "actions": ["Monétiser les données via de nouveaux modèles business", "Déployer des jumeaux numériques pour les opérations critiques", "Contribuer à des consortiums d'innovation sectorielle"], "gain": "+10 à +15 points", "target": "OPTIMISE", "investment": "Élevé"},
    ],
    "AVANCE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Industrialiser l'IA et les plateformes data", "actions": ["Déployer un MLOps pour la gestion du cycle de vie des modèles IA", "Étendre le Data Mesh à toutes les business units", "Lancer une offre data-as-a-service pour les partenaires"], "gain": "+5 à +8 points", "target": "OPTIMISE", "investment": "Élevé"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Créer de la valeur par l'innovation digitale", "actions": ["Développer des plateformes d'écosystème avec partenaires", "Adopter l'architecture Composable Enterprise (MACH)", "Mesurer et maximiser le ROI digital avec des OKRs data-driven"], "gain": "+5 à +7 points", "target": "OPTIMISE", "investment": "Modéré"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Rayonnement et leadership sectoriel", "actions": ["Partager les best practices via publications et conférences", "Nouer des partenariats R&D avec universités et startups", "Piloter des initiatives ESG digitales à impact mesurable"], "gain": "+3 à +5 points", "target": "OPTIMISE", "investment": "Faible"},
    ],
    "OPTIMISE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Maintenir l'avance technologique", "actions": ["Veille active sur les technologies émergentes (Quantum, Gen-AI)", "Benchmarking continu avec les leaders mondiaux", "Programme d'excellence continue (Kaizen digital)"], "gain": "+2 à +4 points", "target": "OPTIMISE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Exporter l'expertise digitale", "actions": ["Créer un centre d'excellence digital partageable", "Monétiser les actifs technologiques propriétaires", "Développer des partenariats stratégiques de co-innovation"], "gain": "+2 à +3 points", "target": "OPTIMISE", "investment": "Faible"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Façonner l'avenir du secteur", "actions": ["Contribuer aux standards et régulations sectorielles", "Investir dans les startups deep-tech du secteur", "Déployer des solutions ESG et d'impact digital mesurable"], "gain": "+2 à +3 points", "target": "OPTIMISE", "investment": "Faible"},
    ],
}


class BenchmarkingEngine:
    def __init__(self):
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    async def benchmark(self, request) -> dict:
        try:
            prompt = self._build_prompt(request)
            raw = await call_mistral(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.5,
                model=self.model,
            )
            data = extract_json(raw)
            return self._normalize(data, request)
        except Exception:
            # LLM unavailable or key invalid — use rule-based fallback
            return self._fallback_benchmark(request)

    # ── Fallback (rule-based) ──────────────────────────────────────────────────

    def _fallback_benchmark(self, request) -> dict:
        sector_key = (request.sector or "").lower().split()[0]
        sd = _SECTOR_DATA.get(sector_key, _DEFAULT_DATA)

        score     = float(request.global_score)
        nat_avg   = float(sd["nat"])
        intl_avg  = float(sd["intl"])
        top_q     = float(sd["top"])

        # Percentile + label
        if score >= top_q:
            percentile = min(99, 75 + int((score - top_q) / max(1, 100 - top_q) * 24))
            label = "Top quartile"
        elif score >= intl_avg:
            percentile = 55 + int((score - intl_avg) / max(1, top_q - intl_avg) * 20)
            label = "Au-dessus de la moyenne internationale"
        elif score >= nat_avg:
            percentile = 35 + int((score - nat_avg) / max(1, intl_avg - nat_avg) * 20)
            label = "Dans la moyenne"
        else:
            percentile = max(5, int(score / nat_avg * 35))
            label = "En dessous de la moyenne"

        # Axis benchmarks
        axis_benchmarks = []
        all_axis_scores = [
            ("METIER",    "Métier",                 float(request.business_score)),
            ("PROCESSUS", "Processus",              float(request.process_score)),
            ("SI",        "Système d'Information",  float(request.si_score)),
            ("CANAUX",    "Canaux & UX",            float(getattr(request, "canaux_score", 0) or 0)),
            ("MARKETING", "Marketing & Communication", float(getattr(request, "marketing_score", 0) or 0)),
            ("RH",        "RH & Culture Digitale",  float(getattr(request, "rh_score", 0) or 0)),
            ("OFFRES",    "Offres Digitales",        float(getattr(request, "offres_score", 0) or 0)),
        ]
        for axis, label, comp_score in all_axis_scores:
            if comp_score == 0:
                continue
            axis_benchmarks.append({
                "axis":           axis,
                "axis_label":     label,
                "company_score":  comp_score,
                "sector_average": nat_avg,
                "top_quartile":   top_q,
                "gap_to_average": round(comp_score - nat_avg, 1),
                "gap_to_top":     round(comp_score - top_q, 1),
            })

        # Trends
        trends = _SECTOR_TRENDS.get(sector_key, _SECTOR_TRENDS["default"])[:5]

        # Leaders
        leaders = _SECTOR_LEADERS.get(sector_key, _SECTOR_LEADERS["default"])

        # Roadmap — pick by maturity level (fallback to INTERMEDIAIRE)
        maturity = (request.maturity_level or "INTERMEDIAIRE").upper()
        roadmap_template = _MATURITY_ROADMAP.get(maturity, _MATURITY_ROADMAP["INTERMEDIAIRE"])
        roadmap = [
            {
                "phase":               p["phase"],
                "objective":           p["objective"],
                "actions":             p["actions"],
                "expected_score_gain": p["gain"],
                "target_level":        p["target"],
                "investment_level":    p["investment"],
            }
            for p in roadmap_template
        ]

        gap_nat = round(score - nat_avg, 1)
        gap_top = round(top_q - score, 1)
        gap_str = f"{'+' if gap_nat >= 0 else ''}{gap_nat}"

        if gap_nat >= 0:
            gap_sentence = "l'entreprise se distingue positivement et doit capitaliser sur ses forces pour consolider son leadership."
        else:
            gap_sentence = f"des actions prioritaires permettraient de combler l'écart de {abs(gap_nat):.0f} points avec la moyenne sectorielle."

        executive_summary = (
            f"{request.company_name} affiche un score de maturité digitale de {score:.0f}/100, "
            f"se positionnant au {percentile}ème percentile du secteur {request.sector}. "
            f"Avec un écart de {gap_str} points par rapport à la moyenne nationale ({nat_avg:.0f}/100), "
            f"{gap_sentence} "
            f"Pour atteindre le top quartile ({top_q:.0f}/100), un gain de {max(0, gap_top):.0f} points est nécessaire."
        )

        return {
            "company_name":   request.company_name,
            "sector":         request.sector,
            "country":        request.country,
            "global_score":   score,
            "maturity_level": request.maturity_level,
            "executive_summary": executive_summary,
            "sector_benchmark": {
                "national_average":      nat_avg,
                "international_average": intl_avg,
                "top_quartile_score":    top_q,
                "company_percentile":    max(5, min(99, percentile)),
                "positioning_label":     label,
                "source":                sd["source"],
            },
            "axis_benchmarks":    axis_benchmarks,
            "trends":             trends,
            "sector_leaders":     leaders,
            "improvement_roadmap": roadmap,
            "key_insights": [
                f"Score global {score:.0f}/100 — {label} dans le secteur {request.sector}.",
                f"Écart de {gap_str} pts vs moyenne nationale ; {max(0, gap_top):.0f} pts restants pour intégrer le top quartile.",
                "Axe prioritaire : renforcer les dimensions les plus en retard par rapport au benchmark sectoriel.",
            ],
        }

    # ── LLM prompts ────────────────────────────────────────────────────────────

    def _system_prompt(self) -> str:
        return (
            "Tu es un expert en benchmarking de maturité digitale. "
            "Produis des analyses de positionnement sectoriel rigoureuses pour les DSI. "
            "Sources : Gartner, McKinsey, WEF, OECD, BCG, IDC (2022-2024). "
            "Réponds UNIQUEMENT en JSON valide, sans texte hors JSON."
        )

    def _build_prompt(self, req) -> str:
        canaux   = getattr(req, "canaux_score",   0) or 0
        marketing = getattr(req, "marketing_score", 0) or 0
        rh       = getattr(req, "rh_score",       0) or 0
        offres   = getattr(req, "offres_score",    0) or 0

        # Only include evaluated axes (score > 0) in the axis_benchmarks template
        axis_lines = [
            '    {{"axis":"METIER","axis_label":"Métier","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
            '    {{"axis":"PROCESSUS","axis_label":"Processus","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
            '    {{"axis":"SI","axis_label":"Système d\'Information","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
        ]
        if canaux > 0:
            axis_lines.append('    {{"axis":"CANAUX","axis_label":"Canaux & UX","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if marketing > 0:
            axis_lines.append('    {{"axis":"MARKETING","axis_label":"Marketing & Communication","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if rh > 0:
            axis_lines.append('    {{"axis":"RH","axis_label":"RH & Culture Digitale","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if offres > 0:
            axis_lines.append('    {{"axis":"OFFRES","axis_label":"Offres Digitales","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')

        axes_template = ",\n".join(axis_lines)

        consultant_section = ""
        if getattr(req, "consultant_prompt", None):
            consultant_section = f"""
⚠️ DIRECTIVES PRIORITAIRES DU CONSULTANT (PRIORITÉ ABSOLUE) :
{req.consultant_prompt}

Ces directives définissent un contexte stratégique spécifique. Adapte l'analyse de benchmarking
(executive_summary, tendances, feuille de route, insights) en conséquence.
"""

        return f"""Produis une analyse de benchmarking pour cette entreprise.

PROFIL : {req.company_name} | Secteur: {req.sector} | Pays: {req.country}
SCORES :
- Global={req.global_score:.1f} | Métier={req.business_score:.1f} | Processus={req.process_score:.1f} | SI={req.si_score:.1f}
- Canaux={canaux:.1f} | Marketing={marketing:.1f} | RH={rh:.1f} | Offres={offres:.1f}
MATURITÉ : {req.maturity_level}
{consultant_section}

Génère ce JSON (respecte EXACTEMENT cette structure) :
{{
  "executive_summary": "3-4 phrases positionnant l'entreprise.",
  "sector_benchmark": {{"national_average": <float>, "international_average": <float>, "top_quartile_score": <float>, "company_percentile": <int>, "positioning_label": "...", "source": "..."}},
  "axis_benchmarks": [
{axes_template}
  ],
  "trends": [{{"title":"...","description":"...","impact_level":"ELEVE|MOYEN|FAIBLE","horizon":"...","adoption_rate":"...","source":"..."}}],
  "sector_leaders": [{{"company":"...","country":"...","estimated_score":<int>,"key_practice":"...","differentiator":"...","source":"..."}}],
  "improvement_roadmap": [{{"phase":"Phase 1 — Court terme (0-6 mois)","objective":"...","actions":["...","...","..."],"expected_score_gain":"+X points","target_level":"...","investment_level":"Faible|Modéré|Élevé"}}],
  "key_insights": ["insight 1","insight 2","insight 3"]
}}"""

    # ── Normalisation (LLM path) ───────────────────────────────────────────────

    def _normalize(self, data: dict, req) -> dict:
        sb = data.get("sector_benchmark", {})
        sector_benchmark = {
            "national_average":      float(sb.get("national_average", 55)),
            "international_average": float(sb.get("international_average", 65)),
            "top_quartile_score":    float(sb.get("top_quartile_score", 80)),
            "company_percentile":    int(sb.get("company_percentile", 50)),
            "positioning_label":     sb.get("positioning_label", "Dans la moyenne"),
            "source":                sb.get("source", "Gartner / McKinsey 2024"),
        }

        axis_benchmarks = [
            {
                "axis":           ab.get("axis", ""),
                "axis_label":     ab.get("axis_label", ab.get("axis", "")),
                "company_score":  float(ab.get("company_score", 0)),
                "sector_average": float(ab.get("sector_average", 0)),
                "top_quartile":   float(ab.get("top_quartile", 0)),
                "gap_to_average": float(ab.get("gap_to_average", 0)),
                "gap_to_top":     float(ab.get("gap_to_top", 0)),
            }
            for ab in data.get("axis_benchmarks", [])
        ]

        trends = [
            {
                "title":         t.get("title", ""),
                "description":   t.get("description", ""),
                "impact_level":  t.get("impact_level", "MOYEN"),
                "horizon":       t.get("horizon", "Moyen terme"),
                "adoption_rate": t.get("adoption_rate", ""),
                "source":        t.get("source", ""),
            }
            for t in data.get("trends", [])
        ]

        leaders = [
            {
                "company":         l.get("company", ""),
                "country":         l.get("country", ""),
                "estimated_score": int(l.get("estimated_score", 80)),
                "key_practice":    l.get("key_practice", ""),
                "differentiator":  l.get("differentiator", ""),
                "source":          l.get("source", ""),
            }
            for l in data.get("sector_leaders", [])
        ]

        roadmap = [
            {
                "phase":               p.get("phase", ""),
                "objective":           p.get("objective", ""),
                "actions":             p.get("actions", []),
                "expected_score_gain": p.get("expected_score_gain", ""),
                "target_level":        p.get("target_level", ""),
                "investment_level":    p.get("investment_level", "Modéré"),
            }
            for p in data.get("improvement_roadmap", [])
        ]

        return {
            "company_name":      req.company_name,
            "sector":            req.sector,
            "country":           req.country,
            "global_score":      float(req.global_score),
            "maturity_level":    req.maturity_level,
            "executive_summary": data.get("executive_summary", ""),
            "sector_benchmark":  sector_benchmark,
            "axis_benchmarks":   axis_benchmarks,
            "trends":            trends,
            "sector_leaders":    leaders,
            "improvement_roadmap": roadmap,
            "key_insights":      data.get("key_insights", []),
        }
