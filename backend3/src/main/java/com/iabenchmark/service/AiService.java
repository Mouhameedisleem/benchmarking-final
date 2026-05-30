package com.iabenchmark.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.EvaluationAnswer;
import com.iabenchmark.repository.EvaluationRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Service
public class AiService {

    private final EvaluationRepository evaluationRepository;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    public AiService(EvaluationRepository evaluationRepository) {
        this.evaluationRepository = evaluationRepository;
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(10_000);
        factory.setReadTimeout(240_000);
        this.restTemplate = new RestTemplate(factory);
    }

    @SuppressWarnings("unchecked")
    public boolean isAiServiceAvailable() {
        try {
            ResponseEntity<Map<String, Object>> response = restTemplate.getForEntity(aiServiceUrl + "/health", (Class<Map<String, Object>>)(Class<?>)Map.class);
            return response.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Calls the AI scoring agent to enrich an EvaluationResponse with
     * AI-generated syntheses, critical gaps, and maturity explanation.
     */
    @SuppressWarnings("unchecked")
    public void enrichWithAiScoring(EvaluationResponse evalResponse, Evaluation evaluation) {
        try {
            List<Map<String, Object>> answers = new ArrayList<>();
            for (EvaluationAnswer a : evaluation.getResponses()) {
                Map<String, Object> ans = new HashMap<>();
                ans.put("question_text", a.getQuestion().getText());
                ans.put("axis", a.getQuestion().getAxis().name());
                ans.put("sub_axis", a.getQuestion().getSubAxis() != null ? a.getQuestion().getSubAxis() : "");
                ans.put("weight", a.getQuestion().getWeight() != null ? a.getQuestion().getWeight() : 3);
                ans.put("source_framework", "");
                ans.put("value", a.getScoreValue().intValue());
                ans.put("comment", a.getComment() != null ? a.getComment() : "");
                answers.add(ans);
            }

            Map<String, Object> payload = new HashMap<>();
            payload.put("company_name", evaluation.getCompany().getName());
            payload.put("sector", evaluation.getCompany().getSector() != null ? evaluation.getCompany().getSector() : "");
            payload.put("country", evaluation.getCompany().getCountry() != null ? evaluation.getCompany().getCountry() : "");
            payload.put("frameworks_used", List.of());
            payload.put("answers", answers);

            ResponseEntity<Map<String, Object>> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/score", payload, (Class<Map<String, Object>>)(Class<?>)Map.class);

            Map<String, Object> body = response.getBody();
            if (!response.getStatusCode().is2xxSuccessful() || body == null) return;

            // Enrich critical gaps
            Object gaps = body.get("critical_gaps");
            if (gaps instanceof List<?> gapList) {
                evalResponse.setCriticalGaps(gapList.stream().map(Object::toString).toList());
            }

            // Enrich maturity explanation
            Object explanation = body.get("maturity_explanation");
            if (explanation != null) {
                evalResponse.setMaturityExplanation(explanation.toString());
            }

            // Enrich axis syntheses with AI strengths/gaps
            Object synthesesObj = body.get("axis_syntheses");
            if (synthesesObj instanceof List<?> synthList) {
                for (Object s : synthList) {
                    if (!(s instanceof Map<?, ?> sm)) continue;
                    String axis = mapAxisLabel(str(sm, "axis"));
                    evalResponse.getSynthesesByAxis().stream()
                        .filter(syn -> syn.getAxis().equals(axis))
                        .findFirst()
                        .ifPresent(syn -> {
                            Object aiSummary = sm.get("summary");
                            if (aiSummary != null && !aiSummary.toString().isBlank()) {
                                // Replace rule-based summary with AI summary
                                syn.setStrengths(toStringList(sm.get("strengths")));
                                syn.setGaps(toStringList(sm.get("gaps")));
                            }
                        });
                }
            }

        } catch (Exception e) {
            // AI enrichment is best-effort — don't fail the evaluation
        }
    }

    public void generateAndStoreAiData(Evaluation evaluation) {
        try {
            List<RecommendationResponse> recs = getAiRecommendations(evaluation.getId());
            evaluation.setRecommendationsJson(objectMapper.writeValueAsString(recs));
        } catch (Exception ignored) {}
        try {
            BenchmarkResponse benchmark = getBenchmark(evaluation.getId());
            evaluation.setBenchmarkJson(objectMapper.writeValueAsString(benchmark));
        } catch (Exception ignored) {}
        try {
            if (evaluation != null) evaluationRepository.save(evaluation);
        } catch (Exception ignored) {}
    }

    public List<RecommendationResponse> getStoredRecommendations(Evaluation evaluation) {
        if (evaluation.getRecommendationsJson() == null) return List.of();
        try {
            return objectMapper.readValue(evaluation.getRecommendationsJson(),
                objectMapper.getTypeFactory().constructCollectionType(List.class, RecommendationResponse.class));
        } catch (Exception e) { return List.of(); }
    }

    public BenchmarkResponse getStoredBenchmark(Evaluation evaluation) {
        if (evaluation.getBenchmarkJson() == null) return null;
        try {
            return objectMapper.readValue(evaluation.getBenchmarkJson(), BenchmarkResponse.class);
        } catch (Exception e) { return null; }
    }

    public void updateStoredRecommendations(Evaluation evaluation, List<RecommendationResponse> recs) {
        try {
            evaluation.setRecommendationsJson(objectMapper.writeValueAsString(recs));
            evaluationRepository.save(evaluation);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to serialize recommendations", e);
        }
    }

    public void storeBenchmark(Evaluation evaluation, BenchmarkResponse benchmark) {
        try {
            evaluation.setBenchmarkJson(objectMapper.writeValueAsString(benchmark));
            evaluationRepository.save(evaluation);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to serialize benchmark", e);
        }
    }

    public List<RecommendationResponse> getAiRecommendations(Long evaluationId) {
        return getAiRecommendations(evaluationId, null);
    }

    public List<RecommendationResponse> getAiRecommendations(Long evaluationId, String consultantPrompt) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(evaluationId))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        // Compute sub-axis scores from evaluation answers
        Map<String, Double> weightedBySubAxis = new java.util.LinkedHashMap<>();
        Map<String, Integer> totalWeightsBySubAxis = new java.util.LinkedHashMap<>();
        for (EvaluationAnswer a : evaluation.getResponses()) {
            String subAxisName = a.getQuestion().getSubAxis() != null ? a.getQuestion().getSubAxis() : "";
            if (subAxisName.isEmpty()) continue;
            String key = a.getQuestion().getAxis().name() + "::" + subAxisName;
            double normalized = (a.getScoreValue() / 5.0) * 100.0;
            int weight = a.getQuestion().getWeight() != null ? a.getQuestion().getWeight() : 3;
            weightedBySubAxis.merge(key, normalized * weight, (a1, b) -> a1 + b);
            totalWeightsBySubAxis.merge(key, weight, (a1, b) -> a1 + b);
        }
        List<Map<String, Object>> subAxisScores = new ArrayList<>();
        for (Map.Entry<String, Double> entry : weightedBySubAxis.entrySet()) {
            String[] parts = entry.getKey().split("::", 2);
            if (parts.length != 2) continue;
            double score = Math.round(entry.getValue() / totalWeightsBySubAxis.get(entry.getKey()) * 10.0) / 10.0;
            Map<String, Object> sas = new HashMap<>();
            sas.put("axis", parts[0]);
            sas.put("sub_axis", parts[1]);
            sas.put("score", score);
            subAxisScores.add(sas);
        }

        Map<String, Object> payload = new HashMap<>();
        payload.put("evaluation_id", evaluationId);
        payload.put("company_name", evaluation.getCompany().getName());
        payload.put("sector", evaluation.getCompany().getSector() != null ? evaluation.getCompany().getSector() : "");
        payload.put("country", evaluation.getCompany().getCountry() != null ? evaluation.getCompany().getCountry() : "");
        payload.put("global_score", evaluation.getGlobalScore());
        payload.put("business_score", evaluation.getBusinessScore());
        payload.put("process_score", evaluation.getProcessScore());
        payload.put("si_score", evaluation.getInformationSystemScore());
        payload.put("canaux_score", evaluation.getCanauxDistributionScore());
        payload.put("marketing_score", evaluation.getMarketingCommunicationScore());
        payload.put("rh_score", evaluation.getRhCultureDigitaleScore());
        payload.put("offres_score", evaluation.getOffresDigitalesScore());
        payload.put("modele_operationnel_score", evaluation.getModeleOperationnelScore());
        payload.put("it_data_score", evaluation.getItDataScore());
        payload.put("maturity_level", evaluation.getMaturityLevel().name());
        payload.put("sub_axis_scores", subAxisScores);
        if (consultantPrompt != null && !consultantPrompt.isBlank()) {
            payload.put("consultant_prompt", consultantPrompt);
        }

        try {
            @SuppressWarnings("unchecked")
            ResponseEntity<Map<String, Object>> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/generate-recommendations", payload, (Class<Map<String, Object>>)(Class<?>)Map.class);
            Map<String, Object> recBody = response.getBody();
            if (response.getStatusCode().is2xxSuccessful() && recBody != null) {
                return parseRecommendations(recBody);
            }
        } catch (Exception e) {
            throw new RuntimeException("AI service unavailable: " + e.getMessage());
        }
        return List.of();
    }

    public BenchmarkResponse getBenchmark(Long evaluationId) {
        return getBenchmark(evaluationId, null);
    }

    public BenchmarkResponse getBenchmark(Long evaluationId, String consultantPrompt) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(evaluationId))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        // Compute sub-axis scores from evaluation answers
        Map<String, Double> weightedBySubAxis = new java.util.LinkedHashMap<>();
        Map<String, Integer> totalWeightsBySubAxis = new java.util.LinkedHashMap<>();
        for (EvaluationAnswer a : evaluation.getResponses()) {
            String subAxisName = a.getQuestion().getSubAxis() != null ? a.getQuestion().getSubAxis() : "";
            if (subAxisName.isEmpty()) continue;
            String key = a.getQuestion().getAxis().name() + "::" + subAxisName;
            double normalized = (a.getScoreValue() / 5.0) * 100.0;
            int weight = a.getQuestion().getWeight() != null ? a.getQuestion().getWeight() : 3;
            weightedBySubAxis.merge(key, normalized * weight, (a1, b) -> a1 + b);
            totalWeightsBySubAxis.merge(key, weight, (a1, b) -> a1 + b);
        }
        List<Map<String, Object>> subAxisScores = new ArrayList<>();
        for (Map.Entry<String, Double> entry : weightedBySubAxis.entrySet()) {
            String[] parts = entry.getKey().split("::", 2);
            if (parts.length != 2) continue;
            double score = Math.round(entry.getValue() / totalWeightsBySubAxis.get(entry.getKey()) * 10.0) / 10.0;
            Map<String, Object> sas = new HashMap<>();
            sas.put("axis", parts[0]);
            sas.put("sub_axis", parts[1]);
            sas.put("score", score);
            sas.put("question_count", totalWeightsBySubAxis.get(entry.getKey()));
            subAxisScores.add(sas);
        }

        Map<String, Object> payload = new HashMap<>();
        payload.put("company_name",              evaluation.getCompany().getName());
        payload.put("sector",                    evaluation.getCompany().getSector() != null ? evaluation.getCompany().getSector() : "");
        payload.put("country",                   evaluation.getCompany().getCountry() != null ? evaluation.getCompany().getCountry() : "");
        payload.put("company_size",              evaluation.getCompany().getSize() != null ? evaluation.getCompany().getSize() : "");
        payload.put("global_score",              evaluation.getGlobalScore());
        payload.put("business_score",            evaluation.getBusinessScore());
        payload.put("process_score",             evaluation.getProcessScore());
        payload.put("si_score",                  evaluation.getInformationSystemScore());
        payload.put("canaux_score",              evaluation.getCanauxDistributionScore());
        payload.put("marketing_score",           evaluation.getMarketingCommunicationScore());
        payload.put("rh_score",                  evaluation.getRhCultureDigitaleScore());
        payload.put("offres_score",              evaluation.getOffresDigitalesScore());
        payload.put("modele_operationnel_score", evaluation.getModeleOperationnelScore());
        payload.put("it_data_score",             evaluation.getItDataScore());
        payload.put("maturity_level",            evaluation.getMaturityLevel().name());
        payload.put("sub_axis_scores",           subAxisScores);
        if (consultantPrompt != null && !consultantPrompt.isBlank()) {
            payload.put("consultant_prompt", consultantPrompt);
        }

        try {
            @SuppressWarnings("unchecked")
            ResponseEntity<Map<String, Object>> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/benchmark", payload, (Class<Map<String, Object>>)(Class<?>)Map.class);

            Map<String, Object> benchBody = response.getBody();
            if (!response.getStatusCode().is2xxSuccessful() || benchBody == null) {
                throw new RuntimeException("AI service returned non-2xx response");
            }
            return parseBenchmarkResponse(benchBody, evaluation);
        } catch (Exception e) {
            throw new RuntimeException("AI benchmark service unavailable: " + e.getMessage());
        }
    }

    private BenchmarkResponse parseBenchmarkResponse(Map<String, Object> body, Evaluation evaluation) {
        BenchmarkResponse res = new BenchmarkResponse();
        res.setCompanyName(str(body, "company_name"));
        res.setSector(str(body, "sector"));
        res.setCountry(str(body, "country"));
        res.setGlobalScore(toDouble(body.get("global_score")));
        res.setMaturityLevel(str(body, "maturity_level"));
        res.setExecutiveSummary(str(body, "executive_summary"));
        res.setKeyInsights(toStringList(body.get("key_insights")));

        // Sector benchmark
        Object sbObj = body.get("sector_benchmark");
        if (sbObj instanceof Map<?, ?> sb) {
            BenchmarkResponse.SectorBenchmark sectorBenchmark = new BenchmarkResponse.SectorBenchmark();
            sectorBenchmark.setNationalAverage(toDouble(sb.get("national_average")));
            sectorBenchmark.setInternationalAverage(toDouble(sb.get("international_average")));
            sectorBenchmark.setTopQuartileScore(toDouble(sb.get("top_quartile_score")));
            sectorBenchmark.setCompanyPercentile(toInt(sb.get("company_percentile")));
            sectorBenchmark.setPositioningLabel(str((Map<?,?>)sb, "positioning_label"));
            sectorBenchmark.setSource(str((Map<?,?>)sb, "source"));
            res.setSectorBenchmark(sectorBenchmark);
        }

        // Axis benchmarks
        Object abList = body.get("axis_benchmarks");
        if (abList instanceof List<?> list) {
            res.setAxisBenchmarks(list.stream().filter(i -> i instanceof Map).map(i -> {
                Map<?,?> m = (Map<?,?>) i;
                BenchmarkResponse.AxisBenchmark ab = new BenchmarkResponse.AxisBenchmark();
                ab.setAxis(str(m, "axis"));
                ab.setAxisLabel(str(m, "axis_label"));
                ab.setCompanyScore(toDouble(m.get("company_score")));
                ab.setSectorAverage(toDouble(m.get("sector_average")));
                ab.setTopQuartile(toDouble(m.get("top_quartile")));
                ab.setGapToAverage(toDouble(m.get("gap_to_average")));
                ab.setGapToTop(toDouble(m.get("gap_to_top")));
                return ab;
            }).toList());
        }

        // Trends
        Object tList = body.get("trends");
        if (tList instanceof List<?> list) {
            res.setTrends(list.stream().filter(i -> i instanceof Map).map(i -> {
                Map<?,?> m = (Map<?,?>) i;
                BenchmarkResponse.BenchmarkTrend t = new BenchmarkResponse.BenchmarkTrend();
                t.setTitle(str(m, "title"));
                t.setDescription(str(m, "description"));
                t.setImpactLevel(str(m, "impact_level"));
                t.setHorizon(str(m, "horizon"));
                t.setAdoptionRate(str(m, "adoption_rate"));
                t.setSource(str(m, "source"));
                t.setSourceUrl(str(m, "source_url"));
                return t;
            }).toList());
        }

        // Sector leaders
        Object lList = body.get("sector_leaders");
        if (lList instanceof List<?> list) {
            res.setSectorLeaders(list.stream().filter(i -> i instanceof Map).map(i -> {
                Map<?,?> m = (Map<?,?>) i;
                BenchmarkResponse.SectorLeader l = new BenchmarkResponse.SectorLeader();
                l.setCompany(str(m, "company"));
                l.setCountry(str(m, "country"));
                l.setEstimatedScore(toInt(m.get("estimated_score")));
                l.setKeyPractice(str(m, "key_practice"));
                l.setDifferentiator(str(m, "differentiator"));
                l.setSource(str(m, "source"));
                l.setSourceUrl(str(m, "source_url"));
                return l;
            }).toList());
        }

        // Roadmap
        Object rList = body.get("improvement_roadmap");
        if (rList instanceof List<?> list) {
            res.setImprovementRoadmap(list.stream().filter(i -> i instanceof Map).map(i -> {
                Map<?,?> m = (Map<?,?>) i;
                BenchmarkResponse.RoadmapPhase p = new BenchmarkResponse.RoadmapPhase();
                p.setPhase(str(m, "phase"));
                p.setObjective(str(m, "objective"));
                p.setActions(toStringList(m.get("actions")));
                p.setExpectedScoreGain(str(m, "expected_score_gain"));
                p.setTargetLevel(str(m, "target_level"));
                p.setInvestmentLevel(str(m, "investment_level"));
                return p;
            }).toList());
        }

        // Sub-axis benchmarks
        Object sabList = body.get("sub_axis_benchmarks");
        if (sabList instanceof List<?> list) {
            res.setSubAxisBenchmarks(list.stream().filter(i -> i instanceof Map).map(i -> {
                Map<?,?> m = (Map<?,?>) i;
                BenchmarkResponse.SubAxisBenchmark sab = new BenchmarkResponse.SubAxisBenchmark();
                sab.setAxis(str(m, "axis"));
                sab.setSubAxis(str(m, "sub_axis"));
                sab.setCompanyScore(toDouble(m.get("company_score")));
                sab.setAnalyseStatique(str(m, "analyse_statique"));
                sab.setMaturiteMaximale(str(m, "maturite_maximale"));
                sab.setAnalysePersonnalisee(str(m, "analyse_personnalisee"));
                sab.setTendances(toListOfMaps(m.get("tendances")));
                sab.setCadreJuridique(toListOfMaps(m.get("cadre_juridique")));
                sab.setMaLeveesFonds(toListOfMaps(m.get("ma_levees_fonds")));
                sab.setLeadersNationaux(toListOfMaps(m.get("leaders_nationaux")));
                sab.setLeadersRegionaux(toListOfMaps(m.get("leaders_regionaux")));
                sab.setLeadersInternationaux(toListOfMaps(m.get("leaders_internationaux")));
                sab.setZoomCaseStudy(toSingleMap(m.get("zoom_case_study")));
                sab.setComparatifOrganisations(toSingleMap(m.get("comparatif_organisations")));
                sab.setRisques(toListOfMaps(m.get("risques")));
                sab.setOpportunites(toListOfMaps(m.get("opportunites")));
                return sab;
            }).toList());
        }

        return res;
    }

    private Double toDouble(Object v) {
        if (v == null) return 0.0;
        if (v instanceof Number n) return n.doubleValue();
        try { return Double.parseDouble(v.toString()); } catch (Exception e) { return 0.0; }
    }

    private Integer toInt(Object v) {
        if (v == null) return 0;
        if (v instanceof Number n) return n.intValue();
        try { return Integer.parseInt(v.toString()); } catch (Exception e) { return 0; }
    }

    // ...existing code...
    @SuppressWarnings("unchecked")
    private List<RecommendationResponse> parseRecommendations(Map<String, Object> body) {
        Object recs = body.get("recommendations");
        if (!(recs instanceof List<?> list)) return List.of();
        return list.stream()
            .filter(item -> item instanceof Map)
            .map(item -> {
                Map<String, Object> m = (Map<String, Object>) item;
                RecommendationResponse r = new RecommendationResponse(str(m, "axis"), str(m, "priority"),
                    str(m, "title"), str(m, "description"), str(m, "best_practice"));
                r.setSource(str(m, "source"));
                r.setSourceUrl(str(m, "source_url"));
                return r;
            }).toList();
    }

    private String mapAxisLabel(String axis) {
        return switch (axis.toUpperCase()) {
            case "BUSINESS" -> "METIER";
            case "PROCESS" -> "PROCESSUS";
            case "INFORMATION_SYSTEM" -> "SI";
            default -> axis.toUpperCase();
        };
    }

    private List<String> toStringList(Object obj) {
        if (obj instanceof List<?> list) return list.stream().map(Object::toString).toList();
        return List.of();
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> toListOfMaps(Object obj) {
        if (!(obj instanceof List<?> list)) return List.of();
        return list.stream()
            .filter(i -> i instanceof Map)
            .map(i -> (Map<String, Object>) i)
            .toList();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> toSingleMap(Object obj) {
        if (obj instanceof Map<?, ?> m) return (Map<String, Object>) m;
        return Map.of();
    }

    private String str(Map<?, ?> m, String key) {
        Object v = m.get(key);
        return v != null ? v.toString() : "";
    }
}
