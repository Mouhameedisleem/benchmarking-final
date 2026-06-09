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
