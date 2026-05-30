package com.iabenchmark.service;

import com.iabenchmark.dto.AnswerSummaryResponse;
import com.iabenchmark.dto.AxisScoreResponse;
import com.iabenchmark.dto.AxisSynthesisResponse;
import com.iabenchmark.dto.EvaluationAnswerRequest;
import com.iabenchmark.dto.EvaluationRequest;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.SubAxisScoreResponse;
import com.iabenchmark.model.Company;
import com.iabenchmark.model.EvaluationAnswer;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.EvaluationStatus;
import com.iabenchmark.model.MaturityLevel;
import com.iabenchmark.model.Question;
import com.iabenchmark.model.QuestionAxis;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.CompanyRepository;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.QuestionnaireRepository;
import com.iabenchmark.repository.UserRepository;
import com.iabenchmark.security.UserDetailsImpl;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.EnumMap;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class EvaluationService {
    private final EvaluationRepository evaluationRepository;
    private final CompanyRepository companyRepository;
    private final QuestionnaireRepository questionnaireRepository;
    private final UserRepository userRepository;
    private final AiService aiService;

    public EvaluationService(EvaluationRepository evaluationRepository,
                             CompanyRepository companyRepository,
                             QuestionnaireRepository questionnaireRepository,
                             UserRepository userRepository,
                             AiService aiService) {
        this.evaluationRepository = evaluationRepository;
        this.companyRepository = companyRepository;
        this.questionnaireRepository = questionnaireRepository;
        this.userRepository = userRepository;
        this.aiService = aiService;
    }

    public EvaluationResponse submitEvaluation(EvaluationRequest request) {
        Company company = companyRepository.findById(Objects.requireNonNull(request.getCompanyId()))
                .orElseThrow(() -> new EntityNotFoundException("Company not found with id: " + request.getCompanyId()));
        Questionnaire questionnaire = questionnaireRepository.findById(Objects.requireNonNull(request.getQuestionnaireId()))
                .orElseThrow(() -> new EntityNotFoundException("Questionnaire not found with id: " + request.getQuestionnaireId()));
        User submittedBy = getCurrentUser();

        Map<Long, Question> questionsById = questionnaire.getQuestions().stream()
                .collect(Collectors.toMap(Question::getId, Function.identity()));

        Evaluation evaluation = new Evaluation();
        evaluation.setCompany(company);
        evaluation.setSubmittedBy(submittedBy);
        evaluation.setQuestionnaire(questionnaire);
        evaluation.setStatus(EvaluationStatus.COMPLETED);
        evaluation.setPendingReview(true);

        Map<QuestionAxis, Double> weightedScores = new EnumMap<>(QuestionAxis.class);
        Map<QuestionAxis, Integer> totalWeights = new EnumMap<>(QuestionAxis.class);
        Map<String, Double> weightedScoresBySubAxis = new LinkedHashMap<>();
        Map<String, Integer> totalWeightsBySubAxis = new LinkedHashMap<>();

        for (EvaluationAnswerRequest answer : request.getAnswers()) {
            Question question = questionsById.get(answer.getQuestionId());
            if (question == null) {
                throw new RuntimeException("Question does not belong to questionnaire: " + answer.getQuestionId());
            }

            double normalizedScore = normalize(answer.getValue());
            EvaluationAnswer response = new EvaluationAnswer();
            response.setQuestion(question);
            response.setScoreValue(answer.getValue());
            response.setComment(answer.getComment());
            evaluation.addResponse(response);

            weightedScores.merge(question.getAxis(), normalizedScore * question.getWeight(), (a, b) -> a + b);
            totalWeights.merge(question.getAxis(), question.getWeight(), (a, b) -> a + b);
            String subAxisKey = buildSubAxisKey(question.getAxis(), question.getSubAxis());
            weightedScoresBySubAxis.merge(subAxisKey, normalizedScore * question.getWeight(), (a, b) -> a + b);
            totalWeightsBySubAxis.merge(subAxisKey, question.getWeight(), (a, b) -> a + b);
        }

        double businessScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.BUSINESS);
        double processScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.PROCESS);
        double informationSystemScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.INFORMATION_SYSTEM);
        double canauxScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.CANAUX_DISTRIBUTION);
        double marketingScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.MARKETING_COMMUNICATION);
        double rhScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.RH_CULTURE_DIGITALE);
        double offresScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.OFFRES_DIGITALES);
        double modeleOperationnelScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.MODELE_OPERATIONNEL_INNOVATION);
        double itDataScore = computeAxisScore(weightedScores, totalWeights, QuestionAxis.IT_DATA);
        double globalScore = computeGlobalScore(weightedScores, totalWeights);

        evaluation.setBusinessScore(businessScore);
        evaluation.setProcessScore(processScore);
        evaluation.setInformationSystemScore(informationSystemScore);
        evaluation.setCanauxDistributionScore(canauxScore);
        evaluation.setMarketingCommunicationScore(marketingScore);
        evaluation.setRhCultureDigitaleScore(rhScore);
        evaluation.setOffresDigitalesScore(offresScore);
        evaluation.setModeleOperationnelScore(modeleOperationnelScore);
        evaluation.setItDataScore(itDataScore);
        evaluation.setGlobalScore(globalScore);
        MaturityLevel maturityLevel = determineMaturityLevel(globalScore);
        evaluation.setMaturityLevel(maturityLevel);
        evaluation.setTargetMaturityLevel(suggestTargetMaturity(maturityLevel));

        Evaluation saved = evaluationRepository.save(evaluation);
        EvaluationResponse response = toResponse(saved);

        // Fast AI enrichment (scoring synthesis) — kept synchronous, completes quickly
        if (aiService.isAiServiceAvailable()) {
            aiService.enrichWithAiScoring(response, saved);
            // Heavy AI generation (recommendations + benchmark) runs in background
            // so the HTTP response is returned immediately to the client
            final Evaluation savedForAsync = saved;
            Thread aiThread = new Thread(() -> {
                try { aiService.generateAndStoreAiData(savedForAsync); } catch (Exception ignored) {}
            });
            aiThread.setDaemon(true);
            aiThread.start();
        }

        return response;
    }

    public EvaluationResponse getEvaluation(Long id) {
        return toResponse(findEvaluation(id));
    }

    public void setTargetMaturity(Long id, MaturityLevel target) {
        Evaluation evaluation = findEvaluation(id);
        evaluation.setTargetMaturityLevel(target);
        evaluationRepository.save(evaluation);
    }

    public List<EvaluationResponse> getCompanyEvaluations(Long companyId) {
        return evaluationRepository.findByCompanyId(companyId).stream()
                .map(this::toResponse)
                .toList();
    }

    public EvaluationResponse getLatestCompanyEvaluation(Long companyId) {
        Evaluation evaluation = evaluationRepository.findFirstByCompanyIdOrderByCreatedAtDesc(companyId);
        if (evaluation == null) {
            return null;
        }
        return toResponse(evaluation);
    }

    private Evaluation findEvaluation(Long id) {
        return evaluationRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found with id: " + id));
    }

    private User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof UserDetailsImpl userDetails)) {
            throw new RuntimeException("Unauthorized");
        }

        return userRepository.findByEmail(userDetails.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }

    private double normalize(Double value) {
        return round((value / 5.0) * 100.0);
    }

    private double computeAxisScore(Map<QuestionAxis, Double> weightedScores,
                                    Map<QuestionAxis, Integer> totalWeights,
                                    QuestionAxis axis) {
        double score = weightedScores.getOrDefault(axis, 0.0);
        int totalWeight = totalWeights.getOrDefault(axis, 0);
        if (totalWeight == 0) {
            return 0.0;
        }
        return round(score / totalWeight);
    }

    private double computeGlobalScore(Map<QuestionAxis, Double> weightedScores, Map<QuestionAxis, Integer> totalWeights) {
        double weightedTotal = weightedScores.values().stream().mapToDouble(Double::doubleValue).sum();
        int totalWeight = totalWeights.values().stream().mapToInt(Integer::intValue).sum();
        if (totalWeight == 0) {
            return 0.0;
        }
        return round(weightedTotal / totalWeight);
    }

    private MaturityLevel determineMaturityLevel(double score) {
        if (score < 20) return MaturityLevel.INITIAL;
        if (score < 40) return MaturityLevel.BASIQUE;
        if (score < 60) return MaturityLevel.INTERMEDIAIRE;
        if (score < 80) return MaturityLevel.AVANCE;
        return MaturityLevel.OPTIMISE;
    }

    private double round(double value) {
        return Math.round(value * 100.0) / 100.0;
    }

    private MaturityLevel suggestTargetMaturity(MaturityLevel current) {
        return switch (current) {
            case INITIAL       -> MaturityLevel.INTERMEDIAIRE;
            case BASIQUE       -> MaturityLevel.INTERMEDIAIRE;
            case INTERMEDIAIRE -> MaturityLevel.AVANCE;
            case AVANCE        -> MaturityLevel.OPTIMISE;
            case OPTIMISE      -> MaturityLevel.OPTIMISE;
        };
    }

    private String buildSubAxisKey(QuestionAxis axis, String subAxis) {
        return axis.name() + "::" + (subAxis == null ? "" : subAxis.trim());
    }

    private String mapAxisLabel(QuestionAxis axis) {
        return switch (axis) {
            case BUSINESS -> "METIER";
            case PROCESS -> "PROCESSUS";
            case INFORMATION_SYSTEM -> "SI";
            case CANAUX_DISTRIBUTION -> "CANAUX_DISTRIBUTION";
            case MARKETING_COMMUNICATION -> "MARKETING_COMMUNICATION";
            case RH_CULTURE_DIGITALE -> "RH_CULTURE_DIGITALE";
            case OFFRES_DIGITALES -> "OFFRES_DIGITALES";
            case MODELE_OPERATIONNEL_INNOVATION -> "MODELE_OPERATIONNEL_INNOVATION";
            case IT_DATA -> "IT_DATA";
        };
    }

    private EvaluationResponse toResponse(Evaluation evaluation) {
        List<AxisScoreResponse> scoresByAxis = List.of(
                new AxisScoreResponse("METIER", evaluation.getBusinessScore()),
                new AxisScoreResponse("PROCESSUS", evaluation.getProcessScore()),
                new AxisScoreResponse("SI", evaluation.getInformationSystemScore()),
                new AxisScoreResponse("CANAUX_DISTRIBUTION", evaluation.getCanauxDistributionScore()),
                new AxisScoreResponse("MARKETING_COMMUNICATION", evaluation.getMarketingCommunicationScore()),
                new AxisScoreResponse("RH_CULTURE_DIGITALE", evaluation.getRhCultureDigitaleScore()),
                new AxisScoreResponse("OFFRES_DIGITALES", evaluation.getOffresDigitalesScore()),
                new AxisScoreResponse("MODELE_OPERATIONNEL_INNOVATION", evaluation.getModeleOperationnelScore()),
                new AxisScoreResponse("IT_DATA", evaluation.getItDataScore())
        );

        List<EvaluationAnswer> sortedResponses = evaluation.getResponses().stream()
                .sorted(Comparator.comparing(answer -> answer.getQuestion().getDisplayOrder()))
                .toList();

        Map<String, List<EvaluationAnswer>> responsesBySubAxis = sortedResponses.stream()
                .collect(Collectors.groupingBy(
                        answer -> buildSubAxisKey(answer.getQuestion().getAxis(), answer.getQuestion().getSubAxis()),
                        LinkedHashMap::new,
                        Collectors.toList()
                ));

        List<SubAxisScoreResponse> scoresBySubAxis = responsesBySubAxis.entrySet().stream()
                .map(entry -> {
                    List<EvaluationAnswer> answers = entry.getValue();
                    Question question = answers.get(0).getQuestion();
                    double weightedScore = answers.stream()
                            .mapToDouble(answer -> normalize(answer.getScoreValue()) * questionWeight(answer))
                            .sum();
                    int totalWeight = answers.stream()
                            .mapToInt(this::questionWeight)
                            .sum();
                    double score = totalWeight == 0 ? 0.0 : round(weightedScore / totalWeight);

                    return new SubAxisScoreResponse(
                            mapAxisLabel(question.getAxis()),
                            question.getSubAxis(),
                            score,
                            answers.size()
                    );
                })
                .sorted(Comparator.comparing(SubAxisScoreResponse::getAxis).thenComparing(SubAxisScoreResponse::getSubAxis))
                .toList();

        List<AnswerSummaryResponse> answerSummaries = sortedResponses.stream()
                .map(answer -> new AnswerSummaryResponse(
                        answer.getQuestion().getId(),
                        answer.getQuestion().getText(),
                        mapAxisLabel(answer.getQuestion().getAxis()),
                        answer.getQuestion().getSubAxis(),
                        answer.getScoreValue(),
                        normalize(answer.getScoreValue()),
                        answer.getQuestion().getWeight(),
                        answer.getComment()
                ))
                .toList();

        List<AxisSynthesisResponse> synthesesByAxis = scoresByAxis.stream()
                .map(axisScore -> new AxisSynthesisResponse(
                        axisScore.getAxis(),
                        axisScore.getScore(),
                        buildAxisSummary(axisScore, scoresBySubAxis, answerSummaries)
                ))
                .toList();

        EvaluationResponse resp = new EvaluationResponse(
                evaluation.getId(),
                evaluation.getCompany().getId(),
                evaluation.getCompany().getName(),
                evaluation.getQuestionnaire().getId(),
                evaluation.getStatus(),
                evaluation.getGlobalScore(),
                evaluation.getMaturityLevel(),
                scoresByAxis,
                scoresBySubAxis,
                synthesesByAxis,
                answerSummaries,
                evaluation.getCreatedAt(),
                evaluation.getUpdatedAt()
        );
        resp.setTargetMaturityLevel(evaluation.getTargetMaturityLevel());
        return resp;
    }

    private int questionWeight(EvaluationAnswer answer) {
        return answer.getQuestion().getWeight() != null ? answer.getQuestion().getWeight() : 0;
    }

    private String buildAxisSummary(AxisScoreResponse axisScore,
                                    List<SubAxisScoreResponse> scoresBySubAxis,
                                    List<AnswerSummaryResponse> answerSummaries) {
        List<SubAxisScoreResponse> subAxisForAxis = scoresBySubAxis.stream()
                .filter(item -> item.getAxis().equals(axisScore.getAxis()))
                .toList();

        List<AnswerSummaryResponse> answersForAxis = answerSummaries.stream()
                .filter(item -> item.getAxis().equals(axisScore.getAxis()))
                .toList();

        long strongCount = answersForAxis.stream()
                .filter(answer -> answer.getNormalizedScore() >= 80)
                .count();
        long mediumCount = answersForAxis.stream()
                .filter(answer -> answer.getNormalizedScore() >= 50 && answer.getNormalizedScore() < 80)
                .count();
        long lowCount = answersForAxis.stream()
                .filter(answer -> answer.getNormalizedScore() < 50)
                .count();
        long commentCount = answersForAxis.stream()
                .map(AnswerSummaryResponse::getComment)
                .filter(Objects::nonNull)
                .map(String::trim)
                .filter(comment -> !comment.isEmpty())
                .count();

        SubAxisScoreResponse strongest = subAxisForAxis.stream()
                .max(Comparator.comparing(SubAxisScoreResponse::getScore))
                .orElse(null);
        SubAxisScoreResponse weakest = subAxisForAxis.stream()
                .min(Comparator.comparing(SubAxisScoreResponse::getScore))
                .orElse(null);

        String maturityLabel = determineMaturityLevel(axisScore.getScore()).name();
        StringBuilder summary = new StringBuilder();
        summary.append(axisScore.getAxis())
                .append(" presente un niveau ")
                .append(maturityLabel)
                .append(" avec un score de ")
                .append(axisScore.getScore())
                .append("/100 sur ")
                .append(answersForAxis.size())
                .append(" reponse(s). ");

        if (strongest != null) {
            summary.append("Le sous-axe le plus solide est ")
                    .append(strongest.getSubAxis())
                    .append(" (")
                    .append(strongest.getScore())
                    .append("/100). ");
        }

        if (weakest != null) {
            summary.append("Le principal point a renforcer est ")
                    .append(weakest.getSubAxis())
                    .append(" (")
                    .append(weakest.getScore())
                    .append("/100). ");
        }

        summary.append("La repartition des reponses montre ")
                .append(strongCount)
                .append(" point(s) fort(s), ")
                .append(mediumCount)
                .append(" point(s) intermediaire(s) et ")
                .append(lowCount)
                .append(" point(s) faible(s).");

        if (commentCount > 0) {
            summary.append(" ")
                    .append(commentCount)
                    .append(" commentaire(s) client ont complete cet axe.");
        }

        return summary.toString();
    }
}
