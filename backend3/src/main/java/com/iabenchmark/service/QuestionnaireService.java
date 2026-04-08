package com.iabenchmark.service;

import com.iabenchmark.dto.QuestionRequest;
import com.iabenchmark.dto.QuestionResponse;
import com.iabenchmark.dto.QuestionnaireRequest;
import com.iabenchmark.dto.QuestionnaireResponse;
import com.iabenchmark.model.Question;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.repository.QuestionnaireRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;
import java.util.Comparator;
import java.util.List;

@Service
public class QuestionnaireService {
    private final QuestionnaireRepository questionnaireRepository;

    public QuestionnaireService(QuestionnaireRepository questionnaireRepository) {
        this.questionnaireRepository = questionnaireRepository;
    }

    public List<QuestionnaireResponse> getAllQuestionnaires() {
        return questionnaireRepository.findAll().stream()
                .map(this::toResponse)
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
        return question;
    }

    private QuestionnaireResponse toResponse(Questionnaire questionnaire) {
        List<QuestionResponse> questions = questionnaire.getQuestions().stream()
                .sorted(Comparator.comparing(Question::getDisplayOrder))
                .map(question -> new QuestionResponse(
                        question.getId(),
                        question.getText(),
                        question.getAxis(),
                        question.getSubAxis(),
                        question.getWeight(),
                        question.getDisplayOrder()
                ))
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
