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


# ── Standardized sub-axis catalog (identical for all sectors) ────────────────
# Aligned with sector_loader.py _SUB_AXIS_FILE_MAP knowledge-base keys.
# Questions are sector-specific in content but all sectors share the same sub-axis names.

_STANDARD_SUB_AXES: dict[str, list[str]] = {
    "BUSINESS": [
        "Stratégie digitale",
        "Orientation client",
        "Innovation",
        "Modèle économique digital",
    ],
    "PROCESS": [
        "Cartographie des processus",
        "Automatisation",
        "Agilité",
        "Performance opérationnelle",
    ],
    "INFORMATION_SYSTEM": [
        "Infrastructure & Cloud",
        "Cybersécurité",
        "Données & Analytics",
        "Intégration & API",
    ],
    "CANAUX_DISTRIBUTION": [
        "Canaux de distribution & expérience client",
        "Selfcare client",
    ],
    "MARKETING_COMMUNICATION": [
        "Marketing & communication digitale",
    ],
    "RH_CULTURE_DIGITALE": [
        "Culture digitale",
        "Poste de travail du banquier",
        "Collaboratif & digital working",
        "Digitalisation de la fonction RH",
        "Agilité",
    ],
    "OFFRES_DIGITALES": [
        "Offres digitales",
        "Open banking (BaaS, BaaP)",
    ],
    "MODELE_OPERATIONNEL_INNOVATION": [
        "Simplification & automatisation des processus",
        "Gouvernance de la transformation digitale",
        "Développement de l'innovation",
    ],
    "IT_DATA": [
        "Socle IT",
        "Data",
    ],
}

# All sector keys resolve to the same standardized catalog.
_SECTOR_SUB_AXES: dict[str, dict[str, list[str]]] = {
    sector: dict(_STANDARD_SUB_AXES)
    for sector in [
        "education", "banking", "healthcare", "retail", "industry",
        "tech", "insurance", "transport", "energy", "construction",
        "hospitality", "media", "agriculture", "default",
    ]
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
sub_axis: "Culture digitale"
question: "Vos enseignants sont-ils formés et certifiés sur les outils pédagogiques numériques ?"
options:
  1. "Aucune formation au numérique, usage des outils limité à la messagerie"
  2. "Formations ponctuelles sans plan structuré, <20% enseignants autonomes"
  3. "Plan annuel de formation, 50% enseignants certifiés sur LMS, Moodle ou Teams"
  4. "Programme certifiant continu, 80%+ enseignants formés, ambassadeurs numériques identifiés"
  5. "Culture d'innovation pédagogique ancrée, certifications reconnues (TICE, DELF numérique), KPIs publiés"
weight: 4, source_framework: 'WEF DTI'""",

            "banking": """EXEMPLE BANQUE (à adapter, ne pas copier) :
sub_axis: "Canaux de distribution & expérience client"
question: "Votre processus d'onboarding client est-il entièrement digital et sans friction ?"
options:
  1. "Onboarding 100% papier, signature manuscrite, délai 10+ jours"
  2. "Formulaires PDF scannés, vérification manuelle, délai 3-5 jours"
  3. "E-signature déployée, vérification identité semi-automatique, délai <48h"
  4. "KYC digital complet, OCR + liveness check, conformité DSP2, délai <4h"
  5. "Onboarding <10 min, IA fraude en temps réel, certification eIDAS niveau substantiel"
weight: 5, source_framework: 'ISO 27001'""",

            "healthcare": """EXEMPLE SANTÉ (à adapter, ne pas copier) :
sub_axis: "Données & Analytics"
question: "Vos données patients sont-elles interopérables et exploitées pour la décision clinique ?"
options:
  1. "Dossiers patients 100% papier, aucun système informatisé"
  2. "Logiciel médical local, non connecté, exports manuels en PDF"
  3. "DPI interne opérationnel, échanges par messagerie sécurisée MSS"
  4. "DPI interopérable FHIR/HL7, partage avec laboratoires et radiologues"
  5. "Espace Numérique de Santé actif, DMP alimenté automatiquement, IA de synthèse médicale"
weight: 5, source_framework: 'ISO 27001'""",

            "retail": """EXEMPLE RETAIL (à adapter, ne pas copier) :
sub_axis: "Marketing & communication digitale"
question: "Votre stratégie marketing digital personnalise-t-elle les offres en temps réel ?"
options:
  1. "Aucune personnalisation, promotions identiques pour tous les clients"
  2. "Segmentation manuelle par âge/zone, emails promotionnels non ciblés"
  3. "CRM basique (Mailchimp), segmentation RFM, taux d'ouverture email <15%"
  4. "Moteur de recommandation (Nosto, Clerk.io), personnalisation homepage, CTR +25%"
  5. "IA prédictive (Adobe Sensei, Dynamic Yield), hyper-personnalisation 1-to-1, panier moyen +35%"
weight: 4, source_framework: 'McKinsey DQ'""",

            "industry": """EXEMPLE INDUSTRIE (à adapter, ne pas copier) :
sub_axis: "Automatisation"
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
