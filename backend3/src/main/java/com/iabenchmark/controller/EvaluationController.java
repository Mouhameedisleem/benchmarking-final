package com.iabenchmark.controller;

import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.dto.EvaluationRequest;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.MaturityLevel;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.UserRepository;
import com.iabenchmark.security.UserDetailsImpl;
import com.iabenchmark.service.ActionPlanService;
import com.iabenchmark.service.AiService;
import com.iabenchmark.service.EmailService;
import com.iabenchmark.service.EvaluationService;
import com.iabenchmark.service.NotificationSseService;
import com.iabenchmark.service.PdfReportService;
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
import java.util.Objects;

@RestController
@RequestMapping("/api/evaluations")
public class EvaluationController {
    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(EvaluationController.class);
    private final EvaluationService evaluationService;
    private final RecommendationService recommendationService;
    private final AiService aiService;
    private final EvaluationRepository evaluationRepository;
    private final EmailService emailService;
    private final UserRepository userRepository;
    private final PdfReportService pdfReportService;
    private final NotificationSseService notificationSseService;
    private final ActionPlanService actionPlanService;

    public EvaluationController(EvaluationService evaluationService,
                                RecommendationService recommendationService,
                                AiService aiService,
                                EvaluationRepository evaluationRepository,
                                EmailService emailService,
                                UserRepository userRepository,
                                PdfReportService pdfReportService,
                                NotificationSseService notificationSseService,
                                ActionPlanService actionPlanService) {
        this.evaluationService = evaluationService;
        this.recommendationService = recommendationService;
        this.aiService = aiService;
        this.evaluationRepository = evaluationRepository;
        this.emailService = emailService;
        this.userRepository = userRepository;
        this.pdfReportService = pdfReportService;
        this.notificationSseService = notificationSseService;
        this.actionPlanService = actionPlanService;
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('CLIENT', 'CONSULTANT', 'ADMIN')")
    public ResponseEntity<EvaluationResponse> submitEvaluation(@Valid @RequestBody EvaluationRequest request) {
        EvaluationResponse response = evaluationService.submitEvaluation(request);
        try {
            Evaluation ev = evaluationRepository.findById(Objects.requireNonNull(response.getEvaluationId())).orElse(null);
            if (ev != null && ev.isPendingReview()) {
                String companyName = ev.getCompany().getName();
                String message = companyName + " vient de soumettre son évaluation";
                // Notifie le consultant assigné si présent
                if (ev.getCompany().getConsultant() != null) {
                    notificationSseService.notifyUser(Objects.requireNonNull(ev.getCompany().getConsultant().getId()), message, "EVALUATION_SUBMITTED");
                }
                // Notifie toujours tous les admins connectés
                userRepository.findByRole(com.iabenchmark.model.Role.ADMIN).forEach(admin ->
                    notificationSseService.notifyUser(Objects.requireNonNull(admin.getId()), message, "EVALUATION_SUBMITTED")
                );
            }
        } catch (Exception ignored) {}
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
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
        EvaluationResponse evaluation = evaluationService.getLatestCompanyEvaluation(companyId);
        if (evaluation == null) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(evaluation);
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

        // Deduplicate: keep only the most recent evaluation per company
        java.util.Map<Long, com.iabenchmark.model.Evaluation> latestByCompany = new java.util.LinkedHashMap<>();
        for (com.iabenchmark.model.Evaluation ev : evaluations) {
            latestByCompany.putIfAbsent(ev.getCompany().getId(), ev);
        }

        List<Map<String, Object>> result = latestByCompany.values().stream()
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
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        // Return stored recommendations if already generated
        List<RecommendationResponse> stored = aiService.getStoredRecommendations(evaluation);
        if (!stored.isEmpty()) {
            return ResponseEntity.ok(stored);
        }

        if (aiService.isAiServiceAvailable()) {
            try {
                List<RecommendationResponse> recs = aiService.getAiRecommendations(id);
                aiService.updateStoredRecommendations(evaluation, recs);
                return ResponseEntity.ok(recs);
            } catch (Exception ignored) {
                // AI service failed — fall through to rule-based
            }
        }
        return ResponseEntity.ok(recommendationService.generateRecommendations(id));
    }

    @GetMapping("/{id}/benchmark")
    public ResponseEntity<BenchmarkResponse> getBenchmark(@PathVariable Long id) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        // Return stored benchmark if already generated — avoids regenerating on every view
        BenchmarkResponse stored = aiService.getStoredBenchmark(evaluation);
        if (stored != null) {
            return ResponseEntity.ok(stored);
        }

        if (!aiService.isAiServiceAvailable()) {
            return ResponseEntity.status(503).build();
        }

        BenchmarkResponse benchmark = aiService.getBenchmark(id);
        aiService.storeBenchmark(evaluation, benchmark);
        return ResponseEntity.ok(benchmark);
    }

    @PostMapping("/{id}/benchmark/regenerate")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<BenchmarkResponse> regenerateBenchmark(@PathVariable Long id) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        if (!aiService.isAiServiceAvailable()) {
            return ResponseEntity.status(503).build();
        }

        BenchmarkResponse benchmark = aiService.getBenchmark(id);
        aiService.storeBenchmark(evaluation, benchmark);
        return ResponseEntity.ok(benchmark);
    }

    @GetMapping("/dashboard")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<Map<String, Object>>> getDashboardData(
            @AuthenticationPrincipal UserDetailsImpl principal) {
        User currentUser = userRepository.findByEmail(principal.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        List<Evaluation> evaluations = currentUser.getRole() == Role.ADMIN
                ? evaluationRepository.findAll().stream()
                    .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
                    .toList()
                : evaluationRepository.findByCompanyConsultantIdOrderByCreatedAtDesc(currentUser.getId());

        List<Map<String, Object>> result = evaluations.stream()
                .map(ev -> {
                    Map<String, Object> item = new java.util.LinkedHashMap<>();
                    item.put("evaluationId", ev.getId());
                    item.put("companyId",    ev.getCompany().getId());
                    item.put("companyName",  ev.getCompany().getName());
                    item.put("sector",       ev.getCompany().getSector());
                    item.put("country",      ev.getCompany().getCountry());
                    item.put("companySize",  ev.getCompany().getSize());
                    item.put("globalScore",  ev.getGlobalScore());
                    item.put("maturityLevel", ev.getMaturityLevel() != null ? ev.getMaturityLevel().name() : null);
                    item.put("status", ev.isValidated() ? "VALIDATED"
                            : ev.isPendingReview() ? "PENDING_REVIEW" : "IN_PROGRESS");
                    item.put("createdAt", ev.getCreatedAt());
                    return item;
                }).toList();
        return ResponseEntity.ok(result);
    }

    @GetMapping("/rapport")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<Map<String, Object>>> getRapportGlobal(
            @AuthenticationPrincipal UserDetailsImpl principal) {
        User currentUser = userRepository.findByEmail(principal.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        List<Evaluation> evaluations = currentUser.getRole() == Role.ADMIN
                ? evaluationRepository.findAll().stream()
                    .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
                    .toList()
                : evaluationRepository.findByCompanyConsultantIdOrderByCreatedAtDesc(currentUser.getId());

        List<Map<String, Object>> result = evaluations.stream()
                .map(ev -> {
                    EvaluationResponse evalResp = evaluationService.getEvaluation(ev.getId());
                    Map<String, Object> item = new java.util.LinkedHashMap<>();
                    item.put("evaluationId", ev.getId());
                    item.put("companyId", ev.getCompany().getId());
                    item.put("companyName", ev.getCompany().getName());
                    item.put("globalScore", ev.getGlobalScore());
                    item.put("maturityLevel", ev.getMaturityLevel().name());
                    item.put("status", ev.isValidated() ? "VALIDATED"
                            : ev.isPendingReview() ? "PENDING_REVIEW" : "IN_PROGRESS");
                    item.put("createdAt", ev.getCreatedAt());
                    item.put("answerSummaries", evalResp.getAnswerSummaries());
                    return item;
                }).toList();
        return ResponseEntity.ok(result);
    }

    @GetMapping("/{id}/full-review")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Map<String, Object>> getFullReview(@PathVariable Long id) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
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

    @GetMapping("/{id}/report/pdf")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT', 'CLIENT')")
    public ResponseEntity<byte[]> downloadPdfReport(@PathVariable Long id) {
        byte[] pdf = pdfReportService.generateReport(id);
        String filename = "rapport-evaluation-" + id + ".pdf";
        return ResponseEntity.ok()
                .header("Content-Type", "application/pdf")
                .header("Content-Disposition", "attachment; filename=\"" + filename + "\"")
                .body(pdf);
    }

    @PutMapping("/{id}/target-maturity")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> setTargetMaturity(@PathVariable Long id,
                                                  @RequestBody Map<String, String> body) {
        String level = body.get("targetMaturityLevel");
        evaluationService.setTargetMaturity(id, MaturityLevel.valueOf(level));
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/{id}/recommendations")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> updateRecommendations(@PathVariable Long id,
                                                      @RequestBody List<RecommendationResponse> recommendations) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        aiService.updateStoredRecommendations(evaluation, recommendations);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{id}/regenerate")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<RecommendationResponse>> regenerateWithPrompt(
            @PathVariable Long id,
            @RequestBody Map<String, String> body) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        String consultantPrompt = body.getOrDefault("consultantPrompt", "");
        List<RecommendationResponse> recs;
        try {
            recs = aiService.getAiRecommendations(id, consultantPrompt);
        } catch (Exception aiEx) {
            try {
                recs = recommendationService.generateRecommendations(id);
            } catch (Exception fallbackEx) {
                recs = List.of();
            }
        }
        try {
            aiService.updateStoredRecommendations(evaluation, recs);
        } catch (Exception ignored) {}
        return ResponseEntity.ok(recs);
    }

    @PostMapping("/{id}/regenerate-benchmark")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<BenchmarkResponse> regenerateBenchmarkWithPrompt(
            @PathVariable Long id,
            @RequestBody Map<String, String> body) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));
        String consultantPrompt = body.getOrDefault("consultantPrompt", "");
        BenchmarkResponse bench;
        try {
            bench = aiService.getBenchmark(id, consultantPrompt);
            aiService.storeBenchmark(evaluation, bench);
        } catch (Exception e) {
            log.error("regenerate-benchmark failed for evaluation {}: {}", id, e.getMessage(), e);
            return ResponseEntity.status(503)
                    .body(null);
        }
        return ResponseEntity.ok(bench);
    }

    @PostMapping("/{id}/validate")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Map<String, String>> validateAndSendResults(
            @PathVariable Long id,
            @RequestBody com.iabenchmark.dto.ValidateRequest request) {
        List<RecommendationResponse> finalRecommendations =
                request.getRecommendations() != null ? request.getRecommendations() : List.of();

        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + id));

        aiService.updateStoredRecommendations(evaluation, finalRecommendations);
        evaluation.setPendingReview(false);
        evaluation.setValidated(true);
        evaluationRepository.save(evaluation);

        try { actionPlanService.generateFromRecommendations(id, finalRecommendations); } catch (Exception ignored) {}

        String companyEmail = evaluation.getCompany().getEmail();
        String companyName  = evaluation.getCompany().getName();
        String emailStatus;
        if (companyEmail != null && !companyEmail.isBlank()) {
            try {
                BenchmarkResponse benchmark = aiService.getStoredBenchmark(evaluation);
                byte[] pdfBytes = null;
                try { pdfBytes = pdfReportService.generateReport(id); } catch (Exception ignored) {}
                // Decode PPT from base64 if provided by the frontend
                byte[] pptBytes = null;
                if (request.getPptBase64() != null && !request.getPptBase64().isBlank()) {
                    try { pptBytes = java.util.Base64.getDecoder().decode(request.getPptBase64()); }
                    catch (Exception ignored) {}
                }
                emailService.sendEvaluationResults(companyEmail, companyName, evaluation,
                        finalRecommendations, benchmark, id, pdfBytes, pptBytes);
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
