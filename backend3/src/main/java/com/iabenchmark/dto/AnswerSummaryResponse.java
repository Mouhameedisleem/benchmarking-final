package com.iabenchmark.dto;

public class AnswerSummaryResponse {
    private Long questionId;
    private String questionText;
    private String axis;
    private String subAxis;
    private Double answerValue;
    private Double normalizedScore;
    private Integer weight;
    private String comment;

    public AnswerSummaryResponse(Long questionId, String questionText, String axis, String subAxis,
                                 Double answerValue, Double normalizedScore, Integer weight, String comment) {
        this.questionId = questionId;
        this.questionText = questionText;
        this.axis = axis;
        this.subAxis = subAxis;
        this.answerValue = answerValue;
        this.normalizedScore = normalizedScore;
        this.weight = weight;
        this.comment = comment;
    }

    public Long getQuestionId() { return questionId; }
    public String getQuestionText() { return questionText; }
    public String getAxis() { return axis; }
    public String getSubAxis() { return subAxis; }
    public Double getAnswerValue() { return answerValue; }
    public Double getNormalizedScore() { return normalizedScore; }
    public Integer getWeight() { return weight; }
    public String getComment() { return comment; }
}
