package com.iabenchmark.service;

import com.iabenchmark.dto.ActionPlanRequest;
import com.iabenchmark.dto.ActionPlanResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.ActionPlan;
import com.iabenchmark.model.ActionPlanStatus;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.repository.ActionPlanRepository;
import com.iabenchmark.repository.EvaluationRepository;
import jakarta.persistence.EntityNotFoundException;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Service
public class ActionPlanService {

    private final ActionPlanRepository actionPlanRepository;
    private final EvaluationRepository evaluationRepository;

    public ActionPlanService(ActionPlanRepository actionPlanRepository,
                             EvaluationRepository evaluationRepository) {
        this.actionPlanRepository = actionPlanRepository;
        this.evaluationRepository = evaluationRepository;
    }

    public List<ActionPlanResponse> generateFromRecommendations(Long evaluationId,
                                                                 List<RecommendationResponse> recommendations) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(evaluationId))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        actionPlanRepository.deleteByEvaluationId(evaluationId);

        String consultantName = "Consultant";
        if (evaluation.getCompany().getConsultant() != null) {
            var c = evaluation.getCompany().getConsultant();
            consultantName = c.getFirstName() + " " + c.getLastName();
        }

        List<ActionPlan> plans = new ArrayList<>();
        for (RecommendationResponse rec : recommendations) {
            ActionPlan plan = new ActionPlan();
            plan.setEvaluation(evaluation);
            plan.setTitle(rec.getTitle());
            plan.setDescription(rec.getDescription());
            plan.setAxe(rec.getAxis());
            plan.setPriority(rec.getPriority());
            plan.setStatus(ActionPlanStatus.TODO);
            plan.setResponsible(consultantName);

            switch (rec.getPriority() == null ? "" : rec.getPriority()) {
                case "HAUTE" -> {
                    plan.setPhase("Phase 1 - Court terme");
                    plan.setDeadline(LocalDate.now().plusDays(30));
                }
                case "BASSE" -> {
                    plan.setPhase("Phase 3 - Long terme");
                    plan.setDeadline(LocalDate.now().plusDays(90));
                }
                default -> {
                    plan.setPhase("Phase 2 - Moyen terme");
                    plan.setDeadline(LocalDate.now().plusDays(60));
                }
            }
            plans.add(plan);
        }

        return actionPlanRepository.saveAll(plans).stream().map(this::toResponse).toList();
    }

    public List<ActionPlanResponse> getByEvaluation(Long evaluationId) {
        return actionPlanRepository.findByEvaluationIdOrderByPriorityAscCreatedAtAsc(evaluationId)
                .stream().map(this::toResponse).toList();
    }

    public boolean hasActionPlan(Long evaluationId) {
        return actionPlanRepository.existsByEvaluationId(evaluationId);
    }

    public ActionPlanResponse update(Long id, ActionPlanRequest request) {
        ActionPlan plan = actionPlanRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("ActionPlan not found: " + id));
        if (request.getTitle()       != null) plan.setTitle(request.getTitle());
        if (request.getDescription() != null) plan.setDescription(request.getDescription());
        if (request.getAxe()         != null) plan.setAxe(request.getAxe());
        if (request.getPriority()    != null) plan.setPriority(request.getPriority());
        if (request.getPhase()       != null) plan.setPhase(request.getPhase());
        if (request.getResponsible() != null) plan.setResponsible(request.getResponsible());
        if (request.getDeadline()    != null) plan.setDeadline(request.getDeadline());
        if (request.getStatus()      != null) plan.setStatus(request.getStatus());
        return toResponse(actionPlanRepository.save(Objects.requireNonNull(plan)));
    }

    public void delete(Long id) {
        actionPlanRepository.deleteById(Objects.requireNonNull(id));
    }

    public byte[] exportToExcel(Long evaluationId) {
        List<ActionPlan> plans = actionPlanRepository
                .findByEvaluationIdOrderByPriorityAscCreatedAtAsc(evaluationId);

        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Plan d'action");

            CellStyle headerStyle = workbook.createCellStyle();
            headerStyle.setFillForegroundColor(IndexedColors.DARK_BLUE.getIndex());
            headerStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);
            Font headerFont = workbook.createFont();
            headerFont.setColor(IndexedColors.WHITE.getIndex());
            headerFont.setBold(true);
            headerStyle.setFont(headerFont);

            String[] headers = {"#", "Phase", "Axe", "Priorité", "Titre", "Description",
                                 "Responsable", "Deadline", "Statut"};
            org.apache.poi.ss.usermodel.Row headerRow = sheet.createRow(0);
            for (int i = 0; i < headers.length; i++) {
                Cell cell = headerRow.createCell(i);
                cell.setCellValue(headers[i]);
                cell.setCellStyle(headerStyle);
            }

            int rowNum = 1;
            for (ActionPlan plan : plans) {
                org.apache.poi.ss.usermodel.Row row = sheet.createRow(rowNum);
                row.createCell(0).setCellValue(rowNum);
                row.createCell(1).setCellValue(nullSafe(plan.getPhase()));
                row.createCell(2).setCellValue(nullSafe(plan.getAxe()));
                row.createCell(3).setCellValue(nullSafe(plan.getPriority()));
                row.createCell(4).setCellValue(nullSafe(plan.getTitle()));
                row.createCell(5).setCellValue(nullSafe(plan.getDescription()));
                row.createCell(6).setCellValue(nullSafe(plan.getResponsible()));
                row.createCell(7).setCellValue(plan.getDeadline() != null ? plan.getDeadline().toString() : "");
                row.createCell(8).setCellValue(plan.getStatus() != null ? statusLabel(plan.getStatus()) : "");
                rowNum++;
            }

            for (int i = 0; i < headers.length; i++) {
                sheet.autoSizeColumn(i);
            }

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            workbook.write(baos);
            return baos.toByteArray();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la génération Excel", e);
        }
    }

    private String nullSafe(String value) {
        return value != null ? value : "";
    }

    private String statusLabel(ActionPlanStatus status) {
        return switch (status) {
            case TODO        -> "À faire";
            case IN_PROGRESS -> "En cours";
            case DONE        -> "Terminé";
        };
    }

    private ActionPlanResponse toResponse(@org.springframework.lang.NonNull ActionPlan plan) {
        return new ActionPlanResponse(
                plan.getId(),
                plan.getEvaluation().getId(),
                plan.getEvaluation().getCompany().getName(),
                plan.getTitle(),
                plan.getDescription(),
                plan.getAxe(),
                plan.getPriority(),
                plan.getPhase(),
                plan.getResponsible(),
                plan.getDeadline(),
                plan.getStatus(),
                plan.getCreatedAt(),
                plan.getUpdatedAt()
        );
    }
}
