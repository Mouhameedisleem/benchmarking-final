package com.iabenchmark.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class EvaluationAnswerRequest {
    @NotNull(message = "Question id is required")
    private Long questionId;

    @NotNull(message = "Answer value is required")
    @Min(value = 0, message = "Answer value must be at least 0")
    @Max(value = 5, message = "Answer value must not exceed 5")
    private Double value;

    private String comment;

    public Long getQuestionId() { return questionId; }
    public void setQuestionId(Long questionId) { this.questionId = questionId; }
    public Double getValue() { return value; }
    public void setValue(Double value) { this.value = value; }
    public String getComment() { return comment; }
    public void setComment(String comment) { this.comment = comment; }
}
