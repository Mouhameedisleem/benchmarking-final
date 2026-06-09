package com.iabenchmark.model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "evaluations")
public class Evaluation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "company_id", nullable = false)
    private Company company;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User submittedBy;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "questionnaire_id", nullable = false)
    private Questionnaire questionnaire;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private EvaluationStatus status = EvaluationStatus.IN_PROGRESS;

    @Column(nullable = false)
    private Double globalScore = 0.0;

    @Column(nullable = false)
    private Double businessScore = 0.0;

    @Column(nullable = false)
    private Double processScore = 0.0;

    @Column(nullable = false)
    private Double informationSystemScore = 0.0;

    @Column(nullable = false)
    private Double canauxDistributionScore = 0.0;

    @Column(nullable = false)
    private Double marketingCommunicationScore = 0.0;

    @Column(nullable = false)
    private Double rhCultureDigitaleScore = 0.0;

    @Column(nullable = false)
    private Double offresDigitalesScore = 0.0;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private MaturityLevel maturityLevel = MaturityLevel.INITIAL;

    @Enumerated(EnumType.STRING)
    private MaturityLevel targetMaturityLevel;

    @OneToMany(mappedBy = "evaluation", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<EvaluationAnswer> responses = new ArrayList<>();

    @Column(nullable = false)
    private Double modeleOperationnelScore = 0.0;

    @Column(nullable = false)
    private Double itDataScore = 0.0;

    @Column(nullable = false)
    private boolean pendingReview = true;

    @Column(nullable = false)
    private boolean validated = false;

    @Column(columnDefinition = "LONGTEXT")
    private String recommendationsJson;

    @Column(columnDefinition = "LONGTEXT")
    private String benchmarkJson;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    public boolean isPendingReview() { return pendingReview; }
    public void setPendingReview(boolean pendingReview) { this.pendingReview = pendingReview; }
    public boolean isValidated() { return validated; }
    public void setValidated(boolean validated) { this.validated = validated; }
    public String getRecommendationsJson() { return recommendationsJson; }
    public void setRecommendationsJson(String recommendationsJson) { this.recommendationsJson = recommendationsJson; }
    public String getBenchmarkJson() { return benchmarkJson; }
    public void setBenchmarkJson(String benchmarkJson) { this.benchmarkJson = benchmarkJson; }

    public void addResponse(EvaluationAnswer response) {
        responses.add(response);
        response.setEvaluation(this);
    }

    public void clearResponses() {
        for (EvaluationAnswer response : responses) {
            response.setEvaluation(null);
        }
        responses.clear();
    }

    public Long getId() { return id; }
    public Company getCompany() { return company; }
    public void setCompany(Company company) { this.company = company; }
    public User getSubmittedBy() { return submittedBy; }
    public void setSubmittedBy(User submittedBy) { this.submittedBy = submittedBy; }
    public Questionnaire getQuestionnaire() { return questionnaire; }
    public void setQuestionnaire(Questionnaire questionnaire) { this.questionnaire = questionnaire; }
    public EvaluationStatus getStatus() { return status; }
    public void setStatus(EvaluationStatus status) { this.status = status; }
    public Double getGlobalScore() { return globalScore; }
    public void setGlobalScore(Double globalScore) { this.globalScore = globalScore; }
    public Double getBusinessScore() { return businessScore; }
    public void setBusinessScore(Double businessScore) { this.businessScore = businessScore; }
    public Double getProcessScore() { return processScore; }
    public void setProcessScore(Double processScore) { this.processScore = processScore; }
    public Double getInformationSystemScore() { return informationSystemScore; }
    public void setInformationSystemScore(Double informationSystemScore) { this.informationSystemScore = informationSystemScore; }
    public Double getCanauxDistributionScore() { return canauxDistributionScore != null ? canauxDistributionScore : 0.0; }
    public void setCanauxDistributionScore(Double s) { this.canauxDistributionScore = s; }
    public Double getMarketingCommunicationScore() { return marketingCommunicationScore != null ? marketingCommunicationScore : 0.0; }
    public void setMarketingCommunicationScore(Double s) { this.marketingCommunicationScore = s; }
    public Double getRhCultureDigitaleScore() { return rhCultureDigitaleScore != null ? rhCultureDigitaleScore : 0.0; }
    public void setRhCultureDigitaleScore(Double s) { this.rhCultureDigitaleScore = s; }
    public Double getOffresDigitalesScore() { return offresDigitalesScore != null ? offresDigitalesScore : 0.0; }
    public void setOffresDigitalesScore(Double s) { this.offresDigitalesScore = s; }
    public Double getModeleOperationnelScore() { return modeleOperationnelScore != null ? modeleOperationnelScore : 0.0; }
    public void setModeleOperationnelScore(Double s) { this.modeleOperationnelScore = s; }
    public Double getItDataScore() { return itDataScore != null ? itDataScore : 0.0; }
    public void setItDataScore(Double s) { this.itDataScore = s; }
    public MaturityLevel getMaturityLevel() { return maturityLevel; }
    public void setMaturityLevel(MaturityLevel maturityLevel) { this.maturityLevel = maturityLevel; }
    public MaturityLevel getTargetMaturityLevel() { return targetMaturityLevel; }
    public void setTargetMaturityLevel(MaturityLevel targetMaturityLevel) { this.targetMaturityLevel = targetMaturityLevel; }
    public List<EvaluationAnswer> getResponses() { return responses; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
