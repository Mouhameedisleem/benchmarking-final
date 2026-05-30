package com.iabenchmark.dto;

import com.iabenchmark.model.ActionPlanStatus;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter @Setter
public class ActionPlanRequest {
    private String title;
    private String description;
    private String axe;
    private String priority;
    private String phase;
    private String responsible;
    private LocalDate deadline;
    private ActionPlanStatus status;
}
