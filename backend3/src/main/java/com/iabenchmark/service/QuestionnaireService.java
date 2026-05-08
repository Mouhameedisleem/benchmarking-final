package com.iabenchmark.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.iabenchmark.dto.QuestionRequest;
import com.iabenchmark.dto.QuestionResponse;
import com.iabenchmark.dto.QuestionnaireRequest;
import com.iabenchmark.dto.QuestionnaireResponse;
import com.iabenchmark.model.Question;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.repository.QuestionnaireRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class QuestionnaireService {
    private final QuestionnaireRepository questionnaireRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final RestTemplate restTemplate = new RestTemplate();
    // Tracks questionnaire IDs currently being regenerated to avoid duplicate background jobs
    private final Set<Long> regeneratingNow = ConcurrentHashMap.newKeySet();

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    public QuestionnaireService(QuestionnaireRepository questionnaireRepository) {
        this.questionnaireRepository = questionnaireRepository;
    }

    public List<QuestionnaireResponse> getAllQuestionnaires() {
        return questionnaireRepository.findAll().stream()
                .map(this::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<QuestionnaireResponse> getQuestionnairesByCompany(Long companyId) {
        return questionnaireRepository.findByCompanyIdOrderByCreatedAtDesc(companyId)
                .stream()
                .map(q -> {
                    boolean needsOptions = q.getQuestions().stream()
                            .anyMatch(question -> question.getOptionsJson() == null
                                    || question.getOptionsJson().isBlank()
                                    || question.getOptionsJson().equals("[]"));
                    if (needsOptions && regeneratingNow.add(q.getId())) {
                        final Long qId = q.getId();
                        Thread t = new Thread(() -> {
                            try {
                                regenerateOptions(qId);
                            } catch (Exception ignored) {
                            } finally {
                                regeneratingNow.remove(qId);
                            }
                        });
                        t.setDaemon(true);
                        t.start();
                    }
                    return toResponse(q);
                })
                .toList();
    }

    public QuestionnaireResponse getQuestionnaireById(Long id) {
        return toResponse(findQuestionnaire(id));
    }

    public QuestionnaireResponse createQuestionnaire(QuestionnaireRequest request) {
        Questionnaire questionnaire = new Questionnaire();
        applyRequest(questionnaire, request);
        return toResponse(questionnaireRepository.save(questionnaire));
    }

    public QuestionnaireResponse updateQuestionnaire(Long id, QuestionnaireRequest request) {
        Questionnaire questionnaire = findQuestionnaire(id);
        applyRequest(questionnaire, request);
        return toResponse(questionnaireRepository.save(questionnaire));
    }

    public void deleteQuestionnaire(Long id) {
        questionnaireRepository.delete(findQuestionnaire(id));
    }

    @Transactional
    @SuppressWarnings("unchecked")
    public void regenerateOptions(Long id) {
        Questionnaire questionnaire = findQuestionnaire(id);
        List<Question> questions = questionnaire.getQuestions().stream()
                .sorted(Comparator.comparing(Question::getDisplayOrder))
                .toList();

        List<Map<String, Object>> qPayload = new ArrayList<>();
        for (Question q : questions) {
            Map<String, Object> item = new HashMap<>();
            item.put("text", q.getText());
            item.put("axis", q.getAxis().name());
            item.put("sub_axis", q.getSubAxis() != null ? q.getSubAxis() : "Général");
            qPayload.add(item);
        }

        ResponseEntity<Map<String, Object>> response = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/generate-options",
                Map.of("questions", qPayload),
                (Class<Map<String, Object>>) (Class<?>) Map.class);

        if (!response.getStatusCode().is2xxSuccessful() || response.getBody() == null) {
            throw new RuntimeException("AI service returned non-2xx response");
        }

        List<Map<String, Object>> updatedQuestions = (List<Map<String, Object>>) response.getBody().get("questions");
        if (updatedQuestions == null || updatedQuestions.size() != questions.size()) {
            throw new RuntimeException("AI service returned unexpected number of questions");
        }

        for (int i = 0; i < questions.size(); i++) {
            Object opts = updatedQuestions.get(i).get("options");
            if (opts instanceof List<?> optsList && optsList.size() == 5) {
                try {
                    questions.get(i).setOptionsJson(objectMapper.writeValueAsString(optsList));
                } catch (Exception ignored) {}
            }
        }

        questionnaireRepository.save(questionnaire);
    }

    private Questionnaire findQuestionnaire(Long id) {
        return questionnaireRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Questionnaire not found with id: " + id));
    }

    private void applyRequest(Questionnaire questionnaire, QuestionnaireRequest request) {
        questionnaire.setTitle(request.getTitle().trim());
        questionnaire.setDescription(request.getDescription() == null ? null : request.getDescription().trim());
        questionnaire.setSector(request.getSector().trim());
        questionnaire.setCountry(request.getCountry().trim());
        questionnaire.setMode(request.getMode());
        questionnaire.setActive(request.isActive());

        questionnaire.clearQuestions();
        request.getQuestions().stream()
                .sorted(Comparator.comparing(QuestionRequest::getDisplayOrder))
                .forEach(questionRequest -> questionnaire.addQuestion(toEntity(questionRequest)));
    }

    private Question toEntity(QuestionRequest request) {
        Question question = new Question();
        question.setText(request.getText().trim());
        question.setAxis(request.getAxis());
        question.setSubAxis(request.getSubAxis().trim());
        question.setWeight(request.getWeight());
        question.setDisplayOrder(request.getDisplayOrder());
        if (request.getOptions() != null && !request.getOptions().isEmpty()) {
            try { question.setOptionsJson(objectMapper.writeValueAsString(request.getOptions())); } catch (Exception ignored) {}
        }
        return question;
    }

    private QuestionnaireResponse toResponse(Questionnaire questionnaire) {
        List<QuestionResponse> questions = questionnaire.getQuestions().stream()
                .sorted(Comparator.comparing(Question::getDisplayOrder))
                .map(question -> {
                    List<String> opts = null;
                    if (question.getOptionsJson() != null) {
                        try { opts = objectMapper.readValue(question.getOptionsJson(), new TypeReference<>() {}); } catch (Exception ignored) {}
                    }
                    return new QuestionResponse(
                            question.getId(),
                            question.getText(),
                            question.getAxis(),
                            question.getSubAxis(),
                            question.getWeight(),
                            question.getDisplayOrder(),
                            opts
                    );
                })
                .toList();

        return new QuestionnaireResponse(
                questionnaire.getId(),
                questionnaire.getTitle(),
                questionnaire.getDescription(),
                questionnaire.getSector(),
                questionnaire.getCountry(),
                questionnaire.getMode(),
                questionnaire.isActive(),
                questionnaire.getCreatedAt(),
                questionnaire.getUpdatedAt(),
                questions
        );
    }
}
