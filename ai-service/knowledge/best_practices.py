"""
Best Practices Knowledge Base
Concrete, actionable best practices per axis and maturity level.
Sources: Gartner, McKinsey, ANSSI, ISO, OCDE, WEF, Accenture, BCG.
"""

# Structure:
# {
#   "axis": {
#     "level": [
#       {"title": str, "actions": [str], "kpi": str, "timeline": str, "source": str}
#     ]
#   }
# }

BEST_PRACTICES: dict[str, dict[str, list[dict]]] = {

    # ── AXE MÉTIER (BUSINESS) ────────────────────────────────────────────────
    "BUSINESS": {

        "INITIAL": [
            {
                "title": "Formaliser une vision et stratégie digitale",
                "actions": [
                    "Réaliser un diagnostic digital (audit flash 2-3 jours)",
                    "Nommer un responsable digital (CDO ou référent numérique)",
                    "Définir 3 à 5 ambitions digitales prioritaires sur 12 mois",
                    "Allouer un budget dédié à la transformation digitale (min. 2% du CA)"
                ],
                "kpi": "Existence d'un plan digital documenté et validé par la direction",
                "timeline": "1-3 mois",
                "source": "McKinsey Digital Strategy Framework"
            },
            {
                "title": "Sensibiliser et former les équipes dirigeantes au digital",
                "actions": [
                    "Organiser des ateliers de sensibilisation pour le CODIR",
                    "Participer à des benchmarks sectoriels et visites d'entreprises digitales",
                    "Désigner des ambassadeurs digitaux dans chaque département"
                ],
                "kpi": "100% des membres du CODIR formés aux enjeux digitaux",
                "timeline": "2-4 mois",
                "source": "Gartner CEO Digital Leadership Survey"
            }
        ],

        "BASIQUE": [
            {
                "title": "Développer l'expérience client omnicanale",
                "actions": [
                    "Cartographier le parcours client actuel (customer journey mapping)",
                    "Mettre en place un CRM (Salesforce, HubSpot, Microsoft Dynamics)",
                    "Lancer un canal digital client (site, app, portail self-service)",
                    "Mesurer la satisfaction client (NPS, CSAT) en temps réel"
                ],
                "kpi": "NPS > 30 ; taux de résolution digitale > 40%",
                "timeline": "3-6 mois",
                "source": "Gartner CX Maturity Model, Forrester CX Index"
            },
            {
                "title": "Structurer une politique d'innovation",
                "actions": [
                    "Créer un processus d'idéation structuré (hackathons, boîte à idées digitale)",
                    "Mettre en place un comité d'innovation mensuel",
                    "Expérimenter avec des POC (proof of concept) sur des cas métier concrets",
                    "Établir des partenariats avec des startups ou des lab d'innovation"
                ],
                "kpi": "Min. 5 POC lancés par an, taux de passage en production > 20%",
                "timeline": "3-6 mois",
                "source": "BCG Innovation Benchmark 2024"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Déployer une stratégie data-driven",
                "actions": [
                    "Mettre en place un tableau de bord KPI en temps réel (Power BI, Tableau)",
                    "Former les managers à la culture data (data literacy program)",
                    "Implémenter des décisions basées sur les données (pricing, offres, stocks)",
                    "Créer une équipe data analytics transverse"
                ],
                "kpi": "80% des décisions stratégiques basées sur des données quantitatives",
                "timeline": "4-8 mois",
                "source": "McKinsey Analytics Value Report, Gartner BI Quadrant"
            },
            {
                "title": "Accélérer le time-to-market par le digital",
                "actions": [
                    "Adopter des méthodes agiles pour le développement produit",
                    "Réduire les cycles de lancement de 30% via la digitalisation",
                    "Automatiser les tests et le déploiement (CI/CD)",
                    "Mettre en place des retours clients rapides (beta testing, A/B testing)"
                ],
                "kpi": "Réduction du time-to-market de ≥30% sur 12 mois",
                "timeline": "4-9 mois",
                "source": "Accenture Agile Transformation Report"
            }
        ],

        "AVANCE": [
            {
                "title": "Développer des produits et services natifs digitaux",
                "actions": [
                    "Lancer des offres 100% digitales (produits as-a-service, plateformes)",
                    "Monétiser les données avec de nouveaux modèles économiques",
                    "Intégrer l'IA générative dans l'offre client (chatbot, personnalisation)",
                    "Créer un écosystème partenaire digital (API marketplace)"
                ],
                "kpi": "Revenus digitaux > 30% du CA total",
                "timeline": "6-12 mois",
                "source": "WEF Digital Business Models, MIT Digital Business"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Positionner l'entreprise comme leader digital du secteur",
                "actions": [
                    "Publier des benchmarks et études sectorielles (thought leadership)",
                    "Contribuer aux standards du secteur (comités normatifs, associations)",
                    "Proposer des services B2B2C basés sur votre maturité digitale",
                    "Exporter vos solutions dans d'autres marchés géographiques"
                ],
                "kpi": "Reconnaissance sectorielle : prix, classements, parts de marché digitales",
                "timeline": "12-24 mois",
                "source": "Gartner Digital Leader Benchmarks"
            }
        ]
    },

    # ── AXE PROCESSUS ────────────────────────────────────────────────────────
    "PROCESS": {

        "INITIAL": [
            {
                "title": "Cartographier et standardiser les processus métier",
                "actions": [
                    "Identifier et documenter les 10 processus les plus critiques",
                    "Utiliser une notation standard (BPMN 2.0) pour la modélisation",
                    "Définir des propriétaires de processus (process owners)",
                    "Établir des SLA internes et des indicateurs de performance"
                ],
                "kpi": "100% des processus critiques documentés avec propriétaire désigné",
                "timeline": "2-4 mois",
                "source": "CMMI Level 2, BPM CBOK"
            },
            {
                "title": "Mettre en place une gouvernance IT de base",
                "actions": [
                    "Créer un comité de pilotage IT mensuel",
                    "Adopter un référentiel de gestion de projet (PMI, PRINCE2)",
                    "Définir un catalogue de services IT avec des niveaux de service",
                    "Implémenter un outil de gestion des tickets (JIRA, ServiceNow)"
                ],
                "kpi": "SLA IT respectés > 90% du temps",
                "timeline": "2-3 mois",
                "source": "COBIT 2019, ITIL v4"
            }
        ],

        "BASIQUE": [
            {
                "title": "Automatiser les processus répétitifs (RPA)",
                "actions": [
                    "Identifier les processus à fort potentiel d'automatisation (ROI > 3x)",
                    "Déployer des outils RPA (UiPath, Automation Anywhere, Power Automate)",
                    "Former les équipes à la conception de robots logiciels",
                    "Mesurer les gains de productivité mensuellement"
                ],
                "kpi": "Automatisation de ≥20% des tâches répétitives ; économie ≥500 h/an",
                "timeline": "3-6 mois",
                "source": "Gartner RPA Magic Quadrant, Forrester RPA Wave"
            },
            {
                "title": "Implémenter un ERP ou système de gestion intégré",
                "actions": [
                    "Cartographier les besoins fonctionnels (finance, RH, achats, stocks)",
                    "Sélectionner un ERP adapté au secteur (SAP, Oracle, Odoo, Sage)",
                    "Planifier le déploiement par phases avec pilote puis généralisation",
                    "Former l'ensemble des utilisateurs (change management)"
                ],
                "kpi": "Taux d'adoption ERP > 85% ; réduction erreurs manuelles > 60%",
                "timeline": "6-18 mois",
                "source": "Gartner ERP Market Guide, APICS"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Adopter le management agile et les pratiques DevOps",
                "actions": [
                    "Former 50% des équipes projets aux méthodes Scrum/Kanban",
                    "Mettre en place des sprints de 2 semaines avec revues régulières",
                    "Implémenter des pipelines CI/CD pour les livrables digitaux",
                    "Mesurer la vélocité des équipes et réduire les délais de livraison"
                ],
                "kpi": "Time-to-market réduit de ≥30% ; taux de satisfaction équipes > 75%",
                "timeline": "3-6 mois",
                "source": "State of Agile Report, DORA DevOps Research"
            },
            {
                "title": "Déployer un système de management de la qualité (SMQ)",
                "actions": [
                    "Viser la certification ISO 9001:2015 pour les processus critiques",
                    "Mettre en place un système de revue des non-conformités",
                    "Automatiser les audits internes avec des outils digitaux",
                    "Créer une culture d'amélioration continue (Kaizen digital)"
                ],
                "kpi": "Réduction des non-conformités de ≥40% ; certification ISO 9001 obtenue",
                "timeline": "6-12 mois",
                "source": "ISO 9001:2015, Six Sigma DMAIC"
            }
        ],

        "AVANCE": [
            {
                "title": "Optimiser les processus par l'IA et le process mining",
                "actions": [
                    "Déployer un outil de process mining (Celonis, ProcessGold)",
                    "Identifier les goulots d'étranglement et inefficacités cachées",
                    "Implémenter des moteurs de décision IA pour les approbations",
                    "Mettre en place un centre d'excellence en automatisation (CoE)"
                ],
                "kpi": "Réduction des coûts de processus de ≥25% ; délais réduits de ≥40%",
                "timeline": "4-9 mois",
                "source": "Gartner Process Mining, McKinsey Operations Excellence"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Atteindre l'excellence opérationnelle continue",
                "actions": [
                    "Déployer des jumeaux numériques des processus critiques",
                    "Implémenter une gouvernance autonome par les données (self-service)",
                    "Partager les meilleures pratiques via des communautés de pratique",
                    "Obtenir des certifications de niveau mondial (CMMI Level 5, ISO 27001)"
                ],
                "kpi": "Benchmark supérieur au top 10% du secteur sur les KPI opérationnels",
                "timeline": "12-24 mois",
                "source": "CMMI Level 5, Gartner Operational Excellence"
            }
        ]
    },

    # ── AXE CANAUX DE DISTRIBUTION & UX ─────────────────────────────────────
    "CANAUX_DISTRIBUTION": {

        "INITIAL": [
            {
                "title": "Lancer une présence digitale de base (site + agence connectée)",
                "actions": [
                    "Créer un site web institutionnel responsive et optimisé mobile",
                    "Mettre en place un simulateur de produits en ligne (crédit, épargne)",
                    "Déployer un formulaire de demande d'ouverture de compte en ligne",
                    "Assurer la présence sur au moins un réseau social professionnel"
                ],
                "kpi": "Site web accessible 99% du temps ; taux rebond < 60%",
                "timeline": "1-3 mois",
                "source": "Hsys Digital Benchmark 2026 — Axe Canaux & UX, GSMA Mobile Banking"
            },
            {
                "title": "Déployer un service SMS Banking de base",
                "actions": [
                    "Offrir les consultations de solde et mini-relevés par SMS",
                    "Envoyer des alertes automatiques (transactions, échéances)",
                    "Configurer des codes USSD pour les clients sans smartphones",
                    "Assurer la couverture sur tous les réseaux opérateurs locaux"
                ],
                "kpi": "Taux d'adoption SMS Banking > 30% de la clientèle active",
                "timeline": "2-4 mois",
                "source": "GSMA Mobile Money Guidelines, BCEAO Instruction 008-05-2015"
            }
        ],

        "BASIQUE": [
            {
                "title": "Déployer une application mobile bancaire (Mobile Banking)",
                "actions": [
                    "Lancer une app iOS/Android avec authentification biométrique",
                    "Implémenter les virements, paiements de factures, recharges mobile",
                    "Intégrer les paiements QR code et contactless (NFC)",
                    "Assurer la conformité PCI DSS pour les paiements mobiles"
                ],
                "kpi": "Taux d'utilisation app mobile > 40% des clients actifs ; note app store > 4/5",
                "timeline": "4-8 mois",
                "source": "Hsys Digital Benchmark 2026, Gartner Digital Banking Maturity"
            },
            {
                "title": "Digitaliser le parcours d'ouverture de compte (KYC digital)",
                "actions": [
                    "Mettre en place la vérification d'identité digitale (e-KYC)",
                    "Automatiser la collecte et la vérification des documents",
                    "Réduire le délai d'ouverture de compte à moins de 24h",
                    "Signer électroniquement les contrats (signature numérique)"
                ],
                "kpi": "Délai ouverture de compte < 24h ; taux abandon parcours < 20%",
                "timeline": "3-6 mois",
                "source": "FATF Digital ID Guidelines, BCEAO Cadre réglementaire e-banking"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Développer une plateforme Internet Banking complète",
                "actions": [
                    "Proposer la gestion complète du compte via portail web sécurisé",
                    "Intégrer la gestion des investissements et produits d'épargne en ligne",
                    "Implémenter le Personal Finance Management (PFM) avec catégorisation",
                    "Offrir un service de chat en temps réel avec des conseillers"
                ],
                "kpi": "Taux de digitalisation des opérations > 60% ; NPS Digital > 40",
                "timeline": "6-12 mois",
                "source": "Forrester Digital Banking Experience Report 2024"
            },
            {
                "title": "Mettre en place un réseau d'agents bancaires (Agency Banking)",
                "actions": [
                    "Déployer un réseau de points de service (épiceries, stations-service)",
                    "Équiper les agents de tablettes/smartphones avec application dédiée",
                    "Couvrir les zones non bancarisées en milieu rural",
                    "Former et certifier les agents aux procédures AML/KYC"
                ],
                "kpi": "Couverture géographique étendue à 80% des zones cibles ; > 500 agents actifs",
                "timeline": "6-18 mois",
                "source": "CGAP Agency Banking Report, BCEAO Instruction Monnaie Electronique"
            }
        ],

        "AVANCE": [
            {
                "title": "Déployer une expérience client omnicanale intégrée",
                "actions": [
                    "Assurer une continuité de parcours entre agence, web, mobile et call center",
                    "Implémenter un CRM bancaire unifié (vue 360° du client)",
                    "Personnaliser les offres en temps réel selon le comportement digital",
                    "Déployer un assistant virtuel IA (chatbot) 24/7"
                ],
                "kpi": "Score d'expérience omnicanale > 80 ; taux résolution digitale > 75%",
                "timeline": "8-18 mois",
                "source": "McKinsey Digital Banking Transformation 2024"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Atteindre l'excellence en expérience client digitale",
                "actions": [
                    "Proposer des parcours 100% digitaux sans rupture de service",
                    "Déployer une IA prédictive pour anticiper les besoins clients",
                    "Offrir des APIs ouvertes pour l'intégration dans des super-apps",
                    "Co-construire les nouveaux produits avec les clients (design thinking)"
                ],
                "kpi": "NPS > 60 ; taux de croissance clients digitaux > 20%/an",
                "timeline": "12-24 mois",
                "source": "WEF Digital Finance Report 2024, GSMA State of Mobile Money"
            }
        ]
    },

    # ── AXE MARKETING & COMMUNICATION DIGITALE ───────────────────────────────
    "MARKETING_COMMUNICATION": {

        "INITIAL": [
            {
                "title": "Établir une présence sur les réseaux sociaux",
                "actions": [
                    "Créer des pages officielles sur Facebook, LinkedIn, WhatsApp Business",
                    "Définir une charte éditoriale et un calendrier de publication",
                    "Former un community manager interne ou prestataire",
                    "Répondre aux demandes clients dans un délai < 24h sur les réseaux"
                ],
                "kpi": "Taux d'engagement > 2% ; croissance followers > 10%/mois",
                "timeline": "1-3 mois",
                "source": "Hsys Digital Benchmark 2026 — Axe Marketing & Communication"
            }
        ],

        "BASIQUE": [
            {
                "title": "Déployer une stratégie de marketing digital",
                "actions": [
                    "Lancer des campagnes publicitaires digitales (Google Ads, Meta Ads)",
                    "Mettre en place le SEO pour améliorer la visibilité en ligne",
                    "Déployer l'email marketing et les newsletters clients",
                    "Mesurer le ROI des campagnes (conversions, coût d'acquisition)"
                ],
                "kpi": "Coût d'acquisition client digital ≤ 50% du coût canal physique ; ROI campagnes > 300%",
                "timeline": "3-6 mois",
                "source": "Google Digital Marketing Playbook, HubSpot State of Marketing"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Personnaliser la communication par la data client",
                "actions": [
                    "Segmenter la base client (RFM, comportement digital, cycle de vie)",
                    "Automatiser les communications personnalisées (marketing automation)",
                    "Personnaliser les offres produits selon le profil et le comportement",
                    "Mettre en place des programmes de fidélité digitaux"
                ],
                "kpi": "Taux d'ouverture emails > 25% ; taux de conversion personnalisation > 5%",
                "timeline": "4-9 mois",
                "source": "Accenture Personalization Report 2024, McKinsey Hyperpersonalization"
            }
        ],

        "AVANCE": [
            {
                "title": "Adopter le marketing data-driven et l'IA",
                "actions": [
                    "Déployer une Customer Data Platform (CDP) unifiée",
                    "Utiliser l'IA pour optimiser les budgets marketing (attribution modeling)",
                    "Implémenter des recommandations produits en temps réel",
                    "Lancer un programme d'influence digitale et de contenu expert"
                ],
                "kpi": "Revenus générés par le marketing digital > 40% du total ; LTV client +25%",
                "timeline": "6-12 mois",
                "source": "Gartner Marketing Technology Survey 2024"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Positionner la marque comme référence digitale du secteur",
                "actions": [
                    "Créer un centre de contenu expert (blog, podcast, webinaires)",
                    "Déployer une stratégie d'ambassador marketing et de co-branding fintech",
                    "Mesurer le brand equity digital et la part de voix en ligne",
                    "Participer activement aux événements et classements sectoriels"
                ],
                "kpi": "Part de voix digitale > 20% sur le secteur ; NPS brand > 50",
                "timeline": "12-24 mois",
                "source": "BCG Brand Advocacy Report, Forrester Brand Experience"
            }
        ]
    },

    # ── AXE RH & CULTURE DIGITALE ────────────────────────────────────────────
    "RH_CULTURE_DIGITALE": {

        "INITIAL": [
            {
                "title": "Sensibiliser les équipes aux enjeux de la transformation digitale",
                "actions": [
                    "Organiser des ateliers de sensibilisation digital pour tous les collaborateurs",
                    "Réaliser un diagnostic des compétences digitales (digital skills assessment)",
                    "Nommer des ambassadeurs digitaux par département",
                    "Communiquer sur la vision et la stratégie digitale de l'entreprise"
                ],
                "kpi": "100% des collaborateurs sensibilisés ; indice de culture digitale mesuré",
                "timeline": "2-4 mois",
                "source": "Hsys Digital Benchmark 2026 — Axe RH & Culture, WEF Future of Jobs"
            }
        ],

        "BASIQUE": [
            {
                "title": "Développer les compétences digitales des collaborateurs",
                "actions": [
                    "Définir un référentiel de compétences digitales par métier",
                    "Lancer un programme de formation digital (e-learning, blended learning)",
                    "Proposer des certifications digitales reconnues (Google, Microsoft, AWS)",
                    "Mettre en place un budget formation digitale ≥ 3% de la masse salariale"
                ],
                "kpi": "Taux de complétion formation > 80% ; ≥ 30% des collaborateurs certifiés",
                "timeline": "3-8 mois",
                "source": "LinkedIn Workplace Learning Report 2024, Gartner HR Technology"
            },
            {
                "title": "Digitaliser les processus RH",
                "actions": [
                    "Déployer un SIRH (Système d'Information RH) intégré",
                    "Dématérialiser les fiches de paie et documents contractuels",
                    "Mettre en place un portail self-service RH pour les collaborateurs",
                    "Digitaliser le processus de recrutement (ATS — Applicant Tracking System)"
                ],
                "kpi": "100% fiches de paie dématérialisées ; temps traitement RH réduit de 40%",
                "timeline": "4-8 mois",
                "source": "Gartner HR Technology Hype Cycle 2024"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Créer une culture agile et apprenante",
                "actions": [
                    "Former les managers aux pratiques de management agile",
                    "Mettre en place des communautés de pratique digitales (CoP)",
                    "Instaurer des rituels d'innovation (hackathons internes, design sprints)",
                    "Mesurer et publier un Digital Culture Index annuel"
                ],
                "kpi": "Score culture digitale > 65/100 ; taux de rétention talents digitaux > 80%",
                "timeline": "6-12 mois",
                "source": "Deloitte Human Capital Report 2024, McKinsey Org Health Index"
            }
        ],

        "AVANCE": [
            {
                "title": "Attirer et fidéliser les talents digitaux",
                "actions": [
                    "Créer une marque employeur digitale forte (Glassdoor, LinkedIn Employer)",
                    "Proposer des modalités de travail flexibles (télétravail, remote-first)",
                    "Déployer des parcours de carrière digitaux attractifs",
                    "Recruter des profils Data Scientists, Product Managers, UX Designers"
                ],
                "kpi": "Délai recrutement profils digitaux < 45j ; taux turnover digital < 15%",
                "timeline": "6-18 mois",
                "source": "LinkedIn Talent Insights 2024, Korn Ferry Future of Work"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Devenir une organisation apprenante à l'ère de l'IA",
                "actions": [
                    "Intégrer l'IA dans les processus de formation et de développement RH",
                    "Déployer des jumeaux digitaux des compétences pour la planification RH",
                    "Co-développer les solutions digitales RH avec les collaborateurs",
                    "Partager les meilleures pratiques RH digitales avec le secteur"
                ],
                "kpi": "Top 10% du secteur pour la maturité RH digitale ; certifications Great Place to Work",
                "timeline": "12-24 mois",
                "source": "Gartner Workforce Futures 2024"
            }
        ]
    },

    # ── AXE OFFRES DIGITALES ─────────────────────────────────────────────────
    "OFFRES_DIGITALES": {

        "INITIAL": [
            {
                "title": "Digitaliser les produits et services existants",
                "actions": [
                    "Cartographier les produits/services à potentiel de digitalisation",
                    "Proposer la souscription en ligne aux produits principaux",
                    "Mettre en place des simulateurs digitaux (crédit, épargne, assurance)",
                    "Lancer un espace client digital avec accès aux contrats et documents"
                ],
                "kpi": "≥ 30% des souscriptions réalisées en ligne ; satisfaction client digitale > 3.5/5",
                "timeline": "3-6 mois",
                "source": "Hsys Digital Benchmark 2026 — Axe Offres Digitales"
            }
        ],

        "BASIQUE": [
            {
                "title": "Développer des produits nativement digitaux",
                "actions": [
                    "Lancer un compte courant ou épargne 100% digital (néo-banque interne)",
                    "Proposer des micro-crédits digitaux avec scoring automatisé",
                    "Créer des produits d'assurance paramétrique et micro-assurance",
                    "Mettre en place le paiement instantané et les wallets digitaux"
                ],
                "kpi": "≥ 2 nouveaux produits 100% digitaux lancés par an ; adoption > 15% de la base client",
                "timeline": "6-12 mois",
                "source": "GSMA Mobile Money State of Industry Report 2024"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Intégrer des services à valeur ajoutée (open banking & partenariats)",
                "actions": [
                    "Exposer des APIs sécurisées pour les partenaires fintech",
                    "Intégrer des services tiers dans le parcours client (e-commerce, transport)",
                    "Lancer des offres co-brandées avec des partenaires digitaux",
                    "Proposer des solutions de paiement à l'international (diaspora)"
                ],
                "kpi": "≥ 5 partenariats API actifs ; revenus non-intérêts digitaux > 20% du total",
                "timeline": "6-18 mois",
                "source": "McKinsey Open Banking Maturity Report 2024"
            },
            {
                "title": "Déployer des solutions de financement digital des PME",
                "actions": [
                    "Créer une plateforme de crédit PME avec scoring IA (alternative data)",
                    "Proposer la facturation et le paiement B2B entièrement digitaux",
                    "Intégrer des solutions de cash management en ligne pour les entreprises",
                    "Lancer un programme d'accompagnement digital pour les PME clientes"
                ],
                "kpi": "Délai de décision crédit PME < 48h ; satisfaction PME > 4/5",
                "timeline": "6-18 mois",
                "source": "IFC Digital Finance for SMEs, AFI Digital Financial Services"
            }
        ],

        "AVANCE": [
            {
                "title": "Construire un écosystème de services financiers digitaux",
                "actions": [
                    "Créer une super-app intégrant banking, assurance, investissement",
                    "Lancer une plateforme Banking-as-a-Service (BaaS) pour les partenaires",
                    "Déployer des produits d'investissement digitaux (actions, OPCVM en ligne)",
                    "Intégrer des solutions DeFi et crypto-actifs de manière réglementée"
                ],
                "kpi": "Revenus digitaux > 35% du PNB ; ≥ 10 partenaires sur la plateforme BaaS",
                "timeline": "12-24 mois",
                "source": "WEF Digital Finance Report, McKinsey Banking Ecosystems"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Devenir une plateforme financière de référence",
                "actions": [
                    "Positionner la banque comme hub financier régional (UEMOA/CEDEAO)",
                    "Offrir des services non-financiers intégrés (marketplace, immobilier, santé)",
                    "Monétiser la data client de manière éthique et consentie",
                    "Exporter les solutions digitales dans d'autres marchés africains"
                ],
                "kpi": "Part de marché digital > 25% ; présence dans ≥ 5 pays CEDEAO",
                "timeline": "24-48 mois",
                "source": "Gartner Digital Business Models, McKinsey Africa Banking Report"
            }
        ]
    },

    # ── AXE SI (INFORMATION_SYSTEM) ──────────────────────────────────────────
    "INFORMATION_SYSTEM": {

        "INITIAL": [
            {
                "title": "Sécuriser les fondamentaux de l'infrastructure IT",
                "actions": [
                    "Mettre en place un pare-feu et une politique d'accès réseau",
                    "Activer les mises à jour automatiques de sécurité sur tous les postes",
                    "Mettre en place une solution antivirus/EDR (CrowdStrike, SentinelOne)",
                    "Créer des sauvegardes régulières testées (règle 3-2-1)",
                    "Former les employés aux risques phishing et ingénierie sociale"
                ],
                "kpi": "0 poste sans antivirus ; sauvegardes testées mensuellement",
                "timeline": "1-2 mois",
                "source": "ANSSI Guide d'hygiène informatique, CIS Controls"
            },
            {
                "title": "Inventorier et cartographier le patrimoine applicatif",
                "actions": [
                    "Lister tous les logiciels et systèmes utilisés (CMDB de base)",
                    "Identifier les systèmes obsolètes (end-of-life) et planifier leur remplacement",
                    "Documenter les flux de données entre les applications",
                    "Prioriser la dette technique à adresser"
                ],
                "kpi": "CMDB à jour avec 100% des applications critiques référencées",
                "timeline": "1-3 mois",
                "source": "ITIL v4, COBIT 2019"
            }
        ],

        "BASIQUE": [
            {
                "title": "Migrer vers le cloud et moderniser l'infrastructure",
                "actions": [
                    "Réaliser un bilan cloud (applications cloud-ready vs legacy)",
                    "Adopter une stratégie cloud hybride (AWS, Azure, Google Cloud)",
                    "Migrer les applications non critiques en premier (lift & shift)",
                    "Former les équipes IT au cloud (certifications AWS/Azure/GCP)"
                ],
                "kpi": "≥30% du SI migré vers le cloud ; réduction coûts infra de ≥20%",
                "timeline": "6-12 mois",
                "source": "Gartner Cloud Strategy, AWS Well-Architected Framework"
            },
            {
                "title": "Implémenter la gestion des identités et des accès (IAM)",
                "actions": [
                    "Déployer une solution IAM centralisée (Azure AD, Okta, Keycloak)",
                    "Activer l'authentification multifacteur (MFA) pour tous les utilisateurs",
                    "Appliquer le principe du moindre privilège",
                    "Automatiser le provisioning/déprovisioning des comptes"
                ],
                "kpi": "MFA activé pour 100% des comptes ; 0 compte orphelin actif",
                "timeline": "2-4 mois",
                "source": "ANSSI — Recommandations IAM, NIST 800-63"
            }
        ],

        "INTERMEDIAIRE": [
            {
                "title": "Déployer une architecture Zero Trust",
                "actions": [
                    "Adopter le principe 'Never trust, always verify'",
                    "Mettre en place la microsegmentation réseau",
                    "Déployer un SIEM (Security Information and Event Management)",
                    "Implémenter une solution ZTNA pour les accès distants"
                ],
                "kpi": "Score CIS Controls ≥ niveau 2 ; temps détection incident < 1h",
                "timeline": "6-12 mois",
                "source": "NIST Zero Trust Architecture, CISA Zero Trust Maturity"
            },
            {
                "title": "Mettre en place une architecture de données robuste",
                "actions": [
                    "Déployer un data warehouse ou data lakehouse (Snowflake, Databricks)",
                    "Établir une gouvernance des données (data catalog, lineage, qualité)",
                    "Mettre en place des pipelines de données automatisés (ETL/ELT)",
                    "Former les équipes métier à la self-service analytics"
                ],
                "kpi": "Données disponibles en temps réel pour ≥80% des KPI métier",
                "timeline": "4-9 mois",
                "source": "Gartner Data & Analytics Maturity, DAMA DMBOK"
            }
        ],

        "AVANCE": [
            {
                "title": "Industrialiser l'IA et le Machine Learning",
                "actions": [
                    "Créer une équipe MLOps pour le déploiement des modèles en production",
                    "Mettre en place une plateforme MLOps (MLflow, Kubeflow, SageMaker)",
                    "Déployer des modèles IA dans au moins 3 processus métier critiques",
                    "Établir une politique d'IA responsable et éthique"
                ],
                "kpi": "≥3 modèles IA en production ; ROI IA documenté > 200%",
                "timeline": "6-12 mois",
                "source": "Gartner AI Maturity Model, Google ML Best Practices"
            },
            {
                "title": "Implémenter un SOC et une réponse aux incidents mature",
                "actions": [
                    "Mettre en place un SOC interne ou SOC managé (MSSP)",
                    "Définir un Incident Response Plan (IRP) et le tester annuellement",
                    "Réaliser des exercices de crise cyber (tabletop, red team)",
                    "Obtenir la certification ISO 27001"
                ],
                "kpi": "MTTD < 4h ; MTTR < 24h ; certification ISO 27001 obtenue",
                "timeline": "6-18 mois",
                "source": "ANSSI, NIST Cybersecurity Framework, ISO 27001"
            }
        ],

        "OPTIMISE": [
            {
                "title": "Atteindre la résilience digitale totale",
                "actions": [
                    "Implémenter une architecture self-healing et chaos engineering",
                    "Déployer des jumeaux numériques du SI pour la simulation",
                    "Atteindre un RTO < 1h et RPO < 15min sur les systèmes critiques",
                    "Automatiser 100% de la réponse aux incidents de sécurité de niveau 1"
                ],
                "kpi": "Disponibilité SI > 99.99% ; 0 violation de données non détectée",
                "timeline": "12-24 mois",
                "source": "Google SRE, DORA DevOps Research, AWS Well-Architected"
            }
        ]
    }
}

# Sector-specific best practices overlay
SECTOR_BEST_PRACTICES: dict[str, list[dict]] = {
    "finance": [
        {
            "axis": "BUSINESS",
            "title": "Définir une stratégie de transformation digitale financière",
            "actions": [
                "Établir une roadmap de digitalisation des produits financiers sur 3 ans",
                "Intégrer des partenariats avec des fintechs pour accélérer l'innovation",
                "Adopter un modèle open finance pour monétiser les données clients via des APIs",
                "Mesurer le ROI digital par ligne de produit (crédit, épargne, assurance)"
            ],
            "source": "McKinsey Global Banking Annual Review 2024"
        },
        {
            "axis": "PROCESS",
            "title": "Automatiser les processus financiers et de conformité réglementaire",
            "actions": [
                "Déployer un moteur de règles pour l'automatisation du KYC/AML (Comply Advantage, Actico)",
                "Robotiser le traitement des opérations de back-office (rapprochements, virements, reporting)",
                "Mettre en place un workflow digital pour l'instruction des crédits (scoring automatisé)",
                "Automatiser la production des reportings réglementaires (IFRS 9, Bâle III)"
            ],
            "source": "Deloitte — Finance Automation Report 2024, BIS Basel Framework"
        },
        {
            "axis": "INFORMATION_SYSTEM",
            "title": "Sécuriser les paiements et prévenir la fraude par l'IA",
            "actions": [
                "Déployer un moteur de scoring de fraude en temps réel (ML)",
                "Implémenter 3D Secure 2.0 pour tous les paiements en ligne",
                "Mettre en place une surveillance comportementale des transactions",
                "Tester régulièrement les scénarios de fraude (red team financier)"
            ],
            "source": "SWIFT CSP, PCI DSS v4, Visa/Mastercard Fraud Guidelines"
        },
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Déployer une expérience client financière omnicanale",
            "actions": [
                "Lancer une application mobile de gestion financière personnelle (PFM)",
                "Intégrer un chatbot financier pour le conseil et le support client 24h/24",
                "Proposer une souscription 100% digitale pour tous les produits (crédit, assurance, épargne)",
                "Mesurer le NPS digital et le taux d'adoption des canaux digitaux mensuellement"
            ],
            "source": "Forrester — Digital Banking Experience Report 2024"
        },
        {
            "axis": "OFFRES_DIGITALES",
            "title": "Développer des produits financiers digitaux innovants",
            "actions": [
                "Lancer des produits d'épargne et d'investissement 100% digitaux (robo-advisor)",
                "Proposer des micro-assurances paramétriques basées sur des données comportementales",
                "Créer des offres de financement instantané (Buy Now Pay Later, crédit en ligne)",
                "Intégrer des APIs financières pour permettre l'intégration dans des super-apps"
            ],
            "source": "WEF — Future of Financial Services 2024, CGAP FinTech Report"
        },
        {
            "axis": "RH_CULTURE_DIGITALE",
            "title": "Développer les compétences digitales et data des équipes financières",
            "actions": [
                "Former les conseillers financiers à l'utilisation des outils CRM et d'analytique client",
                "Lancer un programme de culture data pour les équipes risques et conformité",
                "Recruter des profils data scientists et ingénieurs IA au sein des équipes métier",
                "Créer un lab d'innovation interne (fintech lab) pour tester de nouveaux modèles"
            ],
            "source": "Deloitte — Banking Workforce of the Future 2024"
        },
    ],
    "sante": [
        {
            "axis": "BUSINESS",
            "title": "Définir une stratégie de santé numérique centrée sur le patient",
            "actions": [
                "Élaborer un plan stratégique de transformation numérique aligné sur la politique nationale de santé",
                "Déployer le dossier patient informatisé (DPI) interopérable dans toutes les unités de soin",
                "Nouer des partenariats avec des healthtech pour l'innovation en télémédecine et IA diagnostique",
                "Mesurer les indicateurs de qualité des soins digitaux (taux de réadmission, satisfaction patient)"
            ],
            "source": "OMS — Stratégie mondiale pour la santé numérique 2020-2025"
        },
        {
            "axis": "PROCESS",
            "title": "Digitaliser les parcours de soins et les processus cliniques",
            "actions": [
                "Mettre en place un système de prise de rendez-vous en ligne et de rappels automatisés",
                "Déployer des workflows cliniques digitaux pour réduire les erreurs médicales",
                "Automatiser la gestion des stocks pharmaceutiques et des équipements médicaux",
                "Intégrer un système de gestion de la qualité (accréditation HAS / normes ISO 15189)"
            ],
            "source": "HAS — Guide de la transformation numérique en santé 2024"
        },
        {
            "axis": "INFORMATION_SYSTEM",
            "title": "Mettre en conformité le SI de santé avec HDS et PGSSI-S",
            "actions": [
                "Obtenir ou vérifier la certification HDS de l'hébergeur",
                "Déployer l'identité nationale de santé (INS) dans le DPI",
                "Mettre en place la messagerie sécurisée MSSanté",
                "Auditer les accès aux données patients trimestriellement"
            ],
            "source": "ANS — Agence du Numérique en Santé, PGSSI-S"
        },
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Déployer des services de télémédecine et un portail patient digital",
            "actions": [
                "Lancer une plateforme de téléconsultation certifiée (Doctolib, Medici, ou solution interne)",
                "Créer un portail patient avec accès aux résultats d'analyses, ordonnances et historique médical",
                "Mettre en place une application mobile de suivi des patients chroniques (diabète, hypertension)",
                "Intégrer des dispositifs connectés (IoT santé) pour le monitoring à distance des patients"
            ],
            "source": "GSMA mHealth Report 2023, Commission Européenne — eHealth Action Plan"
        },
        {
            "axis": "OFFRES_DIGITALES",
            "title": "Développer des services de santé digitaux et de prévention connectée",
            "actions": [
                "Lancer des programmes de prévention digitale (coaching santé, bien-être, nutrition en ligne)",
                "Proposer des parcours de soins hybrides (présentiel + téléconsultation) pour les pathologies chroniques",
                "Intégrer l'IA diagnostique pour l'aide à la décision clinique (radiologie, dermatologie)",
                "Créer des services de santé personnalisés basés sur les données génomiques et comportementales"
            ],
            "source": "McKinsey — The Future of Healthcare 2024, WEF Health and Healthcare Report"
        },
        {
            "axis": "RH_CULTURE_DIGITALE",
            "title": "Renforcer les compétences numériques du personnel soignant et administratif",
            "actions": [
                "Former 100% du personnel soignant aux outils du DPI et aux bonnes pratiques numériques",
                "Lancer un programme de sensibilisation à la cybersécurité des données patients",
                "Créer une filière de référents numériques (infirmiers, médecins) dans chaque service",
                "Intégrer les compétences numériques dans les évaluations annuelles du personnel médical"
            ],
            "source": "OMS — Digital Health Workforce Competencies Framework 2023"
        },
    ],
    "industrie": [
        {
            "axis": "BUSINESS",
            "title": "Définir une stratégie Industrie 4.0 et transition vers le manufacturing digital",
            "actions": [
                "Réaliser un audit de maturité Industrie 4.0 et définir une feuille de route sur 3 ans",
                "Identifier les processus de production prioritaires à digitaliser (gains > 20%)",
                "Nouer des partenariats avec des équipementiers et intégrateurs IoT industriels",
                "Mesurer le ROI de la transformation industrielle (OEE, coût unitaire, délais de production)"
            ],
            "source": "WEF — Advanced Manufacturing 2024, Gartner Manufacturing Industry Insights"
        },
        {
            "axis": "PROCESS",
            "title": "Déployer l'automatisation industrielle et le Lean digital",
            "actions": [
                "Implémenter un MES (Manufacturing Execution System) pour piloter la production en temps réel",
                "Déployer des robots collaboratifs (cobots) sur les lignes de production à forte valeur ajoutée",
                "Mettre en place la maintenance prédictive via des capteurs IoT et l'analyse ML",
                "Intégrer les principes Lean avec des outils digitaux (VSM digital, Kaizen boards virtuels)"
            ],
            "source": "IFR — World Robotics Report 2024, McKinsey Industry 4.0 Pulse Survey"
        },
        {
            "axis": "INFORMATION_SYSTEM",
            "title": "Sécuriser les systèmes OT/SCADA (cybersécurité industrielle)",
            "actions": [
                "Réaliser une cartographie des systèmes OT et identifier les actifs critiques",
                "Mettre en place une segmentation stricte IT/OT (zone DMZ industrielle)",
                "Déployer une supervision de sécurité spécifique OT (Claroty, Nozomi)",
                "Appliquer les recommandations IEC 62443 pour les systèmes industriels"
            ],
            "source": "IEC 62443, ANSSI Guide Sécurité Systèmes Industriels"
        },
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Digitaliser les canaux de vente B2B et la relation client industrielle",
            "actions": [
                "Déployer un portail client B2B avec suivi des commandes, stocks et livraisons en temps réel",
                "Lancer un catalogue produit digital avec configurateur en ligne (CPQ)",
                "Intégrer un CRM industriel (Salesforce Manufacturing, SAP CX) pour la gestion des comptes clés",
                "Mettre en place l'EDI (Electronic Data Interchange) pour l'automatisation des commandes clients"
            ],
            "source": "Gartner — Digital Commerce for Manufacturing 2024"
        },
        {
            "axis": "OFFRES_DIGITALES",
            "title": "Développer des offres de services digitaux industriels (servitisation)",
            "actions": [
                "Lancer des offres de maintenance-as-a-service (MaaS) basées sur des capteurs IoT",
                "Proposer des jumeaux numériques (digital twins) pour la simulation et l'optimisation client",
                "Créer des offres de monitoring en temps réel des équipements installés chez les clients",
                "Développer des plateformes de données industrielles partagées avec les partenaires de la supply chain"
            ],
            "source": "IDC — Manufacturing Digital Services 2024, WEF Advanced Manufacturing White Paper"
        },
        {
            "axis": "RH_CULTURE_DIGITALE",
            "title": "Développer les compétences Industrie 4.0 des opérateurs et techniciens",
            "actions": [
                "Former les opérateurs à l'utilisation des interfaces homme-machine digitales (HMI, tablettes industrielles)",
                "Lancer un programme de montée en compétences sur la data et l'IoT pour les techniciens de maintenance",
                "Créer des parcours de formation en réalité augmentée (AR) pour l'assistance à la maintenance",
                "Intégrer les compétences numériques dans les référentiels métier et les grilles de rémunération"
            ],
            "source": "WEF — Future of Jobs in Manufacturing 2023, Siemens Digital Skills Framework"
        },
    ],
    "banque": [
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Déployer une stratégie multicanale adaptée au contexte UEMOA",
            "actions": [
                "Prioriser les canaux mobiles (USSD, SMS, app) pour toucher la clientèle non-bancarisée",
                "Déployer un réseau d'agents bancaires (agency banking) dans les zones rurales",
                "Assurer la compatibilité avec les mobile money locaux (Orange Money, Wave, MTN MoMo)",
                "Intégrer les solutions de paiement régionaux (GIM-UEMOA, BCEAO SIMT)"
            ],
            "source": "BCEAO — Rapport sur la Digitalisation Bancaire UEMOA 2024, Hsys Digital Benchmark 2026"
        },
        {
            "axis": "INFORMATION_SYSTEM",
            "title": "Moderniser le core banking et assurer la conformité BCEAO",
            "actions": [
                "Migrer vers un core banking system moderne (Temenos T24, Oracle Flexcube, Mambu)",
                "Mettre en place le reporting réglementaire automatisé (BCEAO SYSCOA)",
                "Déployer un système de détection de fraude temps réel (scoring ML)",
                "Assurer la conformité à la Loi 2013-015 sur la cybersécurité (UEMOA)"
            ],
            "source": "BCEAO Instructions réglementaires, Loi 2013-015 Cybersécurité UEMOA"
        },
        {
            "axis": "OFFRES_DIGITALES",
            "title": "Développer des offres de mobile money et d'inclusion financière",
            "actions": [
                "Lancer ou intégrer une solution de paiement mobile conforme BCEAO",
                "Proposer des micro-crédits digitaux avec scoring alternatif (mobile data, airtime)",
                "Créer des produits d'épargne digitaux adaptés aux revenus informels",
                "Développer des solutions de paiement pour les transferts de la diaspora"
            ],
            "source": "GSMA State of Mobile Money Africa 2024, BCEAO Instruction 008-05-2015"
        },
        {
            "axis": "BUSINESS",
            "title": "Accélérer la bancarisation par le digital (inclusion financière)",
            "actions": [
                "Fixer un objectif de taux de bancarisation digitale et le mesurer trimestriellement",
                "Lancer des comptes simplifiés (low-KYC) conformes BCEAO pour les populations rurales",
                "Déployer des kiosques digitaux et tablettes en agence pour les clients non-digitaux",
                "Former les agents de terrain à l'évangélisation des services digitaux"
            ],
            "source": "Alliance for Financial Inclusion (AFI), CGAP Financial Inclusion Report 2024"
        },
        {
            "axis": "PROCESS",
            "title": "Automatiser les processus bancaires et la conformité réglementaire",
            "actions": [
                "Robotiser le traitement des opérations de back-office (RPA : rapprochements, virements, KYC)",
                "Déployer un workflow digital pour l'instruction et l'octroi de crédit (scoring automatisé)",
                "Automatiser la production des reportings BCEAO (SYSCOA, ratio de solvabilité, liquidité)",
                "Mettre en place un moteur de règles AML/CTF pour la détection automatique des transactions suspectes"
            ],
            "source": "BCEAO Instruction n°008-05-2015, Accenture Banking Operations Report 2024"
        },
        {
            "axis": "RH_CULTURE_DIGITALE",
            "title": "Développer la culture digitale et les compétences data des équipes bancaires",
            "actions": [
                "Former 100% des conseillers clientèle aux outils CRM et aux techniques de vente digitale",
                "Lancer un programme de culture data pour les équipes risques, conformité et marketing",
                "Créer un parcours de certification interne (digital banking) reconnu et valorisé",
                "Mettre en place des indicateurs de maturité digitale dans les évaluations annuelles"
            ],
            "source": "Deloitte — Banking Talent & Culture Report 2024, EBA Digital Finance Guidelines"
        },
    ],
    "education": [
        {
            "axis": "BUSINESS",
            "title": "Définir une stratégie d'apprentissage hybride (blended learning)",
            "actions": [
                "Cartographier les parcours pédagogiques et identifier les modules digitalisables",
                "Adopter un modèle hybride : 60% présentiel + 40% e-learning asynchrone",
                "Nouer des partenariats avec des plateformes EdTech (Coursera, edX, Google Classroom)",
                "Mesurer le taux de complétion et l'engagement étudiant par module digital"
            ],
            "source": "UNESCO — Rapport sur l'éducation numérique mondiale 2023"
        },
        {
            "axis": "PROCESS",
            "title": "Digitaliser les processus administratifs et pédagogiques",
            "actions": [
                "Mettre en place un ERP éducatif (Classe365, Blackbaud) pour la gestion des inscriptions et résultats",
                "Automatiser les processus d'accréditation et de suivi de conformité réglementaire",
                "Déployer un workflow numérique pour la gestion des examens, corrections et bulletins",
                "Intégrer un portail étudiant self-service (absences, notes, emplois du temps)"
            ],
            "source": "OCDE — Digital Education Outlook 2023"
        },
        {
            "axis": "INFORMATION_SYSTEM",
            "title": "Déployer un LMS sécurisé et conforme RGPD pour la protection des données étudiants",
            "actions": [
                "Adopter un LMS certifié (Moodle, Canvas, Blackboard) avec hébergement souverain ou HDS",
                "Mettre en place une politique de protection des données étudiants (RGPD / loi nationale)",
                "Intégrer xAPI et LRS (Learning Record Store) pour tracer les parcours apprenants",
                "Réaliser un audit de sécurité annuel des accès aux données pédagogiques sensibles"
            ],
            "source": "ANS — Cadre de référence numérique éducatif, RGPD Education 2023"
        },
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Développer des canaux d'accès à l'apprentissage multimodaux",
            "actions": [
                "Lancer une application mobile d'apprentissage accessible hors-connexion (offline-first)",
                "Déployer des classes virtuelles synchrones (Zoom Education, Microsoft Teams for Education)",
                "Créer un portail de ressources éducatives libres (REL) accessible 24h/24",
                "Mettre en place un système de tutorat digital et de support étudiant en ligne"
            ],
            "source": "GSMA Mobile Learning Report 2023, UNESCO REL"
        },
        {
            "axis": "OFFRES_DIGITALES",
            "title": "Développer des offres de formation digitale certifiantes et à distance",
            "actions": [
                "Lancer des micro-certifications digitales (badges numériques, certificats en ligne)",
                "Créer des MOOCs sectoriels en partenariat avec des entreprises locales",
                "Proposer des formations courtes (upskilling) en IA, data et cybersécurité",
                "Intégrer la reconnaissance des acquis d'expérience (RAE) dans les parcours digitaux"
            ],
            "source": "WEF Future of Jobs Report 2023, Coursera Industry Skills Report 2024"
        },
        {
            "axis": "RH_CULTURE_DIGITALE",
            "title": "Renforcer les compétences numériques des enseignants et du personnel",
            "actions": [
                "Lancer un programme de certification numérique pour les enseignants (CUEN, TICE)",
                "Former 100% du corps enseignant aux outils LMS et à la pédagogie inversée",
                "Créer une communauté de pratique EdTech interne pour le partage de ressources",
                "Intégrer des indicateurs de maturité digitale dans les évaluations annuelles du personnel"
            ],
            "source": "DigComp 2.2 — Cadre européen des compétences numériques pour les éducateurs"
        },
        {
            "axis": "CANAUX_DISTRIBUTION",
            "title": "Déployer un portail étudiant omnicanal et une application mobile d'apprentissage",
            "actions": [
                "Lancer un portail étudiant self-service (inscriptions, notes, emplois du temps, absences) accessible 24h/24",
                "Développer une application mobile d'apprentissage offline-first pour les zones à faible connectivité",
                "Mettre en place des classes virtuelles synchrones (Microsoft Teams for Education, Zoom Education)",
                "Intégrer un chatbot pédagogique pour le support étudiant et la FAQ automatisée"
            ],
            "source": "GSMA Mobile Learning Report 2023, Microsoft Education Transformation Framework"
        },
    ],
}


def get_best_practices(axis: str, maturity_level: str, sector: str = None) -> list[dict]:
    """Return best practices for a given axis and maturity level."""
    axis_upper = axis.upper()
    level_upper = maturity_level.upper()
    result = []

    if axis_upper in BEST_PRACTICES and level_upper in BEST_PRACTICES[axis_upper]:
        result.extend(BEST_PRACTICES[axis_upper][level_upper])

    # Add next level practices as stretch goals
    next_levels = {
        "INITIAL": "BASIQUE",
        "BASIQUE": "INTERMEDIAIRE",
        "INTERMEDIAIRE": "AVANCE",
        "AVANCE": "OPTIMISE"
    }
    next_level = next_levels.get(level_upper)
    if next_level and axis_upper in BEST_PRACTICES and next_level in BEST_PRACTICES[axis_upper]:
        result.extend(BEST_PRACTICES[axis_upper][next_level][:1])  # add just 1 stretch goal

    # Add sector-specific practices
    if sector:
        sector_key = sector.lower().strip()
        if sector_key in SECTOR_BEST_PRACTICES:
            for sp in SECTOR_BEST_PRACTICES[sector_key]:
                if sp["axis"] == axis_upper:
                    result.append(sp)

    return result


def format_best_practices_for_prompt(axis: str, maturity_level: str, sector: str = None) -> str:
    """Format best practices as a knowledge block for injection into AI prompts."""
    practices = get_best_practices(axis, maturity_level, sector)
    if not practices:
        return ""

    lines = [f"\nMEILLEURES PRATIQUES — Axe {axis} (niveau actuel : {maturity_level}) :"]
    for p in practices:
        lines.append(f"\n▸ {p['title']}")
        for action in p["actions"][:3]:
            lines.append(f"  • {action}")
        if p.get("kpi"):
            lines.append(f"  KPI cible : {p['kpi']}")
        if p.get("timeline"):
            lines.append(f"  Horizon : {p['timeline']}")
        lines.append(f"  Source : {p['source']}")

    return "\n".join(lines)
