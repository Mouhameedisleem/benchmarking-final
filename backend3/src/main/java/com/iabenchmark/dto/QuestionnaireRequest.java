package com.iabenchmark.dto;

import com.iabenchmark.model.QuestionnaireMode;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import java.util.List;

public class QuestionnaireRequest {
    @NotBlank(message = "Questionnaire title is required")
    private String title;

    private String description;

    @NotBlank(message = "Sector is required")
    private String sector;

    @NotBlank(message = "Country is required")
    private String country;

    @NotNull(message = "Questionnaire mode is required")
    private QuestionnaireMode mode;

    private boolean active = true;

    @Valid
    @NotEmpty(message = "At least one question is required")
    private List<QuestionRequest> questions;

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public QuestionnaireMode getMode() { return mode; }
    public void setMode(QuestionnaireMode mode) { this.mode = mode; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
    public List<QuestionRequest> getQuestions() { return questions; }
    public void setQuestions(List<QuestionRequest> questions) { this.questions = questions; }
}
