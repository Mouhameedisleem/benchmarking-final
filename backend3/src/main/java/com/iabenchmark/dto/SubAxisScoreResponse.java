package com.iabenchmark.dto;

public class SubAxisScoreResponse {
    private String axis;
    private String subAxis;
    private Double score;
    private Integer questionCount;

    public SubAxisScoreResponse(String axis, String subAxis, Double score, Integer questionCount) {
        this.axis = axis;
        this.subAxis = subAxis;
        this.score = score;
        this.questionCount = questionCount;
    }

    public String getAxis() { return axis; }
    public String getSubAxis() { return subAxis; }
    public Double getScore() { return score; }
    public Integer getQuestionCount() { return questionCount; }
}
