import json
import os
from openai import AsyncOpenAI


class QuestionnaireGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def generate(self, sector: str, country: str,
                       company_size: str | None, language: str,
                       num_questions: int) -> dict:

        axis_distribution = self._get_axis_distribution(num_questions)
        prompt = self._build_prompt(sector, country, company_size, language, axis_distribution)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)
        return self._normalize(data, sector, country)

    def _system_prompt(self) -> str:
        return """Tu es un expert en transformation digitale et en benchmarking IA.
Tu génères des questionnaires d'évaluation de maturité digitale professionnels,
basés sur les meilleures pratiques internationales (Gartner, McKinsey, WEF, ISO).

Chaque question doit :
- Être claire, précise et mesurable
- Couvrir les 3 axes : BUSINESS (métier), PROCESS (processus), INFORMATION_SYSTEM (SI)
- Avoir un poids entre 1 et 5 selon son importance stratégique
- Être adaptée au secteur et au pays cibles

Réponds UNIQUEMENT en JSON valide selon le format demandé.
"""

    def _build_prompt(self, sector: str, country: str,
                      company_size: str | None, language: str,
                      distribution: dict) -> str:
        size_info = f", taille: {company_size}" if company_size else ""
        return f"""Génère un questionnaire d'évaluation de maturité digitale pour :
- Secteur : {sector}
- Pays : {country}{size_info}
- Langue : {language}

Distribue les questions ainsi :
- Axe BUSINESS (Métier) : {distribution['BUSINESS']} questions
- Axe PROCESS (Processus) : {distribution['PROCESS']} questions
- Axe INFORMATION_SYSTEM (Système d'information) : {distribution['INFORMATION_SYSTEM']} questions

Pour chaque question, définis :
- text : le texte de la question (réponse sur échelle 1-5 : de "pas du tout" à "complètement")
- axis : BUSINESS | PROCESS | INFORMATION_SYSTEM
- sub_axis : le sous-domaine (ex: "Stratégie digitale", "Automatisation", "Sécurité SI")
- weight : importance de 1 à 5
- display_order : ordre séquentiel

Réponds avec ce JSON exact :
{{
  "title": "Questionnaire de maturité digitale - {sector} - {country}",
  "description": "Évaluation de la maturité digitale adaptée au secteur {sector} en {country}",
  "questions": [
    {{
      "text": "...",
      "axis": "BUSINESS",
      "sub_axis": "...",
      "weight": 3,
      "display_order": 1
    }}
  ]
}}
"""

    def _get_axis_distribution(self, total: int) -> dict:
        business = round(total * 0.40)
        process = round(total * 0.33)
        si = total - business - process
        return {"BUSINESS": business, "PROCESS": process, "INFORMATION_SYSTEM": si}

    def _normalize(self, data: dict, sector: str, country: str) -> dict:
        questions = []
        for i, q in enumerate(data.get("questions", []), start=1):
            questions.append({
                "text": q.get("text", ""),
                "axis": q.get("axis", "BUSINESS").upper(),
                "sub_axis": q.get("sub_axis", "Général"),
                "weight": max(1, min(5, int(q.get("weight", 1)))),
                "display_order": q.get("display_order", i)
            })
        return {
            "title": data.get("title", f"Questionnaire {sector} - {country}"),
            "description": data.get("description", ""),
            "sector": sector,
            "country": country,
            "questions": questions
        }
