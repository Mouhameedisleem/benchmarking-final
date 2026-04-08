"""
AI Agent for Questionnaire Generation
Generates questions grounded in verified digital maturity frameworks.
Each question is tagged with its source framework and maps to a specific maturity criterion.
"""
import json
import os
from groq import AsyncGroq
from knowledge.frameworks import get_frameworks_for_sector, format_frameworks_for_prompt


class QuestionnaireAgent:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def generate(self, sector: str, country: str,
                       company_size: str | None, language: str,
                       num_questions: int) -> dict:

        # Step 1: Select relevant frameworks for this company profile
        frameworks = get_frameworks_for_sector(sector, max_frameworks=3)
        framework_context = format_frameworks_for_prompt(frameworks)
        framework_names = [fw["name"] for fw in frameworks]

        # Step 2: Build axis distribution
        distribution = self._get_axis_distribution(num_questions)

        # Step 3: Build grounded prompt with framework knowledge
        system_prompt = self._build_system_prompt(framework_context)
        user_prompt = self._build_user_prompt(
            sector, country, company_size, language,
            distribution, framework_names
        )

        # Step 4: Call LLM with framework-grounded context
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},  # Groq supports json_object
            temperature=0.5  # Lower temperature for more consistent, factual output
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)
        return self._normalize(data, sector, country, framework_names)

    def _build_system_prompt(self, framework_context: str) -> str:
        return f"""Tu es un agent expert en benchmarking de maturité digitale.
Tu génères des questionnaires d'évaluation professionnels fondés EXCLUSIVEMENT sur des frameworks reconnus internationalement.

KNOWLEDGE BASE — FRAMEWORKS DE RÉFÉRENCE :
{framework_context}

RÈGLES STRICTES :
1. Chaque question DOIT être dérivée d'un critère spécifique des frameworks ci-dessus
2. Chaque question doit indiquer son framework source (source_framework)
3. Les questions doivent être formulées pour une réponse sur échelle 1-5 :
   1 = Pas du tout / Inexistant
   2 = Peu développé / Ad-hoc
   3 = Partiellement en place / Défini
   4 = Bien établi / Géré
   5 = Excellence / Optimisé
4. Les questions doivent être mesurables, objectives et non ambiguës
5. Adapter la formulation au secteur et au pays cible
6. Réponds UNIQUEMENT en JSON valide selon le format demandé.
"""

    def _build_user_prompt(self, sector: str, country: str,
                           company_size: str | None, language: str,
                           distribution: dict, framework_names: list) -> str:
        size_info = f"\n- Taille de l'entreprise : {company_size}" if company_size else ""
        frameworks_used = ", ".join(framework_names)

        return f"""Génère un questionnaire d'évaluation de maturité digitale pour :
- Secteur : {sector}
- Pays : {country}{size_info}
- Langue de rédaction : {language}
- Frameworks à utiliser : {frameworks_used}

DISTRIBUTION DES QUESTIONS :
- Axe BUSINESS (Stratégie, Culture, Innovation, Expérience client) : {distribution['BUSINESS']} questions
- Axe PROCESS (Processus métier, Gestion de projet, Gouvernance) : {distribution['PROCESS']} questions
- Axe INFORMATION_SYSTEM (SI, Données, Cybersécurité, Architecture) : {distribution['INFORMATION_SYSTEM']} questions

Pour chaque question :
- text : formulation claire en {language}, réponse sur échelle 1-5
- axis : BUSINESS | PROCESS | INFORMATION_SYSTEM
- sub_axis : sous-domaine précis (ex: "Stratégie digitale", "Cybersécurité", "Gouvernance SI")
- weight : importance stratégique de 1 à 5 (5 = critique)
- display_order : numéro séquentiel
- source_framework : nom court du framework source (ex: "Gartner DMM", "McKinsey DQ", "ISO 27001", "CMMI", "COBIT 2019", "MIT CISR", "WEF DTI")
- maturity_indicator : ce que chaque niveau de réponse signifie (ex: "1=aucune stratégie, 5=roadmap digitale validée par le COMEX")

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
      "maturity_indicator": "1=... 3=... 5=..."
    }}
  ]
}}
"""

    def _get_axis_distribution(self, total: int) -> dict:
        business = round(total * 0.40)
        process = round(total * 0.33)
        si = total - business - process
        return {"BUSINESS": business, "PROCESS": process, "INFORMATION_SYSTEM": si}

    def _normalize(self, data: dict, sector: str, country: str, framework_names: list) -> dict:
        questions = []
        for i, q in enumerate(data.get("questions", []), start=1):
            questions.append({
                "text": q.get("text", ""),
                "axis": q.get("axis", "BUSINESS").upper(),
                "sub_axis": q.get("sub_axis", "Général"),
                "weight": max(1, min(5, int(q.get("weight", 3)))),
                "display_order": q.get("display_order", i),
                "source_framework": q.get("source_framework", framework_names[0] if framework_names else ""),
                "maturity_indicator": q.get("maturity_indicator", "")
            })

        return {
            "title": data.get("title", f"Questionnaire {sector} — {country}"),
            "description": data.get("description", ""),
            "sector": sector,
            "country": country,
            "frameworks_used": data.get("frameworks_used", framework_names),
            "questions": questions
        }
