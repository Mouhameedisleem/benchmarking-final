"""
QuestionnaireGenerator v2 — Sector-aware, non-repetitive questionnaire generation.

Key improvements over v1:
- Uses shared LLM client (Groq/Ollama via llm_client.py) — no OpenAI dependency
- All 9 digital maturity axes
- Pre-defined sector-specific sub_axis catalog — zero generic sub_axes
- Anti-repetition: each sub_axis allocated exactly once per generation
- Max 20 words per question text (enforced in post-processing)
- 5-level contextualized options per question
- Framework-grounded (Gartner, McKinsey, ISO, CMMI, WEF, COBIT)
"""
import logging
import os
import random
import re
from services.llm_client import call_llm, extract_json, TaskType

logger = logging.getLogger(__name__)


# ── Sector alias normalizer ───────────────────────────────────────────────────

_SECTOR_ALIAS: dict[str, str] = {
    "education": "education", "éducation": "education", "enseignement": "education",
    "université": "education", "universite": "education", "formation": "education",
    "ecole": "education", "école": "education",
    "banking": "banking", "banque": "banking", "finance": "banking",
    "banques": "banking", "financier": "banking", "fintech": "banking",
    "healthcare": "healthcare", "santé": "healthcare", "sante": "healthcare",
    "médical": "healthcare", "medical": "healthcare", "hôpital": "healthcare",
    "clinique": "healthcare", "pharmacie": "healthcare",
    "retail": "retail", "commerce": "retail", "distribution": "retail",
    "e-commerce": "retail", "vente": "retail",
    "industry": "industry", "industrie": "industry", "manufacture": "industry",
    "fabrication": "industry", "production": "industry",
    "tech": "tech", "technologie": "tech", "informatique": "tech",
    "numérique": "tech", "logiciel": "tech", "software": "tech",
    "insurance": "insurance", "assurance": "insurance", "assurances": "insurance",
    "transport": "transport", "logistique": "transport", "livraison": "transport",
    "energy": "energy", "énergie": "energy", "energie": "energy",
    "construction": "construction", "btp": "construction", "immobilier": "construction",
    "hospitality": "hospitality", "hôtellerie": "hospitality", "hotellerie": "hospitality",
    "tourisme": "hospitality", "restauration": "hospitality",
    "media": "media", "médias": "media", "communication": "media",
    "agriculture": "agriculture", "agroalimentaire": "agriculture",
    "telecom": "tech", "télécommunication": "tech",
}


def _resolve_sector(sector: str) -> str:
    s = sector.lower().strip()
    if s in _SECTOR_ALIAS:
        return _SECTOR_ALIAS[s]
    for word in s.replace("-", " ").replace("_", " ").split():
        if word in _SECTOR_ALIAS:
            return _SECTOR_ALIAS[word]
    return "default"


# ── Sector-specific sub_axis catalog ─────────────────────────────────────────
# Each (sector_key, axis) → ordered list of unique, sector-specific sub_axes.
# Questions will be allocated exactly ONE sub_axis per slot — no repetition possible.

_SECTOR_SUB_AXES: dict[str, dict[str, list[str]]] = {

    "education": {
        "BUSINESS": [
            "Stratégie pédagogique numérique",
            "Modèle économique EdTech",
            "Expérience apprenant (UX pédagogique)",
            "Partenariats université-entreprise",
            "Internationalisation & campus virtuel",
            "Innovation pédagogique (MOOC, microlearning)",
        ],
        "PROCESS": [
            "Gestion des inscriptions & admissions en ligne",
            "Évaluation & certification numérique",
            "Suivi de la progression des apprenants",
            "Planification des cours & emplois du temps",
            "Processus d'accréditation & conformité réglementaire",
        ],
        "INFORMATION_SYSTEM": [
            "LMS & plateformes e-learning",
            "Protection des données étudiants (RGPD/APDP)",
            "Infrastructure réseau campus & connectivité",
            "ERP académique & gestion administrative",
            "Cybersécurité des systèmes académiques",
        ],
        "CANAUX_DISTRIBUTION": [
            "Portail étudiant & application mobile",
            "Streaming & enregistrement de cours",
            "Distribution de contenus pédagogiques en ligne",
        ],
        "MARKETING_COMMUNICATION": [
            "Acquisition d'étudiants via le digital",
            "Réputation digitale & réseaux sociaux",
            "Engagement alumni & anciens diplômés",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation des enseignants aux outils numériques",
            "Leadership digital de la direction académique",
            "Culture d'innovation pédagogique",
        ],
        "OFFRES_DIGITALES": [
            "Offres de formation en ligne (MOOC, SPOC)",
            "Micro-certifications & badges numériques",
            "Tutorat IA & personnalisation de l'apprentissage",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Automatisation administrative & gestion des notes",
            "Gouvernance de la transformation numérique",
        ],
        "IT_DATA": [
            "Analytics de l'apprentissage (Learning Analytics)",
            "Infrastructure cloud & SaaS académique",
        ],
    },

    "banking": {
        "BUSINESS": [
            "Digitalisation des offres bancaires",
            "Open Banking & APIs partenaires",
            "Inclusion financière digitale",
            "Modèle économique BaaS & Fintech",
            "Innovation produits financiers numériques",
        ],
        "PROCESS": [
            "Conformité DORA/DSP2/NIS2",
            "KYC & onboarding client 100% digital",
            "Scoring crédit automatisé par IA",
            "Paiements instantanés & virement SEPA",
            "Gestion des réclamations digitale",
        ],
        "INFORMATION_SYSTEM": [
            "Cybersécurité bancaire (DORA)",
            "Architecture microservices & cloud bancaire",
            "Données clients & RGPD bancaire",
            "API Management & interopérabilité",
            "Surveillance des transactions en temps réel",
        ],
        "CANAUX_DISTRIBUTION": [
            "Application mobile banking",
            "Internet Banking & espace client en ligne",
            "Agences digitalisées & self-banking",
        ],
        "MARKETING_COMMUNICATION": [
            "CRM bancaire & personnalisation des offres",
            "Acquisition client digitale (SEA, social)",
            "Fidélisation & programmes de récompenses digitaux",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation des conseillers aux outils digitaux",
            "Recrutement de profils Tech/Data banking",
            "Culture data-driven & agilité bancaire",
        ],
        "OFFRES_DIGITALES": [
            "Crédit instantané & BNPL",
            "Épargne & investissement en ligne",
            "Assurance & bancassurance digitale",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "RPA & automatisation des opérations bancaires",
            "Lab d'innovation & partenariats Fintech",
        ],
        "IT_DATA": [
            "Data Lake bancaire & analytics décisionnel",
            "Gouvernance des données (qualité, RGPD bancaire)",
        ],
    },

    "healthcare": {
        "BUSINESS": [
            "Stratégie de santé numérique",
            "Télémédecine & téléconsultation",
            "Expérience patient digitale",
            "Partenariats MedTech & Healthtech",
            "Parcours patient digitalisé",
        ],
        "PROCESS": [
            "Dossier Patient Informatisé (DPI)",
            "Gestion des rendez-vous & planification en ligne",
            "Conformité HDS & RGPD santé",
            "Codification & facturation numérique",
            "Coordination inter-services digitale",
        ],
        "INFORMATION_SYSTEM": [
            "Cybersécurité des données de santé",
            "Interopérabilité (FHIR, HL7)",
            "Équipements médicaux connectés (IoMT)",
            "IA diagnostique & aide à la décision clinique",
            "Infrastructure cloud HDS certifié",
        ],
        "CANAUX_DISTRIBUTION": [
            "Application patient & portail santé",
            "Dispositifs de télésurveillance à distance",
        ],
        "MARKETING_COMMUNICATION": [
            "Communication santé digitale & e-réputation",
            "Acquisition & fidélisation patients",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation des soignants aux outils numériques",
            "Compétences data & IA médicale",
        ],
        "OFFRES_DIGITALES": [
            "Objets connectés de santé (wearables)",
            "Médecine prédictive & prévention digitale",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Automatisation administrative hospitalière",
            "Gouvernance numérique de l'établissement de santé",
        ],
        "IT_DATA": [
            "Analytics cliniques & recherche médicale",
            "Gestion des identités & accès (IAM santé)",
        ],
    },

    "retail": {
        "BUSINESS": [
            "Stratégie omnicanale (online + offline)",
            "Personnalisation & recommandation IA",
            "Modèle marketplace & e-commerce",
            "Click & Collect / BOPIS",
            "Social commerce & live shopping",
        ],
        "PROCESS": [
            "Gestion des stocks & prévision par IA",
            "Chaîne d'approvisionnement digitale",
            "Gestion des retours (reverse logistics)",
            "Livraison last-mile & quick commerce",
            "Paiements digitaux & Buy Now Pay Later",
        ],
        "INFORMATION_SYSTEM": [
            "Plateforme e-commerce & ERP",
            "CRM & gestion des données clients",
            "Sécurité des paiements (PCI-DSS)",
            "PIM & gestion des catalogues produits",
        ],
        "CANAUX_DISTRIBUTION": [
            "Application mobile e-commerce",
            "Site web & optimisation SEO/SEA",
            "Réseaux sociaux & marketing d'influence",
        ],
        "MARKETING_COMMUNICATION": [
            "Marketing automation & campagnes email",
            "Attribution multi-canal & ROI marketing",
            "Programme de fidélité digitale",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation des équipes retail aux outils digitaux",
            "Culture d'innovation & test & learn",
        ],
        "OFFRES_DIGITALES": [
            "Abonnements & services numériques",
            "Réalité augmentée & essayage virtuel",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Automatisation entrepôts & robotique logistique",
            "Gestion fournisseurs digitale & EDI",
        ],
        "IT_DATA": [
            "Analytics clients & personnalisation en temps réel",
            "Infrastructure cloud scalable & résiliente",
        ],
    },

    "industry": {
        "BUSINESS": [
            "Stratégie Industrie 4.0",
            "Jumeau numérique (Digital Twin)",
            "Modèle économique produit-service (servitisation)",
            "Supply chain digitale & résilience",
            "Décarbonation & usine verte numérique",
        ],
        "PROCESS": [
            "Maintenance prédictive par IA/IoT",
            "Automatisation & robotique collaborative",
            "Traçabilité produit (RFID, blockchain)",
            "Lean manufacturing digital & MES",
            "Gestion de la qualité numérique",
        ],
        "INFORMATION_SYSTEM": [
            "Cybersécurité OT/IT industrielle (IEC 62443)",
            "IoT industriel & capteurs connectés",
            "Cloud industriel & edge computing",
            "SCADA & supervision en temps réel",
            "ERP industriel & intégration MES-ERP",
        ],
        "CANAUX_DISTRIBUTION": [
            "Portail fournisseurs & clients B2B",
            "E-commerce industriel & configurateur",
        ],
        "MARKETING_COMMUNICATION": [
            "Marketing digital B2B & inbound",
            "Communication RSE & durabilité digitale",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation Industrie 4.0 des opérateurs",
            "Compétences data & IA industrielle",
        ],
        "OFFRES_DIGITALES": [
            "Maintenance as-a-service & monitoring IoT",
            "Marketplace pièces détachées & spare parts",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "R&D digitale & innovation produit",
            "Automatisation administrative industrielle",
        ],
        "IT_DATA": [
            "Data Lake industriel & analytics de production",
            "Gouvernance des données de fabrication",
        ],
    },

    "tech": {
        "BUSINESS": [
            "Stratégie produit & product-market fit",
            "Modèle SaaS & économie d'abonnement",
            "API Economy & écosystème partenaires",
            "Expansion internationale & go-to-market",
            "Customer Success & réduction du churn",
        ],
        "PROCESS": [
            "Développement agile & DevOps",
            "CI/CD & déploiement continu (GitOps)",
            "Gestion des incidents & SLA (SRE)",
            "MLOps & déploiement de modèles IA",
            "Conformité RGPD & SecDevOps",
        ],
        "INFORMATION_SYSTEM": [
            "Architecture microservices & cloud-native",
            "Cybersécurité & modèle Zero Trust",
            "Observabilité & monitoring (Prometheus, Grafana)",
            "Gestion des identités & IAM",
            "Infrastructure multi-cloud & résilience",
        ],
        "CANAUX_DISTRIBUTION": [
            "Marketplace & distribution digitale",
            "App Store & distribution mobile",
            "API publique & documentation développeurs",
        ],
        "MARKETING_COMMUNICATION": [
            "Growth hacking & acquisition PLG",
            "Content marketing & SEO technique",
            "Developer Relations (DevRel)",
        ],
        "RH_CULTURE_DIGITALE": [
            "Recrutement tech & employer branding",
            "Culture engineering & qualité logicielle",
            "Remote-first & outils collaboratifs async",
        ],
        "OFFRES_DIGITALES": [
            "Produits IA & LLM-powered features",
            "Plateformes low-code/no-code",
            "Données & analytics as-a-service",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Innovation ouverte & hackathons internes",
            "Brevets & propriété intellectuelle",
        ],
        "IT_DATA": [
            "Data engineering & pipelines ETL/ELT",
            "Feature store & MLOps en production",
        ],
    },

    "insurance": {
        "BUSINESS": [
            "Stratégie InsurTech & digitalisation",
            "Tarification dynamique & comportementale",
            "Expérience assuré digitale",
            "Partenariats InsurTech & API assurance",
            "Nouveaux modèles d'assurance (paramétrique, usage)",
        ],
        "PROCESS": [
            "Souscription en ligne & onboarding digital",
            "Gestion des sinistres automatisée (IA)",
            "Conformité IFRS 17 & Solvabilité II",
            "Lutte contre la fraude par IA/ML",
            "Relation courtiers & distribution digitale",
        ],
        "INFORMATION_SYSTEM": [
            "Core insurance & modernisation SI legacy",
            "Cybersécurité & données assurés (RGPD)",
            "IoT & objets connectés (télématique, santé)",
            "Cloud & architecture modulaire assurance",
        ],
        "CANAUX_DISTRIBUTION": [
            "Application mobile assurée",
            "Comparateurs & distribution en ligne",
            "Canaux digitaux de self-service",
        ],
        "MARKETING_COMMUNICATION": [
            "Marketing personnalisé & CRM assuré",
            "Communication réglementaire digitale",
            "Acquisition & fidélisation en ligne",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation des agents aux outils digitaux",
            "Recrutement data scientists & actuaires digitaux",
        ],
        "OFFRES_DIGITALES": [
            "Assurance paramétrique & micro-assurance",
            "Objets connectés & télématique assurance",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "RPA & automatisation des processus assurance",
            "Lab innovation assurance & partenariats",
        ],
        "IT_DATA": [
            "Actuariat digital & modèles prédictifs",
            "Lac de données assurance",
        ],
    },

    "transport": {
        "BUSINESS": [
            "Stratégie de mobilité digitale (MaaS)",
            "Optimisation des routes par IA",
            "Expérience passager ou expéditeur digitale",
            "Partenariats mobilité & écosystème",
            "Flotte électrique & transition énergétique",
        ],
        "PROCESS": [
            "Traçabilité temps réel des expéditions",
            "Gestion digitale des transports (TMS)",
            "Maintenance prédictive des véhicules/flottes",
            "Conformité réglementaire & sécurité des transports",
            "Planification des tournées & last-mile",
        ],
        "INFORMATION_SYSTEM": [
            "IoT & capteurs connectés (véhicules, entrepôts)",
            "Systèmes de gestion d'entrepôts (WMS)",
            "Cybersécurité des systèmes embarqués",
            "Intégration multimodale & interopérabilité",
        ],
        "CANAUX_DISTRIBUTION": [
            "Application client tracking & suivi",
            "Portail partenaires & expéditeurs",
        ],
        "MARKETING_COMMUNICATION": [
            "Communication client proactive & alertes",
            "Marketing digital B2B transport",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation conducteurs & logisticiens aux outils",
            "Culture sécurité & digital transport",
        ],
        "OFFRES_DIGITALES": [
            "Tracking en temps réel as-a-service",
            "Marketplace fret & bourse de transport",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Automatisation entrepôts & robotique logistique",
            "Véhicules autonomes & drones livraison",
        ],
        "IT_DATA": [
            "Analytics géospatiales & optimisation routes",
            "Data Lake logistique",
        ],
    },

    "energy": {
        "BUSINESS": [
            "Stratégie de transition énergétique numérique",
            "Smart Grid & réseau intelligent",
            "Modèle économique ENR & stockage",
            "Partenariats énergie & écosystème",
            "Efficience énergétique & décarbonation",
        ],
        "PROCESS": [
            "Gestion des actifs énergétiques (EAM)",
            "Maintenance prédictive des infrastructures",
            "Conformité réglementaire énergie (NERC CIP)",
            "Planification de la production & équilibrage",
        ],
        "INFORMATION_SYSTEM": [
            "Cybersécurité OT/IT (IEC 62443, NERC)",
            "SCADA & supervision réseau électrique",
            "Compteurs intelligents & IoT énergie",
            "Cloud & gestion des données énergie",
        ],
        "CANAUX_DISTRIBUTION": [
            "Portail client énergie en ligne",
            "Application mobile consommation & facturation",
        ],
        "MARKETING_COMMUNICATION": [
            "Communication client énergie digitale",
            "Marketing durabilité & RSE",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation techniciens aux outils digitaux",
            "Compétences data énergie & smart grid",
        ],
        "OFFRES_DIGITALES": [
            "Offres flexibilité & effacement énergétique",
            "Plateformes de trading d'énergie",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Jumeaux numériques d'actifs énergétiques",
            "Innovation stockage & hydrogène vert",
        ],
        "IT_DATA": [
            "Analytics énergétiques & prédiction consommation",
            "Gouvernance données énergie",
        ],
    },

    "default": {
        "BUSINESS": [
            "Stratégie de transformation digitale",
            "Expérience client & parcours digital",
            "Modèle économique numérique",
            "Innovation & veille technologique sectorielle",
            "Partenariats & écosystème digital",
        ],
        "PROCESS": [
            "Automatisation des processus opérationnels",
            "Gestion de projet & agilité",
            "Dématérialisation documentaire",
            "Gestion de la qualité numérique",
            "Continuité d'activité (PRA/PCA)",
        ],
        "INFORMATION_SYSTEM": [
            "Infrastructure SI & cloud",
            "Cybersécurité & gestion des risques",
            "Intégration & APIs",
            "Données & analytics décisionnels",
            "Accessibilité & performance des systèmes",
        ],
        "CANAUX_DISTRIBUTION": [
            "Canaux digitaux & présence en ligne",
            "Application mobile clients",
            "Omnicanalité (physique + digital)",
        ],
        "MARKETING_COMMUNICATION": [
            "Marketing digital & SEO/SEA",
            "CRM & personnalisation des communications",
            "Réseaux sociaux & e-réputation",
        ],
        "RH_CULTURE_DIGITALE": [
            "Formation digitale des collaborateurs",
            "Leadership & sponsorship de la transformation",
            "Recrutement de compétences numériques",
        ],
        "OFFRES_DIGITALES": [
            "Produits & services numériques",
            "Offres data-driven & IA",
            "Plateformes & API partenaires",
        ],
        "MODELE_OPERATIONNEL_INNOVATION": [
            "Automatisation end-to-end des processus",
            "Gouvernance & conformité digitale",
        ],
        "IT_DATA": [
            "Socle IT & infrastructure résiliente",
            "Gouvernance des données (qualité, sécurité)",
        ],
    },
}

# Axis distribution — for num_questions per axis
_AXIS_ORDER = [
    "BUSINESS", "PROCESS", "INFORMATION_SYSTEM",
    "CANAUX_DISTRIBUTION", "MARKETING_COMMUNICATION",
    "RH_CULTURE_DIGITALE", "OFFRES_DIGITALES",
    "MODELE_OPERATIONNEL_INNOVATION", "IT_DATA",
]

_AXIS_WEIGHTS = {
    "BUSINESS":                      0.16,
    "PROCESS":                       0.14,
    "INFORMATION_SYSTEM":            0.14,
    "CANAUX_DISTRIBUTION":           0.12,
    "MARKETING_COMMUNICATION":       0.11,
    "RH_CULTURE_DIGITALE":           0.11,
    "OFFRES_DIGITALES":              0.10,
    "MODELE_OPERATIONNEL_INNOVATION": 0.07,
    "IT_DATA":                       0.05,
}

# Framework references used in options / grounding
_AXIS_FRAMEWORKS = {
    "BUSINESS":                      "Gartner DMM, McKinsey DQ, MIT CISR",
    "PROCESS":                       "CMMI, COBIT 2019, SAFe",
    "INFORMATION_SYSTEM":            "ISO 27001, TOGAF, COBIT 2019",
    "CANAUX_DISTRIBUTION":           "McKinsey DQ, Gartner DMM",
    "MARKETING_COMMUNICATION":       "Gartner DMM, McKinsey DQ",
    "RH_CULTURE_DIGITALE":           "WEF DTI, McKinsey DQ, CMMI",
    "OFFRES_DIGITALES":              "MIT CISR, Gartner DMM",
    "MODELE_OPERATIONNEL_INNOVATION": "CMMI, COBIT 2019, WEF DTI",
    "IT_DATA":                       "Gartner DMM, COBIT 2019, ISO 27001",
}


class QuestionnaireGenerator:

    def __init__(self):
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def generate(self, sector: str, country: str,
                       company_size: str | None, language: str,
                       num_questions: int) -> dict:

        sector_key = _resolve_sector(sector)
        sub_axes_catalog = _SECTOR_SUB_AXES.get(sector_key, _SECTOR_SUB_AXES["default"])

        # Build the deterministic question plan: (axis, sub_axis) pairs
        question_plan = self._build_question_plan(num_questions, sub_axes_catalog)

        # Generate all questions in one LLM call
        raw = await call_llm(
            messages=[
                {"role": "system", "content": self._system_prompt(sector, country, sector_key)},
                {"role": "user",   "content": self._build_prompt(
                    sector, country, company_size, language, question_plan, sector_key
                )},
            ],
            temperature=0.7,
            model=self.model,
            task=TaskType.QUESTIONNAIRE,
        )

        data = extract_json(raw)
        return self._normalize(data, sector, country, question_plan)

    # ── Question plan: allocate (axis, sub_axis) slots deterministically ─────

    def _build_question_plan(self, total: int,
                              catalog: dict[str, list[str]]) -> list[dict]:
        """
        Allocate exactly `total` (axis, sub_axis) pairs using the sector catalog.
        Guarantees: each sub_axis appears at most once → zero repetition.
        """
        # Compute per-axis quotas
        quotas: dict[str, int] = {}
        remaining = total
        sorted_axes = sorted(_AXIS_ORDER, key=lambda a: _AXIS_WEIGHTS.get(a, 0.05), reverse=True)

        for i, axis in enumerate(sorted_axes):
            if i == len(sorted_axes) - 1:
                # Last axis gets whatever is left, but at least 1 if the catalog has entries
                available = len(catalog.get(axis, []))
                quotas[axis] = max(min(1, available), min(remaining, available))
            else:
                q = max(1, round(total * _AXIS_WEIGHTS.get(axis, 0.05)))
                # Don't exceed available sub_axes for this axis
                available = len(catalog.get(axis, []))
                q = min(q, available)
                quotas[axis] = q
                remaining -= q

        # Handle overflow: remaining may be negative; re-balance
        if remaining < 0:
            for axis in sorted_axes:
                if quotas[axis] > 1 and remaining < 0:
                    cut = min(-remaining, quotas[axis] - 1)
                    quotas[axis] -= cut
                    remaining += cut
        elif remaining > 0:
            # Distribute extras to axes that still have available sub_axes
            for axis in sorted_axes:
                if remaining <= 0:
                    break
                avail = len(catalog.get(axis, [])) - quotas[axis]
                if avail > 0:
                    add = min(remaining, avail)
                    quotas[axis] += add
                    remaining -= add

        # Build the plan list — shuffle sub-axes so each regeneration picks different topics
        plan: list[dict] = []
        for axis in _AXIS_ORDER:
            n = quotas.get(axis, 0)
            sub_axes = list(catalog.get(axis, []))
            random.shuffle(sub_axes)
            for i in range(min(n, len(sub_axes))):
                plan.append({
                    "axis": axis,
                    "sub_axis": sub_axes[i],
                    "framework": _AXIS_FRAMEWORKS.get(axis, "Gartner DMM"),
                    "slot": len(plan) + 1,
                })

        return plan

    # ── Prompts ───────────────────────────────────────────────────────────────

    def _system_prompt(self, sector: str, country: str, sector_key: str) -> str:
        return f"""Tu es un expert en benchmarking de maturité digitale spécialisé dans le secteur {sector} en {country}.
Tu génères des questionnaires d'évaluation professionnels fondés sur Gartner DMM, McKinsey DQ, \
ISO 27001, CMMI, COBIT 2019, MIT CISR et WEF DTI.

RÈGLES ABSOLUES (violations = réponse rejetée) :
1. Chaque question DOIT être formulée en ≤ 20 mots — compte les mots et coupe si nécessaire.
2. Chaque question DOIT être UNIQUE — aucune formulation similaire à une autre question.
3. Chaque question DOIT être spécifique au secteur {sector} — jamais de formulation applicable \
à n'importe quel secteur.
4. Le sub_axis de chaque question est IMPOSÉ dans la liste — ne le modifie JAMAIS.
5. Chaque option de réponse DOIT nommer des outils/pratiques/états concrets spécifiques \
au secteur {sector} et au sous-domaine évalué — jamais de labels génériques \
comme "Inexistant", "En cours", "Quelques initiatives".
6. Les 5 options forment une progression logique du niveau 1 (rien en place) au niveau 5 \
(excellence mesurée et reconnue) avec des critères chiffrés quand possible.
7. Source_framework = framework exact utilisé comme base pour cette question.
8. Réponds UNIQUEMENT en JSON valide — aucun texte hors JSON."""

    def _build_prompt(self, sector: str, country: str,
                      company_size: str | None, language: str,
                      plan: list[dict], sector_key: str) -> str:

        size_info = f"\n- Taille : {company_size}" if company_size else ""

        # Build the mandatory slot list
        slots_lines = "\n".join(
            f"  Slot {p['slot']:02d}: axis={p['axis']} | sub_axis=\"{p['sub_axis']}\" | framework={p['framework']}"
            for p in plan
        )

        # Build one rich sector-specific example based on sector_key
        example = self._get_sector_example(sector_key)

        return f"""Génère {len(plan)} questions de maturité digitale pour :
- Secteur : {sector}
- Pays : {country}{size_info}
- Langue : {language}

SLOTS OBLIGATOIRES — tu DOIS générer EXACTEMENT une question par slot, dans cet ordre :
{slots_lines}

CONTRAINTES CRITIQUES :
- Chaque question : ≤ 20 mots, spécifique à {sector}, formulée en {language}
- Commence chaque question par un verbe d'action ou un auxiliaire interrogatif \
(Utilisez-vous / Disposez-vous / Avez-vous / Dans quelle mesure / Quel est / \
Comment / Vos / Votre / Les / La)
- Les options DOIVENT nommer des outils, pourcentages, fréquences ou états \
organisationnels réels dans le secteur {sector}

{example}

FORMAT JSON (reproduis EXACTEMENT cette structure) :
{{
  "title": "Évaluation de maturité digitale — {sector} — {country}",
  "description": "Questionnaire fondé sur les frameworks Gartner, McKinsey, ISO, CMMI, WEF — secteur {sector}.",
  "questions": [
    {{
      "text": "<question ≤ 20 mots, spécifique {sector}, en {language}>",
      "axis": "<reprend exactement l'axis du slot>",
      "sub_axis": "<reprend exactement le sub_axis du slot — NE PAS MODIFIER>",
      "weight": <int 1-5>,
      "display_order": <int, reprend le slot number>,
      "source_framework": "<framework exact: Gartner DMM | McKinsey DQ | ISO 27001 | CMMI | COBIT 2019 | MIT CISR | WEF DTI>",
      "options": [
        "<niveau 1 — état initial, rien en place, avec outil ou pratique nommée>",
        "<niveau 2 — premières tentatives isolées, sans standard, outil cité>",
        "<niveau 3 — début de formalisation, usage partiel, outil cité>",
        "<niveau 4 — pratique établie, mesurée, équipes formées, outil cité>",
        "<niveau 5 — excellence, automatisation avancée, chiffre ou KPI cité>"
      ]
    }}
  ]
}}"""

    def _get_sector_example(self, sector_key: str) -> str:
        """Returns a rich, sector-specific example to guide the LLM."""
        examples = {
            "education": """EXEMPLE ÉDUCATION (à adapter, ne pas copier) :
sub_axis: "LMS & plateformes e-learning"
question: "Votre LMS intègre-t-il des analytics d'apprentissage en temps réel ?"
options:
  1. "Aucun LMS, cours distribués par email ou clé USB"
  2. "Moodle installé, utilisé pour dépôt de fichiers uniquement, <20% enseignants actifs"
  3. "Moodle 3.x avec quiz en ligne, rapports basiques, 50% cours digitalisés"
  4. "Canvas ou Brightspace, analytics par cohorte, 80%+ cours actifs, SCORM intégré"
  5. "LMS IA-driven (360Learning, Docebo), recommandations adaptatives, Learning Analytics dashboards temps réel"
weight: 5, source_framework: 'WEF DTI'""",

            "banking": """EXEMPLE BANQUE (à adapter, ne pas copier) :
sub_axis: "KYC & onboarding client 100% digital"
question: "Votre processus KYC est-il entièrement digitalisé et conforme DSP2 ?"
options:
  1. "KYC 100% papier, signature manuscrite, délai 10+ jours"
  2. "Formulaires PDF scannés, vérification manuelle, délai 3-5 jours"
  3. "E-signature déployée, vérification identité semi-automatique, délai <48h"
  4. "KYC digital complet, OCR + liveness check, conformité DSP2, délai <4h"
  5. "Onboarding <10 min, IA fraude en temps réel, certification eIDAS niveau substantiel"
weight: 5, source_framework: 'ISO 27001'""",

            "healthcare": """EXEMPLE SANTÉ (à adapter, ne pas copier) :
sub_axis: "Dossier Patient Informatisé (DPI)"
question: "Votre DPI est-il interopérable avec les établissements partenaires ?"
options:
  1. "Dossiers patients 100% papier, aucun système informatisé"
  2. "Logiciel médical local, non connecté, exports manuels en PDF"
  3. "DPI interne opérationnel, échanges par messagerie sécurisée MSS"
  4. "DPI interopérable FHIR/HL7, partage avec laboratoires et radiologues"
  5. "Espace Numérique de Santé actif, DMP alimenté automatiquement, IA de synthèse médicale"
weight: 5, source_framework: 'ISO 27001'""",

            "retail": """EXEMPLE RETAIL (à adapter, ne pas copier) :
sub_axis: "Personnalisation & recommandation IA"
question: "Votre moteur de recommandation personnalise-t-il les offres en temps réel ?"
options:
  1. "Aucune personnalisation, promotions identiques pour tous les clients"
  2. "Segmentation manuelle par âge/zone, emails promotionnels non ciblés"
  3. "CRM basique (Mailchimp), segmentation RFM, taux d'ouverture email <15%"
  4. "Moteur de recommandation (Nosto, Clerk.io), personnalisation homepage, CTR +25%"
  5. "IA prédictive (Adobe Sensei, Dynamic Yield), hyper-personnalisation 1-to-1, panier moyen +35%"
weight: 4, source_framework: 'McKinsey DQ'""",

            "industry": """EXEMPLE INDUSTRIE (à adapter, ne pas copier) :
sub_axis: "Maintenance prédictive par IA/IoT"
question: "Vos équipements critiques sont-ils équipés de capteurs IoT pour la maintenance prédictive ?"
options:
  1. "Maintenance 100% curative, aucun capteur, arrêts non planifiés fréquents"
  2. "Quelques capteurs isolés, lecture manuelle hebdomadaire, pas d'alertes"
  3. "SCADA basique, alertes sur seuils fixes, maintenance préventive planifiée"
  4. "Plateforme IoT (ThingWorx, Siemens MindSphere), alertes prédictives, MTBF +20%"
  5. "Jumeau numérique opérationnel, IA prédictive (Azure ML), 0 arrêt non planifié, ROI documenté"
weight: 5, source_framework: 'Gartner DMM'""",

            "default": """EXEMPLE GÉNÉRIQUE (à adapter au secteur, ne pas copier) :
question: "Votre stratégie digitale est-elle formalisée avec des KPIs mesurables ?"
options:
  1. "Aucune stratégie digitale, décisions au cas par cas"
  2. "Vision digitale esquissée, non documentée, non partagée"
  3. "Feuille de route digitale, revue annuelle, alignement partiel avec la direction"
  4. "Stratégie formalisée, revue trimestrielle, KPIs suivis en COMEX"
  5. "Stratégie digitale OKR intégrée au plan d'entreprise, révision mensuelle, NPS >60"
weight: 5""",
        }
        return examples.get(sector_key, examples["default"])

    # ── Post-processing & normalization ───────────────────────────────────────

    def _normalize(self, data: dict, sector: str, country: str,
                   plan: list[dict]) -> dict:
        """
        Normalize LLM output:
        1. Enforce ≤ 20 words per question text (truncate if exceeded)
        2. Override axis/sub_axis from the plan (LLM must not modify them)
        3. Validate options: reject generic, enforce 5-level structure
        4. Deduplication: remove questions with nearly identical text
        """
        raw_questions = data.get("questions", [])
        seen_texts: set[str] = set()
        questions = []

        for slot_idx, slot in enumerate(plan):
            # Match raw question by display_order or slot index
            raw = None
            for q in raw_questions:
                if q.get("display_order") == slot["slot"]:
                    raw = q
                    break
            if raw is None and slot_idx < len(raw_questions):
                raw = raw_questions[slot_idx]
            if raw is None:
                # LLM skipped this slot — create a fallback
                raw = {}

            text = str(raw.get("text", "")).strip()
            text = self._enforce_word_limit(text, 20)
            text = self._clean_text(text)

            # Deduplication: skip if near-duplicate of already accepted question
            norm = self._normalize_text(text)
            if norm in seen_texts or len(text) < 10:
                # Generate a variation by prepending axis/sub_axis context
                text = self._make_unique(text, slot)
                norm = self._normalize_text(text)
            seen_texts.add(norm)

            options = raw.get("options", [])
            if not isinstance(options, list) or len(options) != 5:
                options = self._fallback_options(slot)
            else:
                options = [str(o).strip() for o in options]
                if self._has_generic_options(options):
                    options = self._fallback_options(slot)

            questions.append({
                "text":             text,
                "axis":             slot["axis"],
                "sub_axis":         slot["sub_axis"],   # always from plan
                "weight":           max(1, min(5, int(raw.get("weight", 3)))),
                "display_order":    slot["slot"],
                "source_framework": str(raw.get("source_framework", slot["framework"])).strip() or slot["framework"],
                "maturity_indicator": "",
                "options":          options,
            })

        return {
            "title":          data.get("title", f"Évaluation de maturité digitale — {sector} — {country}"),
            "description":    data.get("description", f"Questionnaire de maturité digitale — {sector} — {country}"),
            "sector":         sector,
            "country":        country,
            "frameworks_used": list({slot["framework"].split(",")[0].strip() for slot in plan}),
            "questions":      questions,
        }

    # ── Text helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _enforce_word_limit(text: str, limit: int) -> str:
        """Truncate question text to ≤ `limit` words, ending cleanly."""
        words = text.split()
        if len(words) <= limit:
            return text
        truncated = " ".join(words[:limit])
        # End with "?" if original ended with "?" or if it looks interrogative
        if not truncated.endswith("?") and "?" in text:
            truncated = truncated.rstrip(" ,;:") + " ?"
        elif not truncated.endswith("?"):
            truncated = truncated.rstrip(" ,;:") + " ?"
        return truncated

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove markdown, extra spaces, normalize punctuation."""
        text = re.sub(r"[*_`#]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Lowercase + remove punctuation for dedup comparison."""
        return re.sub(r"[^a-zàâéèêëîïôùûüç0-9 ]", "", text.lower()).strip()

    @staticmethod
    def _make_unique(text: str, slot: dict) -> str:
        """Create a minimal unique variant using sub_axis context."""
        sub = slot["sub_axis"].lower().split("&")[0].strip()
        verb_map = {
            "BUSINESS": "Votre approche concernant",
            "PROCESS": "Vos processus liés à",
            "INFORMATION_SYSTEM": "Votre système pour",
            "CANAUX_DISTRIBUTION": "Vos canaux de",
            "MARKETING_COMMUNICATION": "Votre stratégie de",
            "RH_CULTURE_DIGITALE": "La maturité de vos équipes en",
            "OFFRES_DIGITALES": "Vos offres digitales en matière de",
            "MODELE_OPERATIONNEL_INNOVATION": "Votre modèle opérationnel pour",
            "IT_DATA": "Votre infrastructure pour",
        }
        prefix = verb_map.get(slot["axis"], "Votre niveau en")
        return f"{prefix} {sub} ?"

    @staticmethod
    def _has_generic_options(options: list[str]) -> bool:
        """Detect if options are generic fallback patterns."""
        generic = [
            "inexistant", "aucune pratique", "en cours de structuration",
            "pratiques définies", "amélioration continue",
            "niveau 1", "niveau 2", "niveau 3", "niveau 4", "niveau 5",
            "quelques initiatives isolées",
        ]
        hits = sum(
            1 for opt in options
            if any(kw in opt.lower() for kw in generic)
        )
        return hits >= 3

    @staticmethod
    def _fallback_options(slot: dict) -> list[str]:
        """Sector-aware fallback options using sub_axis name."""
        sub = slot["sub_axis"]
        axis = slot["axis"]
        fallbacks = {
            "INFORMATION_SYSTEM": [
                f"Aucun système dédié à {sub}, gestion ad hoc",
                f"Outil basique pour {sub}, non standardisé, usage limité",
                f"Solution partielle pour {sub}, couvrant les besoins essentiels",
                f"{sub} géré avec des outils établis, processus documentés",
                f"{sub} excellent — automatisé, audité, aligné sur les standards ISO",
            ],
            "PROCESS": [
                f"Aucun processus formalisé pour {sub}",
                f"Processus ad hoc pour {sub}, non documenté",
                f"Processus documenté pour {sub}, appliqué partiellement",
                f"Processus standardisé pour {sub}, mesuré par KPIs",
                f"Processus optimisé pour {sub} — automatisé, audité en continu",
            ],
        }
        default = [
            f"Aucune démarche pour {sub}",
            f"Premières initiatives non structurées pour {sub}",
            f"Démarche partielle pour {sub}, formalisation en cours",
            f"Pratiques établies pour {sub}, mesurées et suivies",
            f"Excellence reconnue pour {sub} — référence sectorielle",
        ]
        return fallbacks.get(axis, default)

    # ── Axis distribution (kept for backwards compatibility) ─────────────────

    def _get_axis_distribution(self, total: int) -> dict:
        dist = {}
        remaining = total
        axes = list(_AXIS_WEIGHTS.keys())
        for i, axis in enumerate(axes):
            if i == len(axes) - 1:
                dist[axis] = max(0, remaining)
            else:
                q = max(1, round(total * _AXIS_WEIGHTS[axis]))
                dist[axis] = q
                remaining -= q
        return dist
