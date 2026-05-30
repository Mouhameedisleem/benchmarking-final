"""
Generic sub-axis extra knowledge — cross-sector fallback.
All 27 sub-axes. Zoom cases use globally recognised tech/industry leaders.
comparatif_organisations uses 3 tiers (leader / intermédiaire / traditionnel).
"""

GENERIC_EXTRA: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════
    # AXE 1 — MÉTIER / BUSINESS
    # ══════════════════════════════════════════════════════════════════

    "BUSINESS::Stratégie digitale": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Day-1 Strategy — culture digitale native & OKRs à tous les niveaux",
            "description": (
                "Amazon fonctionne depuis 1995 selon le principe 'Day 1' : chaque décision "
                "est prise comme si l'entreprise venait de naître, refusant l'inertie "
                "organisationnelle. La stratégie digitale est incarnée par le CEO et déclinée "
                "en Working Backwards Press Release pour chaque initiative. Les OKRs de chaque "
                "BU sont visibles en interne. 16 % du CA est réinvesti en R&D chaque année. "
                "Le CDO siège au COMEX avec pouvoir de veto sur les décisions IT."
            ),
            "resultats": "2 000 Mds$ de capitalisation · AWS leader mondial cloud · NPS +73 · 16% CA en R&D",
            "source": "Amazon Annual Report 2023 / Gartner Digital Business Strategy 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité stratégie digitale — benchmark sectoriel",
            "colonnes": ["Organisation", "Stratégie digitale formalisée", "CDO / Directeur digital nommé", "Budget digital documenté", "OKRs mesurables", "Partenariat tech actif"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "Partiel", "Partiel", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "BUSINESS::Orientation client": {
        "zoom_case_study": {
            "entreprise": "Apple",
            "pays": "USA",
            "technologie": "Human Interface Design — expérience client comme avantage compétitif absolu",
            "description": (
                "Apple a bâti son leadership mondial sur l'obsession de l'expérience client : "
                "chaque produit est conçu par reverse-engineering depuis le besoin utilisateur. "
                "L'Apple Store redéfinit le retail avec un NPS de 75+. Le programme Voice of "
                "Customer analyse 40M+ avis App Store par mois. Les Human Interface Guidelines "
                "sont le standard UX adopté par 35 millions de développeurs tiers."
            ),
            "resultats": "NPS +75 · Satisfaction client 89% · Rétention écosystème 92% · 2 900 Mds$ de capitalisation",
            "source": "Apple Annual Report 2023 / Forrester CX Index 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité orientation client — benchmark sectoriel",
            "colonnes": ["Organisation", "Mesure NPS régulière", "Design UX dédié", "CRM unifié 360°", "Personnalisation offres", "SLA réclamation < 48h"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "Partiel", "✓", "Partiel", "✓"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "Partiel", "✗", "Partiel"]}
            ]
        }
    },

    "BUSINESS::Innovation": {
        "zoom_case_study": {
            "entreprise": "Google / Alphabet",
            "pays": "USA",
            "technologie": "Google X — moonshot factory + règle des 70/20/10",
            "description": (
                "Google institutionnalise l'innovation à deux vitesses : 70% sur le cœur "
                "de métier, 20% sur des projets adjacents, 10% sur des moonshots radicaux "
                "(Google X). Cette structure a produit Gmail, Google Maps, Android, Chrome. "
                "Chaque ingénieur dispose de 20% de son temps pour innover librement. "
                "Google X (Waymo, Wing) opère comme une startup interne avec budget dédié "
                "et droit à l'échec explicitement documenté."
            ),
            "resultats": "20+ produits nés du programme 20% · Waymo valorisée 30 Mds$ · 85 000 brevets · R&D 40 Mds$/an",
            "source": "Alphabet Annual Report 2023 / MIT Sloan Innovation Report 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité innovation — benchmark sectoriel",
            "colonnes": ["Organisation", "Lab / cellule innovation", "Partenariat startups actif", "Hackathon organisé", "Budget R&D dédié", "MVP livré < 3 mois"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "BUSINESS::Modèle économique digital": {
        "zoom_case_study": {
            "entreprise": "Netflix",
            "pays": "USA",
            "technologie": "Subscription economy — pivot DVD → streaming, modèle copié mondialement",
            "description": (
                "Netflix a pivoté en 2007 du DVD physique au streaming en ligne, inventant "
                "le modèle d'abonnement mensuel pour le contenu. Le moteur de recommandation "
                "IA (80% des contenus visionnés via algorithme) optimise la rétention. "
                "En 2022, lancement d'un tier publicitaire diversifiant les revenus. "
                "Le contenu original (House of Cards, Squid Game) crée des barrières à "
                "l'entrée via IP exclusives."
            ),
            "resultats": "260M abonnés · CA 33 Mds$ · Marge nette 16% · 190 pays · Modèle abonnement copié par 10 000+ entreprises",
            "source": "Netflix Annual Report 2023 / McKinsey Digital Revenue Models 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité modèle économique digital — benchmark sectoriel",
            "colonnes": ["Organisation", "Offre 100% digital disponible", "Revenus digitaux > 20%", "Abonnement / freemium digital", "Marketplace / plateforme", "Monétisation données"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "Partiel"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "✗", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 2 — PROCESSUS / PROCESS
    # ══════════════════════════════════════════════════════════════════

    "PROCESS::Cartographie des processus": {
        "zoom_case_study": {
            "entreprise": "Toyota",
            "pays": "Japon",
            "technologie": "Toyota Production System — Value Stream Mapping & Kaizen continu",
            "description": (
                "Toyota a inventé le Value Stream Mapping (VSM) dans les années 1950, "
                "documentant chaque étape de la chaîne de valeur pour éliminer les "
                "gaspillages (Muda). Chaque processus est capturé dans un A3 report : "
                "état actuel, état cible, plan d'action. La méthode Kaizen mobilise "
                "10 millions d'idées d'amélioration par an proposées par les employés. "
                "Le TPS est désormais la référence mondiale de l'optimisation des processus."
            ),
            "resultats": "Productivité ×3 vs concurrents · Défauts -99% · 10M suggestions/an · TPS adopté par 85% des multinationales",
            "source": "Toyota Production System / MIT Lean Enterprise Research 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité cartographie processus — benchmark sectoriel",
            "colonnes": ["Organisation", "BPM / Process mapping déployé", "BPMN documenté", "Process Mining utilisé", "Revue processus annuelle", "Certification qualité (ISO/autre)"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "Partiel", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "PROCESS::Automatisation": {
        "zoom_case_study": {
            "entreprise": "Tesla",
            "pays": "USA",
            "technologie": "Hyper-automation Gigafactory — robots + IA vision + RPA back-office",
            "description": (
                "Tesla a poussé l'automatisation à l'extrême dans ses Gigafactories : "
                "1 000+ robots Kuka sur chaque ligne, pilotés par un jumeau numérique "
                "en temps réel. Le back-office est automatisé via RPA (commandes, facturation, "
                "supply chain). Le superordinateur Dojo entraîne les modèles IA qui détectent "
                "les défauts de fabrication à la microseconde. Résultat : coût de production "
                "du Model 3 divisé par 4 en 5 ans."
            ),
            "resultats": "Coût production -75% en 5 ans · 95% des tâches répétitives automatisées · Délai livraison -40% · Défauts -60%",
            "source": "Tesla Impact Report 2023 / MIT Manufacturing Summit 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité automatisation — benchmark sectoriel",
            "colonnes": ["Organisation", "RPA / workflow automatisé", "OCR documents auto", "Décision automatisée (scoring…)", "Traitement 24/7 sans intervention", "IA cognitive déployée"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "Partiel"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "PROCESS::Agilité": {
        "zoom_case_study": {
            "entreprise": "Spotify",
            "pays": "Suède",
            "technologie": "Squads & Tribes — modèle agile à l'échelle devenu référence mondiale",
            "description": (
                "Spotify a inventé en 2012 le modèle Squads/Tribes/Chapters/Guilds, "
                "permettant à 5 000 ingénieurs de travailler de façon autonome. "
                "Chaque Squad (6–12 pers.) possède son produit de bout en bout, "
                "déploie en production indépendamment et définit ses propres OKRs. "
                "Les Chapters maintiennent l'excellence technique transverse. "
                "Ce modèle est aujourd'hui adopté par ING, BBVA, Microsoft et 30+ grandes entreprises."
            ),
            "resultats": "1 000+ déploiements/jour · Time-to-market ×4 · 100M utilisateurs · Modèle copié par 30+ entreprises mondiales",
            "source": "Spotify Engineering Culture 2022 / McKinsey Agile at Scale 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité agilité — benchmark sectoriel",
            "colonnes": ["Organisation", "Équipes agiles formalisées", "Rituels agiles réguliers", "DevOps déployé", "Product Owner nommé", "Time-to-market < 3 mois"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "PROCESS::Performance opérationnelle": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Operations Excellence — 500 KPIs temps réel, décision 100% data-driven",
            "description": (
                "Amazon mesure 500+ métriques opérationnelles en temps réel dans ses entrepôts "
                "et data centers. Chaque responsable dispose d'un tableau de bord montrant "
                "coût par expédition, taux d'erreur, NPS et vitesse de traitement. "
                "Les alertes automatiques déclenchent des actions correctives sans intervention "
                "managériale. Le principe 'Working Backwards' force chaque initiative à "
                "définir ses KPIs avant tout développement."
            ),
            "resultats": "Coût logistique -30% en 5 ans · SLA 99,8% · Traitement commande 15 min · Anomalie détectée < 5 min",
            "source": "Amazon Operations Report 2023 / Gartner Supply Chain Top 25 Awards",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité performance opérationnelle — benchmark sectoriel",
            "colonnes": ["Organisation", "KPIs digitaux définis et suivis", "SLA mesuré et publié", "Reporting temps réel", "Tableau de bord exécutif", "Coût unitaire mesuré"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "Partiel", "Partiel", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 3 — SYSTÈME D'INFORMATION / INFORMATION_SYSTEM
    # ══════════════════════════════════════════════════════════════════

    "INFORMATION_SYSTEM::Infrastructure & Cloud": {
        "zoom_case_study": {
            "entreprise": "Netflix",
            "pays": "USA",
            "technologie": "Cloud-native AWS + Chaos Engineering — résilience par conception",
            "description": (
                "Netflix a migré 100% de son infrastructure sur AWS en 2016 et inventé "
                "le Chaos Engineering : Chaos Monkey détruit aléatoirement des instances "
                "en production pour tester la résilience. L'architecture microservices "
                "(700+ services indépendants) permet des déploiements sans interruption. "
                "Netflix open-source ses outils (Eureka, Hystrix, Zuul), adoptés par "
                "des milliers d'entreprises mondiales."
            ),
            "resultats": "99,99% disponibilité · 700+ microservices · 0 downtime · 250M utilisateurs servis sans interruption",
            "source": "Netflix Tech Blog 2023 / AWS re:Invent Case Study 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité infrastructure IT — benchmark sectoriel",
            "colonnes": ["Organisation", "Cloud IaaS / SaaS adopté", "Redondance datacenter", "SLA > 99,9%", "Microservices / API-first", "DR testé annuellement"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "✓", "Partiel", "✗", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "Partiel", "✗", "✗", "✗"]}
            ]
        }
    },

    "INFORMATION_SYSTEM::Cybersécurité": {
        "zoom_case_study": {
            "entreprise": "Microsoft",
            "pays": "USA",
            "technologie": "Zero Trust Architecture — sécurité périmètre nul, 65 Mds événements/jour",
            "description": (
                "Suite à la cyberattaque SolarWinds (2020), Microsoft a généralisé le modèle "
                "Zero Trust : aucun utilisateur ni appareil n'est implicitement approuvé, "
                "même en réseau interne. Microsoft Sentinel (SIEM cloud) analyse 65 milliards "
                "d'événements de sécurité par jour. Le programme Secure Future Initiative "
                "investit 4 Mds$/an. Microsoft partage ses blueprints Zero Trust gratuitement "
                "avec 10 000+ entreprises partenaires."
            ),
            "resultats": "65 Mds événements/jour · Détection menaces < 1 min · ISO 27001/SOC2/FedRAMP · Zero Trust adopté par 70% du Fortune 500",
            "source": "Microsoft Security Report 2023 / Gartner Magic Quadrant SIEM 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité cybersécurité — benchmark sectoriel",
            "colonnes": ["Organisation", "ISO 27001 certifié", "SOC opérationnel 24/7", "MFA / Zero Trust déployé", "Tests pénétration annuels", "SIEM / détection incidents"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✓", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "Partiel", "✗", "✗"]}
            ]
        }
    },

    "INFORMATION_SYSTEM::Données & Analytics": {
        "zoom_case_study": {
            "entreprise": "Google",
            "pays": "USA",
            "technologie": "Data Mesh & BigQuery — 10 milliards de requêtes analytiques par jour",
            "description": (
                "Google a inventé MapReduce, BigTable et Dremel (l'ancêtre de BigQuery), "
                "définissant les standards du traitement de données à grande échelle. "
                "En interne, chaque décision produit est data-driven : A/B tests permanents "
                "sur 200+ dimensions, modèles ML mis à jour en temps réel. "
                "BigQuery traite 10 Mds de requêtes/jour pour des clients dans 200 pays. "
                "Le Data Catalog unifié recense 1,5 milliard de datasets actifs."
            ),
            "resultats": "10 Mds requêtes/jour · 99% des décisions produits basées sur données · BigQuery utilisé par 40 000 entreprises mondiales",
            "source": "Google Cloud Report 2023 / MIT CSAIL Data Engineering Research",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité données & analytics — benchmark sectoriel",
            "colonnes": ["Organisation", "Data Warehouse / Lake déployé", "BI self-service", "ML en production", "Data Quality framework", "Reporting réglementaire automatisé"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "Partiel", "✗", "Partiel", "✓"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "Partiel"]}
            ]
        }
    },

    "INFORMATION_SYSTEM::Intégration & API": {
        "zoom_case_study": {
            "entreprise": "Salesforce / MuleSoft",
            "pays": "USA",
            "technologie": "Anypoint Platform — API-led connectivity pour 200 000 entreprises",
            "description": (
                "MuleSoft (acquis par Salesforce en 2018 pour 6,5 Mds$) a popularisé "
                "l'architecture API-led connectivity : les systèmes sont exposés en "
                "couches (System, Process, Experience APIs). Anypoint Platform orchestre "
                "des milliards de transactions pour 200 000 entreprises clientes. "
                "Salesforce intègre MuleSoft dans sa Customer 360 platform pour connecter "
                "en temps réel CRM, ERP, e-commerce et service client."
            ),
            "resultats": "200 000 entreprises clientes · 60 Mds transactions/mois · Intégration 3× plus rapide · ROI moyen 485% (Forrester 2023)",
            "source": "Salesforce / MuleSoft Customer Success Report 2023 / Forrester TEI Study",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité intégration & API — benchmark sectoriel",
            "colonnes": ["Organisation", "API REST publiée", "ESB / Middleware déployé", "Partenaires connectés > 5", "Documentation développeur", "Stratégie API formalisée"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "✓", "Partiel", "✗", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "Partiel", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 4 — CANAUX DE DISTRIBUTION
    # ══════════════════════════════════════════════════════════════════

    "CANAUX_DISTRIBUTION::Canaux de distribution & expérience client": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Omnichannel seamless — web, mobile, voix (Alexa), physique (Amazon Go)",
            "description": (
                "Amazon a construit l'expérience omnicanale la plus avancée au monde : "
                "commande sur app, livraison en 2h (Prime Now), retour en magasin Whole Foods, "
                "achat vocal via Alexa, caisse automatique Amazon Go. Tous les canaux partagent "
                "le même panier, historique et profil client. L'algorithme de recommandation "
                "génère 35% du CA via personnalisation cross-canal."
            ),
            "resultats": "35% du CA via recommandation IA · Livraison même jour dans 100+ villes · NPS +73 · 310M clients actifs",
            "source": "Amazon Annual Report 2023 / Forrester Digital CX Awards 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Canaux de distribution digitaux — benchmark sectoriel",
            "colonnes": ["Organisation", "Site web / portail digital", "Application mobile", "Canal messaging (WhatsApp/chat)", "Self-service autonome", "Expérience omnicanale unifiée"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "Partiel", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✓", "Partiel", "✗", "✗", "✗"]}
            ]
        }
    },

    "CANAUX_DISTRIBUTION::Selfcare client": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Self-service total — 85% des demandes clients résolues sans agent humain",
            "description": (
                "Amazon a transformé le service client en moteur de satisfaction : "
                "85% des interactions sont résolues via self-service (suivi commande en temps "
                "réel, retour en 1 clic, remboursement instantané). L'assistant Alexa répond "
                "à 200M+ questions/jour. La page 'Vos commandes' permet de gérer retours, "
                "livraisons et factures sans jamais contacter un agent. "
                "Coût de service divisé par 10 vs call center traditionnel."
            ),
            "resultats": "85% résolution sans agent · Remboursement en 2 min · Coût service -90% vs traditionnel · NPS selfcare +65",
            "source": "Amazon Customer Service Report 2023 / Gartner CX Innovation Awards",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité selfcare client — benchmark sectoriel",
            "colonnes": ["Organisation", "App mobile fonctionnelle", "Simulation / devis en ligne", "Souscription 100% en ligne", "Suivi demande temps réel", "Score App Store > 4/5"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "✗", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 5 — MARKETING & COMMUNICATION
    # ══════════════════════════════════════════════════════════════════

    "MARKETING_COMMUNICATION::Marketing & communication digitale": {
        "zoom_case_study": {
            "entreprise": "HubSpot",
            "pays": "USA",
            "technologie": "Inbound Marketing — contenu + SEO + automation pour 200 000 clients",
            "description": (
                "HubSpot a inventé l'Inbound Marketing en 2006 : attirer les clients par du "
                "contenu de valeur (blog, vidéos, outils gratuits) plutôt que par la publicité "
                "intrusive. La plateforme mesure ROI de chaque contenu en temps réel. "
                "HubSpot Academy forme 300 000 professionnels/an. "
                "Le blog génère 7M de visiteurs/mois organiquement (0$ de SEA). "
                "Le taux de conversion contenu → client est de 2,7% (×3 vs publicité classique)."
            ),
            "resultats": "200 000 clients · CA 2,2 Mds$ · 7M visiteurs/mois organiques · ROI marketing ×3 vs paid · 300k certifiés/an",
            "source": "HubSpot Annual Report 2023 / Content Marketing Institute Benchmark",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Présence digitale & marketing — benchmark sectoriel",
            "colonnes": ["Organisation", "Site web SEO optimisé", "Réseaux sociaux actifs", "Publicité digitale (Google/Meta)", "Email marketing automatisé", "Analytics / ROI marketing mesuré"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "✓", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "Partiel", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 6 — RH & CULTURE DIGITALE
    # ══════════════════════════════════════════════════════════════════

    "RH_CULTURE_DIGITALE::Culture digitale": {
        "zoom_case_study": {
            "entreprise": "Microsoft",
            "pays": "USA",
            "technologie": "Growth Mindset — transformation culturelle par Satya Nadella",
            "description": (
                "Arrivé en 2014, Satya Nadella transforme Microsoft avec la philosophie "
                "'Growth Mindset' (Carol Dweck) : l'erreur est une opportunité d'apprentissage, "
                "non un échec. Il remplace la courbe de notation forcée par une culture "
                "de collaboration et d'apprentissage continu. 100% des managers sont formés. "
                "LinkedIn Learning est déployé pour 220 000 employés. "
                "Le score de culture digitale interne passe de 40 à 82/100 en 5 ans."
            ),
            "resultats": "Capitalisation ×10 en 10 ans · eNPS +55 · 100% managers formés · Microsoft revient N°1 mondial capitalisation",
            "source": "Microsoft Annual Report 2023 / Harvard Business Review Nadella Case Study",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité culture digitale — benchmark sectoriel",
            "colonnes": ["Organisation", "Formation digitale obligatoire", "E-learning disponible", "Budget formation > 2% masse salariale", "Certification digitale encouragée", "Culture innovation documentée"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "Partiel", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "RH_CULTURE_DIGITALE::Poste de travail du banquier": {
        "zoom_case_study": {
            "entreprise": "Microsoft",
            "pays": "USA",
            "technologie": "Microsoft 365 + Copilot — poste de travail intelligent pour 300M utilisateurs",
            "description": (
                "Microsoft 365 (Teams, Outlook, SharePoint, OneDrive) équipe 300 millions "
                "d'utilisateurs professionnels en poste de travail cloud-native. "
                "Microsoft Copilot (IA générative intégrée) rédige emails, résume réunions "
                "et génère des analyses à la demande. Le déploiement Zero-Touch permet "
                "l'activation complète d'un poste en 15 minutes. Le VPN est remplacé par "
                "Azure AD Conditional Access pour un accès sécurisé partout."
            ),
            "resultats": "300M utilisateurs · Productivité individuelle +20% avec Copilot · Activation poste 15 min · 60% télétravail sans friction",
            "source": "Microsoft Work Trend Index 2023 / Gartner Digital Workplace Magic Quadrant",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Équipement numérique du collaborateur — benchmark sectoriel",
            "colonnes": ["Organisation", "PC portable / accès distant", "Suite bureautique cloud", "CRM / outil métier déployé", "Outils collaboration (Teams/Zoom)", "Poste accessible en mobilité"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "✓", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "Partiel", "Partiel", "✗", "✗"]}
            ]
        }
    },

    "RH_CULTURE_DIGITALE::Collaboratif & digital working": {
        "zoom_case_study": {
            "entreprise": "Salesforce",
            "pays": "USA",
            "technologie": "Slack + Work.com — collaboration digitale unifiée pour 150 000 employés",
            "description": (
                "Salesforce a acquis Slack en 2021 pour 27,7 Mds$ et en fait la colonne "
                "vertébrale de sa collaboration interne pour 150 000 employés. "
                "Slack Huddles remplace 40% des réunions. Les Canvas documentent les "
                "projets collaborativement en temps réel. Salesforce Anywhere permet "
                "de travailler depuis n'importe quel endroit avec productivité équivalente "
                "au bureau. eNPS collaboratif +38 pts depuis le déploiement."
            ),
            "resultats": "40% de réunions remplacées · eNPS +38 · Temps de décision -50% · 150 000 employés en full remote capable",
            "source": "Salesforce Annual Report 2023 / Microsoft Teams vs Slack Gartner Report 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Travail collaboratif digital — benchmark sectoriel",
            "colonnes": ["Organisation", "Télétravail formellement possible", "Outils collaboration déployés", "Espace coworking interne", "RSE / communautés métier", "Politique BYOD"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "Partiel", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "Partiel", "✗", "✗", "✗"]}
            ]
        }
    },

    "RH_CULTURE_DIGITALE::Digitalisation de la fonction RH": {
        "zoom_case_study": {
            "entreprise": "Workday",
            "pays": "USA",
            "technologie": "SIRH cloud-native — RH 100% digitale pour 10 000 entreprises mondiales",
            "description": (
                "Workday a créé en 2005 le premier SIRH cloud-native, remplaçant les silos "
                "SAP on-premise. Paie, recrutement (ATS), gestion talents, évaluation "
                "et formation sur une seule plateforme. Workday Peakon mesure l'engagement "
                "en temps réel via pulse surveys hebdomadaires. "
                "Le module Workday Skills Cloud mappe les compétences de 65M employés "
                "dans 10 000 entreprises pour identifier les gaps et opportunités internes."
            ),
            "resultats": "10 000 entreprises clientes · Délai recrutement -40% · Coût RH -30% · 65M employés dans le Skills Cloud · Paie 100% automatisée",
            "source": "Workday Annual Report 2023 / Gartner Magic Quadrant HCM Suite 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Digitalisation RH — benchmark sectoriel",
            "colonnes": ["Organisation", "SIRH digital déployé", "Recrutement 100% en ligne", "Évaluation dématérialisée", "Portail self-service RH", "E-learning / formation interne"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "✓", "Partiel", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["Partiel", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "RH_CULTURE_DIGITALE::Agilité": {
        "zoom_case_study": {
            "entreprise": "ING Group",
            "pays": "Pays-Bas",
            "technologie": "Transformation agile à l'échelle — 350 Squads, 0 hiérarchie traditionnelle",
            "description": (
                "En 2015, ING Netherlands supprime tous les départements traditionnels "
                "pour créer 350 Squads autonomes regroupées en Tribes thématiques. "
                "Chaque Squad est cross-fonctionnelle (dev, data, business, design) et "
                "livre de la valeur en autonomie. Les silos IT/Business sont éliminés. "
                "Un Agile Coach accompagne chaque Tribe de 150 personnes. "
                "OKRs trimestriels remplacent les objectifs annuels."
            ),
            "resultats": "Time-to-market 6 mois → 3 semaines · Satisfaction employé +40% · 30% features supplémentaires livrées · Modèle adopté par 30+ banques",
            "source": "ING Agile Transformation 2023 / McKinsey Agile Banking Research",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité agilité organisationnelle — benchmark sectoriel",
            "colonnes": ["Organisation", "Équipes agiles formalisées", "OKRs déployés", "Product Owners nommés", "Rituel agile hebdomadaire", "Agile Coach interne"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 7 — OFFRES DIGITALES
    # ══════════════════════════════════════════════════════════════════

    "OFFRES_DIGITALES::Offres digitales": {
        "zoom_case_study": {
            "entreprise": "Apple",
            "pays": "USA",
            "technologie": "App Store ecosystem — 1,8 million d'apps, modèle de plateforme digitale",
            "description": (
                "Apple a créé en 2008 l'App Store, inventant le modèle de distribution "
                "d'offres digitales à grande échelle. La plateforme génère 85 Mds$/an "
                "de revenu pour les développeurs. Chaque nouvelle offre d'Apple "
                "(Apple Music, TV+, Pay, Fitness+) est native-digital, lancée simultanément "
                "dans 175 pays. Le bundling via Apple One (6 services) fidélise via "
                "l'écosystème plutôt qu'un produit unique."
            ),
            "resultats": "1,8M d'apps · 85 Mds$ revenus développeurs/an · Services CA 85 Mds$ · 1 Md+ appareils actifs",
            "source": "Apple Annual Report 2023 / App Store Economics Report 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Offres digitales disponibles — benchmark sectoriel",
            "colonnes": ["Organisation", "Offre cœur de métier 100% digital", "Offre complémentaire digitale", "Souscription / achat en ligne", "Offre mobile native", "Bundling / écosystème digital"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "Partiel"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "Partiel", "Partiel", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "OFFRES_DIGITALES::Open banking (BaaS, BaaP)": {
        "zoom_case_study": {
            "entreprise": "Stripe",
            "pays": "USA",
            "technologie": "API-first platform — infrastructure de paiement pour 4 millions d'entreprises",
            "description": (
                "Stripe a construit en 2010 l'infrastructure de paiement la plus simple "
                "à intégrer : 7 lignes de code pour accepter des paiements en ligne. "
                "La plateforme s'est étendue en 'OS financier' : paiements, facturation, "
                "taxes, identité, financement aux entreprises. 4 millions d'entreprises "
                "utilisent Stripe comme couche financière. Le revenu 2023 dépasse 14 Mds$. "
                "Modèle BaaS pur : Stripe fournit la plomberie, les clients construisent les produits."
            ),
            "resultats": "4M entreprises clientes · CA 14 Mds$ · Valorisation 50 Mds$ · 135 pays · 7 lignes de code pour s'intégrer",
            "source": "Stripe Annual Report 2023 / CB Insights Fintech 250",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité plateforme ouverte (BaaS/API) — benchmark sectoriel",
            "colonnes": ["Organisation", "API publiée & documentée", "Partenaires connectés", "Offre embarquable (BaaS/BaaP)", "SDK / marketplace", "Stratégie plateforme ouverte"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✗", "✗", "✗"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 8 — MODÈLE OPÉRATIONNEL & INNOVATION
    # ══════════════════════════════════════════════════════════════════

    "MODELE_OPERATIONNEL_INNOVATION::Simplification & automatisation des processus": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Fulfilment automation — entrepôts 75% robotisés, livraison en 2h",
            "description": (
                "Amazon a simplifié et automatisé l'intégralité de sa chaîne de valeur : "
                "75% des tâches en entrepôt sont robotisées (Kiva robots), la commande "
                "est traitée en 15 minutes, la livraison garantie en 2h dans 100+ villes. "
                "Le back-office (facturation, retours, réclamations) est automatisé à 90%. "
                "Amazon Go élimine la caisse : les clients prennent et partent, "
                "la facture est débitée automatiquement via vision IA."
            ),
            "resultats": "75% robotisation entrepôts · Traitement commande 15 min · Livraison 2h · Coût opérationnel -40% vs 2018",
            "source": "Amazon Robotics Report 2023 / MIT Operations Research Lab",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Simplification processus clés — benchmark sectoriel",
            "colonnes": ["Organisation", "Onboarding client < 15 min", "Processus cœur automatisé", "Traitement demandes 24/7", "Réclamation traitée < 24h", "Zéro papier pour processus clés"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✓", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "Partiel", "✗", "✗"]}
            ]
        }
    },

    "MODELE_OPERATIONNEL_INNOVATION::Gouvernance de la transformation digitale": {
        "zoom_case_study": {
            "entreprise": "Microsoft",
            "pays": "USA",
            "technologie": "Digital Transformation Office — gouvernance agile de 200+ initiatives simultanées",
            "description": (
                "Microsoft pilote sa transformation via un Digital Transformation Office "
                "qui coordonne 200+ initiatives stratégiques en parallèle. Chaque initiative "
                "a un Executive Sponsor, un Product Owner, des KPIs trimestriels et "
                "un budget dédié. Le Transformation Dashboard est présenté au Board "
                "chaque trimestre. Le Chief Transformation Officer (CTO) siège au COMEX "
                "avec pouvoir de stopper ou accélérer tout projet selon les métriques."
            ),
            "resultats": "200+ initiatives pilotées · ROI transformation ×10 en 10 ans · 0 projet > 6 mois sans livrable · Best Governed Tech Company 2023",
            "source": "Microsoft Annual Report 2023 / Gartner IT Governance Summit 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Gouvernance transformation digitale — benchmark sectoriel",
            "colonnes": ["Organisation", "Comité digital au COMEX", "Budget transformation dédié", "Directeur transformation nommé", "KPIs transformation suivis", "Reporting board trimestriel"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["✓", "Partiel", "Partiel", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    "MODELE_OPERATIONNEL_INNOVATION::Développement de l'innovation": {
        "zoom_case_study": {
            "entreprise": "Google X (Alphabet)",
            "pays": "USA",
            "technologie": "Moonshot Factory — fail fast, learn fast, scale fast",
            "description": (
                "Google X est une usine à moonshots : des projets 10× (non 10%) opérés "
                "comme des startups indépendantes avec budget dédié et droit à l'échec "
                "explicitement documenté. Le processus : identifier un problème mondial "
                "énorme, une solution radicale, une technologie réalisable. "
                "Waymo (véhicules autonomes), Wing (livraison drone), Loon (internet "
                "par ballons) sont nés de ce modèle. 50 équipes évaluées/an, 5 survivent."
            ),
            "resultats": "Waymo valorisée 30 Mds$ · Wing livre 1M colis/an · 50 projets évalués/an · Taux d'échec assumé 90% · ROI moonshots ×100",
            "source": "Alphabet X Annual Report 2023 / Harvard Innovation Lab Case Study",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité développement innovation — benchmark sectoriel",
            "colonnes": ["Organisation", "Lab / studio innovation interne", "Partenariats startups actifs", "Programme innovation interne", "Budget innovation dédié", "Prototypes / MVPs lancés/an"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "Partiel", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "✗", "✗", "✗"]}
            ]
        }
    },

    # ══════════════════════════════════════════════════════════════════
    # AXE 9 — IT & DATA
    # ══════════════════════════════════════════════════════════════════

    "IT_DATA::Socle IT": {
        "zoom_case_study": {
            "entreprise": "Netflix",
            "pays": "USA",
            "technologie": "Cloud-native + Chaos Engineering — socle IT résilient par conception",
            "description": (
                "Netflix a migré 100% de son socle IT sur AWS (2012–2016) avec une architecture "
                "microservices où chaque service est déployé indépendamment. "
                "Chaos Monkey et la Simian Army testent en permanence la résilience "
                "en cassant des composants aléatoirement en production. "
                "CI/CD full automatisé : 1 000+ déploiements/jour sans downtime. "
                "Le DR est testé chaque mois via Chaos Gorilla (suppression d'une zone AWS entière)."
            ),
            "resultats": "99,99% SLA (4 min/an) · 1 000 déploiements/jour · DR mensuel · Coût infra -50% vs datacenter own",
            "source": "Netflix Tech Blog 2023 / AWS re:Invent 2023 Case Study",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité socle IT — benchmark sectoriel",
            "colonnes": ["Organisation", "Cloud IaaS/SaaS adopté", "SLA documenté et mesuré", "DR / BCP testé annuellement", "DevOps / CI-CD déployé", "Système cœur < 10 ans"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "✓", "Partiel", "✗", "✓"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "Partiel", "Partiel", "✗", "✗"]}
            ]
        }
    },

    "IT_DATA::Data": {
        "zoom_case_study": {
            "entreprise": "Amazon",
            "pays": "USA",
            "technologie": "Data Flywheel — chaque interaction enrichit les modèles, chaque modèle améliore l'expérience",
            "description": (
                "Amazon a bâti un avantage compétitif structurel via son Data Flywheel : "
                "chaque achat, clic et retour enrichit les modèles de recommandation, "
                "qui améliorent l'expérience, attirant plus de clients, générant plus de données. "
                "Le moteur de recommandation génère 35% du CA. "
                "AWS Lake Formation gère des exaoctets de données pour 100 000+ clients. "
                "50 000 data scientists et ML engineers en interne."
            ),
            "resultats": "35% CA via recommandation IA · 50 000 data ingénieurs · AWS leader mondial données · Décision en temps réel sur 500M+ produits",
            "source": "Amazon Annual Report 2023 / McKinsey Data Value Creation 2023",
            "annee": "2023"
        },
        "comparatif_organisations": {
            "titre": "Maturité Data & IA — benchmark sectoriel",
            "colonnes": ["Organisation", "Data Catalog déployé", "ML / IA en production", "Reporting réglementaire automatisé", "Data Quality framework", "Self-service analytics métiers"],
            "lignes": [
                {"organisation": "Leader du marché",     "valeurs": ["✓", "✓", "✓", "✓", "✓"]},
                {"organisation": "Acteur intermédiaire", "valeurs": ["Partiel", "Partiel", "✓", "Partiel", "Partiel"]},
                {"organisation": "Acteur traditionnel",  "valeurs": ["✗", "✗", "Partiel", "✗", "✗"]}
            ]
        }
    },

}  # end GENERIC_EXTRA
