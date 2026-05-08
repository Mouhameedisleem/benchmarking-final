package com.iabenchmark.service;

import com.iabenchmark.dto.CompanyRequest;
import com.iabenchmark.dto.CompanyResponse;
import com.iabenchmark.dto.CompanySetupRequest;
import com.iabenchmark.dto.CompanySetupResponse;
import com.iabenchmark.dto.QuestionRequest;
import com.iabenchmark.dto.QuestionResponse;
import com.iabenchmark.model.Company;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.Question;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.model.QuestionnaireMode;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.CompanyRepository;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.QuestionnaireRepository;
import com.iabenchmark.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class CompanyService {
    private final CompanyRepository companyRepository;
    private final UserRepository userRepository;
    private final EvaluationRepository evaluationRepository;
    private final QuestionnaireRepository questionnaireRepository;
    private final QuestionnaireService questionnaireService;
    private final EmailService emailService;
    private final PasswordEncoder passwordEncoder;
    private static RestTemplate buildRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(10_000);   // 10s to connect to AI service
        factory.setReadTimeout(240_000);     // 240s — large model + options batch can take up to 3 min
        return new RestTemplate(factory);
    }
    private final RestTemplate restTemplate = buildRestTemplate();

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    public CompanyService(CompanyRepository companyRepository,
                          UserRepository userRepository,
                          EvaluationRepository evaluationRepository,
                          QuestionnaireRepository questionnaireRepository,
                          QuestionnaireService questionnaireService,
                          EmailService emailService,
                          PasswordEncoder passwordEncoder) {
        this.companyRepository = companyRepository;
        this.userRepository = userRepository;
        this.evaluationRepository = evaluationRepository;
        this.questionnaireRepository = questionnaireRepository;
        this.questionnaireService = questionnaireService;
        this.emailService = emailService;
        this.passwordEncoder = passwordEncoder;
    }

    public List<CompanyResponse> getCompaniesForUser(User user) {
        if (user.getRole() == Role.ADMIN) {
            return companyRepository.findAll().stream().map(this::toResponse).toList();
        }
        return companyRepository.findByConsultantId(user.getId()).stream().map(this::toResponse).toList();
    }

    public List<CompanyResponse> getAllCompanies() {
        return companyRepository.findAll().stream().map(this::toResponse).toList();
    }

    public CompanyResponse getCompanyById(Long id) {
        return toResponse(findCompany(id));
    }

    public CompanyResponse createCompany(CompanyRequest request, User currentUser) {
        if (companyRepository.existsByNameIgnoreCase(request.getName())) {
            throw new RuntimeException("Company name already exists");
        }

        Company company = new Company();
        applyRequest(company, request);

        if (currentUser.getRole() == Role.ADMIN && request.getConsultantId() != null) {
            userRepository.findById(request.getConsultantId()).ifPresent(company::setConsultant);
        } else if (currentUser.getRole() == Role.CONSULTANT) {
            company.setConsultant(currentUser);
        }
        return toResponse(companyRepository.save(company));
    }

    public CompanyResponse updateCompany(Long id, CompanyRequest request) {
        Company company = findCompany(id);
        boolean nameChanged = !company.getName().equalsIgnoreCase(request.getName());

        if (nameChanged && companyRepository.existsByNameIgnoreCase(request.getName())) {
            throw new RuntimeException("Company name already exists");
        }

        applyRequest(company, request);
        if (request.getConsultantId() != null) {
            userRepository.findById(request.getConsultantId()).ifPresent(company::setConsultant);
        }
        return toResponse(companyRepository.save(company));
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> generateAiQuestions(Long companyId) {
        Company company = findCompany(companyId);
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("sector", company.getSector());
        requestBody.put("country", company.getCountry());
        requestBody.put("company_size", company.getSize());
        requestBody.put("language", "fr");
        requestBody.put("num_questions", 28);

        ResponseEntity<Map<String, Object>> aiResponse = restTemplate.postForEntity(
                aiServiceUrl + "/api/ai/generate-questionnaire", requestBody,
                (Class<Map<String, Object>>) (Class<?>) Map.class);
        return aiResponse.getBody();
    }

    @Transactional(readOnly = true)
    public List<QuestionResponse> getSectorQuestions(Long companyId) {
        Company company = findCompany(companyId);
        String sector = company.getSector();
        List<Questionnaire> sectorQuestionnaires = questionnaireRepository.findBySectorIgnoreCaseWithQuestions(sector);

        // Deduplicate by normalized text across all questionnaires for this sector
        // excluding the questionnaire already belonging to this company
        LinkedHashMap<String, QuestionResponse> seen = new LinkedHashMap<>();
        ObjectMapper mapper = new ObjectMapper();

        for (Questionnaire q : sectorQuestionnaires) {
            if (companyId.equals(q.getCompanyId())) continue;
            for (Question question : q.getQuestions()) {
                String key = question.getText().trim().toLowerCase();
                if (!seen.containsKey(key)) {
                    List<String> options = new ArrayList<>();
                    if (question.getOptionsJson() != null) {
                        try {
                            options = mapper.readValue(question.getOptionsJson(),
                                    mapper.getTypeFactory().constructCollectionType(List.class, String.class));
                        } catch (Exception ignored) {}
                    }
                    seen.put(key, new QuestionResponse(
                            question.getId(),
                            question.getText(),
                            question.getAxis(),
                            question.getSubAxis(),
                            question.getWeight(),
                            question.getDisplayOrder(),
                            options
                    ));
                }
            }
        }
        return new ArrayList<>(seen.values());
    }

    public CompanySetupResponse finalizeSetup(Long companyId, CompanySetupRequest request) {
        Company company = findCompany(companyId);

        if (company.getEmail() == null || company.getEmail().isBlank()) {
            throw new RuntimeException("L'entreprise n'a pas d'email. Veuillez en ajouter un avant de finaliser.");
        }

        // Create CLIENT user account for the company
        String rawPassword = UUID.randomUUID().toString().replace("-", "").substring(0, 10);
        if (!userRepository.existsByEmail(company.getEmail())) {
            User clientUser = new User(
                    company.getEmail(),
                    company.getEmail(),
                    passwordEncoder.encode(rawPassword),
                    company.getName(),
                    "",
                    Role.CLIENT
            );
            clientUser.setCompany(company);
            clientUser.setActive(true);
            userRepository.save(clientUser);
        } else {
            rawPassword = null; // account already exists, don't re-send
        }

        // Save the validated questionnaire linked to this company
        Questionnaire questionnaire = new Questionnaire();
        questionnaire.setTitle("Évaluation de maturité digitale — " + company.getName());
        questionnaire.setDescription("Questionnaire généré par IA pour " + company.getName()
                + " (" + company.getSector() + ")");
        questionnaire.setSector(company.getSector());
        questionnaire.setCountry(company.getCountry());
        questionnaire.setMode(QuestionnaireMode.GENERATED);
        questionnaire.setActive(true);
        questionnaire.setCompanyId(companyId);

        request.getQuestions().stream()
                .sorted(Comparator.comparing(QuestionRequest::getDisplayOrder))
                .forEach(qr -> {
                    Question q = new Question();
                    q.setText(qr.getText().trim());
                    q.setAxis(qr.getAxis());
                    q.setSubAxis(qr.getSubAxis() != null ? qr.getSubAxis().trim() : "Général");
                    q.setWeight(qr.getWeight() != null ? qr.getWeight() : 3);
                    q.setDisplayOrder(qr.getDisplayOrder() != null ? qr.getDisplayOrder() : 1);
                    if (qr.getOptions() != null && !qr.getOptions().isEmpty()) {
                        try { q.setOptionsJson(new ObjectMapper().writeValueAsString(qr.getOptions())); } catch (Exception ignored) {}
                    }
                    questionnaire.addQuestion(q);
                });

        Questionnaire saved = questionnaireRepository.save(questionnaire);

        // Regenerate contextual AI options in background — doesn't block the HTTP response
        final Long savedId = saved.getId();
        Thread optionsThread = new Thread(() -> {
            try {
                Thread.sleep(300); // Let the transaction commit first
                questionnaireService.regenerateOptions(savedId);
            } catch (Exception ignored) {}
        });
        optionsThread.setDaemon(true);
        optionsThread.start();

        // Send credentials by email — if SMTP fails, the setup still succeeds
        String emailStatus = "Questionnaire enregistré.";
        if (rawPassword != null) {
            try {
                emailService.sendCompanyCredentials(company.getEmail(), company.getName(),
                        company.getEmail(), rawPassword);
                emailStatus = "Questionnaire enregistré et identifiants envoyés à " + company.getEmail();
            } catch (Exception e) {
                emailStatus = "Questionnaire enregistré. "
                        + "Identifiants : login = " + company.getEmail()
                        + " | mot de passe = " + rawPassword
                        + " (email non envoyé — erreur SMTP : " + e.getMessage() + ")";
            }
        }

        return new CompanySetupResponse(saved.getId(), emailStatus);
    }

    @Transactional
    public void deleteCompany(Long id) {
        Company company = findCompany(id);

        // Delete evaluations (cascades to EvaluationAnswer)
        List<Evaluation> evaluations = evaluationRepository.findByCompanyId(id);
        evaluationRepository.deleteAll(evaluations);

        // Delete questionnaires linked to this company (cascades to questions)
        List<Questionnaire> questionnaires = questionnaireRepository.findByCompanyIdOrderByCreatedAtDesc(id);
        questionnaireRepository.deleteAll(questionnaires);

        // Delete users attached to this company
        List<User> users = userRepository.findByCompanyId(id);
        userRepository.deleteAll(users);

        companyRepository.delete(company);
    }

    private Company findCompany(Long id) {
        return companyRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Company not found with id: " + id));
    }

    private void applyRequest(Company company, CompanyRequest request) {
        company.setName(request.getName().trim());
        company.setSector(request.getSector().trim());
        company.setCountry(request.getCountry().trim());
        company.setSize(request.getSize().trim());
        company.setBusinessDomain(request.getBusinessDomain().trim());
        company.setWebsite(trimToNull(request.getWebsite()));
        company.setPhone(trimToNull(request.getPhone()));
        company.setEmail(trimToNull(request.getEmail()));
        company.setAddress(trimToNull(request.getAddress()));
    }

    private CompanyResponse toResponse(Company company) {
        User primaryContact = userRepository.findFirstByCompanyIdOrderByCreatedAtAsc(company.getId()).orElse(null);
        String email = company.getEmail() != null ? company.getEmail() : primaryContact != null ? primaryContact.getEmail() : null;
        String phone = company.getPhone() != null ? company.getPhone() : primaryContact != null ? primaryContact.getPhone() : null;
        User consultant = company.getConsultant();
        Long consultantId = consultant != null ? consultant.getId() : null;
        String consultantName = consultant != null ? consultant.getFirstName() + " " + consultant.getLastName() : null;

        return new CompanyResponse(
                company.getId(),
                company.getName(),
                company.getSector(),
                company.getCountry(),
                company.getSize(),
                company.getBusinessDomain(),
                company.getWebsite(),
                phone,
                email,
                company.getAddress(),
                company.getCreatedAt(),
                company.getUpdatedAt(),
                consultantId,
                consultantName
        );
    }

    private String trimToNull(String value) {
        if (value == null) return null;
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }
}
