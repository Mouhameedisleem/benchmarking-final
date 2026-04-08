package com.iabenchmark.dto;

import com.iabenchmark.model.EvaluationStatus;
import com.iabenchmark.model.MaturityLevel;

import java.time.LocalDateTime;
import java.util.List;

public class EvaluationResponse {
    private Long evaluationId;
    private Long companyId;
    private String companyName;
    private Long questionnaireId;
    private EvaluationStatus status;
    private Double globalScore;
    private MaturityLevel maturityLevel;
    private List<AxisScoreResponse> scoresByAxis;
    private List<SubAxisScoreResponse> scoresBySubAxis;
    private List<AxisSynthesisResponse> synthesesByAxis;
    private List<AnswerSummaryResponse> answerSummaries;
    private List<String> criticalGaps;
    private String maturityExplanation;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public EvaluationResponse(Long evaluationId, Long companyId, String companyName, Long questionnaireId,
                              EvaluationStatus status, Double globalScore, MaturityLevel maturityLevel,
                              List<AxisScoreResponse> scoresByAxis, List<SubAxisScoreResponse> scoresBySubAxis,
                              List<AxisSynthesisResponse> synthesesByAxis, List<AnswerSummaryResponse> answerSummaries,
                              LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.evaluationId = evaluationId;
        this.companyId = companyId;
        this.companyName = companyName;
        this.questionnaireId = questionnaireId;
        this.status = status;
        this.globalScore = globalScore;
        this.maturityLevel = maturityLevel;
        this.scoresByAxis = scoresByAxis;
        this.scoresBySubAxis = scoresBySubAxis;
        this.synthesesByAxis = synthesesByAxis;
        this.answerSummaries = answerSummaries;
        this.criticalGaps = List.of();
        this.maturityExplanation = "";
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public Long getEvaluationId() { return evaluationId; }
    public Long getCompanyId() { return companyId; }
    public String getCompanyName() { return companyName; }
    public Long getQuestionnaireId() { return questionnaireId; }
    public EvaluationStatus getStatus() { return status; }
    public Double getGlobalScore() { return globalScore; }
    public MaturityLevel getMaturityLevel() { return maturityLevel; }
    public List<AxisScoreResponse> getScoresByAxis() { return scoresByAxis; }
    public List<SubAxisScoreResponse> getScoresBySubAxis() { return scoresBySubAxis; }
    public List<AxisSynthesisResponse> getSynthesesByAxis() { return synthesesByAxis; }
    public List<AnswerSummaryResponse> getAnswerSummaries() { return answerSummaries; }
    public List<String> getCriticalGaps() { return criticalGaps; }
    public String getMaturityExplanation() { return maturityExplanation; }
    public void setCriticalGaps(List<String> criticalGaps) { this.criticalGaps = criticalGaps; }
    public void setMaturityExplanation(String maturityExplanation) { this.maturityExplanation = maturityExplanation; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
