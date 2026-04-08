package com.iabenchmark.dto;

import java.util.List;

public class AxisSynthesisResponse {
    private String axis;
    private Double score;
    private String summary;
    private List<String> strengths;
    private List<String> gaps;

    public AxisSynthesisResponse(String axis, Double score, String summary) {
        this.axis = axis;
        this.score = score;
        this.summary = summary;
        this.strengths = List.of();
        this.gaps = List.of();
    }

    public String getAxis() { return axis; }
    public Double getScore() { return score; }
    public String getSummary() { return summary; }
    public List<String> getStrengths() { return strengths; }
    public List<String> getGaps() { return gaps; }
    public void setStrengths(List<String> strengths) { this.strengths = strengths; }
    public void setGaps(List<String> gaps) { this.gaps = gaps; }
}
