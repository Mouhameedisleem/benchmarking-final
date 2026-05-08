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

        map.put(QuestionAxis.CANAUX_DISTRIBUTION, List.of(
                new String[]{"Présence digitale",
                        "L'entreprise dispose-t-elle d'un site web responsive et d'une application mobile fonctionnelle ?"},
                new String[]{"Canaux transactionnels",
                        "Les clients peuvent-ils réaliser des opérations complètes en ligne (commande, paiement, suivi) ?"},
                new String[]{"Onboarding digital",
                        "Le parcours d'inscription ou de souscription est-il disponible 100% en ligne ?"},
                new String[]{"Accessibilité & couverture",
                        "Les canaux digitaux sont-ils accessibles sur mobile et couvrent-ils l'ensemble de la clientèle cible ?"}
        ));

        map.put(QuestionAxis.MARKETING_COMMUNICATION, List.of(
                new String[]{"Présence réseaux sociaux",
                        "L'entreprise est-elle active sur les réseaux sociaux avec une stratégie éditoriale définie ?"},
                new String[]{"Marketing digital",
                        "Des campagnes de marketing digital (SEO, SEM, email, social ads) sont-elles déployées avec suivi du ROI ?"},
                new String[]{"Personnalisation",
                        "Les communications clients sont-elles personnalisées selon le profil et le comportement digital ?"},
                new String[]{"Notoriété digitale",
                        "La marque bénéficie-t-elle d'une notoriété digitale mesurée (avis en ligne, part de voix) ?"}
        ));

        map.put(QuestionAxis.RH_CULTURE_DIGITALE, List.of(
                new String[]{"Compétences digitales",
                        "Les collaborateurs disposent-ils des compétences digitales nécessaires à leurs fonctions ?"},
                new String[]{"Formation continue",
                        "Un programme de formation digitale structuré (e-learning, certifications) est-il en place ?"},
                new String[]{"SIRH & processus RH",
                        "Les processus RH (paie, recrutement, évaluation) sont-ils digitalisés via un SIRH intégré ?"},
                new String[]{"Culture d'innovation",
                        "L'entreprise encourage-t-elle l'expérimentation et dispose-t-elle de rituels d'innovation ?"}
        ));

        map.put(QuestionAxis.OFFRES_DIGITALES, List.of(
                new String[]{"Digitalisation des offres",
                        "Les produits et services existants sont-ils disponibles en ligne avec souscription digitale ?"},
                new String[]{"Produits nativement digitaux",
                        "L'entreprise propose-t-elle des produits conçus exclusivement pour le canal digital ?"},
                new String[]{"Partenariats & API",
                        "L'entreprise intègre-t-elle des services partenaires ou expose-t-elle des APIs à des tiers ?"},
                new String[]{"Innovation produit digital",
                        "Des nouvelles offres digitales à valeur ajoutée sont-elles en cours de développement ou de lancement ?"}
        ));

        return map;
    }

    // ── Seed initial si aucun questionnaire ──────────────────────────────────────
    private void seedDefaultQuestionnaire() {
        Questionnaire q = new Questionnaire();
        q.setTitle("Benchmark Maturité Digitale — Tous Secteurs");
        q.setDescription("Questionnaire de référence couvrant les 7 axes de maturité digitale.");
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
