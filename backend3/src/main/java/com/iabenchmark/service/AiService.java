package com.iabenchmark.service;

import com.iabenchmark.dto.AxisSynthesisResponse;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.EvaluationAnswer;
import com.iabenchmark.repository.EvaluationRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AiService {

    private final EvaluationRepository evaluationRepository;
    private final RestTemplate restTemplate;

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    public AiService(EvaluationRepository evaluationRepository) {
        this.evaluationRepository = evaluationRepository;
        this.restTemplate = new RestTemplate();
    }

    public boolean isAiServiceAvailable() {
        try {
            ResponseEntity<Map> response = restTemplate.getForEntity(aiServiceUrl + "/health", Map.class);
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

            ResponseEntity<Map> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/score", payload, Map.class);

            if (!response.getStatusCode().is2xxSuccessful() || response.getBody() == null) return;

            Map<String, Object> body = response.getBody();

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

    public List<RecommendationResponse> getAiRecommendations(Long evaluationId) {
        Evaluation evaluation = evaluationRepository.findById(evaluationId)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        Map<String, Object> payload = new HashMap<>();
        payload.put("evaluation_id", evaluationId);
        payload.put("company_name", evaluation.getCompany().getName());
        payload.put("sector", evaluation.getCompany().getSector() != null ? evaluation.getCompany().getSector() : "");
        payload.put("country", evaluation.getCompany().getCountry() != null ? evaluation.getCompany().getCountry() : "");
        payload.put("global_score", evaluation.getGlobalScore());
        payload.put("business_score", evaluation.getBusinessScore());
        payload.put("process_score", evaluation.getProcessScore());
        payload.put("si_score", evaluation.getInformationSystemScore());
        payload.put("maturity_level", evaluation.getMaturityLevel().name());

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/generate-recommendations", payload, Map.class);
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return parseRecommendations(response.getBody());
            }
        } catch (Exception e) {
            throw new RuntimeException("AI service unavailable: " + e.getMessage());
        }
        return List.of();
    }

    @SuppressWarnings("unchecked")
    private List<RecommendationResponse> parseRecommendations(Map<String, Object> body) {
        Object recs = body.get("recommendations");
        if (!(recs instanceof List<?> list)) return List.of();
        return list.stream()
            .filter(item -> item instanceof Map)
            .map(item -> {
                Map<String, Object> m = (Map<String, Object>) item;
                return new RecommendationResponse(str(m, "axis"), str(m, "priority"),
                    str(m, "title"), str(m, "description"), str(m, "best_practice"));
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

    @SuppressWarnings("unchecked")
    private List<String> toStringList(Object obj) {
        if (obj instanceof List<?> list) return list.stream().map(Object::toString).toList();
        return List.of();
    }

    private String str(Map<?, ?> m, String key) {
        Object v = m.get(key);
        return v != null ? v.toString() : "";
    }
}
