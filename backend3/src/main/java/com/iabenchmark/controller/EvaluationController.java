package com.iabenchmark.controller;

import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.dto.EvaluationRequest;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.UserRepository;
import com.iabenchmark.security.UserDetailsImpl;
import com.iabenchmark.service.AiService;
import com.iabenchmark.service.EmailService;
import com.iabenchmark.service.EvaluationService;
import com.iabenchmark.service.RecommendationService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/evaluations")
public class EvaluationController {
    private final EvaluationService evaluationService;
    private final RecommendationService recommendationService;
    private final AiService aiService;
    private final EvaluationRepository evaluationRepository;
    private final EmailService emailService;
    private final UserRepository userRepository;

    public EvaluationController(EvaluationService evaluationService,
                                RecommendationService recommendationService,
                                AiService aiService,
                                EvaluationRepository evaluationRepository,
                                EmailService emailService,
                                UserRepository userRepository) {
        this.evaluationService = evaluationService;
        this.recommendationService = recommendationService;
        this.aiService = aiService;
        this.evaluationRepository = evaluationRepository;
        this.emailService = emailService;
        this.userRepository = userRepository;
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

    @GetMapping("/all")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<Map<String, Object>>> getAllEvaluations() {
        List<Map<String, Object>> result = evaluationRepository.findAll()
                .stream()
                .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
                .map(ev -> {
                    Map<String, Object> item = new java.util.LinkedHashMap<>();
                    item.put("evaluationId", ev.getId());
                    item.put("companyId", ev.getCompany().getId());
                    item.put("companyName", ev.getCompany().getName());
                    item.put("consultantName", ev.getCompany().getConsultant() != null
                            ? ev.getCompany().getConsultant().getFirstName() + " " + ev.getCompany().getConsultant().getLastName()
                            : null);
                    item.put("globalScore", ev.getGlobalScore());
                    item.put("businessScore", ev.getBusinessScore());
                    item.put("processScore", ev.getProcessScore());
                    item.put("siScore", ev.getInformationSystemScore());
                    item.put("canauxDistributionScore", ev.getCanauxDistributionScore());
                    item.put("marketingCommunicationScore", ev.getMarketingCommunicationScore());
                    item.put("rhCultureDigitaleScore", ev.getRhCultureDigitaleScore());
                    item.put("offresDigitalesScore", ev.getOffresDigitalesScore());
                    item.put("maturityLevel", ev.getMaturityLevel().name());
                    item.put("status", ev.isValidated() ? "VALIDATED" : ev.isPendingReview() ? "PENDING_REVIEW" : "IN_PROGRESS");
                    item.put("createdAt", ev.getCreatedAt());
                    return item;
                }).toList();
        return ResponseEntity.ok(result);
    }

    @GetMapping("/pending-review")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<Map<String, Object>>> getPendingReviews(
            @AuthenticationPrincipal UserDetailsImpl principal) {
        User currentUser = userRepository.findByEmail(principal.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        List<com.iabenchmark.model.Evaluation> evaluations = currentUser.getRole() == Role.ADMIN
                ? evaluationRepository.findByPendingReviewTrueOrderByCreatedAtDesc()
                : evaluationRepository.findByPendingReviewTrueAndCompanyConsultantIdOrderByCreatedAtDesc(currentUser.getId());

        List<Map<String, Object>> result = evaluations.stream()
                .map(ev -> {
                    Map<String, Object> item = new java.util.LinkedHashMap<>();
                    item.put("evaluationId", ev.getId());
                    item.put("companyId", ev.getCompany().getId());
                    item.put("companyName", ev.getCompany().getName());
                    item.put("globalScore", ev.getGlobalScore());
                    item.put("maturityLevel", ev.getMaturityLevel().name());
                    item.put("status", ev.isValidated() ? "DELIVERED" : "PENDING_REVIEW");
                    item.put("createdAt", ev.getCreatedAt());
                    return item;
                }).toList();
        return ResponseEntity.ok(result);
    }

    @GetMapping("/{id}/recommendations")
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

    @GetMapping("/{id}/benchmark")
    public ResponseEntity<BenchmarkResponse> getBenchmark(@PathVariable Long id) {
        if (!aiService.isAiServiceAvailable()) {
            return ResponseEntity.status(503).build();
        }
        return ResponseEntity.ok(aiService.getBenchmark(id));
    }

    @GetMapping("/{id}/full-review")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Map<String, Object>> getFullReview(@PathVariable Long id) {
        Evaluation evaluation = evaluationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        EvaluationResponse evalResponse = evaluationService.getEvaluation(id);
        List<RecommendationResponse> recs = aiService.getStoredRecommendations(evaluation);
        BenchmarkResponse benchmark = aiService.getStoredBenchmark(evaluation);

        // AI is pending only if no recommendations have been generated at all
        boolean aiPending = recs.isEmpty();

        Map<String, Object> body = new java.util.LinkedHashMap<>();
        body.put("evaluation", evalResponse);
        body.put("recommendations", recs);
        body.put("benchmark", benchmark != null ? benchmark : Map.of());
        body.put("pendingReview", evaluation.isPendingReview());
        body.put("validated", evaluation.isValidated());
        body.put("aiPending", aiPending);
        return ResponseEntity.ok(body);
    }

    @PutMapping("/{id}/recommendations")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> updateRecommendations(@PathVariable Long id,
                                                      @RequestBody List<RecommendationResponse> recommendations) {
        Evaluation evaluation = evaluationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        aiService.updateStoredRecommendations(evaluation, recommendations);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{id}/regenerate")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<RecommendationResponse>> regenerateWithPrompt(
            @PathVariable Long id,
            @RequestBody Map<String, String> body) {
        Evaluation evaluation = evaluationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        String consultantPrompt = body.getOrDefault("consultantPrompt", "");
        List<RecommendationResponse> recs = aiService.getAiRecommendations(id, consultantPrompt);
        aiService.updateStoredRecommendations(evaluation, recs);
        return ResponseEntity.ok(recs);
    }

    @PostMapping("/{id}/regenerate-benchmark")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<BenchmarkResponse> regenerateBenchmarkWithPrompt(
            @PathVariable Long id,
            @RequestBody Map<String, String> body) {
        Evaluation evaluation = evaluationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        String consultantPrompt = body.getOrDefault("consultantPrompt", "");
        BenchmarkResponse bench = aiService.getBenchmark(id, consultantPrompt);
        aiService.storeBenchmark(evaluation, bench);
        return ResponseEntity.ok(bench);
    }

    @PostMapping("/{id}/validate")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Map<String, String>> validateAndSendResults(
            @PathVariable Long id,
            @RequestBody List<RecommendationResponse> finalRecommendations) {
        Evaluation evaluation = evaluationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        aiService.updateStoredRecommendations(evaluation, finalRecommendations);
        evaluation.setPendingReview(false);
        evaluation.setValidated(true);
        evaluationRepository.save(evaluation);

        String companyEmail = evaluation.getCompany().getEmail();
        String companyName = evaluation.getCompany().getName();
        String emailStatus;
        if (companyEmail != null && !companyEmail.isBlank()) {
            try {
                BenchmarkResponse benchmark = aiService.getStoredBenchmark(evaluation);
                emailService.sendEvaluationResults(companyEmail, companyName, evaluation, finalRecommendations, benchmark);
                emailStatus = "Résultats envoyés à " + companyEmail;
            } catch (Exception e) {
                emailStatus = "Validation enregistrée. Erreur d'envoi email : " + e.getMessage();
            }
        } else {
            emailStatus = "Validation enregistrée. Aucun email configuré pour cette entreprise.";
        }

        return ResponseEntity.ok(Map.of("message", emailStatus));
    }
}
