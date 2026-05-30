package com.iabenchmark.dto;

public class RecommendationResponse {
    private String axis;       // METIER, PROCESSUS, SI
    private String priority;   // HAUTE, MOYENNE, BASSE
    private String title;
    private String description;
    private String bestPractice;
    private String source;
    private String sourceUrl;

    public RecommendationResponse() {}

    public RecommendationResponse(String axis, String priority, String title,
                                  String description, String bestPractice) {
        this.axis = axis;
        this.priority = priority;
        this.title = title;
        this.description = description;
        this.bestPractice = bestPractice;
    }

    public String getAxis() { return axis; }
    public void setAxis(String axis) { this.axis = axis; }
    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getBestPractice() { return bestPractice; }
    public void setBestPractice(String bestPractice) { this.bestPractice = bestPractice; }
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    public String getSourceUrl() { return sourceUrl; }
    public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }
}
