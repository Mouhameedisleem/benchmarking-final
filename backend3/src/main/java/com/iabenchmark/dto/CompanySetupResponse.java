package com.iabenchmark.dto;

public class CompanySetupResponse {
    private Long questionnaireId;
    private String message;

    public CompanySetupResponse(Long questionnaireId, String message) {
        this.questionnaireId = questionnaireId;
        this.message = message;
    }

    public Long getQuestionnaireId() { return questionnaireId; }
    public String getMessage() { return message; }
}
