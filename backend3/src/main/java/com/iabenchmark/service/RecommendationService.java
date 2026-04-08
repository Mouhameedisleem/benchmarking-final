package com.iabenchmark.service;

import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.MaturityLevel;
import com.iabenchmark.repository.EvaluationRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RecommendationService {

    private final EvaluationRepository evaluationRepository;

    public RecommendationService(EvaluationRepository evaluationRepository) {
        this.evaluationRepository = evaluationRepository;
    }

    public List<RecommendationResponse> generateRecommendations(Long evaluationId) {
        Evaluation evaluation = evaluationRepository.findById(evaluationId)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        String sector = evaluation.getCompany().getSector();
        String country = evaluation.getCompany().getCountry();
        double businessScore = evaluation.getBusinessScore();
        double processScore = evaluation.getProcessScore();
        double siScore = evaluation.getInformationSystemScore();
        MaturityLevel maturity = evaluation.getMaturityLevel();

        List<RecommendationResponse> recommendations = new ArrayList<>();

        recommendations.addAll(generateMetierRecommendations(businessScore, sector, country, maturity));
        recommendations.addAll(generateProcessusRecommendations(processScore, sector, country, maturity));
        recommendations.addAll(generateSIRecommendations(siScore, sector, country, maturity));

        return recommendations;
    }

    private List<RecommendationResponse> generateMetierRecommendations(
            double score, String sector, String country, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "METIER", "HAUTE",
                    "Définir une feuille de route de transformation digitale",
                    "L'entreprise n'a pas encore formalisé sa stratégie digitale. Il est prioritaire de définir une vision claire avec des objectifs mesurables à 1, 3 et 5 ans.",
                    "Selon le Digital Maturity Model (Deloitte), les entreprises leaders formalisent leur roadmap digitale en impliquant la direction générale et les métiers dès la phase initiale."
            ));
            recs.add(new RecommendationResponse(
                    "METIER", "HAUTE",
                    "Développer la culture digitale des équipes",
                    "Le manque de compétences digitales au sein des équipes métier freine la transformation. Un programme de formation ciblé est indispensable.",
                    "McKinsey (2023) indique que 70% des transformations digitales échouent en raison d'un déficit de compétences. Le reskilling continu est reconnu comme un facteur clé de succès."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "METIER", "MOYENNE",
                    "Renforcer l'orientation client via les données",
                    "Les données clients sont collectées mais insuffisamment exploitées pour personnaliser les offres et améliorer l'expérience client.",
                    "Gartner recommande l'adoption d'une approche Customer Data Platform (CDP) pour centraliser et activer les données clients en temps réel."
            ));
            recs.add(new RecommendationResponse(
                    "METIER", "MOYENNE",
                    "Intégrer l'IA dans les processus métier prioritaires",
                    "Des opportunités d'automatisation intelligente existent dans les processus métier à forte répétitivité ou à haute valeur décisionnelle.",
                    "D'après le rapport WEF 2023 sur la compétitivité digitale, les entreprises de secteur " + formatSector(sector) + " qui intègrent l'IA dans leurs processus métier gagnent en moyenne 15% de productivité."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "METIER", "MOYENNE",
                    "Développer de nouveaux modèles de revenus numériques",
                    "Le niveau de maturité atteint permet d'explorer de nouveaux modèles économiques basés sur le digital (plateformes, API economy, services data).",
                    "Selon BCG, les entreprises en phase avancée de maturité digitale génèrent 30% de leurs revenus via des canaux numériques. L'objectif est d'atteindre ce seuil dans les 18 mois."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "METIER", "BASSE",
                    "Partager les bonnes pratiques et devenir un acteur de référence",
                    "À ce niveau d'excellence, l'entreprise peut valoriser son savoir-faire digital en le partageant avec son écosystème (partenaires, fournisseurs, clients).",
                    "Les leaders digitaux du secteur " + formatSector(sector) + " participent activement aux benchmarks sectoriels et aux consortiums d'innovation pour maintenir leur avance compétitive."
            ));
        }

        // Recommandation sectorielle spécifique
        if (sector != null && !sector.isEmpty()) {
            recs.add(buildSectorMetierRec(sector, score));
        }

        return recs;
    }

    private List<RecommendationResponse> generateProcessusRecommendations(
            double score, String sector, String country, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "HAUTE",
                    "Cartographier et standardiser les processus clés",
                    "Les processus actuels sont peu documentés et non standardisés, ce qui génère des inefficacités et des risques opérationnels importants.",
                    "La méthode BPM (Business Process Management) recommandée par l'ABPMP permet de cartographier, optimiser et automatiser les processus en priorisant par impact business."
            ));
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "HAUTE",
                    "Mettre en place un programme d'automatisation RPA",
                    "De nombreuses tâches répétitives et chronophages peuvent être automatisées grâce aux outils de RPA (Robotic Process Automation), libérant ainsi du temps pour des activités à valeur ajoutée.",
                    "Forrester Research estime que le RPA réduit les coûts opérationnels de 25 à 50% sur les processus ciblés, avec un ROI positif en moins de 12 mois."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "MOYENNE",
                    "Intégrer les processus via une architecture orientée API",
                    "Les processus sont partiellement digitalisés mais manquent d'intégration entre systèmes, créant des silos d'information et des saisies manuelles redondantes.",
                    "L'approche API-first recommandée par Gartner permet une intégration fluide entre les systèmes internes et externes, réduisant les délais de traitement de 40%."
            ));
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "MOYENNE",
                    "Déployer un outil de pilotage de la performance processus",
                    "Sans mesure des indicateurs de performance processus (KPI), il est difficile d'identifier les goulots d'étranglement et de piloter les améliorations.",
                    "La norme ISO 9001:2015 et le cadre COBIT recommandent la mise en place de tableaux de bord processus avec des KPI mesurables et actionnables."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "MOYENNE",
                    "Adopter une approche d'amélioration continue (Lean/Agile)",
                    "Les processus sont bien structurés. L'étape suivante consiste à instaurer une culture d'amélioration continue pour maintenir l'efficacité opérationnelle.",
                    "Les entreprises qui adoptent le Lean Management réduisent leurs délais de livraison de 50% et améliorent la satisfaction client de 25% selon le MIT Sloan Management Review."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "PROCESSUS", "BASSE",
                    "Explorer les processus augmentés par l'IA générative",
                    "Le niveau d'excellence atteint permet d'explorer l'intégration de l'IA générative dans les processus décisionnels et créatifs pour maintenir l'avantage compétitif.",
                    "D'après Accenture Technology Vision 2024, 95% des dirigeants considèrent que l'IA générative redéfinira fondamentalement leurs processus dans les 3 prochaines années."
            ));
        }

        return recs;
    }

    private List<RecommendationResponse> generateSIRecommendations(
            double score, String sector, String country, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "SI", "HAUTE",
                    "Moderniser l'architecture du système d'information",
                    "Le SI actuel repose sur des technologies obsolètes qui limitent l'agilité et augmentent les risques de sécurité. Une modernisation progressive est indispensable.",
                    "La TOGAF (The Open Group Architecture Framework) recommande une approche de modernisation par couches : d'abord les couches présentations, puis les services métier, enfin les données."
            ));
            recs.add(new RecommendationResponse(
                    "SI", "HAUTE",
                    "Mettre en place une politique de cybersécurité robuste",
                    "La maturité cybersécurité est insuffisante au regard des risques actuels. Un référentiel de sécurité (ISO 27001, NIST) doit être adopté en priorité.",
                    "Selon l'ANSSI, les organisations de secteur " + formatSector(sector) + " font partie des cibles prioritaires des cyberattaques. La certification ISO 27001 réduit le risque d'incident de 60%."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "SI", "MOYENNE",
                    "Accélérer la migration vers le Cloud",
                    "La stratégie Cloud est partiellement définie mais la migration est lente. Un plan de migration structuré (Cloud-first ou Cloud-smart) doit être établi.",
                    "IDC prédit que d'ici 2025, 80% des entreprises de " + formatCountry(country) + " auront adopté une stratégie multi-cloud. Le retard dans cette transition génère un désavantage compétitif croissant."
            ));
            recs.add(new RecommendationResponse(
                    "SI", "MOYENNE",
                    "Mettre en place une gouvernance des données (Data Governance)",
                    "Les données de l'entreprise sont éparpillées dans plusieurs systèmes sans gouvernance claire, limitant leur exploitation à des fins analytiques et décisionnelles.",
                    "Le DAMA-DMBOK (Data Management Body of Knowledge) propose un cadre de gouvernance des données reconnu internationalement, incluant la qualité, la sécurité et le cycle de vie des données."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "SI", "MOYENNE",
                    "Développer une plateforme de données unifiée (Data Platform)",
                    "Les fondations du SI sont solides. L'enjeu est maintenant de construire une plateforme data centralisée permettant l'analyse avancée et l'IA.",
                    "Les architectures Data Lakehouse (Databricks, Snowflake) sont plébiscitées par les entreprises en phase avancée pour unifier les données opérationnelles et analytiques en une seule plateforme."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "SI", "BASSE",
                    "Adopter une architecture orientée IA (AI-ready architecture)",
                    "Le SI mature permet d'aller vers une architecture nativement orientée IA, avec des capacités de Machine Learning en temps réel intégrées aux processus métier.",
                    "Google Cloud Architecture Framework et AWS Well-Architected Framework proposent des patterns d'architecture AI-ready permettant de déployer des modèles ML en production avec une latence minimale."
            ));
        }

        // Recommandation pays spécifique
        if (country != null && !country.isEmpty()) {
            recs.add(buildCountrySIRec(country, score));
        }

        return recs;
    }

    private RecommendationResponse buildSectorMetierRec(String sector, double score) {
        return switch (sector.toLowerCase()) {
            case "banking", "banque" -> new RecommendationResponse(
                    "METIER", score < 50 ? "HAUTE" : "MOYENNE",
                    "Accélérer l'Open Banking et l'innovation fintech",
                    "Le secteur bancaire est en pleine disruption. L'adoption de l'Open Banking et le développement de partenariats fintech sont devenus des impératifs stratégiques.",
                    "La directive DSP2 européenne et les standards UEMOA imposent l'ouverture des APIs bancaires. Les banques leaders de " + sector + " génèrent 20% de leurs revenus via des écosystèmes open banking."
            );
            case "healthcare", "sante" -> new RecommendationResponse(
                    "METIER", score < 50 ? "HAUTE" : "MOYENNE",
                    "Développer le dossier patient numérique et la télémédecine",
                    "La digitalisation du parcours patient est un enjeu de compétitivité et de qualité de soins. Les établissements de santé leaders ont déjà déployé des solutions de santé digitale intégrées.",
                    "L'OMS recommande l'adoption de standards HL7 FHIR pour l'interopérabilité des systèmes de santé. La télémédecine réduit les délais de prise en charge de 35% selon l'étude OCDE 2023."
            );
            case "industry", "industrie" -> new RecommendationResponse(
                    "METIER", score < 50 ? "HAUTE" : "MOYENNE",
                    "Déployer une stratégie Industrie 4.0",
                    "L'industrie 4.0 transforme les modèles de production. L'intégration de l'IoT, de la maintenance prédictive et des jumeaux numériques devient un avantage concurrentiel majeur.",
                    "Le World Economic Forum classe les usines ayant adopté l'Industrie 4.0 comme 'Phares' de la fabrication mondiale. Ces usines atteignent 30% de gain de productivité et 25% de réduction des coûts."
            );
            default -> new RecommendationResponse(
                    "METIER", "MOYENNE",
                    "Benchmarker les leaders digitaux du secteur " + formatSector(sector),
                    "Une analyse comparative des pratiques digitales des leaders de votre secteur permettra d'identifier les axes d'amélioration prioritaires et les meilleures pratiques à adopter.",
                    "Le Digital Transformation Index (Dell Technologies) fournit annuellement un benchmark sectoriel permettant aux entreprises de se positionner par rapport à leurs pairs et d'identifier les leviers d'action."
            );
        };
    }

    private RecommendationResponse buildCountrySIRec(String country, double score) {
        return switch (country.toUpperCase()) {
            case "MA", "MAROC" -> new RecommendationResponse(
                    "SI", score < 50 ? "HAUTE" : "BASSE",
                    "Aligner le SI avec la stratégie Maroc Digital 2030",
                    "La stratégie nationale Maroc Digital 2030 offre des opportunités de financement et d'accompagnement pour la modernisation du SI. Un alignement stratégique est recommandé.",
                    "Le programme Maroc Digital 2030 prévoit 11 milliards MAD d'investissement dans la transformation numérique. Les entreprises alignées avec cette stratégie bénéficient d'un accès privilégié aux financements publics."
            );
            case "TN", "TUNISIE" -> new RecommendationResponse(
                    "SI", score < 50 ? "HAUTE" : "BASSE",
                    "Exploiter les opportunités de la Stratégie Digitale Tunisie 2025",
                    "La Tunisie développe activement son écosystème numérique. Les entreprises qui s'alignent avec les initiatives nationales bénéficient de conditions préférentielles.",
                    "Le plan Tunisie Digitale 2025 vise à doubler la contribution du secteur numérique au PIB. Les entreprises certifiées ISO 27001 ont un accès facilité aux marchés publics numériques."
            );
            case "FR", "FRANCE" -> new RecommendationResponse(
                    "SI", score < 50 ? "HAUTE" : "BASSE",
                    "Assurer la conformité RGPD et renforcer la souveraineté des données",
                    "En France, la conformité RGPD et la souveraineté des données sont des enjeux réglementaires et de confiance client majeurs. Un audit complet du SI sous cet angle est recommandé.",
                    "La CNIL et l'ANSSI publient des guides de conformité RGPD et de sécurisation des SI. Les entreprises non conformes s'exposent à des amendes pouvant atteindre 4% du chiffre d'affaires mondial."
            );
            default -> new RecommendationResponse(
                    "SI", score < 50 ? "HAUTE" : "BASSE",
                    "Assurer la conformité réglementaire locale du SI",
                    "Le cadre réglementaire local impose des exigences spécifiques en matière de données, de sécurité et d'interopérabilité. Un audit de conformité du SI est recommandé.",
                    "Les standards ISO 27001 (sécurité), ISO 27701 (données personnelles) et COBIT (gouvernance IT) fournissent un cadre de référence universel applicable dans tous les contextes réglementaires."
            );
        };
    }

    private String formatSector(String sector) {
        if (sector == null) return "votre secteur";
        return sector.toLowerCase();
    }

    private String formatCountry(String country) {
        if (country == null) return "votre pays";
        return country;
    }
}
