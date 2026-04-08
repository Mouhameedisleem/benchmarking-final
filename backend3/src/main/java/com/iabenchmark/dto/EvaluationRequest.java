package com.iabenchmark.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.util.List;

public class EvaluationRequest {
    @NotNull(message = "Company id is required")
    private Long companyId;

    @NotNull(message = "Questionnaire id is required")
    private Long questionnaireId;

    @Valid
    @NotEmpty(message = "At least one answer is required")
    private List<EvaluationAnswerRequest> answers;

    public Long getCompanyId() { return companyId; }
    public void setCompanyId(Long companyId) { this.companyId = companyId; }
    public Long getQuestionnaireId() { return questionnaireId; }
    public void setQuestionnaireId(Long questionnaireId) { this.questionnaireId = questionnaireId; }
    public List<EvaluationAnswerRequest> getAnswers() { return answers; }
    public void setAnswers(List<EvaluationAnswerRequest> answers) { this.answers = answers; }
}
