"""
Country-specific knowledge context for non-UEMOA markets.

Provides legal framework (cadre_juridique), national leaders,
zoom case studies and static analysis for each supported country.
Merged into the sub-axis KB in benchmarking_engine.py, overriding
CIMA/UEMOA-centric defaults when the evaluated company is not in UEMOA.

Supported countries: Maroc, Tunisie, Algérie, France, Allemagne
Fallback: generic UEMOA context (existing behaviour).
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# MAROC
# ─────────────────────────────────────────────────────────────────────────────

_MAROC = {

    "cadre_juridique": {
        "banking": [
            {
                "texte": "Loi bancaire n°103-12 (Bank Al-Maghrib)",
                "description": "Bank Al-Maghrib régule l'ensemble des établissements de crédit. La loi 103-12 encadre les activités bancaires, le financement participatif et les exigences de fonds propres Bâle III. Toute transformation digitale touchant aux dépôts, crédits ou paiements est soumise à agrément.",
                "impact": "Obligation"
            },
            {
                "texte": "Stratégie Maroc Digital 2030",
                "description": "Feuille de route nationale pour la transformation numérique de l'économie marocaine : e-gouvernement, économie numérique, compétences digitales et infrastructures haut débit. Les entreprises financières bénéficient d'exonérations fiscales pour les investissements en R&D digital.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°09-08 relative à la protection des données personnelles (CNDP)",
                "description": "La Commission Nationale de contrôle de la Protection des Données à caractère Personnel (CNDP) encadre la collecte, le traitement et la conservation des données clients. Toute application mobile bancaire collectant des données biométriques doit obtenir une autorisation préalable de la CNDP.",
                "impact": "Obligation"
            },
            {
                "texte": "Circulaires Bank Al-Maghrib — Paiements digitaux",
                "description": "Les circulaires BAM 2022-2024 encadrent les paiements mobiles, le m-banking et les wallets numériques. Elles imposent des exigences de sécurité (authentification forte, chiffrement) et d'interopérabilité entre opérateurs de paiement.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi n°43-20 relative aux services de confiance pour les transactions électroniques",
                "description": "Reconnaît la valeur juridique des signatures électroniques et des contrats numériques, ouvrant la voie à la souscription 100 % en ligne de produits financiers. Opportunité majeure pour le KYC digital et l'onboarding à distance.",
                "impact": "Opportunité"
            },
        ],
        "insurance": [
            {
                "texte": "Code des assurances (Loi n°17-99) — ACAPS",
                "description": "L'Autorité de Contrôle des Assurances et de la Prévoyance Sociale (ACAPS) supervise le secteur. La loi 17-99 encadre les obligations d'information, les contrats électroniques et les conditions de souscription digitale. Les assureurs doivent obtenir l'approbation de l'ACAPS pour tout nouveau canal digital.",
                "impact": "Obligation"
            },
            {
                "texte": "Circulaire ACAPS n°AS/01/2022 — Distribution digitale",
                "description": "Encadre la distribution des produits d'assurance via les canaux digitaux (sites web, applications mobiles, agrégateurs). Impose des obligations de conseil électronique, de transparence tarifaire et d'archivage des contrats numériques.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi n°09-08 CNDP — Données assurantielles",
                "description": "Réglemente l'utilisation des données de santé et comportementales pour la tarification des risques. Limite l'usage des données issues des objets connectés (IoT, télématique) sans consentement explicite de l'assuré.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°43-20 — Contrats électroniques d'assurance",
                "description": "Valide juridiquement la souscription électronique, la signature numérique des contrats et les notifications par voie électronique. Permet aux assureurs de proposer des offres 100 % digitales sans document papier.",
                "impact": "Opportunité"
            },
        ],
        "education": [
            {
                "texte": "Loi-cadre n°51-17 sur le système d'éducation, de formation et de recherche scientifique",
                "description": "Réforme éducative nationale 2020-2030 : intégre le numérique comme compétence obligatoire, impose des plateformes e-learning dans les établissements publics et encadre la certification des formations digitales.",
                "impact": "Obligation"
            },
            {
                "texte": "Programme GENIE — Généralisation des TIC dans l'Enseignement",
                "description": "Programme national doté de 5 Mds MAD pour équiper les établissements en TIC : labos informatiques, tableaux numériques, connexions haut débit, formation des enseignants et portails pédagogiques (Taalimti, Dawri). 9 000 écoles connectées.",
                "impact": "Opportunité"
            },
            {
                "texte": "Stratégie nationale pour l'enseignement supérieur — Vision 2030",
                "description": "Objectif : porter le taux de scolarisation dans le supérieur à 50 % via la formation à distance, les MOOCs et les partenariats public-privé. Financement BM pour les EdTechs marocaines.",
                "impact": "Opportunité"
            },
        ],
        "healthcare": [
            {
                "texte": "Loi-cadre n°06-22 portant réforme du système de santé",
                "description": "Réforme structurelle : généralisation de l'AMO/RAMED, création des Groupements Sanitaires Territoriaux (GST) et intégration des outils numériques dans les hôpitaux publics.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°131-13 relative à l'exercice de la médecine — Télémédecine",
                "description": "Ouvre la voie à la télémédecine réglementée. Les consultations à distance doivent respecter le secret médical numérique et s'appuyer sur des plateformes homologuées par le Ministère de la Santé.",
                "impact": "Conformité"
            },
            {
                "texte": "Stratégie nationale e-Santé Maroc 2025",
                "description": "Feuille de route pour la numérisation du secteur : dossier médical partagé (DMP), télémédecine, digitalisation des hôpitaux publics. Budget de 2 Mds MAD sur la période 2022-2025.",
                "impact": "Opportunité"
            },
        ],
        "retail": [
            {
                "texte": "Loi n°31-08 édictant les mesures de protection du consommateur",
                "description": "Encadre le e-commerce et la protection des données clients : droit de rétractation de 7 jours pour les achats en ligne, informations précontractuelles obligatoires, mentions légales e-commerce.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan Rawaj Vision 2020 & Plan de développement du commerce intérieur",
                "description": "Programme pour moderniser le commerce marocain : structuration de la grande distribution, digitalisation des PME commerciales et réglementation du e-commerce. Vise à moderniser 50 000 commerces de proximité.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°43-20 — Commerce électronique et transactions numériques",
                "description": "Cadre légal complet pour le e-commerce : contrats électroniques valides, signature numérique, factures électroniques. Obligation pour les plateformes e-commerce de s'enregistrer auprès de l'OMPIC et de la CNDP.",
                "impact": "Opportunité"
            },
        ],
        "industry": [
            {
                "texte": "Plan d'Accélération Industrielle (PAI) & Plan de Relance Industrielle 2021-2023",
                "description": "Programme phare pour la transformation industrielle : création d'écosystèmes industriels intégrés, subventions pour l'automatisation et la digitalisation. Objectif : 500 000 emplois industriels.",
                "impact": "Opportunité"
            },
            {
                "texte": "Zones d'Accélération Industrielle (ZAI) — Loi 12-90",
                "description": "Encadre les parcs industriels et zones franches. Offre des exonérations fiscales de 15 ans pour les exportateurs. Facilite l'implantation de sites industriels connectés (Industry 4.0).",
                "impact": "Opportunité"
            },
            {
                "texte": "Programme Maroc Innovation & Stratégie Industrie 4.0 — ANPME",
                "description": "Encourage l'adoption de technologies Industrie 4.0 : robotisation, IoT industriel, jumeaux numériques, IA de maintenance prédictive. Financement ANPME pour la mise à niveau technologique des PME industrielles.",
                "impact": "Opportunité"
            },
        ],
        "tech": [
            {
                "texte": "Stratégie Maroc Digital 2030 — Hub technologique africain",
                "description": "Objectif 100 000 emplois dans le numérique, 20 licornes à horizon 2030. Subventions et zones offshore (CFC) avec régime fiscal avantageux pour les entreprises IT exportatrices.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°43-20 sur les services de confiance et les transactions électroniques",
                "description": "Cadre légal pour les services cloud, la signature électronique, les certificats numériques. Encadre les prestataires de services de certification électronique (PSCe) agréés par l'ANRT.",
                "impact": "Obligation"
            },
            {
                "texte": "Programme Maroc Offshoring — avantages fiscaux IT",
                "description": "IS réduit à 15 %, exonération TVA sur les prestations export, prime à l'emploi pour les ingénieurs recrutés. Maroc = 1ère destination africaine d'offshoring IT pour la France.",
                "impact": "Opportunité"
            },
        ],
        "transport": [
            {
                "texte": "Loi n°52-05 portant Code de la route & Plan National des Transports 2040",
                "description": "Intègre la digitalisation : billettique unifiée, tracking temps réel, multimodalité et MaaS (Mobility as a Service). Encadre les agréments des opérateurs de transport digital.",
                "impact": "Conformité"
            },
            {
                "texte": "Stratégie portuaire nationale Maroc 2030 — ANP",
                "description": "Modernisation des 38 ports : portail PortNet (guichet unique portuaire), EDI, dématérialisation douanière. PortNet = modèle africain de port numérique.",
                "impact": "Opportunité"
            },
            {
                "texte": "Vision Rail 2040 — ONCF",
                "description": "Investissement ferroviaire de 60 Mds MAD : extension LGV, billettique digitale, application mobile. Objectif : 100 M de voyageurs/an et zéro émission carbone d'ici 2040.",
                "impact": "Opportunité"
            },
        ],
        "energy": [
            {
                "texte": "Loi n°13-09 relative aux énergies renouvelables",
                "description": "Cadre réglementaire pour la production et la vente d'énergie renouvelable. Permet aux opérateurs privés de produire et vendre de l'énergie solaire et éolienne. Fondement légal de la stratégie ENR nationale.",
                "impact": "Obligation"
            },
            {
                "texte": "Stratégie énergétique nationale 2030 — 52 % ENR",
                "description": "Objectif : 52 % de la capacité électrique installée via les ENR. Programme MASEN pour le solaire (Noor), éolien et hydraulique. Investissements de 30 Mds USD avec contrats PPA.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°40-09 portant création de l'ONEE & compteurs intelligents",
                "description": "Régule la production, le transport et la distribution de l'électricité. Impose les smart meters pour les gros consommateurs et les contrats d'injection sur réseau pour les producteurs ENR.",
                "impact": "Obligation"
            },
        ],
        "_default": [
            {
                "texte": "Stratégie Maroc Digital 2030",
                "description": "Programme gouvernemental pour la transformation numérique de l'économie : infrastructure haut débit, e-gouvernement, économie numérique et formation aux métiers du digital. Subventions et incitations fiscales pour les entreprises qui investissent dans la digitalisation.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°09-08 — Protection des données personnelles (CNDP)",
                "description": "Encadre la collecte et le traitement des données à caractère personnel. Toute entreprise collectant des données clients via des canaux digitaux doit déclarer ses traitements auprès de la CNDP et respecter les droits d'accès et de rectification.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°43-20 — Services de confiance numériques",
                "description": "Légalise les transactions électroniques, les signatures numériques et les contrats en ligne, facilitant la dématérialisation des processus métier.",
                "impact": "Opportunité"
            },
            {
                "texte": "Plan d'Accélération Industrielle (PAI) 2014-2020 & Plan de Relance Industrielle",
                "description": "Cadre stratégique pour la modernisation industrielle et technologique du Maroc, incluant des incitations pour la R&D, l'innovation et la transformation numérique des PME et grandes entreprises.",
                "impact": "Opportunité"
            },
        ],
    },

    "leaders_nationaux": {
        "banking": [
            {
                "entreprise": "Attijariwafa Bank",
                "pays": "Maroc",
                "pratique": "Leader de la transformation digitale au Maroc : application Attijarinet avec 3 M+ utilisateurs actifs, onboarding 100 % digital en 10 min, paiement via QR code, chatbot IA 'Jibi' disponible 24/7. Présence dans 26 pays africains.",
                "source": "Attijariwafa Bank Rapport Annuel 2023"
            },
            {
                "entreprise": "CIH Bank",
                "pays": "Maroc",
                "pratique": "Pionnier du Banking-as-a-Service au Maroc. Budget digital supérieur à 25 % du total investissement depuis 2019. Partenariats fintechs actifs (CMI, HPS). Application mobile primée meilleure expérience client au Maroc 2023 (IDC).",
                "source": "CIH Bank Rapport Annuel 2023 / IDC MarCom Awards 2023"
            },
        ],
        "insurance": [
            {
                "entreprise": "Wafa Assurance (Groupe Attijariwafa)",
                "pays": "Maroc",
                "pratique": "Transformation digitale complète : souscription en ligne, espace client digital, déclaration sinistre via application mobile avec photos. Partenariat ACAPS pour la distribution digitale. 40 % des sinistres auto déclarés via mobile en 2023.",
                "source": "Wafa Assurance Rapport Annuel 2023"
            },
            {
                "entreprise": "AXA Assurance Maroc",
                "pays": "Maroc",
                "pratique": "Plateforme eSanté pour la gestion des remboursements en ligne. Contrats auto et habitation souscrits 100 % en ligne. Chatbot de gestion des sinistres. NPS +28 après digitalisation du parcours client.",
                "source": "AXA Maroc Rapport 2023"
            },
        ],
        "education": [
            {
                "entreprise": "UM6P — Université Mohammed VI Polytechnique",
                "pays": "Maroc",
                "pratique": "Référence africaine en enseignement supérieur numérique : campus connecté (IoT, 5G), labos IA et data science, plateforme e-learning UM6P Online avec 50 000+ apprenants, partenariats MIT, Google, AWS.",
                "source": "UM6P Rapport Annuel 2023"
            },
            {
                "entreprise": "OFPPT — Office de la Formation Professionnelle",
                "pays": "Maroc",
                "pratique": "Digitalisation de la formation professionnelle : plateforme OFPPT Digital avec 400 000 stagiaires, cours en ligne, certification digitale, partenariats Microsoft, Cisco, Oracle. 600 établissements connectés.",
                "source": "OFPPT Rapport Annuel 2023"
            },
        ],
        "healthcare": [
            {
                "entreprise": "Cliniques Akdital",
                "pays": "Maroc",
                "pratique": "Premier réseau privé au Maroc : 30+ établissements, dossier patient digital partagé, téléconsultation intégrée, IA de radiologie. Application mobile avec prise de RDV en ligne et suivi post-consultation.",
                "source": "Akdital Rapport Annuel 2023"
            },
            {
                "entreprise": "CHU Ibn Rushd — Programme e-Santé",
                "pays": "Maroc",
                "pratique": "Premier CHU à déployer un Dossier Patient Informatisé (DPI) unifié. Téléconsultation spécialisée avec les hôpitaux régionaux, PACS numérique pour la radiologie, prescription électronique.",
                "source": "Ministère de la Santé Maroc 2023"
            },
        ],
        "retail": [
            {
                "entreprise": "Marjane Holding",
                "pays": "Maroc",
                "pratique": "Leader de la grande distribution : application Marjane Market avec livraison en 2h, click-and-collect, programme de fidélité digital (Nour), supply chain prédictive. 50 M de clients/an.",
                "source": "Marjane Rapport Annuel 2023"
            },
            {
                "entreprise": "Jumia Maroc",
                "pays": "Maroc",
                "pratique": "Plateforme e-commerce leader avec 1 M+ clients actifs. Marketplace multi-vendeurs, paiement mobile (Jumia Pay), logistique last-mile dans 30 villes. Croissance GMV 45 % en 2023.",
                "source": "Jumia Rapport Annuel 2023"
            },
        ],
        "industry": [
            {
                "entreprise": "OCP Group",
                "pays": "Maroc",
                "pratique": "Digital Factory interne avec 500+ développeurs. Jumeaux numériques des mines et usines. Data platform centralisée avec IA prédictive pour la maintenance. Benchmark africain Industrie 4.0.",
                "source": "OCP Annual Report 2023 / MIT Africa Innovation Summit 2023"
            },
            {
                "entreprise": "Renault Maroc — Usine Melloussa",
                "pays": "Maroc",
                "pratique": "Usine label WEF Lighthouse (2022) : 1 000 robots, MES temps réel, jumeaux numériques de la ligne d'assemblage, maintenance prédictive IA. 400 000 véhicules/an avec zéro défaut qualité.",
                "source": "Renault Groupe / WEF Lighthouse Network 2022"
            },
        ],
        "tech": [
            {
                "entreprise": "HPS — HighTech Payment Systems",
                "pays": "Maroc",
                "pratique": "Champion national des paiements digitaux : solution PowerCARD utilisée par 100+ banques dans 50 pays. Certifié PCI-DSS, leader africain des logiciels de gestion de cartes. CA 700 M MAD en 2023.",
                "source": "HPS Rapport Annuel 2023"
            },
            {
                "entreprise": "Outsourcia",
                "pays": "Maroc",
                "pratique": "Leader de l'outsourcing digital francophone : BPO, IA, automatisation RPA. 10 000 collaborateurs, présence dans 4 pays. Certifié ISO 27001, partenaire stratégique de grands groupes européens.",
                "source": "Outsourcia Rapport Annuel 2023"
            },
        ],
        "transport": [
            {
                "entreprise": "ONCF — Office National des Chemins de Fer",
                "pays": "Maroc",
                "pratique": "Transformation digitale complète : application mobile ONCF (billet électronique, suivi train temps réel), billettique sans contact. Al Boraq (LGV Tanger-Casablanca) première LGV africaine. 60 M voyageurs/an.",
                "source": "ONCF Rapport Annuel 2023"
            },
            {
                "entreprise": "Royal Air Maroc",
                "pays": "Maroc",
                "pratique": "Application mobile avec check-in et cartes d'embarquement digitales, IA de pricing dynamique, MRO prédictif. Hub de connectivité Afrique-Europe avec 100+ destinations.",
                "source": "Royal Air Maroc Rapport Annuel 2023"
            },
        ],
        "energy": [
            {
                "entreprise": "MASEN — Moroccan Agency for Sustainable Energy",
                "pays": "Maroc",
                "pratique": "Déploie la plus grande centrale solaire au monde (Noor Ouarzazate, 580 MW). Gestion digitale des parcs ENR avec SCADA connecté, IA de prévision de production, supervision IoT temps réel.",
                "source": "MASEN Rapport Annuel 2023"
            },
            {
                "entreprise": "ONEE — Office National de l'Électricité et de l'Eau Potable",
                "pays": "Maroc",
                "pratique": "Déploiement de 2 M de smart meters, plateforme AMR de télé-relève, espace client digital, détection des pertes techniques par IA. Objectif zéro fraude énergétique 2025.",
                "source": "ONEE Rapport Annuel 2023"
            },
        ],
        "_default": [
            {
                "entreprise": "Maroc Telecom (IAM)",
                "pays": "Maroc",
                "pratique": "Transformation digitale exemplaire : plateforme omnicanale, espace client digital avec IA, IoT pour les entreprises, déploiement 5G en cours. Investissement de 8 Mds MAD dans les infrastructures numériques 2022-2024.",
                "source": "Maroc Telecom Rapport Annuel 2023"
            },
            {
                "entreprise": "OCP Group",
                "pays": "Maroc",
                "pratique": "Digital Factory interne avec 500+ développeurs. Jumeaux numériques des mines et usines. Data platform centralisée avec IA prédictive pour la maintenance. Modèle de transformation reconnu comme benchmark africain.",
                "source": "OCP Annual Report 2023 / MIT Africa Innovation Summit 2023"
            },
        ],
    },

    "zoom_case_study": {
        "_default": {
            "entreprise": "CIH Bank — Onboarding 100 % digital",
            "pays": "Maroc",
            "technologie": "OCR + IA biométrique + signature électronique certifiée",
            "description": "CIH Bank a lancé en 2022 un parcours d'ouverture de compte 100 % en ligne en moins de 10 minutes : scan de la CIN par OCR, reconnaissance faciale par IA, signature électronique via la loi 43-20. Aucun déplacement en agence requis. Résultat : 35 % des nouveaux comptes ouverts en digital en 2023, coût d'acquisition réduit de 60 % vs canal agence, satisfaction client 4,7/5.",
            "resultats": "35 % nouveaux comptes via digital · Coût acquisition -60 % · NPS +31 · 10 min pour ouvrir un compte",
            "source": "CIH Bank Rapport Annuel 2023 / CGEM Digital Awards Maroc 2023",
            "annee": "2023"
        },
    },

    "analyse_statique": "Le Maroc est le pays africain le plus avancé en matière de transformation digitale après l'Afrique du Sud, selon l'indice IDI de l'UIT 2023. La Stratégie Maroc Digital 2030 mobilise 10 Mds MAD d'investissements publics sur la période. Le secteur financier est le plus digitalisé : les banques marocaines (Attijariwafa, CIH, BMCE) ont investi massivement depuis 2018 et rivalisent avec les standards européens en matière d'expérience client digitale. La Loi 43-20 sur les services de confiance numériques constitue un accélérateur réglementaire majeur. Le principal défi reste la fracture digitale entre les zones urbaines (très bien connectées) et les zones rurales (40 % de la population).",
}


# ─────────────────────────────────────────────────────────────────────────────
# TUNISIE
# ─────────────────────────────────────────────────────────────────────────────

_TUNISIE = {

    "cadre_juridique": {
        "banking": [
            {
                "texte": "Loi n°2016-48 relative aux banques et aux établissements financiers (BCT)",
                "description": "La Banque Centrale de Tunisie encadre l'ensemble du secteur bancaire. La loi 2016-48 modernise les exigences prudentielles (Bâle III), régule le financement islamique et encadre les établissements de paiement. Tout service bancaire digital doit être déclaré à la BCT.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°2020-38 — Startups Act tunisien",
                "description": "Le Startup Act permet aux fintechs tunisiennes d'accéder à un cadre réglementaire allégé (sandbox BCT), à des avantages fiscaux et à un accès facilité aux marchés étrangers. Constitue une opportunité majeure pour les partenariats banque-fintech.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi organique n°2004-63 — Protection des données personnelles (INPDP)",
                "description": "L'Instance Nationale de Protection des Données Personnelles (INPDP) régule la collecte et le traitement des données clients. Toute base de données clients doit être déclarée. Comparable au RGPD européen pour les obligations de consentement.",
                "impact": "Obligation"
            },
            {
                "texte": "Circulaires BCT sur les paiements mobiles et le m-banking",
                "description": "La BCT a émis plusieurs circulaires (2019-2023) pour encadrer les paiements instantanés, les portefeuilles électroniques et l'interopérabilité des systèmes. Le système de paiement instantané SIBTEL facilite les virements 24/7.",
                "impact": "Conformité"
            },
        ],
        "insurance": [
            {
                "texte": "Code des assurances tunisien — CGA (Comité Général des Assurances)",
                "description": "Le CGA supervise les compagnies d'assurance. Le code encadre les produits, la solvabilité et la distribution. La distribution digitale est autorisée sous conditions d'agrément spécifique.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°2020-38 Startup Act — InsurTech",
                "description": "Permet aux startups InsurTech d'opérer dans un cadre sandbox avec des obligations allégées pendant 3 ans, facilitant l'innovation dans les produits d'assurance paramétriques et l'assurance à la demande.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi organique n°2004-63 — Données assurantielles (INPDP)",
                "description": "Encadre l'utilisation des données de santé et comportementales pour la tarification. Les assureurs utilisant des objets connectés ou la télématique doivent obtenir une autorisation spéciale de l'INPDP.",
                "impact": "Obligation"
            },
        ],
        "education": [
            {
                "texte": "Loi d'orientation de l'éducation et de l'enseignement scolaire n°2002-80",
                "description": "Encadre le système éducatif tunisien et impose l'intégration des TIC dans les cursus. Le Ministère de l'Éducation déploie des classes numériques et une plateforme e-learning nationale (e-khobza) dans les établissements secondaires.",
                "impact": "Obligation"
            },
            {
                "texte": "Startup Act n°2020-38 — EdTech tunisiennes",
                "description": "Permet aux startups EdTech d'accéder au cadre sandbox réglementaire avec avantages fiscaux, facilite les partenariats universités-entreprises et encourage le développement de plateformes de formation en ligne labellisées.",
                "impact": "Opportunité"
            },
            {
                "texte": "Stratégie nationale pour l'enseignement supérieur et la recherche scientifique",
                "description": "Objectif : développer les formations à distance, les certifications numériques et les MOOCs tunisiens. Budget dédié aux infrastructures IT des universités publiques dans le cadre du Plan Quinquennal 2023-2025.",
                "impact": "Opportunité"
            },
        ],
        "healthcare": [
            {
                "texte": "Code de la santé publique tunisien & Loi n°91-63 sur les établissements de santé",
                "description": "Encadre l'organisation du système de santé, les conditions d'ouverture des établissements privés et l'homologation des dispositifs médicaux connectés. La télémédecine est autorisée sous conditions d'agrément depuis 2020.",
                "impact": "Obligation"
            },
            {
                "texte": "CNAM — Caisse Nationale d'Assurance Maladie & Digitalisation",
                "description": "La CNAM digitalise la gestion des remboursements : carte magnétique ATMED pour la facturation directe, portail en ligne pour les affiliés, dématérialisation des ordonnances dans 80 % des pharmacies.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi organique n°2004-63 — Données de santé (INPDP)",
                "description": "Les données médicales sont des données sensibles soumises à autorisation spéciale de l'INPDP. Toute plateforme e-santé collectant des données patients doit obtenir une accréditation préalable.",
                "impact": "Obligation"
            },
        ],
        "retail": [
            {
                "texte": "Loi n°2000-83 relative aux échanges et au commerce électronique",
                "description": "Cadre légal fondateur du e-commerce tunisien : reconnaissance des contrats électroniques, signature numérique et transactions en ligne. Permet la dématérialisation des processus commerciaux.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°92-117 sur la protection du consommateur",
                "description": "Encadre les pratiques commerciales en ligne : obligations d'information, droit de rétractation, interdiction des clauses abusives dans les CGV e-commerce. Renforcée pour le commerce électronique par des circulaires ministérielles.",
                "impact": "Obligation"
            },
        ],
        "industry": [
            {
                "texte": "Loi n°2016-71 portant loi de l'investissement",
                "description": "Nouveau code de l'investissement modernisant les incitations : exonérations fiscales pour les projets industriels innovants, guichet unique d'investissement, facilitation des partenariats public-privé dans les zones de développement régional.",
                "impact": "Opportunité"
            },
            {
                "texte": "Programme Tunisie Industrie — Stratégie nationale de développement industriel",
                "description": "Feuille de route pour la transformation industrielle : montée en gamme technologique, adoption de l'automatisation et de la robotisation, développement des zones industrielles connectées et formation aux métiers de l'industrie du futur.",
                "impact": "Opportunité"
            },
        ],
        "tech": [
            {
                "texte": "Startup Act n°2020-38 — Écosystème tech",
                "description": "Cadre réglementaire unique en Afrique : labellisation startup, avantages fiscaux (exonération IS 3 ans), accès aux marchés étrangers, sandbox réglementaire. 800+ startups labellisées. Attire les investisseurs étrangers dans la tech tunisienne.",
                "impact": "Opportunité"
            },
            {
                "texte": "Stratégie Tunisie Digitale 2025",
                "description": "Feuille de route pour faire de la Tunisie un hub digital régional : e-gouvernement, développement des compétences IA et data, offshoring IT, incubateurs et accélérateurs. Financement BERD et UE pour les projets numériques.",
                "impact": "Opportunité"
            },
        ],
        "transport": [
            {
                "texte": "Code des transports tunisien & Plan de modernisation des transports 2025",
                "description": "Encadre les opérateurs de transport et ouvre la voie à la numérisation des services : billettique unifiée, applications de mobilité, réglementation des VTC (taxis digitaux). Objectif : intégration multimodale des transports publics.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi n°2000-83 — Échanges électroniques appliqués aux transports",
                "description": "Permet la dématérialisation des documents de transport, des contrats de fret et des procédures douanières. Base légale pour les plateformes logistiques digitales et le tracking en temps réel.",
                "impact": "Opportunité"
            },
        ],
        "energy": [
            {
                "texte": "Loi n°2004-72 relative à la maîtrise de l'énergie — ANME",
                "description": "Encadre l'efficacité énergétique, les audits obligatoires pour les gros consommateurs et les obligations de reporting. L'ANME (Agence Nationale pour la Maîtrise de l'Énergie) supervise la transition énergétique digitale.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan Solaire Tunisien — STEG ENR & Loi n°2015-12",
                "description": "Objectif : 35 % d'énergies renouvelables dans le mix électrique d'ici 2030. Loi autorisant la production privée d'électricité renouvelable. Déploiement de smart grids et de compteurs intelligents via la STEG.",
                "impact": "Opportunité"
            },
        ],
        "_default": [
            {
                "texte": "Stratégie Nationale de l'Économie Numérique — Tunisie Digitale 2025",
                "description": "Feuille de route pour la transformation numérique de l'économie : e-gouvernement, administration digitale, économie numérique. Objectif : faire de la Tunisie un hub digital régional avec 30 % du PIB généré par le numérique à horizon 2025.",
                "impact": "Opportunité"
            },
            {
                "texte": "Startup Act n°2020-38",
                "description": "Cadre réglementaire favorable à l'innovation : labellisation startup, avantages fiscaux, accès aux marchés étrangers, sandbox réglementaire. Plus de 800 startups labellisées depuis 2019.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi organique n°2004-63 — Protection des données (INPDP)",
                "description": "Encadre la collecte, le traitement et la conservation des données personnelles. Obligations de déclaration et de consentement pour tout traitement de données clients.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°2000-83 relative aux échanges et au commerce électronique",
                "description": "Cadre légal pour les transactions électroniques, la signature numérique et les contrats en ligne. Permet la dématérialisation des processus commerciaux.",
                "impact": "Opportunité"
            },
        ],
    },

    "leaders_nationaux": {
        "banking": [
            {
                "entreprise": "Banque de Tunisie (BT)",
                "pays": "Tunisie",
                "pratique": "Transformation digitale avancée : application mobile My BT avec 500 000+ utilisateurs, virement instantané via SIBTEL, onboarding simplifié. Partenariat avec des fintechs locales labellisées Startup Act.",
                "source": "BT Rapport Annuel 2023"
            },
            {
                "entreprise": "Attijari Bank Tunisie",
                "pays": "Tunisie",
                "pratique": "Filiale d'Attijariwafa, déploie les meilleures pratiques du groupe. Application mobile primée, KYC digital, partenariats fintechs. Objectif 50 % des transactions hors agence à horizon 2025.",
                "source": "Attijari Bank Tunisie Rapport 2023"
            },
        ],
        "insurance": [
            {
                "entreprise": "STAR Assurances",
                "pays": "Tunisie",
                "pratique": "Première compagnie d'assurance tunisienne à lancer une souscription 100 % en ligne pour l'auto et l'habitation. Portail client digital avec déclaration sinistre mobile et suivi temps réel. Partenariat COMAR pour les produits santé digitaux.",
                "source": "STAR Assurances Rapport Annuel 2023"
            },
            {
                "entreprise": "GAT Assurances",
                "pays": "Tunisie",
                "pratique": "Transformation digitale accélérée : application mobile GAT pour la gestion des contrats, API d'intégration bancassurance avec les néobanques tunisiennes, scoring IA pour la détection de fraudes. NPS +18 après digitalisation.",
                "source": "GAT Assurances Rapport 2023"
            },
        ],
        "education": [
            {
                "entreprise": "ESPRIT — École Supérieure Privée d'Ingénierie et de Technologies",
                "pays": "Tunisie",
                "pratique": "École d'ingénieurs référence en Tunisie : campus connecté, cursus IA/Data/Cybersécurité, plateforme e-learning propriétaire, partenariats Google, Microsoft, IBM. 10 000+ étudiants, 90 % employabilité à la sortie.",
                "source": "ESPRIT Rapport Institutionnel 2023"
            },
            {
                "entreprise": "Université de Tunis El Manar (UTM)",
                "pays": "Tunisie",
                "pratique": "Première université numérique de Tunisie : plateforme Moodle nationale, formation à distance, recherche en IA avec le CRISTAL Lab, partenariats industriels avec Telnet, Vermeg et fintechs locales.",
                "source": "UTM Rapport Annuel 2023"
            },
        ],
        "healthcare": [
            {
                "entreprise": "Institut Pasteur de Tunis",
                "pays": "Tunisie",
                "pratique": "Centre de recherche biomédicale régional : plateforme de séquençage génomique, bioinformatique, télédiagnostic pour les laboratoires partenaires d'Afrique subsaharienne. Modèle de santé numérique scientifique africain.",
                "source": "Institut Pasteur de Tunis Rapport 2023"
            },
            {
                "entreprise": "Cliniques Tawasol Health",
                "pays": "Tunisie",
                "pratique": "Réseau de cliniques privées avec DPI (Dossier Patient Informatisé) centralisé, application mobile pour les RDV et résultats d'analyses, téléconsultation spécialisée inter-établissements. 15 cliniques connectées.",
                "source": "Tawasol Health 2023"
            },
        ],
        "retail": [
            {
                "entreprise": "Mytek",
                "pays": "Tunisie",
                "pratique": "Leader du e-commerce high-tech en Tunisie : plateforme omnicanale, 500 000+ références, livraison J+1, paiement en ligne sécurisé, programme fidélité digital. CA e-commerce en croissance de 60 % en 2023.",
                "source": "Mytek Rapport 2023"
            },
            {
                "entreprise": "Jumia Tunisie",
                "pays": "Tunisie",
                "pratique": "Marketplace multi-catégories leader : 300 000+ clients actifs, Jumia Pay intégré, partenariats commerçants locaux, logistique last-mile dans les grandes villes. Modèle de marketplace africaine adapté au marché tunisien.",
                "source": "Jumia Group Annual Report 2023"
            },
        ],
        "industry": [
            {
                "entreprise": "Poulina Group Holding",
                "pays": "Tunisie",
                "pratique": "Conglomérat industriel leader : digitalisation des usines agroalimentaires avec MES et ERP SAP, IoT industriel pour le suivi de production, réduction des pertes de 30 % grâce à l'automatisation. 10 000 employés, modèle de transformation industrielle tunisien.",
                "source": "Poulina Group Rapport Annuel 2023"
            },
            {
                "entreprise": "Leoni Tunisia (filiale du groupe allemand Leoni)",
                "pays": "Tunisie",
                "pratique": "Usine câblage automobile 4.0 : 10 000 employés, robots collaboratifs, AGV (véhicules autoguidés), MES temps réel, digital twin partiel. Certifiée ISO/TS 16949. Export vers Volkswagen, BMW, Mercedes.",
                "source": "Leoni AG Annual Report 2023"
            },
        ],
        "tech": [
            {
                "entreprise": "Instadeep (acquis par BioNTech — 2023)",
                "pays": "Tunisie",
                "pratique": "Startup IA tunisienne valorisée 680 M USD, acquise par BioNTech en 2023. Développe des solutions IA décisionnelles pour la pharma, la logistique et la finance. 300 ingénieurs IA, présence dans 10 pays. Fierté de l'écosystème Startup Act.",
                "source": "Instadeep / BioNTech Deal 2023"
            },
            {
                "entreprise": "Vermeg",
                "pays": "Tunisie",
                "pratique": "Éditeur de logiciels financiers (post-trading, assurance) utilisés par 200+ institutions dans 40 pays. Basé à Tunis et Londres, CA 100 M USD. Leader mondial des logiciels de gestion de collatéral et de compliance réglementaire.",
                "source": "Vermeg Rapport Annuel 2023"
            },
        ],
        "transport": [
            {
                "entreprise": "Transtu — Société des Transports de Tunis",
                "pays": "Tunisie",
                "pratique": "Modernisation des transports urbains : application mobile de suivi des bus en temps réel, billettique sans contact NFC, partenariat avec des startups MaaS pour l'intégration multimodale. 400 000 voyageurs/jour.",
                "source": "Transtu Rapport Annuel 2023"
            },
            {
                "entreprise": "Tunisair",
                "pays": "Tunisie",
                "pratique": "Application mobile de réservation et check-in, programme de fidélité digital Carthage Plus, partenariat SITA pour la digitalisation des opérations sol. Optimisation des rotations par IA pour réduire les retards de 25 %.",
                "source": "Tunisair Rapport Annuel 2023"
            },
        ],
        "energy": [
            {
                "entreprise": "STEG Énergies Renouvelables",
                "pays": "Tunisie",
                "pratique": "Filiale de la STEG dédiée aux ENR : gestion digitale des parcs solaires et éoliens, SCADA de supervision, IA de prévision de production. 1 GW de capacité ENR gérée avec plateforme de monitoring temps réel.",
                "source": "STEG ER Rapport Annuel 2023"
            },
            {
                "entreprise": "ANME — Agence Nationale pour la Maîtrise de l'Énergie",
                "pays": "Tunisie",
                "pratique": "Déploiement de 500 000 compteurs intelligents (smart meters) dans le cadre du programme PROSOL et PNME. Portail en ligne pour les audits énergétiques obligatoires des entreprises consommant plus de 500 TEP/an.",
                "source": "ANME Rapport Annuel 2023"
            },
        ],
        "_default": [
            {
                "entreprise": "Telnet Holding",
                "pays": "Tunisie",
                "pratique": "Groupe technologique tunisien leader : développement logiciel, IoT, IA appliquée. Exportateur de services IT vers l'Europe et l'Afrique. Modèle de transformation digitale reconnu régionalement.",
                "source": "Telnet Holding Rapport Annuel 2023"
            },
            {
                "entreprise": "IntilaQ (Ooredoo Tunisie — Incubateur)",
                "pays": "Tunisie",
                "pratique": "Accélérateur de startups digitales avec 200+ entrepreneurs accompagnés. Modèle de transformation par l'innovation ouverte combinant grand groupe et écosystème startup.",
                "source": "IntilaQ / Ooredoo Tunisie 2023"
            },
        ],
    },

    "zoom_case_study": {
        "_default": {
            "entreprise": "Tunisie Telecom — Transformation digitale client",
            "pays": "Tunisie",
            "technologie": "CRM cloud unifié + application mobile self-service + IA analytique",
            "description": "Tunisie Telecom a lancé en 2022 une transformation complète de l'expérience client : portail self-service couvrant 80 % des demandes sans intervention humaine, IA prédictive pour anticiper les pannes réseau 48h avant, application mobile avec 1 M+ téléchargements. Le CRM cloud unifie les interactions des 4,5 M de clients sur tous les canaux (agence, web, mobile, call center).",
            "resultats": "80 % demandes traitées en self-service · NPS +22 pts · 1M+ downloads app · Réduction appels call center 35 %",
            "source": "Tunisie Telecom Rapport Annuel 2023 / IDC Tunisia Digital Awards 2023",
            "annee": "2023"
        },
    },

    "analyse_statique": "La Tunisie se distingue en Afrique du Nord par son Startup Act, unique sur le continent, qui a créé un écosystème de 800+ startups technologiques. Le pays dispose de la meilleure infrastructure numérique du Maghreb hors Maroc (taux de pénétration internet 73 %, 4G couvrant 95 % du territoire). Le secteur bancaire est en cours de modernisation accélérée, notamment via le système SIBTEL de paiement instantané. La principale contrainte reste le contexte macroéconomique difficile (dette publique, crise des changes) qui limite les investissements IT des grandes entreprises. L'Instance Nationale de Protection des Données (INPDP) est l'une des plus actives d'Afrique en matière de réglementation du numérique.",
}


# ─────────────────────────────────────────────────────────────────────────────
# ALGÉRIE
# ─────────────────────────────────────────────────────────────────────────────

_ALGERIE = {

    "cadre_juridique": {
        "banking": [
            {
                "texte": "Loi relative à la monnaie et au crédit (Banque d'Algérie)",
                "description": "La Banque d'Algérie régule l'ensemble du système bancaire. Les règlements 20-01 et 21-03 encadrent les paiements électroniques, les cartes bancaires et les établissements de paiement. Toute offre de service bancaire digital doit obtenir un agrément de la Banque d'Algérie.",
                "impact": "Obligation"
            },
            {
                "texte": "Règlement n°20-01 relatif aux paiements par voie électronique",
                "description": "Encadre les paiements en ligne, les portefeuilles électroniques et le m-banking. Impose des exigences de sécurité (authentification à deux facteurs, journalisation) et des plafonds de transactions. Base réglementaire pour les services fintech en Algérie.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi n°18-07 relative à la protection des personnes physiques dans le traitement des données personnelles",
                "description": "Encadre la collecte, le traitement et la conservation des données personnelles des clients algériens. Toute entreprise traitant des données doit les stocker sur des serveurs localisés en Algérie (data sovereignty) — obligation de localisation des données.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°15-04 relative aux activités et marchés des assurances",
                "description": "CNA (Conseil National des Assurances) supervise le secteur. Encadre la distribution des produits d'assurance, y compris via les canaux digitaux émergents.",
                "impact": "Obligation"
            },
        ],
        "insurance": [
            {
                "texte": "Loi n°06-04 portant loi de finances complémentaire — Assurances",
                "description": "Encadre les compagnies d'assurance algériennes sous la supervision du Conseil National des Assurances (CNA). Impose la séparation des activités vie/non-vie et encadre la distribution digitale des produits d'assurance.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°95-07 relative aux assurances & réformes CNA",
                "description": "Cadre réglementaire fondateur du secteur assurantiel algérien : agréments, obligations prudentielles, tarification réglementée. La distribution via canaux digitaux est autorisée sous conditions d'agrément spécifique du Ministère des Finances.",
                "impact": "Obligation"
            },
        ],
        "education": [
            {
                "texte": "Loi n°08-04 portant loi d'orientation sur l'éducation nationale",
                "description": "Encadre le système éducatif algérien et intègre l'outil informatique dans les programmes scolaires. Le plan OUSRATIC (un micro-ordinateur par famille) et les laboratoires informatiques dans les lycées constituent le socle de la digitalisation éducative.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan de numérisation de l'enseignement supérieur — MESRS",
                "description": "Programme du Ministère de l'Enseignement Supérieur pour déployer des plateformes e-learning dans les 100+ universités algériennes. Accéléré post-COVID avec le déploiement de Moodle national et la formation à distance pour 1,7 M d'étudiants.",
                "impact": "Opportunité"
            },
        ],
        "healthcare": [
            {
                "texte": "Loi sanitaire n°85-05 relative à la protection et à la promotion de la santé",
                "description": "Cadre légal fondateur du système de santé algérien. Les amendements récents encadrent la télémédecine, l'utilisation des dispositifs médicaux connectés et la dématérialisation des ordonnances dans les établissements publics.",
                "impact": "Obligation"
            },
            {
                "texte": "Stratégie nationale e-Santé Algérie 2025 — CNAS & Dossier médical électronique",
                "description": "Programme de digitalisation : dossier médical électronique (DME) dans les hôpitaux publics, carte Chifa pour la gestion des remboursements santé (20 M de cartes actives), plateforme de téléconsultation agréée par le Ministère de la Santé.",
                "impact": "Opportunité"
            },
        ],
        "retail": [
            {
                "texte": "Loi n°09-03 relative à la protection du consommateur et à la répression des fraudes",
                "description": "Encadre les pratiques commerciales en ligne, la qualité des produits et les obligations d'information. Réglemente les plateformes e-commerce opérant sur le marché algérien avec des exigences d'enregistrement local.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi n°18-07 — Données personnelles appliquées au retail digital",
                "description": "Impose la localisation des données clients des consommateurs algériens sur des serveurs en Algérie. Contrainte majeure pour les plateformes e-commerce étrangères souhaitant opérer en Algérie.",
                "impact": "Obligation"
            },
        ],
        "industry": [
            {
                "texte": "Code des investissements — Loi n°22-18",
                "description": "Nouveau code encourageant l'investissement industriel : exonérations fiscales pluriannuelles, simplification des procédures, guichet unique AAPI. Priorité aux projets industriels innovants intégrant les technologies 4.0.",
                "impact": "Opportunité"
            },
            {
                "texte": "Plan national de développement industriel — Schéma Directeur Industriel",
                "description": "Feuille de route pour diversifier l'économie hors hydrocarbures : développement de l'industrie agroalimentaire, mécanique, électronique et pharmaceutique. Intègre des objectifs de modernisation et d'automatisation industrielle.",
                "impact": "Opportunité"
            },
        ],
        "tech": [
            {
                "texte": "Stratégie e-Algérie & Programme National de l'Économie Numérique 2025",
                "description": "Feuille de route pour la transition numérique : e-gouvernement, développement des startups tech, offshoring IT, cloud souverain algérien. Fonds National de la Startup avec financements jusqu'à 10 M DZD.",
                "impact": "Opportunité"
            },
            {
                "texte": "Décret 20-254 & Loi n°21-08 relative aux startups",
                "description": "Label 'startup' avec avantages fiscaux, crowdfunding encadré, incubateurs agréés. Vise à développer 1 000 startups technologiques algériennes d'ici 2025. Contrainte : data sovereignty (loi 18-07) limite les solutions cloud étrangères.",
                "impact": "Opportunité"
            },
        ],
        "transport": [
            {
                "texte": "Code des transports algérien & Plan national des infrastructures de transport",
                "description": "Encadre les opérateurs de transport terrestres, maritimes et aériens. Le plan national intègre la digitalisation des gares ferroviaires, des aéroports et la création d'une billettique interopérable nationale.",
                "impact": "Conformité"
            },
            {
                "texte": "Loi n°18-07 — Données de transport et localisation",
                "description": "Les données de tracking, géolocalisation et historiques de déplacement collectées par les opérateurs de transport doivent être stockées sur des serveurs locaux en Algérie. Contrainte pour les solutions de fleet management étrangères.",
                "impact": "Obligation"
            },
        ],
        "energy": [
            {
                "texte": "Loi n°02-01 relative à l'électricité et à la distribution du gaz par canalisations",
                "description": "Encadre la production, le transport et la distribution de l'énergie en Algérie sous la supervision de la CREG (Commission de Régulation de l'Électricité et du Gaz). Ouvre partiellement la production ENR aux opérateurs privés.",
                "impact": "Obligation"
            },
            {
                "texte": "Programme algérien d'énergies renouvelables — 22 GW ENR d'ici 2030",
                "description": "Objectif ambitieux : 22 GW de capacité ENR (solaire et éolien) d'ici 2030. Programme SHEMS (solaire résidentiel), smart grids en déploiement par Sonelgaz. Investissements Sonatrach dans le solaire pour les champs pétroliers.",
                "impact": "Opportunité"
            },
        ],
        "_default": [
            {
                "texte": "Loi n°18-07 — Protection des données personnelles",
                "description": "Impose la localisation des données personnelles des citoyens algériens sur des serveurs basés en Algérie. Contrainte majeure pour les solutions cloud étrangères. Nécessite une architecture locale ou des accords bilatéraux de transfer de données.",
                "impact": "Obligation"
            },
            {
                "texte": "Stratégie e-Algérie et Programme National de l'Économie Numérique",
                "description": "Feuille de route gouvernementale pour la transition numérique : e-gouvernement, administration digitale, développement des startups tech. Le Fonds National de la Startup soutient les jeunes pousses technologiques avec des financements jusqu'à 10 M DZD.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi sur la startup et le dispositif Algeria Startup — Décret 20-254",
                "description": "Crée un label 'startup' pour les jeunes entreprises innovantes avec des avantages fiscaux, une procédure de création simplifiée et un accès à des marchés publics réservés. Vise à développer l'écosystème technologique algérien.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi n°21-08 relative à l'activité des startups",
                "description": "Complète le décret 20-254 : encadre le financement des startups, les business angels, le crowdfunding et les incubateurs. Crée les conditions d'un écosystème d'investissement pour les entreprises technologiques.",
                "impact": "Opportunité"
            },
        ],
    },

    "leaders_nationaux": {
        "banking": [
            {
                "entreprise": "CPA (Crédit Populaire d'Algérie)",
                "pays": "Algérie",
                "pratique": "Première grande banque publique algérienne à déployer une application mobile complète (CPA Mobile) avec consultation de solde, virement, recharge téléphonique. 500 000 utilisateurs en 2023. Partenariat avec SATIM pour les paiements par carte.",
                "source": "CPA Rapport Annuel 2023"
            },
            {
                "entreprise": "BNA (Banque Nationale d'Algérie)",
                "pays": "Algérie",
                "pratique": "Transformation digitale en cours : refonte du système d'information central, déploiement de GAB nouvelle génération, partenariat avec des fintechs pour les paiements mobiles via le Groupement Monétique Interbancaire (GMI).",
                "source": "BNA Rapport Annuel 2023"
            },
        ],
        "insurance": [
            {
                "entreprise": "SAA — Société Algérienne des Assurances",
                "pays": "Algérie",
                "pratique": "Première compagnie d'assurance algérienne : portail en ligne pour la souscription auto et habitation, application mobile pour la consultation des contrats. Déploiement d'un CRM unifié pour la gestion des 3 M de clients.",
                "source": "SAA Rapport Annuel 2023"
            },
            {
                "entreprise": "CAAT — Compagnie Algérienne des Assurances des Transports",
                "pays": "Algérie",
                "pratique": "Transformation digitale en cours : dématérialisation des polices d'assurance transport, plateforme B2B pour les transitaires et importateurs, interface API avec la douane algérienne pour les déclarations automatisées.",
                "source": "CAAT Rapport Annuel 2023"
            },
        ],
        "education": [
            {
                "entreprise": "USTHB — Université des Sciences et de la Technologie Houari Boumediene",
                "pays": "Algérie",
                "pratique": "Principale université scientifique algérienne : laboratoires d'IA, cybersécurité et data science, plateforme e-learning Moodle institutionnelle, partenariats R&D avec Sonatrach et Djezzy. 25 000 étudiants ingénieurs.",
                "source": "USTHB Rapport Institutionnel 2023"
            },
            {
                "entreprise": "ESI — École Nationale Supérieure d'Informatique",
                "pays": "Algérie",
                "pratique": "Grande école informatique algérienne référence : formation IA, cybersécurité, génie logiciel. Partenariats internationaux (France, Allemagne), incubateur de startups tech, laboratoire de recherche en intelligence artificielle.",
                "source": "ESI Alger Rapport 2023"
            },
        ],
        "healthcare": [
            {
                "entreprise": "CHU Mustapha Pacha d'Alger",
                "pays": "Algérie",
                "pratique": "Premier CHU d'Algérie en cours de digitalisation : déploiement du dossier patient informatisé (DPI), PACS numérique pour la radiologie, téléconsultation intra-CHU. Partenariat avec le Ministère de la Santé pour le modèle e-santé national.",
                "source": "Ministère de la Santé Algérie 2023"
            },
            {
                "entreprise": "Sanofi Algérie",
                "pays": "Algérie",
                "pratique": "Filiale pharmaceutique locale : production numérisée avec MES (Manufacturing Execution System), traçabilité 100 % digitale des médicaments, partenariat avec la CNAS pour la facturation électronique des remboursements santé.",
                "source": "Sanofi Algérie Rapport 2023"
            },
        ],
        "retail": [
            {
                "entreprise": "Jumia Algérie",
                "pays": "Algérie",
                "pratique": "Plateforme e-commerce pionnière en Algérie : 200 000+ clients actifs, Jumia Pay, partenariats avec des marques locales. Adapte son modèle aux contraintes de paiement locales (carte Edahabia/CIB, paiement à la livraison).",
                "source": "Jumia Group Annual Report 2023"
            },
            {
                "entreprise": "Ardis — Centre commercial digital",
                "pays": "Algérie",
                "pratique": "Chaîne de distribution multimarque digitalisant l'expérience client : application mobile, click-and-collect, caisse automatique self-checkout. Modèle de retail moderne dans un marché traditionnellement peu digitalisé.",
                "source": "Ardis Algérie 2023"
            },
        ],
        "industry": [
            {
                "entreprise": "Sonatrach",
                "pays": "Algérie",
                "pratique": "Géant national des hydrocarbures en transformation digitale : jumeaux numériques des plateformes pétrolières, capteurs IoT pour la maintenance prédictive, plateforme de gestion des données sismiques. Budget IT 200 M USD/an.",
                "source": "Sonatrach Rapport Annuel 2023"
            },
            {
                "entreprise": "Condor Electronics",
                "pays": "Algérie",
                "pratique": "Fabricant algérien de smartphones et d'électronique. Transition vers le manufacturing 4.0 avec automatisation partielle et MES pour le suivi de production en temps réel. 3 000 employés, 1 M d'appareils/an.",
                "source": "Condor Electronics 2023"
            },
        ],
        "tech": [
            {
                "entreprise": "Djezzy (Veon Group)",
                "pays": "Algérie",
                "pratique": "Opérateur mobile avec 16 M d'abonnés : plateforme digitale DZmobile, fintech DJezzy Money en lancement, API pour les entreprises. Investit 300 M USD dans la 4G+ et prépare la 5G pour 2025.",
                "source": "Djezzy / Veon Annual Report 2023"
            },
            {
                "entreprise": "Ooredoo Algérie",
                "pays": "Algérie",
                "pratique": "Opérateur télécoms avec 12 M d'abonnés : application My Ooredoo, services cloud B2B, partenariat FinTech pour les paiements mobiles. Incubateur de startups tech algériennes Ooredoo Business Club.",
                "source": "Ooredoo Algérie Rapport 2023"
            },
        ],
        "transport": [
            {
                "entreprise": "Air Algérie",
                "pays": "Algérie",
                "pratique": "Application mobile Air Algérie : réservation, check-in digital, suivi des vols. Modernisation de la flotte avec système de maintenance prédictive AMOS. Objectif : 50 % des billets vendus en ligne d'ici 2025 (vs 20 % en 2023).",
                "source": "Air Algérie Rapport Annuel 2023"
            },
            {
                "entreprise": "SNTF — Société Nationale des Transports Ferroviaires",
                "pays": "Algérie",
                "pratique": "Modernisation ferroviaire : déploiement de la billettique digitale sur les grandes lignes, application mobile de suivi des trains, signalisation automatisée. Réseau de 3 700 km en cours de modernisation avec financement chinois.",
                "source": "SNTF Rapport Annuel 2023"
            },
        ],
        "energy": [
            {
                "entreprise": "Sonelgaz",
                "pays": "Algérie",
                "pratique": "Opérateur national de l'énergie : déploiement de compteurs intelligents AMM dans les grandes villes, SCADA de supervision du réseau électrique, application client en ligne pour la facturation. Objectif smart grid sur les 14 grandes villes d'ici 2026.",
                "source": "Sonelgaz Rapport Annuel 2023"
            },
            {
                "entreprise": "Sonatrach — Division Énergie Solaire",
                "pays": "Algérie",
                "pratique": "Programme de solarisation des champs pétroliers du Sahara : 100 MW de capacité solaire pour alimenter les sites d'extraction, réduisant de 30 % la consommation de gaz torché. Gestion digitale par SCADA centralisé.",
                "source": "Sonatrach Rapport ENR 2023"
            },
        ],
        "_default": [
            {
                "entreprise": "Algérie Télécom",
                "pays": "Algérie",
                "pratique": "Opérateur national déployant la 4G LTE sur 70 % du territoire. Lancement de services cloud pour les entreprises (Djaweb Cloud). Transformation interne avec CRM unifié et portail self-service entreprises.",
                "source": "Algérie Télécom Rapport Annuel 2023"
            },
            {
                "entreprise": "Condor Electronics",
                "pays": "Algérie",
                "pratique": "Fabricant algérien de smartphones et d'électronique. Transition vers un modèle de manufacturing 4.0 avec automatisation partielle et MES (Manufacturing Execution System) pour le suivi de production en temps réel.",
                "source": "Condor Electronics 2023"
            },
        ],
    },

    "zoom_case_study": {
        "_default": {
            "entreprise": "CIB (Caisse d'Épargne — Algérie) — Programme de digitalisation",
            "pays": "Algérie",
            "technologie": "Application mobile BARIDI MOB + paiement QR Code interopérable",
            "description": "L'Algérie a lancé le système EDAHABIA (carte postale digitale) et BARIDI MOB via Algérie Poste, permettant à 14 millions de porteurs de carte d'effectuer des paiements mobiles sans compte bancaire. C'est le projet de digitalisation financière le plus ambitieux d'Algérie : 14 M cartes actives, 40 000 commerçants acceptant le QR code, traitement de 50 M transactions en 2023. Modèle de financial inclusion digitale dans un contexte de sous-bancarisation.",
            "resultats": "14 M cartes actives · 40 000 commerçants · 50 M transactions 2023 · Taux bancarisation +12 pts",
            "source": "Algérie Poste / Banque d'Algérie Rapport Annuel 2023",
            "annee": "2023"
        },
    },

    "analyse_statique": "L'Algérie est en phase de transition numérique accélérée depuis 2020, avec un écosystème startup en forte croissance (1 000+ startups labellisées). La contrainte de localisation des données (loi 18-07) est un différenciateur réglementaire majeur qui oblige les entreprises à construire ou louer des infrastructures locales. Le taux de pénétration mobile dépasse 105 %, mais la bancarisation reste faible (45 % de la population). L'initiative EDAHABIA/Baridi Mob représente le levier le plus significatif d'inclusion financière digitale. Les principales opportunités se situent dans les paiements mobiles, la dématérialisation des services publics et le e-commerce local (54 M habitants, marché considérable).",
}


# ─────────────────────────────────────────────────────────────────────────────
# FRANCE
# ─────────────────────────────────────────────────────────────────────────────

_FRANCE = {

    "cadre_juridique": {
        "banking": [
            {
                "texte": "RGPD — Règlement Général sur la Protection des Données (UE 2016/679)",
                "description": "Règlement européen applicable en France depuis mai 2018. Encadre la collecte, le traitement et la conservation des données personnelles clients. Impose le Privacy by Design, le droit à l'effacement et la notification des violations de données sous 72h. La CNIL est l'autorité de contrôle française. Amendes jusqu'à 4 % du CA mondial.",
                "impact": "Obligation"
            },
            {
                "texte": "DSP2 — Directive sur les Services de Paiement 2 (Transposée en droit français)",
                "description": "Impose l'Open Banking : les banques doivent ouvrir leurs APIs aux fintechs agréées (AISP, PISP). L'authentification forte (SCA) est obligatoire pour les transactions en ligne supérieures à 30€. Crée le marché des agrégateurs bancaires (Linxo, Bankin, Budget Insight).",
                "impact": "Obligation"
            },
            {
                "texte": "Loi PACTE (2019) — Modernisation bancaire et fintech",
                "description": "Facilite l'accès au compte pour les néobanques, simplifie les procédures KYC à distance, crée un cadre sandbox pour les fintechs et encadre les ICOs (crypto). Accélère la concurrence entre banques traditionnelles et nouveaux entrants.",
                "impact": "Opportunité"
            },
            {
                "texte": "Réglementation ACPR — Autorité de Contrôle Prudentiel et de Résolution",
                "description": "L'ACPR supervise les banques et les assurances en France. Exige le respect des ratios Bâle III/IV, impose des stress tests annuels et encadre les risques liés à l'IA et aux algorithmes de crédit. Toute utilisation d'IA dans le scoring crédit doit être explicable (Explicabilité de l'IA).",
                "impact": "Conformité"
            },
            {
                "texte": "Règlement IA européen (AI Act — 2024)",
                "description": "Premier cadre réglementaire mondial sur l'IA. Classe les applications IA par niveau de risque. Les systèmes IA à haut risque (scoring crédit, évaluation assurance, recrutement) sont soumis à des obligations strictes de transparence, d'audit et de registre. Applicable dès 2025.",
                "impact": "Obligation"
            },
        ],
        "insurance": [
            {
                "texte": "Directive Solvabilité II (Solvency II) — ACPR",
                "description": "Encadre les exigences de fonds propres et de gouvernance des assureurs européens. Impose des rapports ORSA annuels et une gestion des risques basée sur les scénarios. La conformité nécessite des investissements significatifs en systèmes d'information actuariel.",
                "impact": "Obligation"
            },
            {
                "texte": "RGPD — Données de santé et assurantielles",
                "description": "Les données de santé sont catégorisées 'données sensibles' sous le RGPD. Leur utilisation pour la tarification des risques santé est strictement encadrée. Les assureurs doivent obtenir un consentement explicite et désigner un DPO (Data Protection Officer).",
                "impact": "Obligation"
            },
            {
                "texte": "Loi Hamon (2014) — Résiliation infra-annuelle",
                "description": "Permet aux assurés de résilier leurs contrats auto et habitation à tout moment après 1 an. Accélère la mobilité client et oblige les assureurs à améliorer en permanence leur expérience et leurs offres digitales pour fidéliser.",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act européen — IA dans l'assurance",
                "description": "Les systèmes IA utilisés pour l'évaluation des risques, la détection de fraude et la tarification comportementale sont classés 'haut risque'. Exigences de transparence algorithmique, de registre d'IA et d'audit tiers obligatoire.",
                "impact": "Conformité"
            },
        ],
        "education": [
            {
                "texte": "Loi pour une école de la confiance (Loi Blanquer, 2019) & Plan École Numérique",
                "description": "Encadre la transformation numérique de l'éducation nationale : déploiement de tablettes, manuels numériques, espace numérique de travail (ENT) dans tous les collèges. Plan 1 élève 1 ordinateur doté de 200 M€. RGPD appliqué aux données scolaires des mineurs.",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act européen — IA dans l'éducation",
                "description": "Les systèmes IA d'évaluation automatique des élèves et de recommandation pédagogique sont classés à risque élevé. Exigences de transparence sur les algorithmes d'orientation et de lutte contre les biais dans les outils EdTech.",
                "impact": "Conformité"
            },
            {
                "texte": "Plan France 2030 — Formation aux compétences numériques et IA",
                "description": "1 Md€ investi dans la formation aux métiers du numérique : IA, cybersécurité, data science. Financement des grandes écoles (CentraleSupélec, Polytechnique) pour l'enseignement de l'IA. Partenariats OPCO pour la formation professionnelle digitale.",
                "impact": "Opportunité"
            },
        ],
        "healthcare": [
            {
                "texte": "Loi HPST (Hôpital, Patients, Santé, Territoires) & Ma Santé 2022",
                "description": "Encadre la transformation numérique des hôpitaux : déploiement du Dossier Médical Partagé (DMP), interopérabilité des systèmes d'information hospitaliers (SIH), télémédecine remboursée par l'Assurance Maladie depuis 2018.",
                "impact": "Obligation"
            },
            {
                "texte": "RGPD — Données de santé & Hébergement HDS (Hébergeur de Données de Santé)",
                "description": "Les données de santé exigent un hébergement certifié HDS (agrément ASIP Santé). Toute plateforme de santé digitale doit être certifiée HDS. CNIL active dans les contrôles du secteur (sanction Doctolib 380 000€ en 2020).",
                "impact": "Obligation"
            },
            {
                "texte": "Règlement européen EHDS (European Health Data Space, 2024)",
                "description": "Nouveau règlement encadrant le partage des données de santé dans l'UE. Crée un espace de données de santé européen. Oblige les États membres à développer des infrastructures de partage sécurisé pour la recherche et les soins transfrontaliers.",
                "impact": "Conformité"
            },
        ],
        "retail": [
            {
                "texte": "RGPD — Données clients e-commerce & cookies",
                "description": "Les données de navigation, le ciblage publicitaire et le profilage des clients e-commerce sont strictement encadrés. Obligation de consentement opt-in pour les cookies. CNIL : 3ème autorité la plus active d'Europe pour les sanctions e-commerce.",
                "impact": "Obligation"
            },
            {
                "texte": "Loi relative à la croissance et la transformation des entreprises (PACTE, 2019) — Retail",
                "description": "Simplifie les démarches pour les e-commerçants, facilite la création d'entreprises et encadre les plateformes marketplaces. Oblige les marketplaces à remettre un bilan à la DGFiP pour les vendeurs dépassant 3 000€/an.",
                "impact": "Conformité"
            },
            {
                "texte": "Règlement DSA (Digital Services Act, 2022) — Grandes plateformes retail",
                "description": "Encadre la responsabilité des plateformes e-commerce pour les contenus illégaux et les produits dangereux. Obligations de transparence algorithmique sur les recommandations produits et la publicité ciblée pour les VLOP (Very Large Online Platforms).",
                "impact": "Obligation"
            },
        ],
        "industry": [
            {
                "texte": "Plan France Industrie du Futur & Alliance Industrie du Futur (AIF)",
                "description": "Programme national pour la modernisation industrielle : soutien à l'adoption des technologies 4.0 (robotique, IA, IoT, cobotique), diagnostics de maturité digitale, subventions BPI France pour les PMI. 1 000+ entreprises accompagnées.",
                "impact": "Opportunité"
            },
            {
                "texte": "Règlement européen sur la cybersécurité des infrastructures industrielles (NIS2, 2024)",
                "description": "Oblige les entreprises industrielles critiques à déployer des mesures avancées de cybersécurité OT/IT, des plans de réponse aux incidents et des audits annuels. Amendes jusqu'à 10 M€ ou 2 % du CA mondial.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan France 2030 — Réindustrialisation et usines du futur",
                "description": "5 Mds€ dédiés à la réindustrialisation : construction de nouvelles usines high-tech (batteries, semi-conducteurs, hydrogène), déploiement de jumeaux numériques et de l'IA dans les processus de fabrication.",
                "impact": "Opportunité"
            },
        ],
        "tech": [
            {
                "texte": "LCEN — Loi pour la Confiance dans l'Économie Numérique (2004) & mise à jour DSA",
                "description": "Cadre fondateur du droit numérique français : responsabilité des hébergeurs, commerce électronique, communications électroniques. Complété par le DSA européen en 2022 pour les grandes plateformes.",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act européen (2024) — Obligations pour les fournisseurs d'IA",
                "description": "Les fournisseurs de systèmes IA classés haut risque (recrutement, crédit, santé) doivent s'enregistrer dans la base EU AI Office, réaliser des évaluations de conformité et désigner un représentant UE. Applicable dès 2026.",
                "impact": "Obligation"
            },
            {
                "texte": "Stratégie nationale pour l'IA (SNIA) & Plan France 2030",
                "description": "1,5 Md€ investis dans la recherche IA, les clusters d'excellence (Paris AI Campus) et la formation. Objectif : faire de la France un leader européen de l'IA de confiance. Régulation sandbox pour les startups IA via le programme French Tech.",
                "impact": "Opportunité"
            },
        ],
        "transport": [
            {
                "texte": "Loi d'Orientation des Mobilités (LOM, 2019)",
                "description": "Encadre la transformation digitale de la mobilité : MaaS (Mobility as a Service), ouverture des données de mobilité (SNCF, RATP), réglementation des VTC et trottinettes électriques, covoiturage. Impose l'interopérabilité des systèmes de billettique.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan Vélo & Marche et Plan de Transport National 2023-2027",
                "description": "Investissements dans les modes de mobilité durables avec numérisation des infrastructures : compteurs connectés, applications de navigation multimodale, données ouvertes pour les startups MaaS.",
                "impact": "Opportunité"
            },
            {
                "texte": "Règlement européen sur les données du transport (ITS Directive) & Data Space Mobilité",
                "description": "Impose aux opérateurs de transport de partager leurs données en temps réel via des APIs standardisées. Crée un espace de données de mobilité européen pour l'optimisation des flux et les services de navigation.",
                "impact": "Conformité"
            },
        ],
        "energy": [
            {
                "texte": "Loi énergie-climat (2019) & Plan de Sobriété Énergétique 2023",
                "description": "Objectif : neutralité carbone en 2050. Encadre le déploiement des compteurs Linky (35 M installés), les communautés d'énergie renouvelable, l'autoconsommation collective et les obligations d'audit énergétique pour les grandes entreprises.",
                "impact": "Obligation"
            },
            {
                "texte": "Règlement européen CSRD (Corporate Sustainability Reporting Directive, 2023)",
                "description": "Oblige les grandes entreprises françaises à reporter leurs performances énergétiques et carbone. Accélère la digitalisation du reporting ESG : capteurs IoT, plateformes de collecte de données énergie, tableaux de bord carbone.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan REPowerEU / Plan France 2030 — Énergies renouvelables",
                "description": "40 GW de capacité solaire d'ici 2030, 50 GW d'éolien. Appels d'offres CRE pour les ENR, développement de l'hydrogène vert et des smart grids. Financement BPI France pour les entreprises de la tech énergétique.",
                "impact": "Opportunité"
            },
        ],
        "_default": [
            {
                "texte": "RGPD (Règlement Général sur la Protection des Données)",
                "description": "Règlement européen fondamental encadrant toute collecte et traitement de données personnelles. Obligatoire pour toutes les entreprises traitant des données de résidents UE. Amendes jusqu'à 20 M€ ou 4 % du CA mondial. La CNIL en est l'autorité française.",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act — Règlement Européen sur l'Intelligence Artificielle (2024)",
                "description": "Premier cadre réglementaire mondial sur l'IA. Impose des obligations de transparence, d'explicabilité et d'audit pour les systèmes IA à haut risque. Applicable progressivement entre 2025 et 2027.",
                "impact": "Obligation"
            },
            {
                "texte": "Plan France 2030 — Stratégie nationale IA et numérique",
                "description": "54 Mds€ investis dans la transformation industrielle et technologique de la France. Focus sur l'IA, la cybersécurité, la santé numérique et la transition énergétique. Appels à projets et financements BPI France pour les entreprises innovantes.",
                "impact": "Opportunité"
            },
            {
                "texte": "Directive NIS2 — Cybersécurité des entités essentielles",
                "description": "Impose des exigences renforcées de cybersécurité aux entreprises dans des secteurs critiques. Obligation de signalement des incidents sous 24h, audits de sécurité réguliers et mesures de gestion des risques cyber.",
                "impact": "Obligation"
            },
        ],
    },

    "leaders_nationaux": {
        "banking": [
            {
                "entreprise": "BNP Paribas",
                "pays": "France",
                "pratique": "Transformation digitale de référence en Europe : Hello bank! (néobanque), application Ma Banque avec 6 M utilisateurs actifs, IA appliquée au KYC et à la détection de fraude, programme 'Simply Digital' visant 80 % des opérations en self-service. Budget IT 3,5 Mds€/an.",
                "source": "BNP Paribas Rapport Annuel 2023 / Gartner Banking Digital Index 2024"
            },
            {
                "entreprise": "Société Générale / Boursorama",
                "pays": "France",
                "pratique": "Boursorama Banque — première néobanque française avec 6 M+ clients. 0 frais de tenue de compte, 100 % digital. SG a cédé ses réseaux physiques et misé sur le full digital. NPS +62 (vs -5 pour le réseau physique SG). Référence mondiale en migration vers le digital.",
                "source": "SG / Boursorama Rapport 2023"
            },
        ],
        "insurance": [
            {
                "entreprise": "AXA France",
                "pays": "France",
                "pratique": "Transformation IA complète : plateforme de détection de fraude (économie de 150 M€/an), tarification comportementale par télématique auto, gestion des sinistres par photos IA. Application Mon AXA avec 4,5 M utilisateurs actifs, NPS +42.",
                "source": "AXA Annual Report 2023"
            },
            {
                "entreprise": "Crédit Agricole Assurances / Pacifica",
                "pays": "France",
                "pratique": "Parcours sinistre 100 % digital pour l'auto et l'habitation. Estimation par IA des dommages en moins de 2 minutes. Paiement immédiat pour les sinistres simples (< 500€). Taux de satisfaction 94 % sur le canal digital.",
                "source": "CA Assurances Rapport 2023"
            },
        ],
        "education": [
            {
                "entreprise": "OpenClassrooms",
                "pays": "France",
                "pratique": "Plateforme française de formation en ligne avec 500 000+ apprenants dans 150 pays. Diplômes reconnus par l'État, mentorat personnalisé, IA de recommandation de parcours. Modèle EdTech français à l'international, valorisé 300 M€.",
                "source": "OpenClassrooms Rapport Annuel 2023"
            },
            {
                "entreprise": "Université Paris-Saclay",
                "pays": "France",
                "pratique": "1ère université française (TOP 15 mondial, QS 2024) : campus numérique de référence, formations IA et data science de classe mondiale, partenariats Thales, Safran, EDF. Incubateur Paris-Saclay avec 100+ startups deeptech.",
                "source": "Université Paris-Saclay Rapport 2023"
            },
        ],
        "healthcare": [
            {
                "entreprise": "Doctolib",
                "pays": "France",
                "pratique": "Leader européen de la santé digitale : 80 M de patients, 300 000 professionnels de santé, 100 M de RDV/an. Téléconsultation, dossier médical, IA de détection de créneaux libres. Valorisation 6,4 Mds€, référence mondiale de la santé numérique.",
                "source": "Doctolib Annual Report 2023"
            },
            {
                "entreprise": "AP-HP — Assistance Publique Hôpitaux de Paris",
                "pays": "France",
                "pratique": "Premier CHU européen en transformation digitale : Dossier Patient Informatisé unifié (DPI ORBIS) pour 750 000 hospitalisations/an, IA de triage aux urgences, télémédecine, entrepôt de données de santé EDS (3 M dossiers pour la recherche).",
                "source": "AP-HP Rapport Annuel 2023"
            },
        ],
        "retail": [
            {
                "entreprise": "Décathlon",
                "pays": "France",
                "pratique": "Transformation retail omnicanale mondiale : RFID sur 100 % des produits, application mobile avec scan&go, caisses automatiques, supply chain prédictive IA. E-commerce représente 18 % du CA (2023). Eco-conception et traçabilité digitale des produits.",
                "source": "Décathlon Rapport Annuel 2023"
            },
            {
                "entreprise": "Carrefour France",
                "pays": "France",
                "pratique": "Programme Act For Food digital : IA de réduction du gaspillage alimentaire (–40 % dans 1 000 magasins), application Carrefour+ avec 12 M utilisateurs actifs, chatbot IA Hopla, drone de surveillance en entrepôt, blockchain pour la traçabilité.",
                "source": "Carrefour Rapport Annuel 2023"
            },
        ],
        "industry": [
            {
                "entreprise": "Airbus France",
                "pays": "France",
                "pratique": "Transformation Industrie 4.0 : usine connectée de Toulouse (jumeaux numériques A320), IA de contrôle qualité (caméras 4K + vision IA), maintenance prédictive moteurs (Skywise platform). Programme Fabs (Factories of the Future) avec 50 usines certifiées.",
                "source": "Airbus Annual Report 2023 / WEF Lighthouse Factory 2023"
            },
            {
                "entreprise": "Schneider Electric",
                "pays": "France",
                "pratique": "Champion de l'Industrie 4.0 et de l'efficacité énergétique digitale : EcoStruxure (plateforme IoT industrielle, 800 000 installations), jumeaux numériques, IA de gestion de l'énergie. 65 % du CA via le digital. WEF Lighthouse Factory x5.",
                "source": "Schneider Electric Annual Report 2023"
            },
        ],
        "tech": [
            {
                "entreprise": "OVHcloud",
                "pays": "France",
                "pratique": "1er opérateur cloud européen : 450 000 serveurs dans 35 datacenters en Europe. Cloud souverain français certifié SecNumCloud par l'ANSSI. Alternative européenne aux GAFAM pour les entreprises soumises au RGPD et à la data sovereignty.",
                "source": "OVHcloud Annual Report 2023"
            },
            {
                "entreprise": "Dassault Systèmes",
                "pays": "France",
                "pratique": "Leader mondial des logiciels PLM et de simulation : plateforme 3DEXPERIENCE utilisée par Airbus, Boeing, Toyota. IA générative pour la conception, jumeaux numériques industriels. CA 5,5 Mds€, 23 000 collaborateurs dans 140 pays.",
                "source": "Dassault Systèmes Annual Report 2023"
            },
        ],
        "transport": [
            {
                "entreprise": "SNCF",
                "pays": "France",
                "pratique": "Transformation digitale ferroviaire : application SNCF Connect (10 M utilisateurs), IA de maintenance prédictive (réduction pannes -30 %), jumeaux numériques des voies, gestion dynamique des capacités. Programme GAIA pour la data SNCF.",
                "source": "SNCF Rapport Annuel 2023"
            },
            {
                "entreprise": "BlaBlaCar",
                "pays": "France",
                "pratique": "Licorne française du transport : 100 M membres dans 22 pays, algorithme IA de matching conducteurs-passagers, BlaBlaBus (transporteur longue distance digital). CA 220 M€ en 2023. Référence mondiale du transport partagé digital.",
                "source": "BlaBlaCar Annual Report 2023"
            },
        ],
        "energy": [
            {
                "entreprise": "EDF",
                "pays": "France",
                "pratique": "Déploiement de 35 M de compteurs Linky : plateforme AMM, portail client e.EDF, IA de prévision de consommation. Programme Digital Factory avec 2 000 développeurs. Jumeaux numériques des réacteurs nucléaires pour la maintenance prédictive.",
                "source": "EDF Rapport Annuel 2023"
            },
            {
                "entreprise": "TotalEnergies",
                "pays": "France",
                "pratique": "Transformation digitale des énergies : plateforme SAFT (batteries connectées), IoT sur 1 000 puits pétroliers, IA de prévision de production ENR, trading algorithmique de l'énergie. Investissement 1,5 Md$/an dans la tech énergétique.",
                "source": "TotalEnergies Annual Report 2023"
            },
        ],
        "_default": [
            {
                "entreprise": "Orange France",
                "pays": "France",
                "pratique": "Transformation digitale exemplaire : plateforme omnicanale avec IA, déploiement de la 5G, services cloud et cybersécurité pour les entreprises (Orange Business), programme de réduction de l'empreinte carbone numérique. Investissement de 15 Mds€ sur 2023-2025.",
                "source": "Orange Rapport Annuel 2023"
            },
            {
                "entreprise": "Michelin",
                "pays": "France",
                "pratique": "Transformation industrielle Industrie 4.0 : jumeaux numériques de 70 usines, maintenance prédictive par IA dans 30 % des sites, programme 'Michelin Digital Factory' avec 1 500 développeurs internes. Réduction des pannes non planifiées de 40 %.",
                "source": "Michelin Rapport Annuel 2023 / WEF Lighthouse Factory 2023"
            },
        ],
    },

    "zoom_case_study": {
        "_default": {
            "entreprise": "Boursorama Banque — modèle de néobanque rentable",
            "pays": "France",
            "technologie": "Architecture cloud-native 100 % AWS + IA de personnalisation + zéro agence physique",
            "description": "Boursorama Banque a atteint en 2023 le seuil de 6 millions de clients — record européen pour une néobanque. Son modèle : zéro frais de tenue de compte, ouverture de compte en 15 minutes, application mobile primée 5 années consécutives. Le coût d'acquisition est de 40€ (vs 300€ pour une banque traditionnelle). La banque est rentable depuis 2022 contrairement aux néobanques comme Revolut ou N26. ROE de 18 % en 2023.",
            "resultats": "6 M clients · Coût acquisition 40€ vs 300€ · Rentable depuis 2022 · NPS +62 · ROE 18 %",
            "source": "Boursorama / Société Générale Rapport Annuel 2023 / L'Agefi Digital Banking Awards 2023",
            "annee": "2023"
        },
    },

    "analyse_statique": "La France est l'un des pays européens les plus avancés en transformation digitale des services financiers, classée 5ème en Europe selon l'indice DESI 2023. Le marché des néobanques (Boursorama, Revolut, Nickel, Orange Bank) est l'un des plus compétitifs d'Europe, avec 12 M de clients en néobanques en 2023. L'AI Act européen, adopté en 2024, place la France et ses entreprises face à des obligations nouvelles en matière d'IA explicable et auditée. Le Plan France 2030 injecte 54 Mds€ dans la transformation industrielle et technologique. La CNIL est l'une des autorités RGPD les plus actives d'Europe (3ème en nombre de sanctions). Le principal enjeu : maintenir la compétitivité face aux GAFAM qui entrent dans les services financiers.",
}


# ─────────────────────────────────────────────────────────────────────────────
# ALLEMAGNE
# ─────────────────────────────────────────────────────────────────────────────

_ALLEMAGNE = {

    "cadre_juridique": {
        "banking": [
            {
                "texte": "DSGVO — Datenschutz-Grundverordnung (RGPD allemand)",
                "description": "L'Allemagne applique le RGPD via le DSGVO avec des exigences supplémentaires nationales (Bundesdatenschutzgesetz — BDSG). Le BfDI (Commissaire fédéral à la protection des données) est l'autorité de contrôle. Amendes parmi les plus élevées d'Europe (Deutsche Wohnen : 14,5 M€).",
                "impact": "Obligation"
            },
            {
                "texte": "KWG — Kreditwesengesetz (Loi bancaire allemande) & BaFin",
                "description": "La BaFin (Bundesanstalt für Finanzdienstleistungsaufsicht) supervise les banques, assurances et fintechs allemandes. La KWG encadre les agréments, les exigences de fonds propres et la gouvernance. Les PSD2 et réglementation Bâle III sont pleinement transposées.",
                "impact": "Obligation"
            },
            {
                "texte": "Digitalstrategie Deutschland 2025",
                "description": "Stratégie fédérale pour la transformation numérique de l'Allemagne : administration numérique, infrastructure 5G, IA souveraine, cybersécurité. Budget de 50 Mds€. Objectif : 90 % des services administratifs disponibles en ligne d'ici 2025.",
                "impact": "Opportunité"
            },
            {
                "texte": "Règlement DORA — Digital Operational Resilience Act (UE 2022/2554)",
                "description": "Encadre la résilience opérationnelle numérique des institutions financières européennes. Impose des tests de pénétration annuels, une gestion rigoureuse des fournisseurs cloud tiers et des plans de continuité d'activité. Applicable depuis janvier 2025.",
                "impact": "Obligation"
            },
        ],
        "insurance": [
            {
                "texte": "VAG — Versicherungsaufsichtsgesetz (Loi de surveillance des assurances) & BaFin",
                "description": "La BaFin supervise le secteur de l'assurance en Allemagne. La VAG transpose Solvabilité II avec des exigences allemandes supplémentaires en matière de gouvernance, gestion des risques et reporting ORSA.",
                "impact": "Obligation"
            },
            {
                "texte": "DSGVO — Données assurantielles sensibles",
                "description": "Les données de santé, biométriques et comportementales utilisées pour la tarification sont catégorisées 'données sensibles'. Leur utilisation est strictement encadrée avec exigences de consentement explicite, de minimisation et de DPO obligatoire.",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act européen — IA dans l'assurance",
                "description": "Les systèmes d'évaluation des risques par IA sont classés haut risque. Exigences de transparence algorithmique, d'audit tiers et d'enregistrement dans la base EU AI Office. L'Allemagne est en pointe dans l'application via la BaFin.",
                "impact": "Conformité"
            },
        ],
        "education": [
            {
                "texte": "Digitalpakt Schule — Programme fédéral de numérisation scolaire (5 Mds€)",
                "description": "Programme d'investissement doté de 5 Mds€ pour équiper les écoles allemandes en infrastructure numérique : haut débit, terminaux, logiciels pédagogiques. Prolongé par Digitalpakt 2.0 (2024) avec focus sur la formation des enseignants au numérique et à l'IA.",
                "impact": "Opportunité"
            },
            {
                "texte": "DSGVO — Données des mineurs dans les systèmes éducatifs",
                "description": "Protection renforcée des données des élèves et étudiants : interdiction d'utiliser les données scolaires à des fins commerciales, obligations strictes pour les logiciels éducatifs étrangers (Microsoft 365 Education a fait l'objet de litiges DSGVO dans plusieurs Länder).",
                "impact": "Obligation"
            },
            {
                "texte": "KI-Hochschule Programme & Excellence Initiative — Enseignement supérieur IA",
                "description": "Programme fédéral pour développer l'enseignement de l'IA dans les universités : création de chaires IA dans 50 universités, financement de la recherche en IA explicable et éthique. TU München, TU Berlin, Karlsruhe en tête.",
                "impact": "Opportunité"
            },
        ],
        "healthcare": [
            {
                "texte": "Digitale-Versorgung-Gesetz (DVG, 2019) — DiGA (Applications de santé sur ordonnance)",
                "description": "Loi révolutionnaire permettant aux médecins de prescrire des applications mobiles de santé (DiGA) remboursées par les caisses d'assurance maladie. 50+ DiGA approuvées en 2023. Seule loi au monde permettant le remboursement des apps santé.",
                "impact": "Opportunité"
            },
            {
                "texte": "Gesundheitsdatennutzungsgesetz (GDNG, 2024) — Données de santé",
                "description": "Nouveau règlement facilitant l'utilisation secondaire des données de santé pour la recherche et l'IA médicale. Crée un espace de données de santé (Health Data Space) conforme au EHDS européen. Encadre strictement le consentement des patients.",
                "impact": "Conformité"
            },
            {
                "texte": "DSGVO + BDSG — Données médicales sensibles",
                "description": "Protection maximale des données de santé : hébergement obligatoire en Allemagne ou UE, désignation d'un DPO médical, audit annuel des systèmes de santé digitaux. Le BfDI a sanctionné plusieurs acteurs de la santé numérique pour non-conformité.",
                "impact": "Obligation"
            },
        ],
        "retail": [
            {
                "texte": "DSGVO — E-commerce et profilage clients",
                "description": "Application stricte par les Länder : obligation de consentement opt-in pour les cookies, droit à l'effacement, interdiction du profilage comportemental sans base légale explicite. L'Allemagne est l'un des marchés où le DSGVO est le plus strictement appliqué pour le retail digital.",
                "impact": "Obligation"
            },
            {
                "texte": "HDE (Handelsverband Deutschland) — Standards digitaux du retail allemand",
                "description": "La fédération des commerçants allemands définit les standards de l'omnicanal, de la durabilité digitale et du e-commerce responsable. Programme DigiLog pour accompagner la digitalisation de 50 000 PME du commerce de détail.",
                "impact": "Conformité"
            },
            {
                "texte": "Règlement DSA (Digital Services Act) — Marketplaces allemandes",
                "description": "Oblige les grandes marketplaces (Zalando, Otto) à modérer les produits illégaux, à assurer la transparence algorithmique et à déclarer leurs pratiques publicitaires. Zalando et Amazon sont désignés VLOP (Very Large Online Platform).",
                "impact": "Obligation"
            },
        ],
        "industry": [
            {
                "texte": "Plattform Industrie 4.0 & RAMI 4.0 (Reference Architecture Model Industrie 4.0)",
                "description": "Initiative nationale fédérant 300+ entreprises autour de standards communs (OPC UA, RAMI 4.0). RAMI 4.0 est le standard de référence mondial pour l'architecture des usines connectées. Financement BMBF et BMWi pour la R&D industrielle numérique.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi sur la chaîne d'approvisionnement (Lieferkettensorgfaltspflichtengesetz, LkSG, 2023)",
                "description": "Oblige les grandes entreprises allemandes à tracer et contrôler les conditions de production dans toute leur chaîne d'approvisionnement mondiale. Accélère le déploiement de plateformes de traçabilité digitale et de blockchain supply chain.",
                "impact": "Obligation"
            },
            {
                "texte": "DSGVO + NIS2 — Sécurité des systèmes OT industriels",
                "description": "Les systèmes de contrôle industriels (SCADA, MES, automates) sont soumis à des exigences NIS2. L'Office fédéral de la sécurité des systèmes d'information (BSI) impose des certifications de sécurité pour les infrastructures critiques.",
                "impact": "Obligation"
            },
        ],
        "tech": [
            {
                "texte": "Digitalstrategie Deutschland 2025 & Zukunftsstrategie Forschung und Innovation",
                "description": "Stratégie fédérale pour la transformation numérique : administration numérique, infrastructure 5G, IA souveraine, cybersécurité. Budget de 50 Mds€. Objectif : 90 % des services administratifs disponibles en ligne d'ici 2025.",
                "impact": "Opportunité"
            },
            {
                "texte": "DSGVO + BDSG & BSI-Grundschutz — Sécurité des produits tech",
                "description": "L'Office fédéral de la sécurité des systèmes d'information (BSI) certifie les produits tech selon le standard BSI-Grundschutz. Obligatoire pour les services cloud hébergeant des données de l'administration fédérale (C5-Testat).",
                "impact": "Obligation"
            },
            {
                "texte": "AI Act européen — Développeurs IA en Allemagne",
                "description": "L'Allemagne via la BaFin et le BSI est en pointe dans l'application de l'AI Act. Les fournisseurs d'IA à haut risque doivent s'enregistrer dans la base EU AI Office dès 2025. Écosystème de certification IA en développement avec TÜV Rheinland.",
                "impact": "Obligation"
            },
        ],
        "transport": [
            {
                "texte": "Bundesverkehrswegeplan 2030 & Digitale Schiene Deutschland",
                "description": "Plan fédéral d'investissement de 270 Mds€ dans les transports. Programme 'Digitale Schiene' : digitalisation complète du réseau ferroviaire avec ETCS (European Train Control System), automatisation des gares et IA de gestion des flux.",
                "impact": "Opportunité"
            },
            {
                "texte": "Loi sur la conduite autonome (Autonomes-Fahren-Gesetz, 2021)",
                "description": "Première loi au monde autorisant la conduite autonome de niveau 4 sur voie publique. Encadre les responsabilités légales, les obligations de journalisation des systèmes IA embarqués et les conditions de déploiement commercial des véhicules autonomes.",
                "impact": "Opportunité"
            },
            {
                "texte": "DSGVO — Données de mobilité et géolocalisation",
                "description": "Les données de localisation des conducteurs et passagers sont des données personnelles. Restrictions strictes sur leur conservation et leur utilisation à des fins commerciales. S'applique aux applications MaaS, carpooling et VTC.",
                "impact": "Obligation"
            },
        ],
        "energy": [
            {
                "texte": "Erneuerbare-Energien-Gesetz (EEG 2023) — Loi sur les énergies renouvelables",
                "description": "Objectif : 80 % d'électricité renouvelable d'ici 2030. Encadre les tarifs de rachat, les appels d'offres solaires/éoliens et les communautés énergétiques. Accélère le déploiement des smart grids et de la gestion intelligente de l'énergie.",
                "impact": "Obligation"
            },
            {
                "texte": "Energiewende & Plan national de décarbonation (Klimaschutzgesetz)",
                "description": "Loi climat imposant des objectifs sectoriels contraignants de réduction des émissions. Oblige les grandes entreprises à réduire leur empreinte carbone et à digitaliser leur reporting ESG. Pénalités si les objectifs sectoriels ne sont pas atteints.",
                "impact": "Obligation"
            },
            {
                "texte": "DSGVO — Données des compteurs intelligents (Smart Meter Gateway)",
                "description": "Les données des compteurs intelligents sont des données personnelles sensibles. Le BSI impose un chiffrement de bout en bout via le Smart Meter Gateway (SMGW). Déploiement obligatoire des SMGW pour les consommateurs > 6 000 kWh/an depuis 2023.",
                "impact": "Obligation"
            },
        ],
        "_default": [
            {
                "texte": "DSGVO + BDSG — Protection des données",
                "description": "Le cadre allemand de protection des données est l'un des plus stricts au monde. Le BfDI et les autorités des Länder assurent un contrôle très actif. La conformité nécessite un DPO interne obligatoire dès 20 personnes traitant des données personnelles.",
                "impact": "Obligation"
            },
            {
                "texte": "Digitalstrategie Deutschland & Industrie 4.0",
                "description": "L'Allemagne est le berceau de l'Industrie 4.0. La Plattform Industrie 4.0 fédère 300+ entreprises autour de standards communs (OPC UA, RAMI 4.0). Financement public massif via BMBF et BMWi pour la R&D industrielle numérique.",
                "impact": "Opportunité"
            },
            {
                "texte": "Règlement DORA — Résilience opérationnelle numérique",
                "description": "Applicable depuis janvier 2025, DORA impose aux institutions financières des obligations de résilience cyber : tests annuels, gestion des risques tiers (cloud), reporting incidents sous 4h.",
                "impact": "Obligation"
            },
            {
                "texte": "Directive NIS2 — Sécurité des réseaux et systèmes d'information",
                "description": "Transposée en droit allemand en 2024. Oblige les opérateurs d'infrastructures critiques à mettre en œuvre des mesures de sécurité avancées, des audits réguliers et des plans de réponse aux incidents.",
                "impact": "Obligation"
            },
        ],
    },

    "leaders_nationaux": {
        "banking": [
            {
                "entreprise": "Deutsche Bank",
                "pays": "Allemagne",
                "pratique": "Programme de transformation 'Strategy 2025' : migration cloud AWS/Azure, IA pour la gestion des risques et la détection de fraude, application Deutsche Bank Mobile avec 3 M+ utilisateurs actifs, plateforme Qdos pour les PME. Investissement IT 13 Mds€ sur 2022-2025.",
                "source": "Deutsche Bank Annual Report 2023"
            },
            {
                "entreprise": "N26 (néobanque allemande)",
                "pays": "Allemagne",
                "pratique": "Néobanque leader en Europe avec 8 M+ clients dans 24 pays. Architecture cloud-native, onboarding en 8 minutes, AI-powered fraud detection (99,7 % de précision). Valorisation 9 Mds$ (2021). Référence mondiale en UX bancaire mobile.",
                "source": "N26 Annual Report 2023 / Forbes Fintech 50 2023"
            },
        ],
        "insurance": [
            {
                "entreprise": "Allianz SE",
                "pays": "Allemagne",
                "pratique": "Assureur N°1 mondial en transformation digitale : plateforme Allianz Direct (souscription 100 % en ligne), IA de détection de fraude (économies 200 M€/an), télématique auto, gestion sinistres par photos IA. CA 153 Mds€, présence dans 70 pays.",
                "source": "Allianz Annual Report 2023"
            },
            {
                "entreprise": "Munich Re",
                "pays": "Allemagne",
                "pratique": "Réassureur leader en IA et data : plateforme NATHAN pour la tarification des risques de vie par IA, modèles catastrophe digitaux, partenariats InsurTech. Investissements de 500 M€ dans les solutions digitales d'assurance 2022-2025.",
                "source": "Munich Re Annual Report 2023"
            },
        ],
        "education": [
            {
                "entreprise": "Hasso-Plattner-Institut (HPI)",
                "pays": "Allemagne",
                "pratique": "Institut d'excellence en ingénierie logicielle : plateforme openHPI avec 1,5 M d'apprenants dans 180 pays, MOOCs sur l'IA, le design thinking et la cybersécurité. Partenariat SAP, référence mondiale en EdTech universitaire.",
                "source": "HPI Annual Report 2023"
            },
            {
                "entreprise": "Fraunhofer-Gesellschaft",
                "pays": "Allemagne",
                "pratique": "Réseau de 76 instituts de recherche appliquée : transfert technologique vers l'industrie, formation continue en Industrie 4.0 et IA, plateformes e-learning Fraunhofer Academy. 30 000 chercheurs, 3 Mds€ de budget annuel.",
                "source": "Fraunhofer Annual Report 2023"
            },
        ],
        "healthcare": [
            {
                "entreprise": "Siemens Healthineers",
                "pays": "Allemagne",
                "pratique": "Leader mondial du diagnostic médical digital : IRM et scanners connectés, plateforme teamplay pour le partage de données d'imagerie, IA de détection de tumeurs (AI-Rad Companion). CA 21 Mds€, présence dans 70 pays.",
                "source": "Siemens Healthineers Annual Report 2023"
            },
            {
                "entreprise": "SAP Health — Solutions pour établissements de santé",
                "pays": "Allemagne",
                "pratique": "Plateforme SAP S/4HANA for Healthcare pour la gestion des hôpitaux : DPI intégré, gestion des lits en temps réel, analytics cliniques. Utilisée par 200+ hôpitaux européens. IA de prédiction des durées de séjour.",
                "source": "SAP Annual Report 2023"
            },
        ],
        "retail": [
            {
                "entreprise": "Zalando",
                "pays": "Allemagne",
                "pratique": "2ème e-commerçant mode en Europe : IA de recommandation (35 % du CA), algorithme de sizing IA, plateforme Zalando Partner Program (50 000 marques). CA 10,1 Mds€ en 2023, 50 M clients actifs dans 25 pays.",
                "source": "Zalando Annual Report 2023"
            },
            {
                "entreprise": "Otto Group",
                "pays": "Allemagne",
                "pratique": "Transformation retail IA exemplaire : algorithme de prévision des ventes (99 % précision) réduisant les stocks de 30 %, livraison prédictive (colis expédiés avant commande), plateforme marketplace avec 7 M clients actifs.",
                "source": "Otto Group Annual Report 2023"
            },
        ],
        "industry": [
            {
                "entreprise": "Siemens AG — Digital Industries",
                "pays": "Allemagne",
                "pratique": "Leader mondial de l'Industrie 4.0 : plateforme MindSphere (jumeaux numériques industriels), 300+ usines connectées, IA de maintenance prédictive. Programme 'Siemens Digital Industries' avec 10 Mds€ investis en R&D annuellement.",
                "source": "Siemens Annual Report 2023 / WEF Global Lighthouse Network 2023"
            },
            {
                "entreprise": "Bosch",
                "pays": "Allemagne",
                "pratique": "Transformation Industrie 4.0 de 250 usines : plateforme IoT Bosch IoT Suite, IA de contrôle qualité vision, maintenance prédictive (économies de 200 M€/an), usine modèle Reutlingen (WEF Lighthouse 2023). 400 000 employés, 88 Mds€ de CA.",
                "source": "Bosch Annual Report 2023 / WEF Lighthouse 2023"
            },
        ],
        "tech": [
            {
                "entreprise": "SAP SE",
                "pays": "Allemagne",
                "pratique": "ERP cloud leader mondial avec SAP S/4HANA. Migration de 400 M+ utilisateurs vers le cloud. IA intégrée (Joule) dans tous les processus métier. Plateforme BTP pour la transformation digitale de 300 000 clients dans 180 pays.",
                "source": "SAP Annual Report 2023"
            },
            {
                "entreprise": "Deutsche Telekom / T-Systems",
                "pays": "Allemagne",
                "pratique": "Cloud souverain allemand T-Systems : certifié C5 BSI, partenaire Microsoft Azure pour la souveraineté des données. Cybersécurité industrielle, 5G privée pour les usines (network slicing). CA T-Systems 4 Mds€, 28 000 experts IT.",
                "source": "Deutsche Telekom Annual Report 2023"
            },
        ],
        "transport": [
            {
                "entreprise": "Deutsche Bahn",
                "pays": "Allemagne",
                "pratique": "Transformation digitale ferroviaire : application DB Navigator (10 M utilisateurs), IA de maintenance prédictive (économies 100 M€/an), programme 'Digitale Schiene' avec ETCS sur 13 000 km. CA 45 Mds€, 340 000 employés.",
                "source": "Deutsche Bahn Annual Report 2023"
            },
            {
                "entreprise": "DHL Group",
                "pays": "Allemagne",
                "pratique": "Leader logistique mondial en transformation digitale : IA de tri (100 000 colis/heure automatisés), drones de livraison (programme DHL Parcelcopter), jumeaux numériques d'entrepôts, robotique collaborative (Boston Dynamics). 600 000 employés dans 220 pays.",
                "source": "DHL Annual Report 2023"
            },
        ],
        "energy": [
            {
                "entreprise": "RWE",
                "pays": "Allemagne",
                "pratique": "2ème producteur ENR en Europe : parcs solaires et éoliens gérés par IA, plateforme de trading algorithmique de l'énergie, jumeaux numériques des parcs éoliens offshore. Investissement 50 Mds€ dans les ENR 2024-2030. Objectif 65 GW d'ENR.",
                "source": "RWE Annual Report 2023"
            },
            {
                "entreprise": "Siemens Energy",
                "pays": "Allemagne",
                "pratique": "Technologies de transition énergétique : turbines à hydrogène vert, smart grids intelligents, SCADA de supervision de réseaux électriques, IA de prévision de production éolienne (précision +15 %). CA 29 Mds€, présence dans 90 pays.",
                "source": "Siemens Energy Annual Report 2023"
            },
        ],
        "_default": [
            {
                "entreprise": "Siemens AG",
                "pays": "Allemagne",
                "pratique": "Leader mondial de l'Industrie 4.0 : plateforme MindSphere (jumeaux numériques industriels), 300+ usines connectées, IA de maintenance prédictive. Programme 'Siemens Digital Industries' avec 10 Mds€ investis en R&D digitale annuellement.",
                "source": "Siemens Annual Report 2023 / WEF Global Lighthouse Network 2023"
            },
            {
                "entreprise": "SAP SE",
                "pays": "Allemagne",
                "pratique": "ERP cloud leader mondial avec SAP S/4HANA. Migration de 400 M+ utilisateurs vers le cloud. IA intégrée (Joule) dans tous les processus métier. Plateforme BTP pour la transformation digitale de 300 000 clients dans 180 pays.",
                "source": "SAP Annual Report 2023"
            },
        ],
    },

    "zoom_case_study": {
        "_default": {
            "entreprise": "Volkswagen Group — Volkswagen Automotive Cloud",
            "pays": "Allemagne",
            "technologie": "Microsoft Azure + IDA (Intelligent Digital Accelerator) + data mesh architecture",
            "description": "Volkswagen Group a lancé en 2022 la Volkswagen Automotive Cloud sur Microsoft Azure — la plus grande transformation cloud industrielle d'Europe. 10 millions de véhicules connectés, mises à jour OTA (Over-The-Air), IA pour la maintenance prédictive et la personnalisation de l'expérience conducteur. La plateforme IDA traite 20 TB de données/jour provenant des véhicules. Investissement de 2 Mds€ sur 5 ans. Réduction des rappels de véhicules de 35 % grâce à la détection précoce des défauts.",
            "resultats": "10 M véhicules connectés · 20 TB data/jour · Rappels -35 % · Économies maintenance 500 M€/an",
            "source": "Volkswagen / Microsoft Case Study 2023 / WEF Lighthouse Factory Award 2023",
            "annee": "2023"
        },
    },

    "analyse_statique": "L'Allemagne est la première économie industrielle d'Europe et le berceau de l'Industrie 4.0. Avec 3 000+ robots pour 10 000 employés industriels, elle affiche le 3ème taux de robotisation mondial. Le secteur financier est dominé par des acteurs solides (Deutsche Bank, Commerzbank, DZ Bank) mais est challengé par des néobanques comme N26 qui ont redéfini les standards d'expérience utilisateur. Le DSGVO appliqué avec rigueur par le BfDI et les autorités des Länder crée un environnement de très haute conformité. La Digitalstrategie 2025 investit massivement dans la 5G, l'IA et la cybersécurité. Principal défi : la transformation digitale de la Mittelstand (PME familiales qui représentent 60 % du PIB) — traditionnellement réticentes au cloud et aux données partagées.",
}


# ─────────────────────────────────────────────────────────────────────────────
# COUNTRY REGISTRY & PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

_REGISTRY: dict[str, dict] = {
    # Maroc
    "maroc": _MAROC,
    "morocco": _MAROC,
    "المغرب": _MAROC,
    # Tunisie
    "tunisie": _TUNISIE,
    "tunisia": _TUNISIE,
    "تونس": _TUNISIE,
    # Algérie
    "algérie": _ALGERIE,
    "algerie": _ALGERIE,
    "algeria": _ALGERIE,
    "الجزائر": _ALGERIE,
    # France
    "france": _FRANCE,
    # Allemagne
    "allemagne": _ALLEMAGNE,
    "germany": _ALLEMAGNE,
    "deutschland": _ALLEMAGNE,
}


def get_country_context(country: str, sector: str = "") -> dict:
    """
    Return country-specific KB context for a given country and sector.

    The returned dict is structured to be merged into the sub-axis KB:
      - cadre_juridique  : list[dict]  — country-specific legal framework
      - leaders_nationaux: list[dict]  — national reference companies
      - zoom_case_study  : dict        — a representative case study
      - analyse_statique : str         — static contextual analysis

    Returns {} for UEMOA countries (existing KB already handles them well)
    and for unrecognised countries.
    """
    if not country:
        return {}

    key = country.lower().strip()
    ctx = _REGISTRY.get(key)
    if ctx is None:
        # Try partial match (e.g. "République française" → "france")
        for reg_key, reg_ctx in _REGISTRY.items():
            if reg_key in key or key in reg_key:
                ctx = reg_ctx
                break

    if ctx is None:
        return {}

    sector_key = sector.lower().strip() if sector else "_default"

    result: dict = {}

    # Legal framework: try sector-specific, fall back to _default
    cadre = ctx.get("cadre_juridique", {})
    result["cadre_juridique"] = cadre.get(sector_key) or cadre.get("_default", [])

    # National leaders: try sector-specific, fall back to _default
    leaders = ctx.get("leaders_nationaux", {})
    result["leaders_nationaux"] = leaders.get(sector_key) or leaders.get("_default", [])

    # Zoom case study: try sector-specific, fall back to _default
    zoom = ctx.get("zoom_case_study", {})
    result["zoom_case_study"] = zoom.get(sector_key) or zoom.get("_default", {})

    # Static analysis
    result["analyse_statique"] = ctx.get("analyse_statique", "")

    return result
