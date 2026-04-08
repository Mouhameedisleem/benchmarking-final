package com.iabenchmark.dto;

public class AxisScoreResponse {
    private String axis;
    private Double score;

    public AxisScoreResponse(String axis, Double score) {
        this.axis = axis;
        this.score = score;
    }

    public String getAxis() { return axis; }
    public Double getScore() { return score; }
}
