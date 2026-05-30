package com.iabenchmark.dto;

import com.iabenchmark.model.ActionPlanStatus;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter @Setter @AllArgsConstructor
public class ActionPlanResponse {
    private Long id;
    private Long evaluationId;
    private String companyName;
    private String title;
    private String description;
    private String axe;
    private String priority;
    private String phase;
    private String responsible;
    private LocalDate deadline;
    private ActionPlanStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
