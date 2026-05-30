package com.iabenchmark.controller;

import com.iabenchmark.dto.ActionPlanRequest;
import com.iabenchmark.dto.ActionPlanResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.service.ActionPlanService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/action-plans")
public class ActionPlanController {

    private final ActionPlanService actionPlanService;

    public ActionPlanController(ActionPlanService actionPlanService) {
        this.actionPlanService = actionPlanService;
    }

    @PostMapping("/generate/{evaluationId}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<ActionPlanResponse>> generate(
            @PathVariable Long evaluationId,
            @RequestBody List<RecommendationResponse> recommendations) {
        return ResponseEntity.ok(actionPlanService.generateFromRecommendations(evaluationId, recommendations));
    }

    @GetMapping("/{evaluationId}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<ActionPlanResponse>> getByEvaluation(@PathVariable Long evaluationId) {
        return ResponseEntity.ok(actionPlanService.getByEvaluation(evaluationId));
    }

    @GetMapping("/{evaluationId}/exists")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Map<String, Boolean>> exists(@PathVariable Long evaluationId) {
        return ResponseEntity.ok(Map.of("exists", actionPlanService.hasActionPlan(evaluationId)));
    }

    @PutMapping("/task/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<ActionPlanResponse> update(@PathVariable Long id,
                                                      @RequestBody ActionPlanRequest request) {
        return ResponseEntity.ok(actionPlanService.update(id, request));
    }

    @DeleteMapping("/task/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        actionPlanService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{evaluationId}/export")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<byte[]> exportExcel(@PathVariable Long evaluationId) {
        byte[] bytes = actionPlanService.exportToExcel(evaluationId);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"plan-action-" + evaluationId + ".xlsx\"")
                .contentType(MediaType.parseMediaType(
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
                .body(bytes);
    }
}
