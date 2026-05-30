package com.iabenchmark.service;

import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.MaturityLevel;
import com.iabenchmark.repository.EvaluationRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Service
public class RecommendationService {

    private final EvaluationRepository evaluationRepository;

    public RecommendationService(EvaluationRepository evaluationRepository) {
        this.evaluationRepository = evaluationRepository;
    }

    public List<RecommendationResponse> generateRecommendations(Long evaluationId) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(evaluationId))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        String sector = evaluation.getCompany().getSector();
        String country = evaluation.getCompany().getCountry();
        double businessScore = evaluation.getBusinessScore();
        double processScore = evaluation.getProcessScore();
        double siScore = evaluation.getInformationSystemScore();
        double canauxScore = evaluation.getCanauxDistributionScore();
        double marketingScore = evaluation.getMarketingCommunicationScore();
        double rhScore = evaluation.getRhCultureDigitaleScore();
        double offresScore = evaluation.getOffresDigitalesScore();
        double modeleOperationnelScore = evaluation.getModeleOperationnelScore();
        double itDataScore = evaluation.getItDataScore();
        MaturityLevel maturity = evaluation.getMaturityLevel();

        List<RecommendationResponse> recommendations = new ArrayList<>();

        recommendations.addAll(generateMetierRecommendations(businessScore, sector, country, maturity));
        recommendations.addAll(generateProcessusRecommendations(processScore, sector, country, maturity));
        recommendations.addAll(generateSIRecommendations(siScore, sector, country, maturity));
        if (canauxScore > 0) recommendations.addAll(generateCanauxRecommendations(canauxScore, sector, maturity));
        if (marketingScore > 0) recommendations.addAll(generateMarketingRecommendations(marketingScore, sector, maturity));
        if (rhScore > 0) recommendations.addAll(generateRhRecommendations(rhScore, maturity));
        if (offresScore > 0) recommendations.addAll(generateOffresRecommendations(offresScore, sector, maturity));
        if (modeleOperationnelScore > 0) recommendations.addAll(generateModeleOperationnelRecommendations(modeleOperationnelScore, maturity));
        if (itDataScore > 0) recommendations.addAll(generateItDataRecommendations(itDataScore, sector, maturity));

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

    private List<RecommendationResponse> generateCanauxRecommendations(
            double score, String sector, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "CANAUX_DISTRIBUTION", "HAUTE",
                    "Lancer une application mobile et activer le SMS/USSD Banking",
                    "L'entreprise n'offre pas encore de canaux digitaux de distribution. Le mobile est le canal prioritaire pour toucher la clientèle dans le contexte africain.",
                    "Selon le rapport GSMA State of Mobile Money 2024, plus de 60% des transactions financières en Afrique de l'Ouest passent désormais par le mobile. L'absence de canal mobile représente une perte de compétitivité majeure."
            ));
            recs.add(new RecommendationResponse(
                    "CANAUX_DISTRIBUTION", "HAUTE",
                    "Digitaliser le parcours d'ouverture de compte (e-KYC)",
                    "Le processus d'onboarding client est entièrement manuel, ce qui limite la croissance et augmente les coûts d'acquisition client.",
                    "Les solutions e-KYC adaptées au contexte africain (Smile ID, Onfido) permettent de réduire le délai d'ouverture de compte de plusieurs jours à moins de 24h, avec un taux d'abandon du parcours réduit de 40%."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "CANAUX_DISTRIBUTION", "MOYENNE",
                    "Déployer un réseau d'agents bancaires (Agency Banking)",
                    "Les canaux digitaux existent mais la couverture géographique reste insuffisante, notamment en zones rurales et périurbaines.",
                    "D'après la BCEAO, le réseau d'agents bancaires est le levier le plus efficace pour étendre la bancarisation en zones non couvertes. Les banques leaders de l'UEMOA ont multiplié leur base clients de 3x grâce à l'agency banking."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "CANAUX_DISTRIBUTION", "MOYENNE",
                    "Assurer une expérience client omnicanale sans rupture",
                    "Les canaux digitaux sont actifs mais ne communiquent pas entre eux. Un client qui commence une opération sur mobile doit pouvoir la finaliser en agence sans ressaisie.",
                    "McKinsey Digital Banking Transformation 2024 indique que les banques offrant une expérience omnicanale cohérente atteignent un NPS supérieur de 25 points et un taux de rétention client plus élevé de 18%."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "CANAUX_DISTRIBUTION", "BASSE",
                    "Intégrer les super-apps et les APIs partenaires pour étendre la portée",
                    "L'excellence multicanale atteinte permet d'exposer les services bancaires dans des super-apps tierces et de proposer une expérience Banking-as-a-Service.",
                    "Les banques leaders en Afrique de l'Ouest intègrent leurs services dans des plateformes comme Wave, Orange Money ou des super-apps locales pour atteindre les clients là où ils se trouvent déjà."
            ));
        }
        return recs;
    }

    private List<RecommendationResponse> generateMarketingRecommendations(
            double score, String sector, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "MARKETING_COMMUNICATION", "HAUTE",
                    "Établir une présence digitale active sur les réseaux sociaux",
                    "L'entreprise n'a pas encore de stratégie de communication digitale structurée, ce qui limite sa visibilité et sa capacité à acquérir de nouveaux clients en ligne.",
                    "HubSpot State of Marketing 2024 montre que les entreprises avec une présence active sur les réseaux sociaux génèrent 3x plus de leads qualifiés que celles qui s'appuient uniquement sur les canaux traditionnels."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "MARKETING_COMMUNICATION", "MOYENNE",
                    "Déployer une stratégie de marketing digital avec mesure du ROI",
                    "Les actions de communication digitale sont ponctuelles et leur impact n'est pas mesuré. Une approche structurée avec des KPI clairs est nécessaire.",
                    "Google et Meta recommandent une approche test & learn avec des budgets publicitaires trackés par canal. Les entreprises qui mesurent précisément leur ROI digital optimisent leur budget marketing de 30% en moyenne."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "MARKETING_COMMUNICATION", "MOYENNE",
                    "Personnaliser la communication par la segmentation data",
                    "Le marketing digital est actif mais générique. La personnalisation des messages selon le profil et le comportement client est la prochaine étape de maturité.",
                    "Accenture Personalization Report 2024 indique que 91% des consommateurs sont plus susceptibles d'acheter auprès de marques qui reconnaissent leurs préférences. La personnalisation augmente le taux de conversion de 5 à 8x."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "MARKETING_COMMUNICATION", "BASSE",
                    "Activer le marketing prédictif par l'IA pour l'hyperpersonnalisation",
                    "L'excellence marketing atteinte permet de passer à l'hyperpersonnalisation par l'IA, avec des offres générées en temps réel selon le contexte client.",
                    "McKinsey Next in Personalization 2024 estime que les leaders de la personnalisation génèrent 40% de revenus supplémentaires par rapport à leurs pairs. L'IA prédictive est le levier différenciant du niveau OPTIMISÉ."
            ));
        }
        return recs;
    }

    private List<RecommendationResponse> generateRhRecommendations(
            double score, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "RH_CULTURE_DIGITALE", "HAUTE",
                    "Lancer un programme de sensibilisation et de formation digitale",
                    "Les compétences digitales des collaborateurs sont insuffisantes pour soutenir la transformation. Un programme structuré de montée en compétences est indispensable.",
                    "McKinsey Global Institute (2023) estime que 375 millions de travailleurs devront changer de métier ou acquérir de nouvelles compétences d'ici 2030. Les entreprises qui investissent tôt dans le reskilling réduisent leur coût de recrutement de 50%."
            ));
            recs.add(new RecommendationResponse(
                    "RH_CULTURE_DIGITALE", "HAUTE",
                    "Digitaliser les processus RH (SIRH, fiches de paie, recrutement)",
                    "Les processus RH sont encore manuels et papier, ce qui génère des erreurs, des délais et une mauvaise expérience collaborateur.",
                    "Gartner HR Technology 2024 indique que la digitalisation des processus RH réduit le temps consacré aux tâches administratives de 40% et améliore la satisfaction des collaborateurs de 22%."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "RH_CULTURE_DIGITALE", "MOYENNE",
                    "Créer un référentiel de compétences digitales et certifier les équipes",
                    "Les formations digitales existent mais ne sont pas structurées autour d'un référentiel clair. Les collaborateurs manquent de visibilité sur les compétences attendues.",
                    "LinkedIn Workplace Learning Report 2024 montre que les entreprises dotées d'un référentiel de compétences clairement défini ont un taux de rétention des talents 30% plus élevé que la moyenne du secteur."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "RH_CULTURE_DIGITALE", "MOYENNE",
                    "Instaurer une culture agile et des rituels d'innovation",
                    "La culture digitale est en développement mais les pratiques agiles et l'innovation ne sont pas encore ancrées dans le quotidien des équipes.",
                    "Le rapport Deloitte Human Capital Trends 2024 indique que les organisations qui pratiquent l'innovation collaborative (hackathons, design sprints) développent de nouveaux produits 60% plus vite que leurs concurrents."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "RH_CULTURE_DIGITALE", "BASSE",
                    "Devenir un employeur de référence pour les talents digitaux",
                    "L'excellence RH digitale atteinte permet d'attirer les meilleurs profils technologiques en développant une marque employeur différenciante.",
                    "Korn Ferry Future of Work 2024 estime que la pénurie mondiale de talents technologiques atteindra 85 millions de personnes d'ici 2030. Les entreprises qui investissent dans leur marque employeur digitale aujourd'hui sécurisent leurs capacités de transformation futures."
            ));
        }
        return recs;
    }

    private List<RecommendationResponse> generateOffresRecommendations(
            double score, String sector, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "OFFRES_DIGITALES", "HAUTE",
                    "Digitaliser les produits et services existants",
                    "Les produits et services sont uniquement disponibles via des canaux physiques. La digitalisation de l'offre est un prérequis pour rester compétitif.",
                    "Hsys Digital Benchmark 2026 montre que les entreprises de la zone UEMOA dont moins de 20% des souscriptions se font en ligne perdent en moyenne 15% de parts de marché par an au profit d'acteurs nativement digitaux."
            ));
            recs.add(new RecommendationResponse(
                    "OFFRES_DIGITALES", "HAUTE",
                    "Lancer des produits nativement digitaux (mobile money, micro-crédit digital)",
                    "Le marché attend des offres digitales accessibles, rapides et sans contrainte de déplacement. Le mobile money et le micro-crédit digital sont les segments à fort potentiel dans le contexte UEMOA.",
                    "GSMA State of Mobile Money Africa 2024 indique que le volume de transactions mobile money en Afrique de l'Ouest a dépassé 500 milliards USD en 2023. Les acteurs sans offre mobile money risquent une désintermédiation rapide."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "OFFRES_DIGITALES", "MOYENNE",
                    "Développer des partenariats Open Banking et exposer des APIs",
                    "L'offre digitale existe mais reste fermée. L'ouverture via des APIs partenaires permettrait d'intégrer les services dans des écosystèmes tiers et de multiplier les points de contact client.",
                    "McKinsey Open Banking Maturity Report 2024 indique que les banques ayant exposé des APIs partenaires génèrent en moyenne 20% de revenus supplémentaires grâce aux commissions de l'écosystème dans les 3 ans suivant l'ouverture."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "OFFRES_DIGITALES", "MOYENNE",
                    "Construire un écosystème de services financiers intégrés",
                    "Le catalogue digital est mature. L'étape suivante est d'intégrer des services non-financiers (assurance, commerce, santé) pour devenir une super-app de référence.",
                    "WEF Digital Finance 2024 montre que les super-apps financières asiatiques (WeChat Pay, Grab Financial) ont multiplié par 5 leur valeur client en intégrant des services non-financiers. Ce modèle est en cours de déploiement en Afrique (M-Pesa, Wave)."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "OFFRES_DIGITALES", "BASSE",
                    "Exporter les solutions digitales dans d'autres marchés CEDEAO",
                    "L'excellence en offres digitales locales ouvre des opportunités d'expansion régionale. Les solutions éprouvées localement peuvent être déployées dans d'autres pays de la CEDEAO.",
                    "Gartner Digital Business Models 2024 et McKinsey Africa Banking Report indiquent que les banques panafricaines leaders valorisent leur expertise digitale comme actif exportable, générant des revenus récurrents via des licences de plateforme dans d'autres marchés."
            ));
        }
        return recs;
    }

    private List<RecommendationResponse> generateModeleOperationnelRecommendations(
            double score, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "HAUTE",
                    "Identifier et automatiser les processus à fort potentiel (RPA / IA)",
                    "Les processus internes sont encore largement manuels. Une démarche de cartographie puis d'automatisation par vagues priorisées (quick wins d'abord) est indispensable pour réduire les coûts et les délais.",
                    "Forrester Research estime que la RPA et l'hyperautomatisation réduisent de 25 à 50% les coûts opérationnels sur les processus ciblés. Les banques leaders ont automatisé plus de 40% de leurs tâches back-office d'ici 2025."
            ));
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "HAUTE",
                    "Mettre en place une gouvernance formelle de la transformation digitale",
                    "L'absence de gouvernance claire freine la prise de décision et la cohérence des initiatives digitales. Un comité de pilotage dédié avec des KPI de transformation est nécessaire.",
                    "McKinsey Digital Transformation Survey 2024 indique que 70% des transformations échouent faute de gouvernance. Les programmes gouvernés par un Chief Digital Officer (CDO) avec mandat clair ont 2,5x plus de chances de succès."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "MOYENNE",
                    "Structurer un programme d'hyperautomatisation (RPA + IA + BPM)",
                    "Des automatisations ponctuelles existent mais ne sont pas coordonnées. Un programme d'hyperautomatisation unifié permettrait de maximiser l'impact et d'assurer la cohérence.",
                    "Gartner Hyperautomation Forecast 2024 prévoit que les organisations qui adoptent l'hyperautomatisation réduisent leurs coûts opérationnels de 30% d'ici 2026 et améliorent la qualité de service de 40%."
            ));
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "MOYENNE",
                    "Développer un cadre d'innovation structuré (labs, incubateurs, partenariats startups)",
                    "L'innovation reste sporadique et peu formalisée. Un cadre d'innovation avec des processus clairs (idéation, prototypage, mise à l'échelle) est nécessaire pour soutenir la croissance.",
                    "Deloitte Innovation Benchmark 2024 montre que les entreprises dotées d'un lab d'innovation lancent des produits 40% plus vite et atteignent 2x plus souvent leurs objectifs de croissance digitale."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "MOYENNE",
                    "Accélérer l'innovation ouverte et les partenariats avec l'écosystème fintech",
                    "La maturité opérationnelle atteinte permet d'ouvrir l'innovation à des partenaires extérieurs. Les collaborations avec des fintechs et startups accélèrent le cycle d'innovation.",
                    "Accenture Fintech Partnership Report 2024 indique que les banques ayant une stratégie de partenariat fintech structurée lancent 3x plus de nouveaux services par an et réduisent leur time-to-market de 60%."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "MODELE_OPERATIONNEL", "BASSE",
                    "Valoriser le modèle opérationnel comme actif exportable",
                    "L'excellence opérationnelle atteinte constitue un avantage compétitif exportable. Le partage des pratiques et la licence du modèle à d'autres entités peuvent générer de nouvelles sources de revenus.",
                    "BCG Operations Excellence 2024 montre que les leaders opérationnels mondiaux valorisent leur savoir-faire via des plateformes de services partagés et des accords de franchise opérationnelle, générant 15 à 20% de revenus additionnels."
            ));
        }
        return recs;
    }

    private List<RecommendationResponse> generateItDataRecommendations(
            double score, String sector, MaturityLevel maturity) {

        List<RecommendationResponse> recs = new ArrayList<>();

        if (score < 40) {
            recs.add(new RecommendationResponse(
                    "IT_DATA", "HAUTE",
                    "Moderniser le socle IT : migration cloud et décommissionnement du legacy",
                    "L'infrastructure IT repose sur des systèmes anciens (legacy) qui limitent l'agilité, augmentent les coûts de maintenance et fragilisent la sécurité. Une migration progressive vers le cloud est prioritaire.",
                    "IDC Infrastructure 2024 estime que le maintien de systèmes legacy coûte en moyenne 60% du budget IT total. Une migration cloud réduit ces coûts de 30 à 40% tout en améliorant la résilience et la scalabilité."
            ));
            recs.add(new RecommendationResponse(
                    "IT_DATA", "HAUTE",
                    "Mettre en place les fondations d'une stratégie data (collecte, qualité, gouvernance)",
                    "Les données sont éparpillées dans de multiples silos, non gouvernées et de qualité insuffisante pour alimenter des analyses fiables ou des modèles IA.",
                    "DAMA International estime que la mauvaise qualité des données coûte en moyenne 12,9 millions USD par an aux grandes organisations. Une Data Strategy avec gouvernance formelle est le prérequis de toute initiative data-driven."
            ));
        } else if (score < 60) {
            recs.add(new RecommendationResponse(
                    "IT_DATA", "MOYENNE",
                    "Déployer une plateforme cloud hybride et renforcer la cybersécurité",
                    "Le socle IT est partiellement modernisé mais l'architecture cloud hybride n'est pas encore optimisée. La sécurité des environnements cloud mérite une attention particulière.",
                    "NIST Cybersecurity Framework et CIS Controls recommandent une approche Zero Trust pour sécuriser les architectures hybrides. Les organisations certifiées ISO 27001 en cloud réduisent leur risque de breach de 55%."
            ));
            recs.add(new RecommendationResponse(
                    "IT_DATA", "MOYENNE",
                    "Construire un Data Warehouse / Data Lake pour centraliser les données",
                    "Les données sont partiellement consolidées mais sans plateforme unifiée. Un Data Warehouse ou Data Lakehouse centralisé est nécessaire pour activer des analyses avancées.",
                    "Snowflake Data Cloud Survey 2024 montre que les organisations dotées d'une plateforme data centralisée réduisent leurs délais d'analyse de 70% et multiplient par 3 leurs capacités de reporting en temps réel."
            ));
        } else if (score < 80) {
            recs.add(new RecommendationResponse(
                    "IT_DATA", "MOYENNE",
                    "Activer la data science et les premiers cas d'usage IA métier",
                    "L'infrastructure data est mature. L'étape suivante est de déployer des modèles de machine learning sur des cas d'usage à fort impact (scoring crédit, détection fraude, personnalisation).",
                    "McKinsey State of AI 2024 indique que les entreprises du secteur " + formatSector(sector) + " qui déploient l'IA sur au moins 3 cas d'usage métier constatent une amélioration de 15 à 25% de leurs indicateurs clés de performance."
            ));
        } else {
            recs.add(new RecommendationResponse(
                    "IT_DATA", "BASSE",
                    "Déployer une stratégie d'IA à l'échelle (AI at Scale) et valoriser les données",
                    "L'excellence IT & Data atteinte permet de passer à l'IA généralisée : modèles en production, DataOps, et monétisation des données via des APIs ou des produits data.",
                    "WEF Data Economy 2024 estime que les organisations qui monétisent leurs données (produits data, APIs, partenariats data) génèrent 2 à 5x plus de valeur par donnée collectée que celles qui les utilisent uniquement en interne."
            ));
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
