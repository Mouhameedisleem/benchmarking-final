from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from services.questionnaire_agent import QuestionnaireAgent
from services.recommendation_engine import RecommendationEngine
from services.scoring_agent import ScoringAgent
from services.benchmarking_engine import BenchmarkingEngine
from knowledge.frameworks import get_frameworks_for_sector, FRAMEWORKS

load_dotenv()

app = FastAPI(
    title="IA Benchmark — AI Service",
    description="Agent IA pour la génération de questionnaires fondés sur des frameworks reconnus (Gartner, McKinsey, ISO, CMMI, COBIT, MIT CISR, WEF) et l'évaluation de la maturité digitale.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

questionnaire_agent = QuestionnaireAgent()
recommendation_engine = RecommendationEngine()
scoring_agent = ScoringAgent()
benchmarking_engine = BenchmarkingEngine()


# ── Request / Response models ─────────────────────────────────────────────────

class QuestionnaireRequest(BaseModel):
    sector: str
    country: str
    company_size: Optional[str] = None
    language: str = "fr"
    num_questions: int = 30

class GeneratedQuestion(BaseModel):
    text: str
    axis: str
    sub_axis: str
    weight: int
    display_order: int
    source_framework: str = ""
    maturity_indicator: str = ""

class QuestionnaireResponse(BaseModel):
    title: str
    description: str
    sector: str
    country: str
    frameworks_used: list[str] = []
    questions: list[GeneratedQuestion]


class RecommendationRequest(BaseModel):
    evaluation_id: int
    company_name: str
    sector: str
    country: str
    global_score: float
    business_score: float
    process_score: float
    si_score: float
    canaux_score: float = 0.0
    marketing_score: float = 0.0
    rh_score: float = 0.0
    offres_score: float = 0.0
    maturity_level: str
    sub_axis_scores: Optional[list[dict]] = []
    consultant_prompt: Optional[str] = None

class RecommendationItem(BaseModel):
    axis: str
    priority: str
    title: str
    description: str
    best_practice: str

class RecommendationsResponse(BaseModel):
    evaluation_id: int
    recommendations: list[RecommendationItem]


class AnswerInput(BaseModel):
    question_text: str
    axis: str
    sub_axis: str
    weight: int = 3
    source_framework: str = ""
    value: int          # 1-5
    comment: Optional[str] = None

class ScoringRequest(BaseModel):
    company_name: str
    sector: str
    country: str
    frameworks_used: Optional[list[str]] = []
    answers: list[AnswerInput]

class SubAxisScore(BaseModel):
    sub_axis: str
    axis: str
    score: float
    question_count: int

class AxisSynthesis(BaseModel):
    axis: str
    score: float
    summary: str
    strengths: list[str] = []
    gaps: list[str] = []

class ScoringResponse(BaseModel):
    global_score: float
    business_score: float
    process_score: float
    si_score: float
    maturity_level: str
    sub_axis_scores: list[SubAxisScore] = []
    axis_syntheses: list[AxisSynthesis] = []
    critical_gaps: list[str] = []
    maturity_explanation: str = ""


# ── Benchmarking models ───────────────────────────────────────────────────────

class BenchmarkRequest(BaseModel):
    company_name: str
    sector: str
    country: str
    company_size: Optional[str] = None
    global_score: float
    business_score: float
    process_score: float
    si_score: float
    canaux_score: float = 0.0
    marketing_score: float = 0.0
    rh_score: float = 0.0
    offres_score: float = 0.0
    maturity_level: str
    consultant_prompt: Optional[str] = None

class SectorBenchmark(BaseModel):
    national_average: float
    international_average: float
    top_quartile_score: float
    company_percentile: int
    positioning_label: str
    source: str

class AxisBenchmark(BaseModel):
    axis: str
    axis_label: str
    company_score: float
    sector_average: float
    top_quartile: float
    gap_to_average: float
    gap_to_top: float

class BenchmarkTrend(BaseModel):
    title: str
    description: str
    impact_level: str
    horizon: str
    adoption_rate: str = ""
    source: str = ""

class SectorLeader(BaseModel):
    company: str
    country: str
    estimated_score: int
    key_practice: str
    differentiator: str
    source: str = ""

class RoadmapPhase(BaseModel):
    phase: str
    objective: str
    actions: list[str]
    expected_score_gain: str
    target_level: str
    investment_level: str

class BenchmarkResponse(BaseModel):
    company_name: str
    sector: str
    country: str
    global_score: float
    maturity_level: str
    executive_summary: str
    sector_benchmark: SectorBenchmark
    axis_benchmarks: list[AxisBenchmark] = []
    trends: list[BenchmarkTrend] = []
    sector_leaders: list[SectorLeader] = []
    improvement_roadmap: list[RoadmapPhase] = []
    key_insights: list[str] = []


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "IA Benchmark AI Agent",
        "version": "2.0.0",
        "frameworks_available": list(FRAMEWORKS.keys())
    }


@app.get("/api/ai/frameworks")
def list_frameworks(sector: Optional[str] = None):
    """Returns available frameworks, optionally filtered by sector relevance."""
    if sector:
        frameworks = get_frameworks_for_sector(sector)
        return {
            "sector": sector,
            "recommended_frameworks": [
                {
                    "key": fw["key"],
                    "name": fw["name"],
                    "authority": fw["authority"],
                    "focus": fw["focus"]
                }
                for fw in frameworks
            ]
        }
    return {
        "frameworks": [
            {"key": k, "name": v["name"], "authority": v["authority"], "focus": v["focus"]}
            for k, v in FRAMEWORKS.items()
        ]
    }


@app.post("/api/ai/generate-questionnaire", response_model=QuestionnaireResponse)
async def generate_questionnaire(request: QuestionnaireRequest):
    """
    Génère un questionnaire de maturité digitale grounded dans des frameworks reconnus.
    Chaque question est taguée avec son framework source et son indicateur de maturité.
    """
    try:
        result = await questionnaire_agent.generate(
            sector=request.sector,
            country=request.country,
            company_size=request.company_size,
            language=request.language,
            num_questions=request.num_questions
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@app.post("/api/ai/score", response_model=ScoringResponse)
async def score_evaluation(request: ScoringRequest):
    """
    Évalue la maturité digitale d'une entreprise à partir de ses réponses.
    Utilise l'IA pour mapper les réponses aux critères des frameworks et produire
    un score détaillé avec synthèses par axe et gaps critiques.
    """
    try:
        result = await scoring_agent.score({
            "company_name": request.company_name,
            "sector": request.sector,
            "country": request.country,
            "frameworks_used": request.frameworks_used,
            "answers": [a.model_dump() for a in request.answers]
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de scoring: {str(e)}")


@app.post("/api/ai/generate-recommendations", response_model=RecommendationsResponse)
async def generate_recommendations(request: RecommendationRequest):
    """
    Génère des recommandations IA personnalisées basées sur les scores et le contexte.
    """
    try:
        result = await recommendation_engine.generate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@app.post("/api/ai/benchmark", response_model=BenchmarkResponse)
async def generate_benchmark(request: BenchmarkRequest):
    """
    Génère une analyse de benchmarking sectoriel complète :
    positionnement national/international, tendances, leaders du secteur,
    et feuille de route d'amélioration. Fait partie du livrable rapport.
    """
    try:
        result = await benchmarking_engine.benchmark(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de benchmarking: {str(e)}")


class OptionsRegenerationRequest(BaseModel):
    questions: list[dict]  # [{text, axis, sub_axis}, ...]


@app.post("/api/ai/generate-options")
async def generate_contextual_options(request: OptionsRegenerationRequest):
    """
    Generates or regenerates contextual options for a list of existing questions.
    Each question must have at minimum: text, axis, sub_axis.
    Returns the same questions list with an 'options' array added/replaced on each.
    """
    try:
        data = {"questions": [dict(q) for q in request.questions]}
        # Force all questions to be treated as needing options
        for q in data["questions"]:
            q.pop("options", None)  # Remove existing options so _is_generic_options returns True
        data = await questionnaire_agent._fix_generic_options(data)
        return {"questions": data["questions"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération d'options: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AI_SERVICE_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
