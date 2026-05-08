package com.iabenchmark.dto;

import java.util.List;

public class CompanySetupRequest {
    private List<QuestionRequest> questions;

    public List<QuestionRequest> getQuestions() { return questions; }
    public void setQuestions(List<QuestionRequest> questions) { this.questions = questions; }
}
