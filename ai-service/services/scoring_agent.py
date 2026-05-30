"""
AI Scoring Agent
Maps questionnaire answers to digital maturity levels using framework criteria.
Produces: global score, axis scores, sub-axis scores, maturity level, and explanation.
"""
import json
import os
from knowledge.frameworks import get_frameworks_for_sector, FRAMEWORKS
from knowledge.sector_benchmarks import format_benchmark_for_prompt
from knowledge.regulations import format_regulations_for_prompt
from services.llm_client import call_llm as call_groq, extract_json, TaskType


class ScoringAgent:
    def __init__(self):
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def score(self, request: dict) -> dict:
        """
        request: {
          sector, country, company_name,
          frameworks_used: [str],
          answers: [{ question_text, sub_axis, axis, weight, source_framework, value (1-5), comment }]
        }
        """
        # Build a weighted score baseline (rule-based, fast)
        baseline = self._compute_baseline(request["answers"])

        # Enrich context with knowledge bases
        benchmark_context = format_benchmark_for_prompt(
            request.get("sector", ""), request.get("country", ""), baseline["global_score"]
        )
        regulations_context = format_regulations_for_prompt(
            request.get("sector", ""), request.get("country", "")
        )

        # Use AI to produce richer scoring with explanations
        prompt = self._build_prompt(request, baseline, benchmark_context, regulations_context)
        raw = await call_groq(
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            model=self.model,
            task=TaskType.SCORING,
        )
        data = extract_json(raw)
        return self._normalize(data, baseline, request)

    def _system_prompt(self) -> str:
        return """Tu es un agent d'évaluation expert en maturité digitale.
Tu analyses les réponses d'une entreprise à un questionnaire basé sur des frameworks reconnus
(Gartner, McKinsey, ISO 27001, CMMI, COBIT, MIT CISR, WEF) et tu calcules :
- Un score global sur 100
- Un score par axe (BUSINESS, PROCESS, INFORMATION_SYSTEM) sur 100
- Un score par sous-axe sur 100
- Un niveau de maturité global (INITIAL, BASIQUE, INTERMEDIAIRE, AVANCE, OPTIMISE)
- Une synthèse narrative par axe (2-3 phrases, points forts + points faibles)
- Des insights clés sur les gaps critiques identifiés

RÈGLES DE SCORING :
- Score = moyenne pondérée des réponses (valeur 1-5), normalisée sur 100
- Pondération par le poids de chaque question (1-5)
- Niveau de maturité :
  0-20  → INITIAL
  21-40 → BASIQUE
  41-60 → INTERMEDIAIRE
  61-80 → AVANCE
  81-100 → OPTIMISE
- Utilise le benchmark sectoriel fourni pour contextualiser le score (au-dessus/en dessous de la moyenne)
- Signale les non-conformités réglementaires potentielles dans les gaps critiques
- La synthèse doit citer les frameworks pertinents, le positionnement sectoriel et nommer les gaps précis
- Réponds UNIQUEMENT en JSON valide.
"""

    def _build_prompt(self, req: dict, baseline: dict,
                      benchmark_context: str = "", regulations_context: str = "") -> str:
        answers_summary = self._format_answers(req["answers"])
        frameworks = req.get("frameworks_used", ["Gartner DMM", "McKinsey DQ"])

        return f"""Évalue la maturité digitale de cette entreprise :

CONTEXTE :
- Entreprise : {req.get('company_name', 'N/A')}
- Secteur : {req.get('sector', 'N/A')}
- Pays : {req.get('country', 'N/A')}
- Frameworks utilisés : {', '.join(frameworks)}

SCORES DE RÉFÉRENCE (calcul pondéré automatique) :
- Score global estimé : {baseline['global_score']:.1f}/100
- Score BUSINESS : {baseline['business_score']:.1f}/100
- Score PROCESS : {baseline['process_score']:.1f}/100
- Score INFORMATION_SYSTEM : {baseline['si_score']:.1f}/100
- Score CANAUX_DISTRIBUTION : {baseline['canaux_score']:.1f}/100
- Score MARKETING_COMMUNICATION : {baseline['marketing_score']:.1f}/100
- Score RH_CULTURE_DIGITALE : {baseline['rh_score']:.1f}/100
- Score OFFRES_DIGITALES : {baseline['offres_score']:.1f}/100
{benchmark_context}
{regulations_context}

RÉPONSES AU QUESTIONNAIRE :
{answers_summary}

Génère une évaluation complète au format JSON :
{{
  "global_score": <float 0-100>,
  "business_score": <float 0-100>,
  "process_score": <float 0-100>,
  "si_score": <float 0-100>,
  "canaux_score": <float 0-100>,
  "marketing_score": <float 0-100>,
  "rh_score": <float 0-100>,
  "offres_score": <float 0-100>,
  "maturity_level": "INITIAL|BASIQUE|INTERMEDIAIRE|AVANCE|OPTIMISE",
  "sub_axis_scores": [
    {{"sub_axis": "...", "axis": "BUSINESS|PROCESS|INFORMATION_SYSTEM|CANAUX_DISTRIBUTION|MARKETING_COMMUNICATION|RH_CULTURE_DIGITALE|OFFRES_DIGITALES", "score": <float>, "question_count": <int>}}
  ],
  "axis_syntheses": [
    {{
      "axis": "BUSINESS|PROCESS|INFORMATION_SYSTEM|CANAUX_DISTRIBUTION|MARKETING_COMMUNICATION|RH_CULTURE_DIGITALE|OFFRES_DIGITALES",
      "score": <float>,
      "summary": "Synthèse narrative 2-3 phrases avec points forts et gaps identifiés, référençant les frameworks.",
      "strengths": ["point fort 1", "point fort 2"],
      "gaps": ["gap critique 1", "gap critique 2"]
    }}
  ],
  "critical_gaps": ["Description du gap le plus urgent #1", "..."],
  "maturity_explanation": "Explication du niveau de maturité attribué en 2 phrases."
}}
"""

    def _format_answers(self, answers: list) -> str:
        lines = []
        for a in answers:
            score_label = {1: "Inexistant", 2: "Insuffisant", 3: "Partiel", 4: "Bien établi", 5: "Excellence"}.get(
                int(a.get("value", 1)), "N/A"
            )
            line = (
                f"[{a.get('axis','?')} / {a.get('sub_axis','?')}] "
                f"({a.get('source_framework','')}) "
                f"Q: {a.get('question_text','?')} "
                f"→ Réponse: {a.get('value',1)}/5 ({score_label})"
            )
            if a.get("comment"):
                line += f" | Commentaire: {a['comment']}"
            lines.append(line)
        return "\n".join(lines)

    def _compute_baseline(self, answers: list) -> dict:
        """Fast weighted average per axis — used as reference for the AI."""
        axis_data = {
            "BUSINESS": [], "PROCESS": [], "INFORMATION_SYSTEM": [],
            "CANAUX_DISTRIBUTION": [], "MARKETING_COMMUNICATION": [],
            "RH_CULTURE_DIGITALE": [], "OFFRES_DIGITALES": [],
        }
        all_values = []

        for a in answers:
            axis = a.get("axis", "BUSINESS").upper()
            value = float(a.get("value", 1))
            weight = float(a.get("weight", 1))
            normalized = ((value - 1) / 4) * 100  # 1-5 → 0-100

            if axis in axis_data:
                axis_data[axis].append((normalized, weight))
            all_values.append((normalized, weight))

        def weighted_avg(items):
            if not items:
                return 0.0
            total_weight = sum(w for _, w in items)
            if total_weight == 0:
                return 0.0
            return sum(v * w for v, w in items) / total_weight

        return {
            "global_score":   weighted_avg(all_values),
            "business_score": weighted_avg(axis_data["BUSINESS"]),
            "process_score":  weighted_avg(axis_data["PROCESS"]),
            "si_score":       weighted_avg(axis_data["INFORMATION_SYSTEM"]),
            "canaux_score":   weighted_avg(axis_data["CANAUX_DISTRIBUTION"]),
            "marketing_score": weighted_avg(axis_data["MARKETING_COMMUNICATION"]),
            "rh_score":       weighted_avg(axis_data["RH_CULTURE_DIGITALE"]),
            "offres_score":   weighted_avg(axis_data["OFFRES_DIGITALES"]),
        }

    def _normalize(self, data: dict, baseline: dict, req: dict) -> dict:
        valid_levels = {"INITIAL", "BASIQUE", "INTERMEDIAIRE", "AVANCE", "OPTIMISE"}

        global_score = float(data.get("global_score", baseline["global_score"]))
        maturity_level = data.get("maturity_level", "INITIAL").upper()
        if maturity_level not in valid_levels:
            maturity_level = self._score_to_level(global_score)

        sub_axis_scores = []
        for s in data.get("sub_axis_scores", []):
            sub_axis_scores.append({
                "sub_axis": s.get("sub_axis", ""),
                "axis": s.get("axis", "BUSINESS"),
                "score": float(s.get("score", 0)),
                "question_count": int(s.get("question_count", 1))
            })

        axis_syntheses = []
        for s in data.get("axis_syntheses", []):
            axis_syntheses.append({
                "axis": s.get("axis", ""),
                "score": float(s.get("score", 0)),
                "summary": s.get("summary", ""),
                "strengths": s.get("strengths", []),
                "gaps": s.get("gaps", [])
            })

        return {
            "global_score": round(global_score, 1),
            "business_score": round(float(data.get("business_score", baseline["business_score"])), 1),
            "process_score": round(float(data.get("process_score", baseline["process_score"])), 1),
            "si_score": round(float(data.get("si_score", baseline["si_score"])), 1),
            "maturity_level": maturity_level,
            "sub_axis_scores": sub_axis_scores,
            "axis_syntheses": axis_syntheses,
            "critical_gaps": data.get("critical_gaps", []),
            "maturity_explanation": data.get("maturity_explanation", "")
        }

    def _score_to_level(self, score: float) -> str:
        if score <= 20: return "INITIAL"
        if score <= 40: return "BASIQUE"
        if score <= 60: return "INTERMEDIAIRE"
        if score <= 80: return "AVANCE"
        return "OPTIMISE"
