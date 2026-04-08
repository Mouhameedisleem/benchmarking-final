import json
import os
from groq import AsyncGroq


class RecommendationEngine:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def generate(self, request) -> dict:
        prompt = self._build_prompt(request)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)
        return {
            "evaluation_id": request.evaluation_id,
            "recommendations": self._normalize(data.get("recommendations", []))
        }

    def _system_prompt(self) -> str:
        return """Tu es un consultant expert en transformation digitale et en stratégie IA,
spécialisé dans les benchmarks de maturité digitale pour les entreprises africaines et européennes.

Tu génères des recommandations d'amélioration personnalisées, concrètes et actionnables,
basées sur des sources fiables : Gartner, McKinsey, WEF, Accenture, BCG, ANSSI, ISO, OCDE.

Chaque recommandation doit être :
- Spécifique au score, au secteur et au pays de l'entreprise
- Fondée sur des meilleures pratiques régionales et internationales
- Priorisée (HAUTE / MOYENNE / BASSE) selon l'urgence et l'impact
- Actionnable à court ou moyen terme

Réponds UNIQUEMENT en JSON valide.
"""

    def _build_prompt(self, req) -> str:
        sub_axis_summary = ""
        if req.sub_axis_scores:
            weak = [s for s in req.sub_axis_scores if s.get("score", 100) < 50]
            if weak:
                sub_axis_summary = "\nSous-axes faibles (<50) : " + ", ".join(
                    f"{s['subAxis']} ({s['score']:.0f}/100)" for s in weak[:5]
                )

        return f"""Génère des recommandations d'amélioration pour cette entreprise :

CONTEXTE :
- Entreprise : {req.company_name}
- Secteur : {req.sector}
- Pays : {req.country}
- Niveau de maturité : {req.maturity_level}

SCORES :
- Score global : {req.global_score:.1f}/100
- Axe Métier (BUSINESS) : {req.business_score:.1f}/100
- Axe Processus (PROCESS) : {req.process_score:.1f}/100
- Axe SI (INFORMATION_SYSTEM) : {req.si_score:.1f}/100
{sub_axis_summary}

INSTRUCTIONS :
- Génère 2 à 4 recommandations par axe selon les scores (plus le score est bas, plus de recommandations HAUTE priorité)
- Pour les scores > 75, génère 1 recommandation BASSE priorité (maintien de l'excellence)
- Cite des frameworks, standards ou études de référence dans best_practice
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

Les valeurs possibles pour axis : METIER, PROCESSUS, SI
Les valeurs possibles pour priority : HAUTE, MOYENNE, BASSE
"""

    def _normalize(self, items: list) -> list:
        valid_axes = {"METIER", "PROCESSUS", "SI"}
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
