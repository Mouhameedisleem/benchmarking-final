package com.iabenchmark.dto;

import java.util.List;

public class BenchmarkResponse {

    private String companyName;
    private String sector;
    private String country;
    private Double globalScore;
    private String maturityLevel;
    private String executiveSummary;
    private SectorBenchmark sectorBenchmark;
    private List<AxisBenchmark> axisBenchmarks;
    private List<BenchmarkTrend> trends;
    private List<SectorLeader> sectorLeaders;
    private List<RoadmapPhase> improvementRoadmap;
    private List<String> keyInsights;

    // ── Nested classes ─────────────────────────────────────────────────────────

    public static class SectorBenchmark {
        private Double nationalAverage;
        private Double internationalAverage;
        private Double topQuartileScore;
        private Integer companyPercentile;
        private String positioningLabel;
        private String source;

        public Double getNationalAverage() { return nationalAverage; }
        public void setNationalAverage(Double v) { this.nationalAverage = v; }
        public Double getInternationalAverage() { return internationalAverage; }
        public void setInternationalAverage(Double v) { this.internationalAverage = v; }
        public Double getTopQuartileScore() { return topQuartileScore; }
        public void setTopQuartileScore(Double v) { this.topQuartileScore = v; }
        public Integer getCompanyPercentile() { return companyPercentile; }
        public void setCompanyPercentile(Integer v) { this.companyPercentile = v; }
        public String getPositioningLabel() { return positioningLabel; }
        public void setPositioningLabel(String v) { this.positioningLabel = v; }
        public String getSource() { return source; }
        public void setSource(String v) { this.source = v; }
    }

    public static class AxisBenchmark {
        private String axis;
        private String axisLabel;
        private Double companyScore;
        private Double sectorAverage;
        private Double topQuartile;
        private Double gapToAverage;
        private Double gapToTop;

        public String getAxis() { return axis; }
        public void setAxis(String v) { this.axis = v; }
        public String getAxisLabel() { return axisLabel; }
        public void setAxisLabel(String v) { this.axisLabel = v; }
        public Double getCompanyScore() { return companyScore; }
        public void setCompanyScore(Double v) { this.companyScore = v; }
        public Double getSectorAverage() { return sectorAverage; }
        public void setSectorAverage(Double v) { this.sectorAverage = v; }
        public Double getTopQuartile() { return topQuartile; }
        public void setTopQuartile(Double v) { this.topQuartile = v; }
        public Double getGapToAverage() { return gapToAverage; }
        public void setGapToAverage(Double v) { this.gapToAverage = v; }
        public Double getGapToTop() { return gapToTop; }
        public void setGapToTop(Double v) { this.gapToTop = v; }
    }

    public static class BenchmarkTrend {
        private String title;
        private String description;
        private String impactLevel;
        private String horizon;
        private String adoptionRate;
        private String source;

        public String getTitle() { return title; }
        public void setTitle(String v) { this.title = v; }
        public String getDescription() { return description; }
        public void setDescription(String v) { this.description = v; }
        public String getImpactLevel() { return impactLevel; }
        public void setImpactLevel(String v) { this.impactLevel = v; }
        public String getHorizon() { return horizon; }
        public void setHorizon(String v) { this.horizon = v; }
        public String getAdoptionRate() { return adoptionRate; }
        public void setAdoptionRate(String v) { this.adoptionRate = v; }
        public String getSource() { return source; }
        public void setSource(String v) { this.source = v; }
    }

    public static class SectorLeader {
        private String company;
        private String country;
        private Integer estimatedScore;
        private String keyPractice;
        private String differentiator;
        private String source;

        public String getCompany() { return company; }
        public void setCompany(String v) { this.company = v; }
        public String getCountry() { return country; }
        public void setCountry(String v) { this.country = v; }
        public Integer getEstimatedScore() { return estimatedScore; }
        public void setEstimatedScore(Integer v) { this.estimatedScore = v; }
        public String getKeyPractice() { return keyPractice; }
        public void setKeyPractice(String v) { this.keyPractice = v; }
        public String getDifferentiator() { return differentiator; }
        public void setDifferentiator(String v) { this.differentiator = v; }
        public String getSource() { return source; }
        public void setSource(String v) { this.source = v; }
    }

    public static class RoadmapPhase {
        private String phase;
        private String objective;
        private List<String> actions;
        private String expectedScoreGain;
        private String targetLevel;
        private String investmentLevel;

        public String getPhase() { return phase; }
        public void setPhase(String v) { this.phase = v; }
        public String getObjective() { return objective; }
        public void setObjective(String v) { this.objective = v; }
        public List<String> getActions() { return actions; }
        public void setActions(List<String> v) { this.actions = v; }
        public String getExpectedScoreGain() { return expectedScoreGain; }
        public void setExpectedScoreGain(String v) { this.expectedScoreGain = v; }
        public String getTargetLevel() { return targetLevel; }
        public void setTargetLevel(String v) { this.targetLevel = v; }
        public String getInvestmentLevel() { return investmentLevel; }
        public void setInvestmentLevel(String v) { this.investmentLevel = v; }
    }

    // ── Root getters/setters ───────────────────────────────────────────────────

    public String getCompanyName() { return companyName; }
    public void setCompanyName(String v) { this.companyName = v; }
    public String getSector() { return sector; }
    public void setSector(String v) { this.sector = v; }
    public String getCountry() { return country; }
    public void setCountry(String v) { this.country = v; }
    public Double getGlobalScore() { return globalScore; }
    public void setGlobalScore(Double v) { this.globalScore = v; }
    public String getMaturityLevel() { return maturityLevel; }
    public void setMaturityLevel(String v) { this.maturityLevel = v; }
    public String getExecutiveSummary() { return executiveSummary; }
    public void setExecutiveSummary(String v) { this.executiveSummary = v; }
    public SectorBenchmark getSectorBenchmark() { return sectorBenchmark; }
    public void setSectorBenchmark(SectorBenchmark v) { this.sectorBenchmark = v; }
    public List<AxisBenchmark> getAxisBenchmarks() { return axisBenchmarks; }
    public void setAxisBenchmarks(List<AxisBenchmark> v) { this.axisBenchmarks = v; }
    public List<BenchmarkTrend> getTrends() { return trends; }
    public void setTrends(List<BenchmarkTrend> v) { this.trends = v; }
    public List<SectorLeader> getSectorLeaders() { return sectorLeaders; }
    public void setSectorLeaders(List<SectorLeader> v) { this.sectorLeaders = v; }
    public List<RoadmapPhase> getImprovementRoadmap() { return improvementRoadmap; }
    public void setImprovementRoadmap(List<RoadmapPhase> v) { this.improvementRoadmap = v; }
    public List<String> getKeyInsights() { return keyInsights; }
    public void setKeyInsights(List<String> v) { this.keyInsights = v; }
}
