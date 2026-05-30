package com.iabenchmark.config;

import com.iabenchmark.model.Question;
import com.iabenchmark.model.QuestionAxis;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.model.QuestionnaireMode;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.QuestionnaireRepository;
import com.iabenchmark.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Component
public class DataInitializer implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    private final UserRepository userRepository;
    private final QuestionnaireRepository questionnaireRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository,
                           QuestionnaireRepository questionnaireRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.questionnaireRepository = questionnaireRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional
    public void run(ApplicationArguments args) {
        if (userRepository.count() == 0) {
            createUser("admin", "admin@iabenchmark.com", "Admin@123", "Admin", "Principal", Role.ADMIN);
            createUser("consultant1", "consultant@iabenchmark.com", "Consultant@123", "Jean", "Dupont", Role.CONSULTANT);
            log.info("Données initiales créées. Admin: admin@iabenchmark.com / Admin@123");
        }

        if (questionnaireRepository.count() == 0) {
            seedDefaultQuestionnaire();
            log.info("Questionnaire par défaut créé avec les 7 axes de maturité digitale.");
        } else {
            backfillMissingAxes();
            migrateSubAxes();
        }
    }

    // ── Backfill : ajoute les questions manquantes dans les questionnaires existants ──
    private void backfillMissingAxes() {
        Map<QuestionAxis, List<String[]>> defaults = buildDefaultQuestions();
        List<Questionnaire> questionnaires = questionnaireRepository.findAll();

        for (Questionnaire q : questionnaires) {
            Set<QuestionAxis> coveredAxes = q.getQuestions().stream()
                    .map(Question::getAxis)
                    .collect(Collectors.toSet());

            int maxOrder = q.getQuestions().stream()
                    .mapToInt(Question::getDisplayOrder)
                    .max()
                    .orElse(0);

            boolean modified = false;
            for (QuestionAxis axis : QuestionAxis.values()) {
                if (!coveredAxes.contains(axis)) {
                    for (String[] qd : defaults.get(axis)) {
                        maxOrder++;
                        addQuestion(q, maxOrder, axis, qd[0], qd[1]);
                    }
                    modified = true;
                    log.info("Questionnaire '{}' (id={}) : axe {} ajouté.", q.getTitle(), q.getId(), axis);
                }
            }
            if (modified) {
                questionnaireRepository.save(q);
            }
        }
    }

    // ── Questions par défaut pour chaque axe ─────────────────────────────────────
    private Map<QuestionAxis, List<String[]>> buildDefaultQuestions() {
        Map<QuestionAxis, List<String[]>> map = new EnumMap<>(QuestionAxis.class);

        map.put(QuestionAxis.BUSINESS, List.of(
                new String[]{"Stratégie digitale",
                        "L'entreprise dispose-t-elle d'une stratégie digitale formalisée avec des objectifs mesurables ?"},
                new String[]{"Orientation client",
                        "Dans quelle mesure les décisions stratégiques sont-elles guidées par les données clients ?"},
                new String[]{"Innovation",
                        "L'entreprise dispose-t-elle d'un processus structuré pour expérimenter et lancer des innovations digitales ?"},
                new String[]{"Modèle économique digital",
                        "Quelle part du chiffre d'affaires est générée via des canaux ou produits numériques ?"}
        ));

        map.put(QuestionAxis.PROCESS, List.of(
                new String[]{"Cartographie des processus",
                        "Les processus métier critiques sont-ils documentés, standardisés et disposent-ils de propriétaires désignés ?"},
                new String[]{"Automatisation",
                        "Quel est le niveau d'automatisation des tâches répétitives (RPA, workflows digitaux) ?"},
                new String[]{"Agilité",
                        "Les équipes projet appliquent-elles des méthodes agiles (Scrum, Kanban) dans leurs cycles de livraison ?"},
                new String[]{"Performance opérationnelle",
                        "Dispose-t-on de tableaux de bord KPI opérationnels avec des indicateurs suivis en temps réel ?"}
        ));

        map.put(QuestionAxis.INFORMATION_SYSTEM, List.of(
                new String[]{"Infrastructure & Cloud",
                        "L'infrastructure IT est-elle modernisée (cloud, virtualisation) et résiliente ?"},
                new String[]{"Cybersécurité",
                        "L'entreprise dispose-t-elle d'une politique de cybersécurité documentée et opérationnelle (IAM, MFA, SIEM) ?"},
                new String[]{"Données & Analytics",
                        "Les données sont-elles centralisées, gouvernées et disponibles pour l'analyse décisionnelle ?"},
                new String[]{"Intégration & API",
                        "Les systèmes internes communiquent-ils via des APIs standardisées permettant une intégration fluide ?"}
        ));

        map.put(QuestionAxis.MODELE_OPERATIONNEL_INNOVATION, List.of(
                new String[]{"Simplification & automatisation des processus",
                        "Les processus sont-ils dématérialisés, des workflows digitaux sont-ils en place et l'automatisation par RPA/IA est-elle déployée ?"},
                new String[]{"Gouvernance de la transformation digitale",
                        "Une stratégie et feuille de route digitale sont-elles définies avec une gouvernance, des budgets et un pilotage dédiés ?"},
                new String[]{"Développement de l'innovation",
                        "L'innovation est-elle développée en interne (labs, hackatons) avec des liens avec l'écosystème des fintechs et une veille concurrentielle du digital ?"}
        ));

        map.put(QuestionAxis.IT_DATA, List.of(
                new String[]{"Socle IT",
                        "L'infrastructure IT est-elle modernisée avec recours au cloud (IaaS, PaaS, SaaS), une architecture modulaire (micro-services) et ouverte (couche API) ?"},
                new String[]{"Socle IT",
                        "L'entreprise dispose-t-elle d'une politique de cybersécurité opérationnelle et investit-elle dans les nouvelles technologies (IA, IoT) ?"},
                new String[]{"Data",
                        "Les données (internes/externes) sont-elles acquises, mises en qualité et accessibles pour l'exploitation analytique et décisionnelle ?"},
                new String[]{"Data",
                        "Une gouvernance de la donnée est-elle en place avec une équipe dédiée à la data et des outils adaptés de gestion du cycle de vie des données ?"}
        ));

        map.put(QuestionAxis.CANAUX_DISTRIBUTION, List.of(
                new String[]{"Canaux de distribution & expérience client",
                        "Les clients peuvent-ils accéder aux services via des canaux digitaux (web/mobile), physiques et distants avec une expérience omnicanale cohérente ?"},
                new String[]{"Canaux de distribution & expérience client",
                        "La tarification et le modèle relationnel sont-ils adaptés et différenciés selon les canaux de distribution (digital, physique, distant) ?"},
                new String[]{"Selfcare client",
                        "Les fonctionnalités selfcare sont-elles développées sur les canaux digitaux (consultation, opérations, souscription, réclamation) ?"},
                new String[]{"Selfcare client",
                        "L'usage des canaux est-il piloté avec des indicateurs et un dispositif d'accompagnement des clients dans leur autonomisation digitale ?"}
        ));

        map.put(QuestionAxis.MARKETING_COMMUNICATION, List.of(
                new String[]{"Marketing & communication digitale",
                        "Une stratégie de communication digitale est-elle formalisée et déployée sur les canaux numériques avec une cohérence de marque ?"},
                new String[]{"Marketing & communication digitale",
                        "Des outils de marketing digital et de lead management sont-ils déployés avec mesure du ROI sur les campagnes ?"},
                new String[]{"Marketing & communication digitale",
                        "Des dispositifs d'écoute client (enquêtes de satisfaction, NPS) et de conduite de projets d'amélioration sont-ils opérationnels ?"}
        ));

        map.put(QuestionAxis.RH_CULTURE_DIGITALE, List.of(
                new String[]{"Culture digitale",
                        "Des programmes d'acculturation digitale et de formation aux nouveaux usages sont-ils déployés pour l'ensemble des collaborateurs ?"},
                new String[]{"Poste de travail du banquier",
                        "Les conseillers sont-ils équipés d'outils d'assistance technologique (IA, tableaux de bord data) pour améliorer la qualité de conseil ?"},
                new String[]{"Collaboratif & digital working",
                        "Des outils collaboratifs modernes (Teams, SharePoint...) sont-ils déployés et le télétravail est-il organisé de façon sécurisée ?"},
                new String[]{"Digitalisation de la fonction RH",
                        "Les processus RH (recrutement, évaluation, formation) sont-ils digitalisés et l'impact du digital sur les métiers est-il mesuré ?"},
                new String[]{"Agilité",
                        "Des méthodes agiles et une digital factory (labs UX, design sprints) sont-elles en place pour accélérer les projets de transformation ?"}
        ));

        map.put(QuestionAxis.OFFRES_DIGITALES, List.of(
                new String[]{"Offres digitales",
                        "L'entreprise propose-t-elle des offres de type néo-banque/banque en ligne avec des parcours de souscription 100% digitaux ?"},
                new String[]{"Offres digitales",
                        "Des services de conseil automatisés (agrégation patrimoniale, robot-advisor, coaching financier digital) sont-ils disponibles ?"},
                new String[]{"Open banking (BaaS, BaaP)",
                        "L'entreprise développe-t-elle des partenariats avec des fintechs et start-ups innovantes pour co-construire de nouvelles offres ?"},
                new String[]{"Open banking (BaaS, BaaP)",
                        "Les données et services sont-ils exposés via des APIs ouvertes dans une logique Banking-as-a-Service (BaaS) ou Banking-as-a-Platform (BaaP) ?"}
        ));

        return map;
    }

    // ── Seed initial si aucun questionnaire ──────────────────────────────────────
    private void seedDefaultQuestionnaire() {
        Questionnaire q = new Questionnaire();
        q.setTitle("Benchmark Maturité Digitale — Tous Secteurs");
        q.setDescription("Questionnaire de référence couvrant les 9 axes de maturité digitale.");
        q.setSector("Tous secteurs");
        q.setCountry("Tous pays");
        q.setMode(QuestionnaireMode.GENERATED);
        q.setActive(true);

        int order = 1;
        Map<QuestionAxis, List<String[]>> defaults = buildDefaultQuestions();
        for (QuestionAxis axis : QuestionAxis.values()) {
            for (String[] qd : defaults.get(axis)) {
                order = addQuestion(q, order, axis, qd[0], qd[1]);
            }
        }
        questionnaireRepository.save(q);
    }

    // ── Migration : met à jour les sous-axes par axe (idempotent) ────────────────
    private void migrateSubAxes() {
        Map<QuestionAxis, Map<String, String>> renamingByAxis = buildSubAxisRenamingMap();
        List<Questionnaire> questionnaires = questionnaireRepository.findAll();

        for (Questionnaire q : questionnaires) {
            boolean modified = false;

            // Renommer les anciens sous-axes selon leur axe (évite les conflits de noms)
            for (Question question : q.getQuestions()) {
                String old = question.getSubAxis();
                QuestionAxis axis = question.getAxis();
                if (old != null && renamingByAxis.containsKey(axis)) {
                    String newName = renamingByAxis.get(axis).get(old);
                    if (newName != null) {
                        question.setSubAxis(newName);
                        modified = true;
                    }
                }
            }

            // Ajouter les sous-axes totalement nouveaux manquants
            int maxOrder = q.getQuestions().stream().mapToInt(Question::getDisplayOrder).max().orElse(0);

            // RH : Poste de travail du banquier + Collaboratif & digital working
            boolean hasRh = q.getQuestions().stream().anyMatch(qn -> qn.getAxis() == QuestionAxis.RH_CULTURE_DIGITALE);
            if (hasRh) {
                if (q.getQuestions().stream().noneMatch(qn -> "Poste de travail du banquier".equals(qn.getSubAxis()))) {
                    maxOrder++;
                    addQuestion(q, maxOrder, QuestionAxis.RH_CULTURE_DIGITALE,
                            "Poste de travail du banquier",
                            "Les conseillers sont-ils équipés d'outils d'assistance technologique (IA, tableaux de bord data) pour améliorer la qualité de conseil ?");
                    modified = true;
                }
                if (q.getQuestions().stream().noneMatch(qn -> "Collaboratif & digital working".equals(qn.getSubAxis()))) {
                    maxOrder++;
                    addQuestion(q, maxOrder, QuestionAxis.RH_CULTURE_DIGITALE,
                            "Collaboratif & digital working",
                            "Des outils collaboratifs modernes (Teams, SharePoint...) sont-ils déployés et le télétravail est-il organisé de façon sécurisée ?");
                    modified = true;
                }
            }

            // Nouveaux axes complets : ajouter toutes leurs questions si absents
            Map<QuestionAxis, List<String[]>> defaults = buildDefaultQuestions();
            for (QuestionAxis newAxis : new QuestionAxis[]{QuestionAxis.MODELE_OPERATIONNEL_INNOVATION, QuestionAxis.IT_DATA}) {
                boolean axisAbsent = q.getQuestions().stream().noneMatch(qn -> qn.getAxis() == newAxis);
                if (axisAbsent) {
                    for (String[] qd : defaults.get(newAxis)) {
                        maxOrder++;
                        addQuestion(q, maxOrder, newAxis, qd[0], qd[1]);
                    }
                    modified = true;
                    log.info("Questionnaire '{}' : axe {} ajouté.", q.getTitle(), newAxis);
                }
            }

            if (modified) {
                questionnaireRepository.save(q);
                log.info("Questionnaire '{}' (id={}) : sous-axes migrés.", q.getTitle(), q.getId());
            }
        }
    }

    private Map<QuestionAxis, Map<String, String>> buildSubAxisRenamingMap() {
        Map<QuestionAxis, Map<String, String>> map = new EnumMap<>(QuestionAxis.class);

        // CANAUX_DISTRIBUTION
        Map<String, String> canaux = new LinkedHashMap<>();
        canaux.put("Présence digitale",          "Canaux de distribution & expérience client");
        canaux.put("Canaux transactionnels",     "Canaux de distribution & expérience client");
        canaux.put("Onboarding digital",         "Selfcare client");
        canaux.put("Accessibilité & couverture", "Selfcare client");
        map.put(QuestionAxis.CANAUX_DISTRIBUTION, canaux);

        // MARKETING_COMMUNICATION
        Map<String, String> marketing = new LinkedHashMap<>();
        marketing.put("Présence réseaux sociaux", "Marketing & communication digitale");
        marketing.put("Marketing digital",        "Marketing & communication digitale");
        marketing.put("Personnalisation",         "Marketing & communication digitale");
        marketing.put("Notoriété digitale",       "Marketing & communication digitale");
        map.put(QuestionAxis.MARKETING_COMMUNICATION, marketing);

        // RH_CULTURE_DIGITALE
        Map<String, String> rh = new LinkedHashMap<>();
        rh.put("Compétences digitales",  "Culture digitale");
        rh.put("Formation continue",     "Culture digitale");
        rh.put("SIRH & processus RH",    "Digitalisation de la fonction RH");
        rh.put("Culture d'innovation",   "Agilité");
        map.put(QuestionAxis.RH_CULTURE_DIGITALE, rh);

        // OFFRES_DIGITALES
        Map<String, String> offres = new LinkedHashMap<>();
        offres.put("Digitalisation des offres",    "Offres digitales");
        offres.put("Produits nativement digitaux", "Offres digitales");
        offres.put("Partenariats & API",           "Open banking (BaaS, BaaP)");
        offres.put("Innovation produit digital",   "Open banking (BaaS, BaaP)");
        map.put(QuestionAxis.OFFRES_DIGITALES, offres);

        return map;
    }

    private void createUser(String username, String email, String password,
                            String firstName, String lastName, Role role) {
        User user = new User(username, email, passwordEncoder.encode(password), firstName, lastName, role);
        user.setActive(true);
        userRepository.save(user);
    }

    private int addQuestion(Questionnaire q, int order, QuestionAxis axis, String subAxis, String text) {
        Question question = new Question();
        question.setText(text);
        question.setAxis(axis);
        question.setSubAxis(subAxis);
        question.setWeight(1);
        question.setDisplayOrder(order);
        q.addQuestion(question);
        return order + 1;
    }
}
