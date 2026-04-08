package com.iabenchmark.controller;

import com.iabenchmark.dto.EvaluationRequest;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.service.AiService;
import com.iabenchmark.service.EvaluationService;
import com.iabenchmark.service.RecommendationService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/evaluations")
@CrossOrigin(origins = "*")
public class EvaluationController {
    private final EvaluationService evaluationService;
    private final RecommendationService recommendationService;
    private final AiService aiService;

    public EvaluationController(EvaluationService evaluationService,
                                RecommendationService recommendationService,
                                AiService aiService) {
        this.evaluationService = evaluationService;
        this.recommendationService = recommendationService;
        this.aiService = aiService;
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('CLIENT', 'CONSULTANT', 'ADMIN')")
    public ResponseEntity<EvaluationResponse> submitEvaluation(@Valid @RequestBody EvaluationRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(evaluationService.submitEvaluation(request));
    }

    @GetMapping("/{id}")
    public ResponseEntity<EvaluationResponse> getEvaluation(@PathVariable Long id) {
        return ResponseEntity.ok(evaluationService.getEvaluation(id));
    }

    @GetMapping
    public ResponseEntity<List<EvaluationResponse>> getCompanyEvaluations(@RequestParam Long companyId) {
        return ResponseEntity.ok(evaluationService.getCompanyEvaluations(companyId));
    }

    @GetMapping("/latest")
    public ResponseEntity<EvaluationResponse> getLatestCompanyEvaluation(@RequestParam Long companyId) {
        return ResponseEntity.ok(evaluationService.getLatestCompanyEvaluation(companyId));
    }

    @GetMapping("/{id}/recommendations")
    @PreAuthorize("hasAnyRole('CLIENT', 'CONSULTANT', 'ADMIN')")
    public ResponseEntity<List<RecommendationResponse>> getRecommendations(@PathVariable Long id) {
        if (aiService.isAiServiceAvailable()) {
            try {
                return ResponseEntity.ok(aiService.getAiRecommendations(id));
            } catch (Exception ignored) {
                // AI service failed — fall through to rule-based
            }
        }
        return ResponseEntity.ok(recommendationService.generateRecommendations(id));
    }
}
