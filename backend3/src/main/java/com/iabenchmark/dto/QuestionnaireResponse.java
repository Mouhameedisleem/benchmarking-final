package com.iabenchmark.dto;

import com.iabenchmark.model.QuestionnaireMode;
import java.time.LocalDateTime;
import java.util.List;

public class QuestionnaireResponse {
    private Long id;
    private String title;
    private String description;
    private String sector;
    private String country;
    private QuestionnaireMode mode;
    private boolean active;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private List<QuestionResponse> questions;

    public QuestionnaireResponse(Long id, String title, String description, String sector, String country,
                                 QuestionnaireMode mode, boolean active, LocalDateTime createdAt,
                                 LocalDateTime updatedAt, List<QuestionResponse> questions) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.sector = sector;
        this.country = country;
        this.mode = mode;
        this.active = active;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.questions = questions;
    }

    public Long getId() { return id; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getSector() { return sector; }
    public String getCountry() { return country; }
    public QuestionnaireMode getMode() { return mode; }
    public boolean isActive() { return active; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public List<QuestionResponse> getQuestions() { return questions; }
}
