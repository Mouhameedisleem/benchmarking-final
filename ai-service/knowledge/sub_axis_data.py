"""
Sub-axis Knowledge Base — Hsys Solutions Digital Benchmark
Structured static data for all 22 sub-axes across 9 axes.
Context: Banking sector / UEMOA + international reference.

Structure per sub-axis:
  tendances          : current digital trends (title, description, source)
  analyse_statique   : pre-built factual analysis (contenu figé)
  leaders_nationaux  : UEMOA/national banking leaders
  leaders_regionaux  : Africa regional leaders
  leaders_internationaux : world-class leaders
  cadre_juridique    : applicable laws & regulations
  ma_levees_fonds    : M&A and major funding rounds
  maturite_maximale  : description of excellence level
"""

SUB_AXIS_DATA = {

    # ═══════════════════════════════════════════════════════════════
    # AXE 1 — MÉTIER / BUSINESS
    # ═══════════════════════════════════════════════════════════════

    "BUSINESS::Stratégie digitale": {
        "tendances": [
            {
                "titre": "Stratégie digitale intégrée au plan d'entreprise",
                "description": "Les banques leaders ne traitent plus le digital comme un projet IT isolé mais l'intègrent dans leur plan stratégique global avec des OKRs mesurables et un budget dédié supérieur à 15% du OPEX.",
                "source": "McKinsey Global Banking Report 2024",
                "annee": "2024"
            },
            {
                "titre": "Chief Digital Officer (CDO) comme rôle stratégique",
                "description": "73% des banques du top 100 mondial ont nommé un CDO avec pouvoir de décision budgétaire direct. En UEMOA, ce rôle émerge progressivement dans les grandes banques panafricaines.",
                "source": "Gartner Digital Banking Survey 2024",
                "annee": "2024"
            },
            {
                "titre": "Alignement ESG et transformation digitale",
                "description": "La stratégie digitale intègre désormais les critères ESG : réduction de l'empreinte carbone via la dématérialisation, inclusion financière mesurée comme KPI stratégique.",
                "source": "WEF Financial Services 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "En zone UEMOA, la maturité stratégique digitale reste hétérogène. "
            "Les banques panafricaines (Ecobank, Bank of Africa, UBA) disposent de feuilles de route digitales formalisées, "
            "tandis que les banques locales de taille moyenne n'ont souvent qu'une vision digitale non documentée. "
            "Selon l'enquête BCEAO 2023, moins de 40% des établissements bancaires de l'UEMOA disposent d'une stratégie digitale "
            "avec des objectifs mesurables et un pilotage dédié. Le gap avec les banques marocaines (CIH Bank, Attijariwafa) "
            "qui ont investi massivement depuis 2018 est significatif."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank Transnational", "pays": "Pan-UEMOA", "pratique": "Stratégie 'Fintech Ready' avec 10M$ investis annuellement dans la transformation digitale, CDO nommé au comité exécutif", "source": "Ecobank Annual Report 2023"},
            {"entreprise": "Coris Bank International", "pays": "Burkina Faso / UEMOA", "pratique": "Plan de transformation digitale 2022-2025 avec 3 axes prioritaires : mobile, data, cybersécurité", "source": "Coris Bank Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Budget digital de 25% du total investissement, transformation complète en banque omnicanale depuis 2019", "source": "CIH Bank Rapport Annuel 2023"},
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "Stratégie 'Digital First' depuis 2017 — 97% des transactions hors agence, présence dans 7 pays africains", "source": "Equity Bank Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "DBS Bank", "pays": "Singapour", "pratique": "Transformation en 'techfin' — 100% des services digitalisés, IA dans 1000+ processus, économie de 500M SGD en 3 ans", "source": "DBS Annual Report 2023"},
            {"entreprise": "ING Group", "pays": "Pays-Bas", "pratique": "Think Forward Strategy — plateforme unifiée sur 40 pays, 100% cloud-native depuis 2022", "source": "ING Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Directive BCEAO n°08/2002/CM/UEMOA", "description": "Cadre de promotion de la bancarisation et des moyens de paiement scripturaux dans l'UEMOA", "impact": "Obligation"},
            {"texte": "Règlement UEMOA n°15/2002/CM/UEMOA", "description": "Systèmes de paiement dans l'UEMOA — interopérabilité et surveillance", "impact": "Conformité"},
            {"texte": "Stratégie Nationale de Finance Inclusive (SNFI)", "description": "Chaque état membre définit sa stratégie d'inclusion financière alignée avec la BCEAO", "impact": "Opportunité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Acquisition", "detail": "Ecobank acquiert les activités de Nedbank en Afrique de l'Ouest (2021) — consolidation régionale", "montant": "Non divulgué", "annee": "2021"},
            {"operation": "Levée de fonds", "detail": "Wave Money (fintech UEMOA) lève 200M$ Serie A — concurrence directe aux banques traditionnelles sur les paiements mobiles", "montant": "200M USD", "annee": "2021"}
        ],
        "maturite_maximale": (
            "Excellence = stratégie digitale révisée trimestriellement, intégrée au plan d'entreprise, "
            "pilotée par des OKRs mesurables, avec CDO au COMEX, budget digital >15% OPEX total, "
            "et roadmap publique communiquée aux investisseurs et clients."
        )
    },

    "BUSINESS::Orientation client": {
        "tendances": [
            {
                "titre": "Hyper-personnalisation par la data client",
                "description": "Les banques utilisent l'IA pour analyser jusqu'à 200 points de données par client afin de personnaliser chaque interaction en temps réel. Le NPS des banques hyper-personnalisées est supérieur de 25 points.",
                "source": "Accenture Banking Consumer Study 2024",
                "annee": "2024"
            },
            {
                "titre": "Moments de vie comme déclencheurs de produits",
                "description": "L'approche 'life events banking' (mariage, naissance, achat immobilier) permet de proposer le bon produit au bon moment avec des taux de conversion 5x supérieurs aux campagnes génériques.",
                "source": "McKinsey Customer Experience 2024",
                "annee": "2024"
            },
            {
                "titre": "Voice of Customer (VoC) en temps réel",
                "description": "Collecte automatisée des avis (stores mobiles, enquêtes in-app, réseaux sociaux) analysés par IA pour détecter les irritants en moins de 24h.",
                "source": "Forrester CX Index 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "En UEMOA, l'orientation client reste principalement centrée sur la gestion des réclamations réactives. "
            "Peu de banques ont mis en place des dispositifs proactifs de mesure de satisfaction (NPS, CSAT). "
            "Les banques ivoiriennes testées affichent des taux de réponse aux avis stores entre 20% et 60%. "
            "Orabank et Société Générale CI sont les plus avancées avec des enquêtes de satisfaction régulières."
        ),
        "leaders_nationaux": [
            {"entreprise": "Société Générale Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Enquêtes NPS trimestrielles, dispositif de réclamation multicanal avec SLA de 48h", "source": "SGCI Rapport 2023"},
            {"entreprise": "Orabank", "pays": "Pan-UEMOA", "pratique": "Application mobile avec système de feedback intégré, score store 4.2/5", "source": "Orabank Digital Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Centre de données client unifié (CDP) alimentant 200+ segments dynamiques pour la personnalisation", "source": "Attijariwafa Annual Report 2023"},
            {"entreprise": "KCB Group", "pays": "Kenya", "pratique": "IA conversationnelle traitant 85% des réclamations sans intervention humaine", "source": "KCB Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "BBVA", "pays": "Espagne", "pratique": "Moteur de personnalisation IA analysant 3Mds interactions/jour, NPS de +45 (vs +15 moyenne secteur)", "source": "BBVA Annual Report 2023"},
            {"entreprise": "Capital One", "pays": "USA", "pratique": "Assistant virtuel Eno — anticipe les besoins avant que le client ne les exprime, 40M utilisateurs actifs", "source": "Capital One Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi n°2013-015 (Mali) / Équivalents UEMOA", "description": "Protection des données à caractère personnel — encadre la collecte et l'utilisation des données clients", "impact": "Conformité"},
            {"texte": "Instruction BCEAO sur la protection du consommateur de services financiers", "description": "Obligations d'information, de transparence et de traitement des réclamations", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Yabx (fintech scoring crédit Afrique) lève 3M$ pour améliorer le scoring client des banques partenaires", "montant": "3M USD", "annee": "2023"},
            {"operation": "Partenariat", "detail": "Orabank x Mastercard — déploiement d'outils d'analyse comportementale client sur 12 pays", "montant": "N/A", "annee": "2023"}
        ],
        "maturite_maximale": (
            "Excellence = CDP (Customer Data Platform) unifié, NPS mesuré en temps réel, "
            "personnalisation de chaque interaction par IA, taux de résolution réclamation <24h, "
            "score stores >4.5/5 avec réponse systématique aux avis."
        )
    },

    "BUSINESS::Innovation": {
        "tendances": [
            {
                "titre": "Labs d'innovation et incubateurs bancaires",
                "description": "Les banques leaders créent des labs internes (Garage BNP Paribas, BBVA New Digital Businesses) capables de lancer un MVP en 6 semaines.",
                "source": "Deloitte Banking Innovation Survey 2024",
                "annee": "2024"
            },
            {
                "titre": "Partenariats fintechs comme levier d'innovation",
                "description": "60% des banques mondiales privilégient les partenariats fintechs à l'innovation interne pour réduire le time-to-market. En Afrique, Wave, Julaya et Wizall bousculent les acteurs traditionnels.",
                "source": "BCG Fintech Control Tower 2024",
                "annee": "2024"
            },
            {
                "titre": "Innovation frugale adaptée aux marchés africains",
                "description": "Le modèle africain d'innovation (USSD, feature phones, agents bancaires) prouve que l'innovation n'exige pas les mêmes infrastructures qu'en occident. M-Pesa reste la référence mondiale.",
                "source": "GSMA Mobile Money Report 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'écosystème fintech UEMOA est en forte croissance : +120 startups fintech actives en 2023 (source : AfriQore). "
            "Les principales fintechs qui challengent les banques : Wave (paiements mobiles, 8M users), "
            "Julaya (paiements B2B), CinetPay (agrégateur de paiements), Bizao (API banking). "
            "Les banques les plus avancées en partenariats fintechs sont Ecobank et UBA."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "EcoBank Fintech Challenge annuel — 50+ fintechs évaluées, 5 intégrées en 2023", "source": "Ecobank Annual Report 2023"},
            {"entreprise": "UBA Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Partenariat avec Julaya pour les paiements B2B digitaux", "source": "UBA Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "Equity Innovation Centre — 200+ développeurs internes, 15 produits lancés en 2023", "source": "Equity Annual Report 2023"},
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "CIH Lab — partenariat avec 8 startups fintech marocaines intégrées dans l'offre bancaire", "source": "CIH Bank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Goldman Sachs", "pays": "USA", "pratique": "Marcus — néobanque interne lancée en 2016, 110Mds$ d'actifs en 2023", "source": "Goldman Sachs Report 2023"},
            {"entreprise": "BBVA", "pays": "Espagne", "pratique": "BBVA Ventures — 250M€ investis dans 40+ fintechs mondiales depuis 2016", "source": "BBVA Ventures 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Cadre réglementaire sandbox BCEAO", "description": "La BCEAO a lancé un bac à sable réglementaire pour les fintechs UEMOA en 2022", "impact": "Opportunité"},
            {"texte": "Agrément établissement de monnaie électronique (BCEAO)", "description": "Instruction n°008-05-2015 encadrant les EME — obligation pour toute activité de monnaie électronique", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Wave (fintech UEMOA) lève 200M$ — valorisation de 1.7Mds$ (unicorn africain)", "montant": "200M USD", "annee": "2021"},
            {"operation": "Levée de fonds", "detail": "Bizao (API banking UEMOA) lève 8.2M€ pour accélérer l'open banking en Afrique", "montant": "8.2M EUR", "annee": "2022"},
            {"operation": "Acquisition", "detail": "MTN acquiert Wayawaya (fintech remittances) pour renforcer son offre mobile money", "montant": "Non divulgué", "annee": "2023"}
        ],
        "maturite_maximale": (
            "Excellence = lab d'innovation dédié avec budget propre, pipeline de partenariats fintechs actif, "
            "hackathons internes réguliers, time-to-market MVP <8 semaines, veille concurrentielle structurée."
        )
    },

    "BUSINESS::Modèle économique digital": {
        "tendances": [
            {
                "titre": "Monétisation des données et revenus non-transactionnels",
                "description": "Les banques avancées génèrent jusqu'à 20% de leurs revenus via des services data et des APIs exposées à des tiers. L'open banking devient un centre de profit.",
                "source": "McKinsey Open Banking Report 2024",
                "annee": "2024"
            },
            {
                "titre": "Banking-as-a-Service (BaaS) comme modèle de croissance",
                "description": "Le BaaS permet aux banques d'exposer leurs licences et infrastructures à des acteurs non-bancaires. Marché mondial estimé à 7Mds$ en 2026.",
                "source": "Gartner BaaS Forecast 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "En UEMOA, moins de 10% des banques génèrent des revenus significatifs via des canaux purement digitaux. "
            "Les frais de tenue de compte et les commissions sur opérations physiques restent dominants. "
            "Wave et Orange Money ont capté une part croissante des revenus de paiement au détriment des banques traditionnelles."
        ),
        "leaders_nationaux": [
            {"entreprise": "Orabank", "pays": "Pan-UEMOA", "pratique": "Offre digitale 'Ora Express' — ouverture de compte 100% mobile avec revenus de commissions digitales", "source": "Orabank 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "M-Pesa / Safaricom", "pays": "Kenya", "pratique": "Écosystème de services financiers générant 35% du PIB kényan en transactions, modèle BaaS pour 10+ banques", "source": "Safaricom Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Solarisbank", "pays": "Allemagne", "pratique": "Pure BaaS player — infrastructure bancaire pour 100+ fintechs, 20Mds€ en encours gérés", "source": "Solarisbank 2023"},
            {"entreprise": "Stripe", "pays": "USA", "pratique": "Financial infrastructure as a service — valorisation 50Mds$, 1M+ entreprises clientes", "source": "Stripe 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Instruction BCEAO n°008-05-2015", "description": "Régit les activités de monnaie électronique et les modèles de revenus associés", "impact": "Obligation"},
            {"texte": "Règlement sur les systèmes de paiement UEMOA", "description": "Encadre les modèles de revenus sur les paiements électroniques", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "CinetPay (agrégateur paiements CI/UEMOA) lève 7M$ pour étendre son infrastructure BaaS", "montant": "7M USD", "annee": "2022"}
        ],
        "maturite_maximale": "Excellence = >30% revenus via canaux digitaux, plateforme BaaS opérationnelle, APIs monétisées auprès de partenaires tiers."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 2 — PROCESSUS / PROCESS
    # ═══════════════════════════════════════════════════════════════

    "PROCESS::Cartographie des processus": {
        "tendances": [
            {
                "titre": "Process Mining automatisé",
                "description": "Les outils de process mining (Celonis, UiPath Process Mining) analysent les logs systèmes pour cartographier automatiquement les processus réels vs théoriques. Écart moyen constaté : 40%.",
                "source": "Gartner Process Mining Report 2024",
                "annee": "2024"
            },
            {
                "titre": "BPM cloud et gestion des processus en temps réel",
                "description": "Les plateformes BPM cloud (Pega, Appian, Camunda) permettent la modélisation, l'exécution et le monitoring des processus en temps réel avec des tableaux de bord opérationnels.",
                "source": "Forrester BPM Wave 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La cartographie des processus bancaires en UEMOA est majoritairement manuelle et non maintenue. "
            "Les processus critiques (ouverture de compte, octroi de crédit, KYC) sont souvent documentés dans des Word/Excel non actualisés. "
            "Délai moyen d'ouverture de compte en agence : 3-5 jours (vs <24h pour les néobanques africaines)."
        ),
        "leaders_nationaux": [
            {"entreprise": "BNI Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Démarche de certification ISO 9001 avec cartographie des processus clés", "source": "BNI Rapport 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Plateforme BPM Pega déployée sur 80% des processus back-office, réduction des délais de 60%", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "ING Bank", "pays": "Pays-Bas", "pratique": "Process Mining Celonis sur l'ensemble des processus opérationnels — 300M€ d'économies identifiées", "source": "ING Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Normes BCEAO sur la gestion des risques opérationnels", "description": "Obligation de documenter et contrôler les processus critiques", "impact": "Obligation"},
            {"texte": "Bâle III / CRBF", "description": "Exigences de contrôle interne imposant la cartographie des processus à risque", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Celonis (process mining leader) valorisé à 13Mds$ après levée de 1Md$ en 2021", "montant": "1Md USD", "annee": "2021"}
        ],
        "maturite_maximale": "Excellence = 100% processus critiques cartographiés avec process mining, propriétaires désignés, KPIs opérationnels en temps réel."
    },

    "PROCESS::Automatisation": {
        "tendances": [
            {
                "titre": "Hyperautomatisation : RPA + IA + BPM combinés",
                "description": "L'hyperautomatisation combine RPA, IA et orchestration de processus pour automatiser les tâches cognitives et manuelles. Gartner prédit 25% de réduction des coûts opérationnels d'ici 2026.",
                "source": "Gartner Hyperautomation 2024",
                "annee": "2024"
            },
            {
                "titre": "Automatisation du KYC et de l'onboarding",
                "description": "Les solutions e-KYC (Smile ID, Onfido, Jumio) permettent la vérification d'identité en moins de 2 minutes, réduisant le coût d'acquisition client de 70%.",
                "source": "KPMG Digital Banking 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Les processus back-office bancaires UEMOA restent fortement manuels. "
            "Traitement des virements : 60% manuel en moyenne. Rapprochement comptable : 80% manuel. "
            "Les banques les plus avancées (Ecobank, Société Générale CI) ont déployé des robots RPA sur les traitements de nuit "
            "mais la couverture reste inférieure à 30% des tâches automatisables."
        ),
        "leaders_nationaux": [
            {"entreprise": "Société Générale CI", "pays": "Côte d'Ivoire", "pratique": "RPA déployé sur le rapprochement SWIFT et les virements de masse — économie de 2 ETP/mois", "source": "SGCI 2023"},
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Automatisation du reporting réglementaire BCEAO avec réduction de 80% du temps de production", "source": "Ecobank Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "97% des transactions traitées de façon automatisée, 0 intervention humaine sur les paiements standards", "source": "Equity Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "JPMorgan Chase", "pays": "USA", "pratique": "COIN (Contract Intelligence) — analyse 12 000 contrats/an en secondes vs 360 000h humaines", "source": "JPMorgan Annual Report 2023"},
            {"entreprise": "BNP Paribas", "pays": "France", "pratique": "1 200 robots RPA en production sur les processus back-office, 30% de réduction des coûts opérationnels", "source": "BNP Paribas Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Instruction BCEAO sur la maîtrise des risques liés aux systèmes d'information", "description": "Encadre les systèmes automatisés et les obligations de contrôle et de traçabilité", "impact": "Conformité"},
            {"texte": "Réglementation sur la piste d'audit", "description": "Toute automatisation doit garantir la traçabilité complète des opérations", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "UiPath (leader RPA) IPO à 35Mds$ — accélération de l'adoption entreprise", "montant": "1.3Md USD IPO", "annee": "2021"},
            {"operation": "Acquisition", "detail": "SAP acquiert Signavio (process intelligence) pour intégrer le process mining dans son ERP", "montant": "1.2Md USD", "annee": "2021"}
        ],
        "maturite_maximale": "Excellence = 70%+ des tâches répétitives automatisées, hyperautomatisation combinant RPA+IA, monitoring temps réel de tous les robots."
    },

    "PROCESS::Agilité": {
        "tendances": [
            {
                "titre": "Scaled Agile Framework (SAFe) dans les grandes banques",
                "description": "Les banques adoptent SAFe pour déployer l'agilité à grande échelle (100+ équipes). ING, BNP Paribas et Attijariwafa ont réalisé cette transformation.",
                "source": "Deloitte Agile Banking Survey 2024",
                "annee": "2024"
            },
            {
                "titre": "Digital Factory : séparation IT/Métier dépassée",
                "description": "Les banques leaders créent des squads pluridisciplinaires (tech + métier + UX + data) qui gèrent le produit de bout en bout, sans frontière IT/Métier.",
                "source": "McKinsey Agile at Scale 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'agilité dans les banques UEMOA est à ses débuts. La majorité des projets IT sont encore gérés en cycle en V (Waterfall). "
            "Quelques pilotes Scrum existent dans les grandes banques panafricaines mais sans transformation organisationnelle profonde. "
            "Délai moyen de mise en production d'une fonctionnalité : 6-18 mois (vs 2-4 semaines chez les leaders)."
        ),
        "leaders_nationaux": [
            {"entreprise": "Orabank", "pays": "Pan-UEMOA", "pratique": "Équipes Scrum déployées sur les projets digital depuis 2021", "source": "Orabank 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Digital Factory Rabat — 12 squads agiles, time-to-market réduit de 18 mois à 3 mois", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "ING Bank", "pays": "Pays-Bas", "pratique": "Transformation agile totale en 2015 (modèle Spotify) — référence mondiale, 13 000 employés en squads", "source": "ING Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Circulaire BCEAO sur la gouvernance des SI", "description": "Exigences de documentation et de contrôle des évolutions des systèmes d'information", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Jira/Atlassian — outils agile en SaaS, croissance de 30% en Afrique subsaharienne en 2023", "montant": "N/A", "annee": "2023"}
        ],
        "maturite_maximale": "Excellence = 100% des équipes produit en squads agiles, SAFe déployé, time-to-market <4 semaines, Digital Factory opérationnelle."
    },

    "PROCESS::Performance opérationnelle": {
        "tendances": [
            {
                "titre": "Tableaux de bord opérationnels temps réel",
                "description": "Les banques leaders déploient des 'control towers' numériques permettant au management de suivre en temps réel les KPIs opérationnels (SLA, taux d'échec, volumes) avec alertes automatiques.",
                "source": "Gartner Digital Operational Excellence 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Le pilotage de la performance opérationnelle en UEMOA repose encore largement sur des reportings Excel hebdomadaires. "
            "Les indicateurs de disponibilité des systèmes (uptime), de délai de traitement et de taux d'erreur sont rarement suivis en temps réel."
        ),
        "leaders_nationaux": [
            {"entreprise": "BNI Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Tableau de bord de pilotage des opérations avec revue hebdomadaire des KPIs", "source": "BNI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "KCB Group", "pays": "Kenya", "pratique": "Operations Control Center 24/7 avec monitoring temps réel de 500+ indicateurs", "source": "KCB 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Standard Chartered", "pays": "Royaume-Uni", "pratique": "Digital Operations Command Center — IA détectant les anomalies opérationnelles en <5 minutes", "source": "Standard Chartered 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Plan de Continuité d'Activité (PCA) BCEAO", "description": "Obligation de mesurer et garantir la continuité des services critiques", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = KPIs temps réel sur 100% des processus critiques, alertes automatiques, revue quotidienne des indicateurs, SLA client <1h."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 3 — SYSTÈME D'INFORMATION / INFORMATION_SYSTEM
    # ═══════════════════════════════════════════════════════════════

    "INFORMATION_SYSTEM::Infrastructure & Cloud": {
        "tendances": [
            {
                "titre": "Cloud souverain pour les données sensibles bancaires",
                "description": "Face aux exigences réglementaires de souveraineté des données, les banques africaines adoptent des stratégies cloud hybride avec datacenters locaux. AWS, Azure et Google ont ouvert des régions en Afrique du Sud et au Nigeria.",
                "source": "IDC Cloud Africa 2024",
                "annee": "2024"
            },
            {
                "titre": "Microservices et architecture event-driven",
                "description": "Le remplacement progressif des core banking monolithiques (Temenos, Finacle, Profile) par des architectures microservices permet une agilité 10x supérieure pour lancer de nouveaux produits.",
                "source": "Gartner Core Banking Modernization 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La majorité des banques UEMOA utilisent des core banking legacy (Temenos T24, Delta Bank, DELTA/XP). "
            "Le recours au cloud public est limité à moins de 20% des workloads en raison des restrictions réglementaires locales. "
            "La disponibilité moyenne des systèmes bancaires UEMOA est estimée à 97% (vs 99.99% pour les néobanques). "
            "Les systèmes de datacenter sont généralement locaux avec peu de redondance géographique."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Migration vers T24 cloud-native sur 35 pays — infrastructure unifiée et résiliente", "source": "Ecobank Tech Report 2023"},
            {"entreprise": "BICICI / BNP Paribas CI", "pays": "Côte d'Ivoire", "pratique": "Infrastructure partagée groupe BNP Paribas avec datacenter redondant", "source": "BICICI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Migration cloud hybride Azure complète en 2022, PCA testé mensuellement", "source": "CIH Bank 2023"},
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "Infrastructure 100% cloud AWS depuis 2021, uptime 99.98%", "source": "Equity Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "DBS Bank", "pays": "Singapour", "pratique": "100% cloud native sur AWS et Azure depuis 2022, zéro datacenter propriétaire, économies de 40%", "source": "DBS Annual Report 2023"},
            {"entreprise": "N26", "pays": "Allemagne", "pratique": "Architecture microservices sur GCP — 1500 déploiements/jour, 0 downtime en 2023", "source": "N26 Tech Blog 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Instruction BCEAO sur les exigences techniques des systèmes d'information bancaires", "description": "Exigences de disponibilité, de sécurité et de localisation des données dans l'UEMOA", "impact": "Obligation"},
            {"texte": "Règlement sur la résidence des données UEMOA", "description": "Certaines données critiques doivent résider dans l'espace UEMOA", "impact": "Contrainte"},
            {"texte": "PCA/PRA obligatoire BCEAO", "description": "Plan de Continuité d'Activité et Plan de Reprise d'Activité obligatoires pour les établissements de crédit", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Investissement", "detail": "AWS ouvre sa région Afrique du Sud (2020) et annonce une région Afrique de l'Ouest d'ici 2026", "montant": "N/A", "annee": "2020"},
            {"operation": "Levée de fonds", "detail": "Temenos (core banking cloud) lève 400M$ pour accélérer sa migration SaaS en Afrique", "montant": "400M USD", "annee": "2023"}
        ],
        "maturite_maximale": "Excellence = architecture cloud hybride certifiée, uptime >99.9%, microservices, déploiement continu (CI/CD), zéro datacenter legacy."
    },

    "INFORMATION_SYSTEM::Cybersécurité": {
        "tendances": [
            {
                "titre": "Zero Trust Architecture dans les banques",
                "description": "Le modèle Zero Trust ('ne jamais faire confiance, toujours vérifier') remplace le périmètre réseau traditionnel. Obligatoire pour les banques avec télétravail et cloud.",
                "source": "NIST Cybersecurity Framework 2024",
                "annee": "2024"
            },
            {
                "titre": "SOC (Security Operations Center) externalisé ou mutualisé",
                "description": "Les banques de taille moyenne adoptent les SOC-as-a-Service pour accéder à un monitoring 24/7 sans investissement massif. En Afrique, des acteurs comme Liquid Technologies proposent ces services.",
                "source": "Gartner Security Operations 2024",
                "annee": "2024"
            },
            {
                "titre": "Fraude mobile et deepfakes — nouvelles menaces",
                "description": "Les attaques sur les canaux mobiles bancaires ont augmenté de 150% en Afrique entre 2021 et 2023. Les deepfakes vocaux permettent de contourner les systèmes de biométrie vocale.",
                "source": "Interpol African Cyberthreat Assessment 2023",
                "annee": "2023"
            }
        ],
        "analyse_statique": (
            "La cybersécurité est le risque n°1 identifié par les DSI bancaires UEMOA (enquête BCEAO 2023). "
            "Les incidents majeurs en 2022-2023 : tentatives de fraude SWIFT sur plusieurs banques ouest-africaines. "
            "Moins de 30% des banques UEMOA disposent d'un SOC opérationnel. "
            "La certification ISO 27001 reste rare (moins de 10 établissements certifiés dans la zone)."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "SOC régional partagé, certification ISO 27001 obtenue en 2022 pour 15 filiales", "source": "Ecobank Tech 2023"},
            {"entreprise": "SGCI", "pays": "Côte d'Ivoire", "pratique": "Adossée à la politique sécurité groupe SG — Zero Trust déployé, SIEM opérationnel", "source": "SGCI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Safaricom / M-Pesa", "pays": "Kenya", "pratique": "Détection de fraude IA temps réel sur 50M+ transactions/jour, taux de fraude <0.001%", "source": "Safaricom Annual Report 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "JPMorgan Chase", "pays": "USA", "pratique": "600M$/an de budget cybersécurité, 3000 experts cyber, protection contre 45Mds d'attaques/jour", "source": "JPMorgan Annual Report 2023"},
            {"entreprise": "HSBC", "pays": "Royaume-Uni", "pratique": "IA de détection de fraude réduisant les faux positifs de 70%, biométrie comportementale déployée", "source": "HSBC Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Circulaire BCEAO sur la cybersécurité des établissements financiers (2021)", "description": "Exigences minimales de sécurité informatique pour tous les établissements de crédit UEMOA", "impact": "Obligation"},
            {"texte": "Loi sur les transactions électroniques UEMOA (2016)", "description": "Encadre la sécurité des transactions électroniques et la responsabilité en cas de fraude", "impact": "Conformité"},
            {"texte": "Directive NIS2 (référence internationale)", "description": "Standard de cybersécurité européen de référence pour les infrastructures critiques", "impact": "Référence"},
            {"texte": "ISO/IEC 27001", "description": "Standard international de management de la sécurité de l'information", "impact": "Référence"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Cybereason (cybersécurité) lève 325M$ — accélération des solutions de détection pour secteur financier", "montant": "325M USD", "annee": "2021"},
            {"operation": "Acquisition", "detail": "Mastercard acquiert RiskRecon (risk intelligence) pour renforcer la cybersécurité bancaire", "montant": "Non divulgué", "annee": "2020"}
        ],
        "maturite_maximale": "Excellence = ISO 27001 certifié, SOC 24/7 opérationnel, Zero Trust Architecture, Red Team annuel, détection fraude IA temps réel, DAST/SAST sur toutes les applications."
    },

    "INFORMATION_SYSTEM::Données & Analytics": {
        "tendances": [
            {
                "titre": "Data Lakehouse comme architecture de référence",
                "description": "L'architecture Data Lakehouse (Delta Lake, Apache Iceberg) unifie les usages analytiques et opérationnels sur une seule plateforme. Databricks et Snowflake s'imposent comme leaders.",
                "source": "Databricks State of Data + AI 2024",
                "annee": "2024"
            },
            {
                "titre": "IA générative sur les données bancaires internes",
                "description": "Les banques utilisent des LLMs fine-tunés sur leurs données internes pour automatiser le reporting, l'analyse de risque et le conseil client. ROI moyen : 15% de gain de productivité analytique.",
                "source": "McKinsey State of AI in Banking 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Les banques UEMOA souffrent de silos de données entre les systèmes core banking, CRM, monnaie électronique et reporting BCEAO. "
            "La qualité des données est un problème structurel : doublons clients estimés à 15-25%, adresses non normalisées, NIU manquants. "
            "Les outils analytiques déployés sont principalement des outils de reporting (Crystal Reports, Excel) sans capacité prédictive."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Data Warehouse centralisé Teradata sur 33 pays — reporting BCEAO automatisé", "source": "Ecobank Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Data Lake Azure Synapse — 50+ cas d'usage analytiques, scoring crédit IA avec 30% moins de défauts", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Ant Group (Alipay)", "pays": "Chine", "pratique": "Analyse de 1 milliard de transactions en temps réel, scoring crédit en 3 secondes pour 500M utilisateurs", "source": "Ant Group 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi sur la protection des données personnelles UEMOA", "description": "Encadre la collecte, le traitement et la conservation des données clients", "impact": "Obligation"},
            {"texte": "Reporting réglementaire BCEAO", "description": "Obligations de transmission de données financières mensuelles/trimestrielles à la Banque Centrale", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Snowflake IPO à 33Mds$ — accélération de l'adoption cloud data dans le secteur bancaire mondial", "montant": "3.4Mds USD IPO", "annee": "2020"}
        ],
        "maturite_maximale": "Excellence = Data Lakehouse unifié, gouvernance des données formalisée (Data Catalog, Data Quality), 20+ modèles IA en production, self-service analytics pour les métiers."
    },

    "INFORMATION_SYSTEM::Intégration & API": {
        "tendances": [
            {
                "titre": "API-first et Open Banking",
                "description": "L'approche API-first transforme les banques en plateformes. Les API Management Platforms (MuleSoft, Apigee, Kong) permettent d'exposer des centaines de services à des partenaires.",
                "source": "Gartner API Management 2024",
                "annee": "2024"
            },
            {
                "titre": "Event-driven architecture pour l'intégration temps réel",
                "description": "Kafka et les architectures event-driven permettent l'intégration en temps réel entre core banking, CRM, mobile et partenaires externes. Latence réduite de heures à millisecondes.",
                "source": "Confluent State of Data Streaming 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'intégration des systèmes bancaires UEMOA repose majoritairement sur des fichiers batch nocturnes (FTP, SFTP). "
            "L'intégration temps réel est rare. Les APIs REST publiques sont inexistantes dans la majorité des banques locales. "
            "Bizao et CinetPay proposent des couches d'intégration aux banques partenaires mais l'adoption reste limitée."
        ),
        "leaders_nationaux": [
            {"entreprise": "Bizao", "pays": "UEMOA / Côte d'Ivoire", "pratique": "Hub d'APIs bancaires permettant la connexion de 15+ banques UEMOA à l'écosystème fintech", "source": "Bizao 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Flutterwave", "pays": "Nigeria", "pratique": "Plateforme d'APIs de paiement couvrant 34 pays africains, 300M transactions/an", "source": "Flutterwave 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "BBVA", "pays": "Espagne", "pratique": "BBVA Open Platform — 1000+ APIs exposées, 3000+ développeurs partenaires, modèle BaaP", "source": "BBVA Open Platform 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Interopérabilité des systèmes de paiement UEMOA (BCEAO)", "description": "Obligation d'interopérabilité entre les systèmes de paiement des établissements", "impact": "Obligation"},
            {"texte": "Standard GIM-UEMOA", "description": "Normes d'interopérabilité pour les paiements interbancaires dans l'UEMOA", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Flutterwave lève 250M$ (Serie D) — valorisation 3Mds$, accélération API payments Afrique", "montant": "250M USD", "annee": "2022"}
        ],
        "maturite_maximale": "Excellence = API Gateway déployé, 50+ APIs documentées et exposées, intégration temps réel avec partenaires, developer portal public, SLA APIs >99.9%."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 4 — CANAUX DE DISTRIBUTION
    # ═══════════════════════════════════════════════════════════════

    "CANAUX_DISTRIBUTION::Canaux de distribution & expérience client": {
        "tendances": [
            {
                "titre": "Super-apps bancaires : tout en un",
                "description": "Les banques leaders transforment leur app mobile en super-app intégrant paiements, épargne, crédit, assurance et services non-financiers. WeChat Pay et M-Pesa sont les modèles africains.",
                "source": "McKinsey Digital Banking 2024",
                "annee": "2024"
            },
            {
                "titre": "Instant Payment et paiement en temps réel 24/7",
                "description": "Le virement instantané devient la norme mondiale. En UEMOA, le système STAR-UEMOA est opérationnel mais l'adoption par les clients reste limitée (<15% des virements).",
                "source": "BCEAO Rapport sur les systèmes de paiement 2023",
                "annee": "2023"
            },
            {
                "titre": "Agency Banking comme canal de proximité",
                "description": "Les agents bancaires (épiceries, stations-service, pharmacies équipées de TPE) permettent de bancariser les zones non couvertes. Au Sénégal, Wave a 100 000+ agents.",
                "source": "GSMA Mobile Money Africa 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Comparatif des services digitaux des banques ivoiriennes (source : étude terrain 2023) :\n"
            "- Internet Banking : BNI Online, Or@net, BOAweb, UBA Internet Banking, Ecobank Online, "
            "  BICICINET, Atlantique Net, ANET, BGFIOnline, CONNECT\n"
            "- Mobile Banking : BNI Online, B.FREE, MYBOA, UBA Mobile APP, Ecobank Mobile, "
            "  BICICIMOBILE, Atlantique Mobile, BGFIMobile, CONNECT\n"
            "- SMS Banking : Oramobile, B-SMS, UBA Alert-SMS, Ecobank via USSD, MOBIBANK, A Mobile, SMSBanking, MESSALIA\n"
            "Tarification : modèle quasi-gratuit (néobanques) → freemium (banques en ligne) → tout payant (banques réseau traditionnel). "
            "Tenue de compte : 1-2€/mois (banques en ligne) vs gratuit (néobanques). "
            "Virements SEPA : gratuits pour toutes les catégories."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank Mobile", "pays": "Côte d'Ivoire / UEMOA", "pratique": "App mobile avec 15+ fonctionnalités, disponible en 35 pays, interface en 4 langues", "source": "Ecobank 2023"},
            {"entreprise": "BNI Online", "pays": "Côte d'Ivoire", "pratique": "Internet + Mobile Banking avec consultation solde, virements, localisation GAB, gestion cartes", "source": "BNI 2023"},
            {"entreprise": "CONNECT (Coris Bank)", "pays": "UEMOA", "pratique": "Service omnicanal intégrant Internet, Mobile et SMS Banking avec simulateur de crédits", "source": "Coris Bank 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "M-Pesa (Safaricom)", "pays": "Kenya", "pratique": "50M utilisateurs actifs, 500+ services disponibles, 12% du PIB kényan transité via M-Pesa", "source": "Safaricom Annual Report 2023"},
            {"entreprise": "Wave", "pays": "Sénégal / UEMOA", "pratique": "Application mobile zero-fee, 8M utilisateurs en UEMOA, transferts instantanés à 1% de frais maximum", "source": "Wave 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Revolut", "pays": "Royaume-Uni", "pratique": "Super-app avec 35+ services (banking, crypto, travel, insurance), 35M clients dans 35 pays", "source": "Revolut Annual Report 2023"},
            {"entreprise": "N26", "pays": "Allemagne", "pratique": "100% digital, onboarding en 8 minutes, 7M clients, disponible dans 25 pays européens", "source": "N26 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi n°2016-012 (Mali) sur les transactions électroniques", "description": "Régit les transactions, échanges et services électroniques bancaires", "impact": "Obligation"},
            {"texte": "Loi n°2016-012 juillet 2018 (USSD)", "description": "Conditions d'ouverture et d'exploitation du canal USSD bancaire", "impact": "Obligation"},
            {"texte": "Règlement UEMOA sur les systèmes de paiement (2002)", "description": "Interopérabilité et sécurité des systèmes de paiement", "impact": "Conformité"},
            {"texte": "Directives BCEAO sur l'accessibilité des services bancaires", "description": "Obligations d'accessibilité des services de base pour les populations non bancarisées", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Wave (UEMOA) lève 200M$ Serie A — accélération réseau d'agents et couverture géographique", "montant": "200M USD", "annee": "2021"},
            {"operation": "Partenariat", "detail": "Orabank x Mastercard — déploiement de solutions de paiement digital dans 12 pays UEMOA", "montant": "N/A", "annee": "2022"},
            {"operation": "Acquisition", "detail": "Orange acquiert Groupama Banque pour étendre son offre bancaire mobile en Afrique francophone", "montant": "Non divulgué", "annee": "2023"}
        ],
        "maturite_maximale": (
            "Excellence = super-app bancaire avec 20+ services intégrés, onboarding 100% digital <10 minutes, "
            "paiement instantané 24/7, réseau d'agents capillaire, expérience omnicanale sans rupture, "
            "notation store >4.5/5."
        )
    },

    "CANAUX_DISTRIBUTION::Selfcare client": {
        "tendances": [
            {
                "titre": "Chatbots bancaires et assistants virtuels IA",
                "description": "Les chatbots IA (basés sur GPT-4, Claude) traitent jusqu'à 85% des demandes clients sans intervention humaine. Capital One (Eno), Bank of America (Erica) et Société Générale (Djingo) sont références.",
                "source": "Gartner Conversational AI Banking 2024",
                "annee": "2024"
            },
            {
                "titre": "Autonomisation complète du client (full selfcare)",
                "description": "Les clients veulent tout faire seuls : ouvrir un compte, commander une carte, faire opposition, modifier des plafonds, sans appeler la banque. Les banques full selfcare réduisent leur coût de service de 60%.",
                "source": "Forrester Customer Service Index 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Les fonctionnalités selfcare disponibles dans les banques ivoiriennes (enquête 2023) :\n"
            "Internet Banking : consultation solde (100%), virements (95%), relevé RIB (60%), opposition carte (40%), simulation crédit (30%)\n"
            "Mobile Banking : consultation (100%), virement (85%), gestion carte (55%), simulation crédit (30%)\n"
            "Selfcare avancé (modification plafonds, souscription en ligne, réclamation digitale) : disponible dans moins de 20% des banques testées.\n"
            "Capital One 'Eno' : anticipe les besoins client, alerte sur les abonnements, détecte les opérations suspectes — modèle de référence."
        ),
        "leaders_nationaux": [
            {"entreprise": "Atlantique Banque", "pays": "Côte d'Ivoire", "pratique": "Reconnaissance faciale pour l'authentification mobile, selfcare carte prépayée", "source": "Atlantique Banque 2023"},
            {"entreprise": "BGFIBank", "pays": "Gabon / CI", "pratique": "BGFIMobile avec demande de rendez-vous, virement compte virtuel, selfcare complet", "source": "BGFI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "KCB Group", "pays": "Kenya", "pratique": "KCB Mobi — 95% des opérations disponibles en selfcare 24/7 sans assistance humaine", "source": "KCB 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Capital One", "pays": "USA", "pratique": "Eno — assistant virtuel qui gère 40M de clients, anticipe les besoins, détecte fraudes en mode supervisé", "source": "Capital One Annual Report 2023"},
            {"entreprise": "Bank of America", "pays": "USA", "pratique": "Erica — 37M utilisateurs actifs, 1.5Md d'interactions en 2023, satisfaction client +28 points NPS", "source": "BofA Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Réglementation e-KYC BCEAO", "description": "Conditions d'identification électronique des clients pour l'onboarding digital", "impact": "Obligation"},
            {"texte": "Loi sur la signature électronique UEMOA", "description": "Valeur juridique des signatures et consentements électroniques dans les actes bancaires", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Smile ID (e-KYC Afrique) lève 20M$ pour déployer la vérification d'identité digitale dans 20 pays africains", "montant": "20M USD", "annee": "2023"}
        ],
        "maturite_maximale": "Excellence = 95%+ opérations disponibles en selfcare 24/7, assistant virtuel IA, onboarding 100% digital, aucune visite en agence requise pour les opérations courantes."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 5 — MARKETING & COMMUNICATION
    # ═══════════════════════════════════════════════════════════════

    "MARKETING_COMMUNICATION::Marketing & communication digitale": {
        "tendances": [
            {
                "titre": "Marketing automation et personnalisation à grande échelle",
                "description": "Les plateformes de marketing automation (Salesforce Marketing Cloud, HubSpot, Adobe Experience Cloud) permettent des parcours clients entièrement automatisés avec personnalisation temps réel.",
                "source": "HubSpot State of Marketing 2024",
                "annee": "2024"
            },
            {
                "titre": "Réseaux sociaux comme canal d'acquisition bancaire",
                "description": "En Afrique de l'Ouest, Facebook et WhatsApp sont les canaux digitaux dominants (pénétration >60% des internautes). Les banques leaders gèrent des communautés de 500K+ abonnés.",
                "source": "We Are Social Digital Report Africa 2024",
                "annee": "2024"
            },
            {
                "titre": "Mesure du ROI digital et attribution multicanal",
                "description": "Les outils d'attribution (Google Analytics 4, Adobe Analytics) permettent de mesurer précisément l'impact de chaque canal sur l'acquisition et la rétention. ROI moyen du marketing digital bancaire : 3-5x.",
                "source": "Google Marketing Insights 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Positionnement des banques ivoiriennes sur les réseaux sociaux (septembre 2022) :\n\n"
            "FACEBOOK : Société Générale CI (1M abonnés, 4/semaine), UBA CI (125K, 10/semaine), Coris Bank (88K, 10/semaine), "
            "Orabank (547K, 2/semaine), BNI (50K, 2/semaine), Ecobank (48K, 2/semaine), NISA Banque (133K, 1/semaine)\n\n"
            "LINKEDIN : Orabank (136K, 6/semaine), CORIS BANK (10K, 10/semaine), UBA CI (41K, 10/semaine), "
            "Société Générale (103K, 3/semaine), NISA (100K, 1/semaine)\n\n"
            "TWITTER : Ecobank (40.2K, présente), UBA CI (2.4K, présente), BNI (1.3K, présente), SGCI (5.3K, présente)\n\n"
            "YOUTUBE : Ecobank (5.4K abonnés), SGCI (4.8K), CORIS BANK (621), Afriland First Bank (présente)\n\n"
            "Banques INACTIVES sur au moins 2 réseaux : CIM Bank, BRM CI, BMS-CI, BOA CI\n\n"
            "Site de référence en marketing digital bancaire : BNP Paribas (mabanque.bnpparibas) — "
            "éléments remarquables : CTA optimisés, menu sticky 3 niveaux, espace 'Ma Banque en pratique', selfcare didacticiel, "
            "proposition de valeur claire pour l'ouverture de compte."
        ),
        "leaders_nationaux": [
            {"entreprise": "Société Générale CI", "pays": "Côte d'Ivoire", "pratique": "Présence active sur 4 réseaux sociaux, 1M abonnés Facebook, stratégie de contenu alignée avec la marque groupe", "source": "Enquête terrain 2022"},
            {"entreprise": "Orabank", "pays": "Pan-UEMOA", "pratique": "136K abonnés LinkedIn, 547K Facebook — meilleure présence sociale de la zone UEMOA", "source": "Enquête terrain 2022"},
            {"entreprise": "UBA Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Fréquence de publication la plus élevée (10/semaine sur Facebook et LinkedIn)", "source": "Enquête terrain 2022"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Marketing automation Salesforce MC, 3M emails personnalisés/mois, taux d'ouverture de 35%", "source": "Attijariwafa 2023"},
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Campagnes digitales ROI mesuré, 40% des nouvelles souscriptions via canaux digitaux", "source": "CIH Bank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "BNP Paribas", "pays": "France", "pratique": "Plateforme e-commerce banque complète, UX primée, NPS digital de +32", "source": "BNP Paribas Digital 2023"},
            {"entreprise": "Revolut", "pays": "Royaume-Uni", "pratique": "Growth hacking 100% digital — 35M clients acquis sans agence, CAC de 12€, viral loop intégré", "source": "Revolut 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi sur la publicité et la communication commerciale électronique (UEMOA)", "description": "Encadre les communications marketing électroniques — opt-in obligatoire", "impact": "Obligation"},
            {"texte": "Protection des données personnelles dans le marketing", "description": "Consentement explicite requis pour l'utilisation des données à des fins marketing", "impact": "Obligation"},
            {"texte": "Réglementation BCEAO sur la publicité bancaire", "description": "Obligations d'information dans les communications publicitaires bancaires", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "HubSpot (marketing automation) valorisé à 20Mds$ — adoption croissante dans les banques africaines", "montant": "N/A", "annee": "2023"},
            {"operation": "Partenariat", "detail": "Meta x banques UEMOA — programme de formation au marketing digital pour 50 institutions financières", "montant": "N/A", "annee": "2022"}
        ],
        "maturite_maximale": (
            "Excellence = présence active sur 5+ réseaux sociaux, publication quotidienne, marketing automation déployé, "
            "ROI mesuré par canal, NPS digital >30, taux d'acquisition digital >40%, "
            "dispositif d'écoute client en temps réel (NPS in-app, suivi stores, social listening)."
        )
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 6 — RH & CULTURE DIGITALE
    # ═══════════════════════════════════════════════════════════════

    "RH_CULTURE_DIGITALE::Culture digitale": {
        "tendances": [
            {
                "titre": "Digital Academy interne comme actif stratégique",
                "description": "Les banques leaders créent des académies digitales internes (BNP Paribas Digital Academy, Société Générale Campus Digital) formant 100% des collaborateurs aux fondamentaux digitaux.",
                "source": "LinkedIn Workplace Learning Report 2024",
                "annee": "2024"
            },
            {
                "titre": "Parcours de certification digitale pour les banquiers",
                "description": "Les certifications digitales (Google Digital Garage, Microsoft Digital Skills, certifications internes) deviennent des critères d'évaluation annuelle dans les banques avancées.",
                "source": "WEF Future of Jobs Report 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'acculturation digitale des collaborateurs bancaires UEMOA est un chantier prioritaire mais sous-financé. "
            "Les formations digitales se limitent souvent aux outils bureautiques (Word, Excel) sans aller vers les nouvelles pratiques (data, IA, agilité). "
            "Moins de 20% des collaborateurs ont accès à des programmes de formation digitale structurés."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Ecobank Academy — plateforme de formation en ligne pour 15 000 collaborateurs dans 35 pays", "source": "Ecobank Report 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Campus digital interne — 100% des collaborateurs formés aux fondamentaux digitaux en 2022", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "BNP Paribas", "pays": "France", "pratique": "BNP Paribas Digital Academy — 190 000 collaborateurs formés, 100h de formation digitale/an/collaborateur", "source": "BNP Paribas Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Obligation légale de formation professionnelle continue (droit du travail UEMOA)", "description": "Obligation de maintien des compétences des salariés", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = Digital Academy interne, 100% collaborateurs formés aux fondamentaux digitaux, certifications obligatoires, mesure de l'impact de la formation."
    },

    "RH_CULTURE_DIGITALE::Poste de travail du banquier": {
        "tendances": [
            {
                "titre": "Conseiller augmenté par l'IA",
                "description": "Les conseillers bancaires utilisent des outils IA qui leur suggèrent en temps réel les produits adaptés au client, les risques à signaler et les argumentaires optimaux. Réduction du temps de préparation de 70%.",
                "source": "Accenture Banking Technology Vision 2024",
                "annee": "2024"
            },
            {
                "titre": "Tablette conseiller et poste de travail unifié",
                "description": "Le poste de travail du conseiller évolue vers une interface unique (CRM + core banking + document management) accessible sur tablette, permettant de servir le client n'importe où en agence.",
                "source": "Capgemini World Retail Banking Report 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Les conseillers bancaires UEMOA utilisent généralement des terminaux fixes avec 3-5 applications différentes "
            "(core banking, messagerie, reporting, outil crédit) sans intégration. "
            "Le temps de préparation avant un entretien client est estimé à 45-60 minutes faute d'outils unifiés. "
            "Peu de banques ont déployé des tablettes conseillers ou des outils de proposition automatique."
        ),
        "leaders_nationaux": [
            {"entreprise": "Société Générale CI", "pays": "Côte d'Ivoire", "pratique": "Poste de travail conseiller unifié déployé en 2022 avec accès CRM Salesforce", "source": "SGCI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Tablettes conseillers avec CRM 360° intégré — temps de traitement client réduit de 40%", "source": "CIH Bank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "HSBC", "pays": "Royaume-Uni", "pratique": "Relationship Manager Tool IA — suggestions automatiques au conseiller pendant l'entretien client", "source": "HSBC Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Réglementation sur le devoir de conseil bancaire (UEMOA)", "description": "Obligation de proposer des produits adaptés au profil du client", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = poste de travail unifié, tablette conseiller, suggestions IA temps réel, CRM 360° intégré, zéro ressaisie."
    },

    "RH_CULTURE_DIGITALE::Collaboratif & digital working": {
        "tendances": [
            {
                "titre": "Digital Workplace comme standard post-COVID",
                "description": "Microsoft 365, Google Workspace et Slack sont devenus les standards de la collaboration digitale. Les banques qui n'ont pas déployé ces outils perdent en attractivité face aux talents tech.",
                "source": "Gartner Digital Workplace Survey 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Le déploiement d'outils collaboratifs dans les banques UEMOA a été accéléré par le COVID-19 en 2020. "
            "Microsoft Teams est l'outil le plus adopté (60% des grandes banques). "
            "Le télétravail reste limité à moins de 10% des jours travaillés en moyenne."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Microsoft 365 déployé sur 35 pays, Teams utilisé quotidiennement par 15 000 collaborateurs", "source": "Ecobank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "ING Bank", "pays": "Pays-Bas", "pratique": "100% remote-ready depuis 2020, collaboration asynchrone avec Slack + Miro + Confluence", "source": "ING 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Réglementation sur le télétravail (droit du travail UEMOA)", "description": "Cadre juridique du télétravail en cours de définition dans plusieurs pays membres", "impact": "Conformité"},
            {"texte": "Sécurité des accès distants (Circulaire BCEAO)", "description": "Exigences de sécurité pour les accès distants aux systèmes d'information bancaires", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = Digital Workplace déployé (M365/Google Workspace), télétravail sécurisé possible pour 80% des postes, outils collaboratifs utilisés quotidiennement."
    },

    "RH_CULTURE_DIGITALE::Digitalisation de la fonction RH": {
        "tendances": [
            {
                "titre": "SIRH cloud et expérience collaborateur",
                "description": "Les SIRH cloud (Workday, SAP SuccessFactors, Oracle HCM) unifient la gestion RH et améliorent l'expérience collaborateur. Self-service RH : 80% des demandes traitées sans intervention HR.",
                "source": "Gartner HR Technology Hype Cycle 2024",
                "annee": "2024"
            },
            {
                "titre": "Recrutement digital et marque employeur tech",
                "description": "LinkedIn, les job boards spécialisés fintech et les hackathons de recrutement deviennent les canaux prioritaires. Les banques qui recrutent des profils tech doivent rivaliser avec les GAFAM.",
                "source": "LinkedIn Talent Insights Banking 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La digitalisation RH dans les banques UEMOA est à ses débuts. "
            "La majorité des processus RH (paie, congés, évaluations) sont encore gérés sur des outils locaux peu intégrés. "
            "La gestion des compétences digitales n'est pas encore formalisée dans les référentiels métiers."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "SAP SuccessFactors déployé sur 35 pays — gestion unifiée de 15 000 collaborateurs", "source": "Ecobank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Goldman Sachs", "pays": "USA", "pratique": "Recrutement tech via hackathons internes, marque employeur #1 fintech selon LinkedIn 2023", "source": "Goldman Sachs 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Code du travail UEMOA — obligations de formation", "description": "Obligation légale de formation et de développement des compétences", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = SIRH cloud unifié, 100% processus RH digitalisés, marque employeur digitale forte, référentiel de compétences digitales formalisé."
    },

    "RH_CULTURE_DIGITALE::Agilité": {
        "tendances": [
            {
                "titre": "Digital Factory bancaire",
                "description": "La Digital Factory réunit des squads pluridisciplinaires (tech + métier + UX + data) pour lancer des produits digitaux en cycles courts (2-6 semaines). Attijariwafa, CIH Bank et BNP Paribas ont lancé leurs factories.",
                "source": "McKinsey Agile Banking 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'organisation agile dans les banques UEMOA est embryonnaire. "
            "Les projets IT suivent encore largement un cycle en V avec des durées de 12-18 mois. "
            "Les banques qui ont expérimenté le Scrum le font sur des périmètres limités sans transformation organisationnelle globale."
        ),
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Digital Factory opérationnelle depuis 2020 — 200 collaborateurs, 15 squads, time-to-market 10x réduit", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "ING Bank", "pays": "Pays-Bas", "pratique": "Organisation agile complète depuis 2015, 13 000 collaborateurs en squads, référence mondiale", "source": "ING 2023"}
        ],
        "cadre_juridique": [],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = Digital Factory opérationnelle, 100% projets produit en agilité, time-to-market <6 semaines, design sprints systématiques, UX Lab interne."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 7 — OFFRES DIGITALES
    # ═══════════════════════════════════════════════════════════════

    "OFFRES_DIGITALES::Offres digitales": {
        "tendances": [
            {
                "titre": "Néobanques et banques en ligne comme nouveau standard",
                "description": "Les néobanques africaines (Kuda, TymeBank, Umba) offrent des comptes ouverts en 5 minutes, sans frais. Elles capturent 20% des nouveaux clients bancaires en Afrique subsaharienne.",
                "source": "BCG Neobanking Africa Report 2024",
                "annee": "2024"
            },
            {
                "titre": "Robot-advisor et conseil financier automatisé",
                "description": "Les services de conseil automatisé (agrégation patrimoniale, simulation épargne, coaching dépenses) réduisent le coût du conseil et démocratisent l'accès à la planification financière.",
                "source": "Deloitte Wealth Management Digital 2024",
                "annee": "2024"
            },
            {
                "titre": "BNPL (Buy Now Pay Later) et micro-crédit digital",
                "description": "Le crédit instantané embarqué dans les parcours d'achat connaît une croissance de 200% en Afrique. M-Shwari (Kenya), Orange Money Crédit et Sama Money (Mali) sont les pionniers.",
                "source": "GSMA Digital Credit Africa 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Offres digitales des banques ivoiriennes (2023) :\n\n"
            "CARTES BANCAIRES : BNI (débit+prépayée), Orabank (débit+prépayée), Bank of Africa (débit), "
            "UBA (débit+prépayée), Ecobank (débit+prépayée+E-Payment+M-Payment), BICICI (débit+M-Payment), "
            "Banque Atlantique (débit+prépayée+E-Payment+packs), BGFI (débit+prépayée), "
            "ONSIA (débit+prépayée+E-Payment+M-Payment), SIB (débit+prépayée+E-Payment)\n\n"
            "SERVICES DIGITAUX RETAIL : SIB (Money Gram + SIBNET + SIB SMS + simulateur crédits), "
            "Banque Populaire (Banking Online + SMS Banking + simulateurs), "
            "GTCO (GIM UEMOA MC + SKS Ados + NRI + MasterCard GTCrea8 + 737# Simple + GT World cote)\n\n"
            "SERVICES DIGITAUX CORPORATE : BNI (BNI Online + CREALLIA + E-CNPS + DAILY MAIL + SWIFT BNI), "
            "Orabank (KIT TPE/mPOS + WeCollect UEMOA + convertisseur devise), "
            "UBA (UBA Business Direct + E-Statement + self service client complet)"
        ),
        "leaders_nationaux": [
            {"entreprise": "BNI Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "Gamme digitale complète : BNI Online, CREALLIA (offres entreprise), E-CNPS, plateforme SWIFT intégrée", "source": "BNI 2023"},
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Mobile money intégré, E-Payment, M-Payment (Bank to Wallet) disponibles sur toute la zone UEMOA", "source": "Ecobank 2023"},
            {"entreprise": "UBA Côte d'Ivoire", "pays": "Côte d'Ivoire", "pratique": "UBA Business Direct — gestion de compte Corporate en temps réel, self-service client étendu", "source": "UBA 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "TymeBank", "pays": "Afrique du Sud", "pratique": "Néobanque 100% digitale — ouverture de compte en 5 minutes, 5M clients en 3 ans, BNPL intégré", "source": "TymeBank 2023"},
            {"entreprise": "Kuda Bank", "pays": "Nigeria", "pratique": "Néobanque zéro frais — 5M clients, micro-crédit automatique, épargne automatique basée sur les dépenses", "source": "Kuda 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Revolut", "pays": "Royaume-Uni", "pratique": "35+ produits financiers intégrés : compte, crypto, trading, assurance voyage, prêts — 35M clients", "source": "Revolut 2023"},
            {"entreprise": "Nubank", "pays": "Brésil", "pratique": "100M clients, zéro agence, carte sans frais, crédit IA — valorisation de 30Mds$", "source": "Nubank Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Instruction BCEAO n°008-05-2015 sur la monnaie électronique", "description": "Conditions d'agrément et d'exercice des activités de monnaie électronique", "impact": "Obligation"},
            {"texte": "Loi n°2016-012 sur les services électroniques", "description": "Régit les services bancaires en ligne et les obligations associées", "impact": "Obligation"},
            {"texte": "Réglementation sur le crédit à la consommation digital (BCEAO)", "description": "Encadre les conditions d'octroi de crédit via les canaux digitaux", "impact": "Conformité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Kuda Bank (Nigeria) lève 55M$ Serie B — néobanque africaine leader", "montant": "55M USD", "annee": "2021"},
            {"operation": "Levée de fonds", "detail": "Carbon (fintech crédit digital) lève 15M$ pour déployer le micro-crédit en UEMOA", "montant": "15M USD", "annee": "2022"},
            {"operation": "Acquisition", "detail": "Wave acquiert les actifs de Free Money (Sénégal) pour consolider sa position mobile money UEMOA", "montant": "Non divulgué", "annee": "2023"}
        ],
        "maturite_maximale": (
            "Excellence = offres nativement digitales avec souscription 100% en ligne, "
            "robot-advisor opérationnel, micro-crédit automatique en <24h, "
            "wallet digital intégré, BNPL disponible sur parcours d'achat."
        )
    },

    "OFFRES_DIGITALES::Open banking (BaaS, BaaP)": {
        "tendances": [
            {
                "titre": "Banking-as-a-Platform (BaaP) : la banque comme écosystème",
                "description": "Les banques exposent leurs APIs pour permettre à des tiers (fintechs, retailers, opérateurs télécom) d'intégrer des services bancaires dans leurs propres applications. Marché mondial BaaS : 7Mds$ en 2026.",
                "source": "McKinsey Open Banking 2024",
                "annee": "2024"
            },
            {
                "titre": "Collaboration banque-fintech : de la compétition au partenariat",
                "description": "70% des banques mondiales ont établi des partenariats stratégiques avec des fintechs en 2023, contre 30% en 2020. Le modèle coopétition s'impose.",
                "source": "BCG Fintech Control Tower 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "L'open banking en UEMOA est à un stade précoce. "
            "Bizao (UEMOA) est la seule plateforme d'APIs bancaires mutualisées opérationnelle. "
            "Les partenariats banque-fintech se développent mais restent souvent informels (sans API formalisée). "
            "La monétisation des données via APIs est inexistante dans les banques UEMOA. "
            "Quelques banques ont des intégrations avec Orange Money/MTN Money pour les virements cross-canal."
        ),
        "leaders_nationaux": [
            {"entreprise": "Bizao", "pays": "UEMOA / Côte d'Ivoire", "pratique": "Connecteur API banking pour 15+ banques UEMOA, interface standardisée mobile money + banking", "source": "Bizao 2023"},
            {"entreprise": "CinetPay", "pays": "Côte d'Ivoire", "pratique": "Agrégateur de paiements avec APIs ouvertes — 1000+ marchands connectés en UEMOA", "source": "CinetPay 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Flutterwave", "pays": "Nigeria", "pratique": "APIs de paiement pour 34 pays africains, intégrations avec 200+ banques africaines", "source": "Flutterwave 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "BBVA", "pays": "Espagne", "pratique": "BBVA Open Platform — 1000+ APIs exposées, 3000+ développeurs partenaires, BaaP leader en Europe", "source": "BBVA 2023"},
            {"entreprise": "Starling Bank", "pays": "Royaume-Uni", "pratique": "BaaS pur — infrastructure bancaire pour 30+ fintechs européennes, 3Mds£ d'actifs gérés pour tiers", "source": "Starling 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Sandbox réglementaire BCEAO (2022)", "description": "Cadre expérimental permettant aux fintechs de tester des services innovants sous supervision BCEAO", "impact": "Opportunité"},
            {"texte": "Agrément établissement de paiement BCEAO", "description": "Obligation d'agrément pour toute activité de services de paiement pour compte de tiers", "impact": "Obligation"},
            {"texte": "DSP2 européenne (référence internationale)", "description": "Directive qui impose l'open banking en Europe — modèle de référence pour les régulateurs africains", "impact": "Référence"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Bizao lève 8.2M€ pour déployer l'open banking en Afrique francophone", "montant": "8.2M EUR", "annee": "2022"},
            {"operation": "Partenariat", "detail": "BCEAO x BIS (Banque des Règlements Internationaux) — projet pilote open banking UEMOA 2024-2025", "montant": "N/A", "annee": "2024"}
        ],
        "maturite_maximale": "Excellence = Developer Portal public avec 50+ APIs documentées, partenariats fintechs actifs, revenus API >5% du total, modèle BaaS ou BaaP opérationnel."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 8 — MODÈLE OPÉRATIONNEL & INNOVATION
    # ═══════════════════════════════════════════════════════════════

    "MODELE_OPERATIONNEL_INNOVATION::Simplification & automatisation des processus": {
        "tendances": [
            {
                "titre": "Dématérialisation totale des dossiers bancaires",
                "description": "Les banques leaders visent le zéro papier : dossiers de crédit 100% digitaux, signatures électroniques, archivage GED conforme. Réduction des coûts de traitement de 70%.",
                "source": "Capgemini Digital Banking Report 2024",
                "annee": "2024"
            },
            {
                "titre": "Workflows intelligents et automatisation cognitive",
                "description": "Les plateformes de low-code/no-code (ServiceNow, Appian) permettent aux métiers de créer leurs propres workflows automatisés sans passer par l'IT, réduisant les délais de digitalisation.",
                "source": "Gartner Low-Code Magic Quadrant 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La dématérialisation dans les banques UEMOA progresse mais reste incomplète. "
            "Les processus les plus avancés : ordres de virement (70% digitalisés), relevés de compte (90% digitaux). "
            "Les processus les moins avancés : dossiers de crédit (30% digitaux), KYC (20% digital), ouverture de compte (15% digital en ligne). "
            "Le GED (Gestion Électronique des Documents) est déployé dans moins de 40% des banques UEMOA."
        ),
        "leaders_nationaux": [
            {"entreprise": "Société Générale CI", "pays": "Côte d'Ivoire", "pratique": "Dossier de crédit dématérialisé, RPA sur le rapprochement bancaire, workflows automatisés", "source": "SGCI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "100% des processus back-office dématérialisés, GED Documentum déployé, zéro papier en agence", "source": "Attijariwafa 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "ING Bank", "pays": "Pays-Bas", "pratique": "1 200 robots RPA en production, hyperautomatisation combinant RPA + IA + BPM, 30% d'économies", "source": "ING 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi sur la signature électronique (UEMOA)", "description": "Valeur juridique de la signature électronique dans les actes bancaires", "impact": "Opportunité"},
            {"texte": "Archivage électronique à valeur probante", "description": "Conditions de validité juridique de l'archivage électronique des documents bancaires", "impact": "Conformité"},
            {"texte": "Règlement sur la dématérialisation des paiements BCEAO", "description": "Obligations progressives de dématérialisation des moyens de paiement", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "ServiceNow valorisé à 110Mds$ — leader mondial de l'automatisation des workflows d'entreprise", "montant": "N/A", "annee": "2023"}
        ],
        "maturite_maximale": "Excellence = 90%+ processus dématérialisés, zéro papier en agence, RPA sur toutes les tâches répétitives, workflows low-code déployés par les métiers."
    },

    "MODELE_OPERATIONNEL_INNOVATION::Gouvernance de la transformation digitale": {
        "tendances": [
            {
                "titre": "Transformation digitale portée par le COMEX",
                "description": "Les transformations digitales réussies sont celles portées directement par le CEO et le COMEX. 70% des projets qui échouent manquent de sponsoring exécutif (McKinsey 2024).",
                "source": "McKinsey Digital Transformation Survey 2024",
                "annee": "2024"
            },
            {
                "titre": "Budget digital dédié et suivi ROI",
                "description": "Les banques avancées allouent 15-25% de leur budget total aux investissements digitaux avec un tableau de bord de ROI spécifique, présenté trimestriellement au Conseil d'Administration.",
                "source": "Deloitte Banking Transformation ROI 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La gouvernance de la transformation digitale dans les banques UEMOA est souvent portée par la DSI "
            "sans mandat stratégique fort du COMEX. "
            "Le budget digital est rarement isolé du budget IT global. "
            "Les KPIs de transformation (taux de digitalisation, NPS digital, revenus digitaux) sont peu suivis formellement."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "CDO au COMEX depuis 2020, comité digital mensuel, reporting transformation trimestriel au CA", "source": "Ecobank 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Feuille de route digitale 5 ans publiée, budget digital 25% du total investissement, CDO depuis 2018", "source": "CIH Bank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "DBS Bank", "pays": "Singapour", "pratique": "CEO Piyush Gupta champion personnel de la transformation — DBS reconnu 'Most Digital Bank' 8 ans consécutifs", "source": "Euromoney 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Circulaire BCEAO sur la gouvernance des établissements de crédit", "description": "Obligations de gouvernance d'entreprise incluant la surveillance des risques IT et digitaux", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [],
        "maturite_maximale": "Excellence = CDO au COMEX, budget digital dédié >15% OPEX, feuille de route publiée, KPIs de transformation suivis mensuellement, reporting CA trimestriel."
    },

    "MODELE_OPERATIONNEL_INNOVATION::Développement de l'innovation": {
        "tendances": [
            {
                "titre": "Écosystème d'innovation fintech en UEMOA",
                "description": "L'UEMOA compte 120+ fintechs actives en 2023. Les secteurs les plus dynamiques : paiements mobiles (40%), crédit digital (25%), assurance (15%), épargne (10%). Le sandbox BCEAO crée un cadre favorable.",
                "source": "AfriQore Fintech Census 2023",
                "annee": "2023"
            },
            {
                "titre": "Hackathons et open innovation bancaire",
                "description": "Les banques organisent des hackathons pour identifier les talents et les solutions innovantes. Ecobank et UBA organisent des challenges fintechs régionaux annuels.",
                "source": "Ecobank Fintech Challenge Report 2023",
                "annee": "2023"
            }
        ],
        "analyse_statique": (
            "La veille concurrentielle digitale est peu structurée dans les banques UEMOA. "
            "Les benchmarks formels (comme ce document Hsys) sont réalisés par des cabinets externes, pas en interne. "
            "Les partenariats fintechs existent mais de façon ad hoc, sans programme structuré. "
            "Seules Ecobank et UBA ont des programmes d'innovation ouverte formalisés à l'échelle régionale."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Ecobank Fintech Challenge annuel — 50 startups sélectionnées, 5 intégrées en partenariat en 2023", "source": "Ecobank 2023"},
            {"entreprise": "UBA", "pays": "Pan-UEMOA", "pratique": "UBA Hackathon Africa annuel, fonds d'innovation de 2M$ pour les startups partenaires", "source": "UBA 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "Equity Innovation Centre — accélérateur de 200 startups depuis 2018, 15 produits co-développés", "source": "Equity 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "Citi Ventures", "pays": "USA", "pratique": "Bras d'investissement Citi dans 100+ startups fintech mondiales, 500M$ investis", "source": "Citi Annual Report 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Sandbox réglementaire BCEAO (2022)", "description": "Bac à sable réglementaire permettant aux fintechs de tester des services innovants", "impact": "Opportunité"},
            {"texte": "Stratégie Régionale d'Inclusion Financière UEMOA 2022-2026", "description": "Programme d'accélération de l'innovation financière dans la zone", "impact": "Opportunité"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Wave (UEMOA, 1er licorne fintech d'Afrique francophone) valorisée à 1.7Mds$ après 200M$", "montant": "200M USD", "annee": "2021"},
            {"operation": "Levée de fonds", "detail": "Julaya (paiements B2B UEMOA) lève 5M$ pour accélérer sa croissance", "montant": "5M USD", "annee": "2022"}
        ],
        "maturite_maximale": "Excellence = programme d'innovation ouvert formalisé, hackathon annuel, 5+ partenariats fintechs actifs, veille concurrentielle mensuelle, fonds d'innovation dédié."
    },

    # ═══════════════════════════════════════════════════════════════
    # AXE 9 — IT & DATA
    # ═══════════════════════════════════════════════════════════════

    "IT_DATA::Socle IT": {
        "tendances": [
            {
                "titre": "Migration des core banking vers le cloud natif",
                "description": "Temenos, Mambu et Thought Machine proposent des core banking 100% cloud-native. La migration permet de réduire les coûts d'infrastructure de 40% et d'accélérer le time-to-market de 80%.",
                "source": "Gartner Core Banking Modernization 2024",
                "annee": "2024"
            },
            {
                "titre": "Architecture micro-services et API-first dans les banques",
                "description": "Le découpage du monolithe bancaire en micro-services permet une évolutivité et une résilience incomparables. Les banques natives digitales déploient 1500 fois par jour (N26).",
                "source": "CNCF State of Cloud Native Banking 2024",
                "annee": "2024"
            },
            {
                "titre": "IA et IoT comme nouvelles technologies bancaires",
                "description": "L'IA de scoring crédit, la détection de fraude temps réel et les capteurs IoT (assurance comportementale) transforment les produits et services bancaires. Investissement mondial IA bancaire : 35Mds$ en 2024.",
                "source": "IDC Worldwide AI Banking Forecast 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "Les infrastructures IT des banques UEMOA sont dominées par des core banking legacy des années 2000 "
            "(Temenos T24 version ancienne, Delta Bank, Profile). "
            "Le recours au cloud est limité à <20% des workloads. "
            "La dette technique est estimée à 60-70% du budget IT annuel pour la maintenance. "
            "Les architectures API sont embryonnaires. "
            "Investissement IT moyen des banques UEMOA : 3-5% du PNB (vs 10-15% pour les banques digitales mondiales). "
            "\nInfrastructure cloud en Afrique :\n"
            "- AWS : région Afrique du Sud (2020), annonce Afrique de l'Ouest d'ici 2026\n"
            "- Azure : datacenter Afrique du Sud + Nigéria\n"
            "- Google Cloud : région Afrique du Sud depuis 2021"
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Migration T24 cloud sur 35 pays, infrastructure mutualisée régionale, 99.5% uptime", "source": "Ecobank Tech 2023"},
            {"entreprise": "SGCI / Société Générale CI", "pays": "Côte d'Ivoire", "pratique": "Infrastructure adossée au groupe SG — cloud hybride, cybersécurité Zero Trust, SLA garanti", "source": "SGCI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "100% cloud AWS depuis 2021, architecture microservices, 99.98% uptime, 200 déploiements/mois", "source": "Equity Annual Report 2023"},
            {"entreprise": "CIH Bank", "pays": "Maroc", "pratique": "Migration Azure complète 2022, architecture API-first sur 80% des services, PCA mensuel", "source": "CIH Bank 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "DBS Bank", "pays": "Singapour", "pratique": "100% cloud-native AWS/Azure, zéro datacenter propriétaire, 1000 déploiements/jour, économies 500M SGD", "source": "DBS Annual Report 2023"},
            {"entreprise": "N26", "pays": "Allemagne", "pratique": "Architecture 100% microservices GCP, 1500 déploiements/jour, 0 downtime 2023, DevOps complet", "source": "N26 Tech Blog 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Instruction BCEAO sur les exigences techniques des SI bancaires", "description": "Normes minimales de disponibilité, sécurité et performance des systèmes d'information bancaires", "impact": "Obligation"},
            {"texte": "PCA/PRA obligatoire BCEAO", "description": "Plan de Continuité et Plan de Reprise d'Activité — tests obligatoires, seuils de disponibilité", "impact": "Obligation"},
            {"texte": "Localisation des données sensibles UEMOA", "description": "Certaines données critiques (KYC, transactions) doivent résider dans l'espace UEMOA", "impact": "Contrainte"},
            {"texte": "Norme PCI-DSS", "description": "Standard international de sécurité des données de paiement — obligatoire pour les émetteurs de cartes", "impact": "Obligation"}
        ],
        "ma_levees_fonds": [
            {"operation": "Investissement", "detail": "Temenos (core banking) capte 400M$ de nouveau financement pour accélérer la migration SaaS en Afrique", "montant": "400M USD", "annee": "2023"},
            {"operation": "Investissement", "detail": "Mambu (core banking cloud-native) valorisé à 5Mds$ — alternative moderne aux legacy bancaires", "montant": "235M USD", "annee": "2021"}
        ],
        "maturite_maximale": (
            "Excellence = core banking cloud-native, architecture microservices + API-first, "
            "uptime >99.9%, zéro legacy, CI/CD avec 100+ déploiements/mois, "
            "IA intégrée dans les processus critiques (scoring, fraude, personnalisation)."
        )
    },

    "IT_DATA::Data": {
        "tendances": [
            {
                "titre": "Gouvernance de la donnée comme actif stratégique",
                "description": "Les banques qui maîtrisent leur patrimoine data génèrent 2-3x plus de valeur par client. Le Data Catalog (Collibra, Alation) et le Data Quality framework deviennent des prérequis.",
                "source": "DAMA International Data Management 2024",
                "annee": "2024"
            },
            {
                "titre": "IA générative sur les données bancaires internes",
                "description": "Les LLMs fine-tunés sur les données internes permettent aux conseillers d'interroger en langage naturel les systèmes bancaires (soldes, historiques, profils risque). Time-to-insight divisé par 10.",
                "source": "McKinsey State of AI in Financial Services 2024",
                "annee": "2024"
            },
            {
                "titre": "Équipes Data dédiées : de la BI au Data Science",
                "description": "Les banques leaders constituent des équipes data pluridisciplinaires (Data Engineers, Data Scientists, Data Analysts) avec des ratios de 1 data scientist pour 50 collaborateurs.",
                "source": "LinkedIn Talent Insights FinData 2024",
                "annee": "2024"
            }
        ],
        "analyse_statique": (
            "La maturité data des banques UEMOA est préoccupante :\n"
            "- Silos de données entre core banking, mobile banking, CRM et reporting BCEAO\n"
            "- Qualité des données : 15-25% de doublons clients, adresses non normalisées\n"
            "- Absence de Data Catalog dans >90% des banques\n"
            "- Outils analytiques : Crystal Reports et Excel prédominants, peu de BI self-service\n"
            "- Équipes data : moins de 5 personnes en moyenne dans les grandes banques\n"
            "- Scoring crédit : modèles statistiques simples, pas de Machine Learning\n"
            "- Reporting BCEAO : processus manuel dans 60% des établissements\n\n"
            "En comparaison, les banques marocaines (Attijariwafa, CIH) ont 50-100 data scientists en production."
        ),
        "leaders_nationaux": [
            {"entreprise": "Ecobank", "pays": "Pan-UEMOA", "pratique": "Data Warehouse Teradata centralisé, reporting BCEAO automatisé, équipe data de 30+ personnes", "source": "Ecobank 2023"},
            {"entreprise": "SGCI", "pays": "Côte d'Ivoire", "pratique": "Adossée au data hub groupe SG — 200+ modèles analytiques partagés, BI Tableau déployé", "source": "SGCI 2023"}
        ],
        "leaders_regionaux": [
            {"entreprise": "Attijariwafa Bank", "pays": "Maroc", "pratique": "Data Lake Azure Synapse, 50+ modèles ML en production, scoring crédit IA réduisant défauts de 30%", "source": "Attijariwafa 2023"},
            {"entreprise": "Equity Bank", "pays": "Kenya", "pratique": "Data Science team de 80 personnes, 20+ modèles en production (churn, fraude, scoring, marketing)", "source": "Equity 2023"}
        ],
        "leaders_internationaux": [
            {"entreprise": "JPMorgan Chase", "pays": "USA", "pratique": "50 000 techniciens data, 400 modèles ML en production, détection fraude en 40ms sur 200M transactions/jour", "source": "JPMorgan Annual Report 2023"},
            {"entreprise": "Ant Group (Alipay)", "pays": "Chine", "pratique": "Scoring crédit en 3 secondes pour 500M clients, 0 analyste crédit humain sur prêts <10 000 CNY", "source": "Ant Group 2023"}
        ],
        "cadre_juridique": [
            {"texte": "Loi sur la protection des données personnelles (UEMOA, variantes nationales)", "description": "Encadre la collecte, le traitement, la conservation et le transfert des données personnelles", "impact": "Obligation"},
            {"texte": "Reporting réglementaire BCEAO (mensuel/trimestriel)", "description": "Obligations de transmission de données financières structurées à la Banque Centrale", "impact": "Obligation"},
            {"texte": "Règles de conservation des données bancaires (10 ans)", "description": "Durée légale de conservation des données de transactions et des dossiers clients", "impact": "Obligation"},
            {"texte": "RGPD (référence internationale / filiales européennes)", "description": "Standard européen de protection des données — applicable aux filiales en Europe", "impact": "Référence"}
        ],
        "ma_levees_fonds": [
            {"operation": "Levée de fonds", "detail": "Yabx (credit scoring AI Afrique) lève 3M$ pour améliorer le scoring des PME en UEMOA", "montant": "3M USD", "annee": "2023"},
            {"operation": "Levée de fonds", "detail": "Kwara (data bancaire coopératives Afrique) lève 4M$ Serie A pour digitaliser les données credit unions", "montant": "4M USD", "annee": "2022"},
            {"operation": "Investissement", "detail": "Snowflake ouvre une région Afrique du Sud — accélération adoption Data Cloud pour banques africaines", "montant": "N/A", "annee": "2023"}
        ],
        "maturite_maximale": (
            "Excellence = Data Lakehouse unifié (Snowflake/Databricks), gouvernance formalisée (Data Catalog + DQ framework), "
            "équipe data 20+ personnes, 10+ modèles ML en production (scoring, fraude, churn, recommandation), "
            "reporting BCEAO 100% automatisé, self-service analytics pour les métiers."
        )
    },
}


# ─────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────

try:
    from knowledge.sub_axis_extra import get_sub_axis_extra as _get_extra
except ImportError:
    try:
        from sub_axis_extra import get_sub_axis_extra as _get_extra
    except ImportError:
        def _get_extra(axis: str, sub_axis: str) -> dict:
            return {}


def get_sub_axis_data(axis: str, sub_axis: str, sector: str = "") -> dict | None:
    """Return knowledge data merged with extra enrichment for a given axis + sub_axis pair."""
    key = f"{axis}::{sub_axis}"
    base = SUB_AXIS_DATA.get(key)
    if base is None:
        return None
    extra = _get_extra(axis, sub_axis, sector=sector)
    if extra:
        return {**base, **extra}
    return base


def format_sub_axis_for_prompt(axis: str, sub_axis: str, company_score: float) -> str:
    """Format sub-axis knowledge as a compact LLM context block."""
    data = get_sub_axis_data(axis, sub_axis)
    if not data:
        return ""

    lines = [f"=== SOUS-AXE : {sub_axis} (Score entreprise : {company_score:.0f}/100) ==="]

    if data.get("tendances"):
        lines.append("TENDANCES :")
        for t in data["tendances"][:3]:
            lines.append(f"  • {t['titre']} — {t['description'][:120]}... ({t['source']})")

    if data.get("leaders_nationaux"):
        lines.append("LEADERS NATIONAUX/UEMOA :")
        for l in data["leaders_nationaux"][:2]:
            lines.append(f"  • {l['entreprise']} ({l['pays']}) : {l['pratique'][:120]}")

    if data.get("leaders_internationaux"):
        lines.append("LEADERS INTERNATIONAUX :")
        for l in data["leaders_internationaux"][:2]:
            lines.append(f"  • {l['entreprise']} ({l['pays']}) : {l['pratique'][:120]}")

    if data.get("cadre_juridique"):
        lines.append("CADRE JURIDIQUE :")
        for c in data["cadre_juridique"][:3]:
            lines.append(f"  • {c['texte']} : {c['description'][:100]} [{c['impact']}]")

    if data.get("ma_levees_fonds"):
        lines.append("M&A / LEVÉES DE FONDS :")
        for m in data["ma_levees_fonds"][:2]:
            lines.append(f"  • {m['operation']} {m['annee']} : {m['detail'][:120]}")

    if data.get("maturite_maximale"):
        lines.append(f"MATURITÉ MAXIMALE : {data['maturite_maximale'][:200]}")

    return "\n".join(lines)


def get_all_sub_axes() -> list[tuple[str, str]]:
    """Return all (axis, sub_axis) pairs in the knowledge base."""
    result = []
    for key in SUB_AXIS_DATA:
        parts = key.split("::", 1)
        if len(parts) == 2:
            result.append((parts[0], parts[1]))
    return result
