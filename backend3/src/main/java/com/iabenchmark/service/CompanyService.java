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
import com.iabenchmark.repository.ActionPlanRepository;
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
import java.util.Objects;
import java.util.UUID;

@Service
public class CompanyService {
    private final CompanyRepository companyRepository;
    private final UserRepository userRepository;
    private final EvaluationRepository evaluationRepository;
    private final QuestionnaireRepository questionnaireRepository;
    private final ActionPlanRepository actionPlanRepository;
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
                          ActionPlanRepository actionPlanRepository,
                          QuestionnaireService questionnaireService,
                          EmailService emailService,
                          PasswordEncoder passwordEncoder) {
        this.companyRepository = companyRepository;
        this.userRepository = userRepository;
        this.evaluationRepository = evaluationRepository;
        this.questionnaireRepository = questionnaireRepository;
        this.actionPlanRepository = actionPlanRepository;
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
            userRepository.findById(Objects.requireNonNull(request.getConsultantId())).ifPresent(company::setConsultant);
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
            userRepository.findById(Objects.requireNonNull(request.getConsultantId())).ifPresent(company::setConsultant);
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
        requestBody.put("num_questions", 27);

        try {
            ResponseEntity<Map<String, Object>> aiResponse = restTemplate.postForEntity(
                    aiServiceUrl + "/api/ai/generate-questionnaire", requestBody,
                    (Class<Map<String, Object>>) (Class<?>) Map.class);
            Map<String, Object> body = aiResponse.getBody();
            if (body != null) {
                body.put("aiAvailable", true);
                return body;
            }
        } catch (Exception ignored) {
            // AI service is down — fall through to fallback
        }

        // Fallback: use sector questions from the database
        List<QuestionResponse> sectorQs = getSectorQuestions(companyId);
        List<Map<String, Object>> fallbackQuestions;
        if (!sectorQs.isEmpty()) {
            fallbackQuestions = new ArrayList<>();
            for (int i = 0; i < sectorQs.size(); i++) {
                QuestionResponse q = sectorQs.get(i);
                Map<String, Object> qMap = new HashMap<>();
                qMap.put("text", q.getText());
                qMap.put("axis", q.getAxis().name());
                qMap.put("sub_axis", q.getSubAxis() != null ? q.getSubAxis() : "Général");
                qMap.put("weight", q.getWeight() != null ? q.getWeight() : 3);
                qMap.put("display_order", i + 1);
                qMap.put("options", q.getOptions() != null ? q.getOptions() : List.of());
                fallbackQuestions.add(qMap);
            }
        } else {
            fallbackQuestions = buildDefaultQuestions();
        }

        Map<String, Object> result = new HashMap<>();
        result.put("questions", fallbackQuestions);
        result.put("aiAvailable", false);
        result.put("source", sectorQs.isEmpty() ? "default" : "sector");
        return result;
    }

    private List<Map<String, Object>> buildDefaultQuestions() {
        record Q(String text, String axis, String subAxis) {}
        List<Q> defaults = List.of(
            new Q("Votre stratégie de transformation digitale est-elle formalisée et partagée ?",           "BUSINESS",               "Stratégie"),
            new Q("Vos processus métier sont-ils documentés et optimisés ?",                               "BUSINESS",               "Processus métier"),
            new Q("Utilisez-vous des indicateurs digitaux pour piloter votre activité ?",                  "BUSINESS",               "Pilotage"),
            new Q("Votre offre produits/services intègre-t-elle une dimension digitale ?",                 "BUSINESS",               "Offre"),
            new Q("Vos processus opérationnels sont-ils automatisés ?",                                    "PROCESS",                "Automatisation"),
            new Q("Avez-vous mis en place une gestion de la qualité numérique ?",                          "PROCESS",                "Qualité"),
            new Q("Vos processus de décision s'appuient-ils sur des données en temps réel ?",             "PROCESS",                "Décision"),
            new Q("La gestion documentaire est-elle dématérialisée ?",                                    "PROCESS",                "Dématérialisation"),
            new Q("Votre infrastructure SI est-elle adaptée aux besoins actuels ?",                       "INFORMATION_SYSTEM",     "Infrastructure"),
            new Q("Utilisez-vous des solutions cloud pour vos applications métier ?",                     "INFORMATION_SYSTEM",     "Cloud"),
            new Q("La sécurité des systèmes d'information est-elle gérée activement ?",                   "INFORMATION_SYSTEM",     "Sécurité"),
            new Q("Vos systèmes sont-ils intégrés et interopérables ?",                                   "INFORMATION_SYSTEM",     "Intégration"),
            new Q("Utilisez-vous des canaux digitaux pour distribuer vos produits/services ?",            "CANAUX_DISTRIBUTION",    "Canaux digitaux"),
            new Q("Votre site web est-il optimisé pour la conversion client ?",                           "CANAUX_DISTRIBUTION",    "Web"),
            new Q("Proposez-vous une application mobile à vos clients ?",                                 "CANAUX_DISTRIBUTION",    "Mobile"),
            new Q("Vos canaux digitaux et physiques sont-ils intégrés (omnicanal) ?",                     "CANAUX_DISTRIBUTION",    "Omnicanal"),
            new Q("Menez-vous des campagnes marketing digitales ciblées ?",                               "MARKETING_COMMUNICATION","Marketing digital"),
            new Q("Analysez-vous les données clients pour personnaliser vos communications ?",            "MARKETING_COMMUNICATION","Personnalisation"),
            new Q("Votre présence sur les réseaux sociaux est-elle active et mesurée ?",                  "MARKETING_COMMUNICATION","Social media"),
            new Q("Mesurez-vous le retour sur investissement de vos actions marketing digitales ?",       "MARKETING_COMMUNICATION","ROI"),
            new Q("Vos collaborateurs bénéficient-ils de formations aux outils digitaux ?",              "RH_CULTURE_DIGITALE",    "Formation"),
            new Q("La culture digitale est-elle intégrée dans vos processus RH ?",                       "RH_CULTURE_DIGITALE",    "Culture"),
            new Q("Disposez-vous de profils digitaux au sein de vos équipes ?",                          "RH_CULTURE_DIGITALE",    "Compétences"),
            new Q("La direction impulse-t-elle la transformation digitale ?",                            "RH_CULTURE_DIGITALE",    "Leadership"),
            new Q("Proposez-vous des services/produits nativement digitaux ?",                           "OFFRES_DIGITALES",       "Offres digitales"),
            new Q("Vos offres s'appuient-elles sur des données et l'IA ?",                               "OFFRES_DIGITALES",       "Data & IA"),
            new Q("Votre modèle économique intègre-t-il des revenus digitaux ?",                         "OFFRES_DIGITALES",       "Modèle économique"),
            new Q("Innover digitalement fait-il partie de votre stratégie produit ?",                    "OFFRES_DIGITALES",                 "Innovation"),
            new Q("Vos processus métier clés sont-ils automatisés de bout en bout (0 ressaisie) ?",      "MODELE_OPERATIONNEL_INNOVATION",   "Automatisation"),
            new Q("Une gouvernance digitale et une politique de conformité sont-elles formalisées ?",    "MODELE_OPERATIONNEL_INNOVATION",   "Gouvernance"),
            new Q("Des initiatives d'innovation digitale (IoT, IA) sont-elles engagées ?",              "MODELE_OPERATIONNEL_INNOVATION",   "Innovation"),
            new Q("L'infrastructure IT est-elle fiable, redondante et disponible en permanence ?",      "IT_DATA",                          "Socle IT"),
            new Q("Des outils d'analyse de données et d'aide à la décision sont-ils déployés ?",        "IT_DATA",                          "Data & Analytics"),
            new Q("Une gouvernance des données (qualité, sécurité, valorisation) est-elle définie ?",   "IT_DATA",                          "Gouvernance données")
        );
        List<Map<String, Object>> result = new ArrayList<>();
        for (int i = 0; i < defaults.size(); i++) {
            Q q = defaults.get(i);
            Map<String, Object> qMap = new HashMap<>();
            qMap.put("text", q.text());
            qMap.put("axis", q.axis());
            qMap.put("sub_axis", q.subAxis());
            qMap.put("weight", 3);
            qMap.put("display_order", i + 1);
            qMap.put("options", List.of());
            result.add(qMap);
        }
        return result;
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

        // Regenerate contextual AI options in background if any question has missing/generic options
        boolean hasGenericOptions = saved.getQuestions().stream().anyMatch(q -> {
            String opts = q.getOptionsJson();
            if (opts == null || opts.isBlank() || opts.equals("[]")) return true;
            return opts.contains("Aucun dispositif ou outil en place")
                || opts.contains("Premiers essais isolés, sans processus établi")
                || opts.contains("Pratiques partiellement formalisées, adoption en cours");
        });
        if (hasGenericOptions) {
            final Long savedId = saved.getId();
            Thread optionsThread = new Thread(() -> {
                try {
                    Thread.sleep(500);
                    questionnaireService.regenerateOptions(savedId);
                } catch (Exception ignored) {}
            });
            optionsThread.setDaemon(true);
            optionsThread.start();
        }

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

        List<Evaluation> evaluations = evaluationRepository.findByCompanyId(id);

        // 1. Delete action plans before evaluations (FK: action_plan.evaluation_id → evaluations.id)
        for (Evaluation evaluation : evaluations) {
            actionPlanRepository.deleteByEvaluationId(evaluation.getId());
        }

        // 2. Delete evaluations (cascades to EvaluationAnswer via JPA cascade)
        evaluationRepository.deleteAll(Objects.requireNonNull(evaluations));

        // 3. Delete questionnaires linked to this company (cascades to questions)
        List<Questionnaire> questionnaires = questionnaireRepository.findByCompanyIdOrderByCreatedAtDesc(id);
        questionnaireRepository.deleteAll(Objects.requireNonNull(questionnaires));

        // 4. Delete users attached to this company
        List<User> users = userRepository.findByCompanyId(id);
        userRepository.deleteAll(Objects.requireNonNull(users));

        companyRepository.delete(Objects.requireNonNull(company));
    }

    private Company findCompany(Long id) {
        return companyRepository.findById(Objects.requireNonNull(id))
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
