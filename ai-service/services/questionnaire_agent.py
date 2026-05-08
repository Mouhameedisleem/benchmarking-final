"""
AI Agent for Questionnaire Generation
Generates questions grounded in verified digital maturity frameworks.
Each question is tagged with its source framework and maps to a specific maturity criterion.
"""
import json
import os
from knowledge.frameworks import get_frameworks_for_sector, format_frameworks_for_prompt
from knowledge.regulations import format_regulations_for_prompt
from knowledge.sector_benchmarks import format_benchmark_for_prompt
from services.mistral_client import call_mistral, extract_json


class QuestionnaireAgent:
    def __init__(self):
        # Use a fast model for questionnaire generation — quality is sufficient
        # and speed matters more here (user waits on the setup page)
        self.model = os.getenv("MISTRAL_MODEL_QUESTIONNAIRE", "mistral-small-latest")

    async def generate(self, sector: str, country: str,
                       company_size: str | None, language: str,
                       num_questions: int) -> dict:

        # Step 1: Select relevant frameworks for this company profile
        frameworks = get_frameworks_for_sector(sector, max_frameworks=3)
        framework_context = format_frameworks_for_prompt(frameworks)
        framework_names = [fw["name"] for fw in frameworks]

        # Step 2: Build regulatory and benchmark context
        regulations_context = format_regulations_for_prompt(sector, country)
        benchmark_context = format_benchmark_for_prompt(sector, country)

        # Step 3: Build axis distribution
        distribution = self._get_axis_distribution(num_questions)

        # Step 4: Build grounded prompt with all knowledge bases
        system_prompt = self._build_system_prompt(framework_context, regulations_context, benchmark_context)
        user_prompt = self._build_user_prompt(
            sector, country, company_size, language,
            distribution, framework_names
        )

        # Step 5: Call Mistral asynchronously (non-blocking, 120s timeout)
        raw = await call_mistral(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            model=self.model,
        )
        data = extract_json(raw)

        # Step 6: Detect and fix any remaining generic options in one batched call
        data = await self._fix_generic_options(data)

        return self._normalize(data, sector, country, framework_names)

    def _build_system_prompt(self, framework_context: str,
                             regulations_context: str = "",
                             benchmark_context: str = "") -> str:
        return f"""Tu es un agent expert en benchmarking de maturité digitale.
Tu génères des questionnaires d'évaluation professionnels fondés sur des frameworks reconnus internationalement, \
en tenant compte des réglementations applicables et des benchmarks sectoriels.

KNOWLEDGE BASE — FRAMEWORKS DE RÉFÉRENCE :
{framework_context}
{regulations_context}
{benchmark_context}

RÈGLES STRICTES :
1. Chaque question DOIT être dérivée d'un critère spécifique des frameworks ci-dessus.
2. Inclure des questions couvrant les obligations réglementaires identifiées (RGPD, DORA, NIS2, HDS, etc.).
3. Chaque question doit indiquer son framework source (source_framework).
4. Chaque question doit avoir EXACTEMENT 5 options de réponse CONTEXTUALISÉES et SPÉCIFIQUES au sujet évalué.
   Les options décrivent des pratiques concrètes, des outils, des états organisationnels précis — PAS des labels génériques.

   ✅ BON EXEMPLE pour "Dans quelle mesure utilisez-vous l'analyse de données pour piloter vos décisions marketing ?" :
   - "Aucun outil analytique, décisions basées sur l'intuition ou l'expérience"
   - "Google Analytics de base, lecture ponctuelle sans processus d'analyse"
   - "Tableaux de bord actifs, KPIs définis mais rarement actionnés"
   - "A/B testing régulier, segmentation clients, reporting hebdomadaire automatisé"
   - "Modèles prédictifs en production, personnalisation temps réel, data science marketing"

   ❌ MAUVAIS EXEMPLE (interdit — ces formulations génériques ne sont PAS acceptées) :
   - "Inexistant"
   - "Quelques initiatives isolées, non formalisées"
   - "Approche en cours de structuration"
   - "Pratiques définies et déployées en grande partie"
   - "Maîtrise complète, mesurée et en amélioration continue"

5. Chaque option doit :
   - Nommer des outils, méthodes, pratiques ou états organisationnels concrets
   - Décrire la fréquence, l'automatisation, le niveau d'équipe impliquée si pertinent
   - Être compréhensible sans relire la question
   - Former une progression logique et continue du niveau 1 (rien) au niveau 5 (excellence)
6. Les questions doivent être mesurables, objectives et non ambiguës.
7. Adapter la formulation au secteur, au pays et aux enjeux réglementaires identifiés.
8. Réponds UNIQUEMENT en JSON valide selon le format demandé.
"""

    def _build_user_prompt(self, sector: str, country: str,
                           company_size: str | None, language: str,
                           distribution: dict, framework_names: list) -> str:
        size_info = f"\n- Taille de l'entreprise : {company_size}" if company_size else ""
        frameworks_used = ", ".join(framework_names)

        dist_lines = "\n".join([
            f"- Axe BUSINESS (Stratégie digitale, Culture, Innovation, Expérience client) : {distribution['BUSINESS']} questions",
            f"- Axe PROCESS (Processus métier, Gestion de projet, Gouvernance, Agilité) : {distribution['PROCESS']} questions",
            f"- Axe INFORMATION_SYSTEM (SI, Données, Cybersécurité, Architecture technique) : {distribution['INFORMATION_SYSTEM']} questions",
            f"- Axe CANAUX_DISTRIBUTION (Canaux digitaux, Mobile, Web, Distribution omnicanal) : {distribution['CANAUX_DISTRIBUTION']} questions",
            f"- Axe MARKETING_COMMUNICATION (Marketing digital, CRM, Communication, Acquisition client) : {distribution['MARKETING_COMMUNICATION']} questions",
            f"- Axe RH_CULTURE_DIGITALE (Compétences numériques, Formation, Culture digitale, RH) : {distribution['RH_CULTURE_DIGITALE']} questions",
            f"- Axe OFFRES_DIGITALES (Offres numériques, Produits digitaux, Open Banking, Services en ligne) : {distribution['OFFRES_DIGITALES']} questions",
        ])

        return f"""Génère un questionnaire d'évaluation de maturité digitale pour :
- Secteur : {sector}
- Pays : {country}{size_info}
- Langue de rédaction : {language}
- Frameworks à utiliser : {frameworks_used}

DISTRIBUTION DES QUESTIONS (OBLIGATOIRE — tu DOIS générer exactement ces 7 axes) :
{dist_lines}

Pour chaque question :
- text : formulation claire en {language}, réponse sur échelle 1-5
- axis : BUSINESS | PROCESS | INFORMATION_SYSTEM | CANAUX_DISTRIBUTION | MARKETING_COMMUNICATION | RH_CULTURE_DIGITALE | OFFRES_DIGITALES
- sub_axis : sous-domaine précis (ex: "Stratégie digitale", "Cybersécurité", "Canaux mobiles", "Marketing automation")
- weight : importance stratégique de 1 à 5 (5 = critique)
- display_order : numéro séquentiel
- source_framework : nom court du framework source (ex: "Gartner DMM", "McKinsey DQ", "ISO 27001", "CMMI", "COBIT 2019", "MIT CISR", "WEF DTI")
- options : tableau de 5 phrases courtes décrivant chaque niveau de maturité spécifique à CETTE question

FORMAT JSON REQUIS :
{{
  "title": "Évaluation de maturité digitale — {sector} — {country}",
  "description": "Questionnaire fondé sur {frameworks_used}. Évalue la maturité digitale selon les standards internationaux.",
  "frameworks_used": ["{frameworks_used}"],
  "questions": [
    {{
      "text": "...",
      "axis": "BUSINESS",
      "sub_axis": "...",
      "weight": 4,
      "display_order": 1,
      "source_framework": "...",
      "options": [
        "Aucune stratégie digitale formalisée, décisions au cas par cas",
        "Vision digitale esquissée mais non documentée ni partagée",
        "Feuille de route digitale existante, revue annuelle, alignement partiel",
        "Stratégie digitale formalisée, revue trimestrielle, KPIs suivis par la direction",
        "Stratégie digitale intégrée au plan d'entreprise, pilotage OKR, révision continue"
      ]
    }}
  ]
}}
"""

    def _is_generic_options(self, options: list) -> bool:
        """Returns True if options look like the generic fallback — not contextual."""
        if not isinstance(options, list) or len(options) != 5:
            return True
        generic_keywords = [
            "inexistant", "aucune pratique", "quelques initiatives", "non formalisées",
            "en cours de structuration", "approche en cours", "pratiques définies",
            "amélioration continue", "maîtrise complète",
        ]
        matches = sum(
            1 for opt in options
            if any(kw in opt.lower() for kw in generic_keywords)
        )
        return matches >= 3

    async def _fix_generic_options(self, data: dict) -> dict:
        """Detect questions with generic options and regenerate them in one batched LLM call.
        Only fires the extra call if >40% of questions have generic options — avoids doubling
        generation time when the main prompt already produced good contextual options."""
        questions = data.get("questions", [])
        to_fix = [
            (i, q) for i, q in enumerate(questions)
            if self._is_generic_options(q.get("options", []))
        ]
        if not to_fix:
            return data
        # Skip expensive second call if only a small minority of questions are generic
        if len(to_fix) / max(len(questions), 1) < 0.4:
            return data

        questions_text = "\n".join(
            f"{rank+1}. [{q.get('axis','')}/{q.get('sub_axis','')}] {q.get('text','')}"
            for rank, (_, q) in enumerate(to_fix)
        )
        prompt = f"""Tu es expert en maturité digitale. Pour chaque question ci-dessous, génère 5 options de réponse \
CONTEXTUALISÉES qui décrivent précisément les 5 niveaux de maturité du sujet évalué.

RÈGLES :
- Chaque option doit être spécifique à la question (outils, méthodes, pratiques, état organisationnel concrets)
- Option 1 : aucune pratique ou outil, état initial
- Option 2 : tentatives isolées, sans processus standardisé
- Option 3 : début de formalisation, usage partiel
- Option 4 : pratiques bien établies, mesurées, équipes formées
- Option 5 : excellence, automatisation avancée, amélioration continue pilotée par la donnée
- INTERDIT : ne pas utiliser "Inexistant", "Quelques initiatives isolées", "Approche en cours", "Pratiques définies", "Amélioration continue" seuls

QUESTIONS :
{questions_text}

Réponds UNIQUEMENT en JSON :
{{
  "options_by_question": [
    ["option1", "option2", "option3", "option4", "option5"],
    ...un tableau par question dans le même ordre...
  ]
}}"""

        try:
            raw = await call_mistral(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                model=self.model,
            )
            result = extract_json(raw)
            options_list = result.get("options_by_question", [])
            for rank, (orig_idx, _) in enumerate(to_fix):
                if rank < len(options_list) and isinstance(options_list[rank], list) and len(options_list[rank]) == 5:
                    data["questions"][orig_idx]["options"] = options_list[rank]
        except Exception:
            pass  # Keep original options if regeneration fails

        return data

    def _get_axis_distribution(self, total: int) -> dict:
        axes = [
            "BUSINESS", "PROCESS", "INFORMATION_SYSTEM",
            "CANAUX_DISTRIBUTION", "MARKETING_COMMUNICATION",
            "RH_CULTURE_DIGITALE", "OFFRES_DIGITALES",
        ]
        base = total // len(axes)
        remainder = total % len(axes)
        distribution = {axis: base for axis in axes}
        for i in range(remainder):
            distribution[axes[i]] += 1
        return distribution

    _LAST_RESORT_OPTIONS = [
        "Aucun dispositif ou outil en place",
        "Premiers essais isolés, sans processus établi",
        "Pratiques partiellement formalisées, adoption en cours",
        "Pratiques établies, mesurées, déployées à grande échelle",
        "Excellence opérationnelle, pilotage continu par la donnée",
    ]

    def _normalize(self, data: dict, sector: str, country: str, framework_names: list) -> dict:
        questions = []
        for i, q in enumerate(data.get("questions", []), start=1):
            raw_options = q.get("options", [])
            if isinstance(raw_options, list) and len(raw_options) == 5:
                options = raw_options
            else:
                options = self._LAST_RESORT_OPTIONS
            questions.append({
                "text": q.get("text", ""),
                "axis": q.get("axis", "BUSINESS").upper(),
                "sub_axis": q.get("sub_axis", "Général"),
                "weight": max(1, min(5, int(q.get("weight", 3)))),
                "display_order": q.get("display_order", i),
                "source_framework": q.get("source_framework", framework_names[0] if framework_names else ""),
                "options": options
            })

        return {
            "title": data.get("title", f"Questionnaire {sector} — {country}"),
            "description": data.get("description", ""),
            "sector": sector,
            "country": country,
            "frameworks_used": data.get("frameworks_used", framework_names),
            "questions": questions
        }
