package com.iabenchmark.dto;

import java.util.List;

public class ValidateRequest {
    private List<RecommendationResponse> recommendations;
    private String pptBase64;

    public List<RecommendationResponse> getRecommendations() { return recommendations; }
    public void setRecommendations(List<RecommendationResponse> recommendations) { this.recommendations = recommendations; }
    public String getPptBase64() { return pptBase64; }
    public void setPptBase64(String pptBase64) { this.pptBase64 = pptBase64; }
}
