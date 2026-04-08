package com.iabenchmark.dto;

public class RecommendationResponse {
    private String axis;       // METIER, PROCESSUS, SI
    private String priority;   // HAUTE, MOYENNE, BASSE
    private String title;
    private String description;
    private String bestPractice;

    public RecommendationResponse(String axis, String priority, String title,
                                  String description, String bestPractice) {
        this.axis = axis;
        this.priority = priority;
        this.title = title;
        this.description = description;
        this.bestPractice = bestPractice;
    }

    public String getAxis() { return axis; }
    public String getPriority() { return priority; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getBestPractice() { return bestPractice; }
}
