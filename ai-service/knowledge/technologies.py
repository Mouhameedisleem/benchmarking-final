"""
Technology Reference Knowledge Base
Maps maturity levels and axes to recommended technology solutions.
Sources: Gartner Magic Quadrant, Forrester Wave, G2, StackShare industry reports.
"""

# Structure:
# {
#   "axis": {
#     "sub_axis": {
#       "maturity_level": [
#         {"name": str, "category": str, "description": str, "examples": [str], "open_source": bool}
#       ]
#     }
#   }
# }

TECHNOLOGY_STACK: dict[str, dict] = {

    # ── AXE MÉTIER ───────────────────────────────────────────────────────────
    "BUSINESS": {
        "CRM & Relation Client": {
            "INITIAL": [
                {
                    "name": "CRM de base",
                    "category": "Customer Relationship Management",
                    "description": "Gestion centralisée des contacts et du pipeline commercial",
                    "examples": ["HubSpot CRM (gratuit)", "Zoho CRM", "Pipedrive"],
                    "open_source": False,
                    "investment": "Faible (0-200€/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "CRM avancé avec automation marketing",
                    "category": "CRM + Marketing Automation",
                    "description": "Automatisation des campagnes, scoring des leads, analytics client",
                    "examples": ["Salesforce Sales Cloud", "HubSpot Marketing Hub", "Microsoft Dynamics 365"],
                    "open_source": False,
                    "investment": "Moyen (500-3000€/mois)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme Customer Data (CDP)",
                    "category": "Customer Data Platform",
                    "description": "Vue unifiée 360° du client, personnalisation en temps réel",
                    "examples": ["Segment", "Tealium", "Adobe Real-Time CDP", "Salesforce CDP"],
                    "open_source": False,
                    "investment": "Élevé (2000-10000€/mois)"
                }
            ],
            "AVANCE": [
                {
                    "name": "IA personnalisation & recommendation engine",
                    "category": "AI-Driven Personalization",
                    "description": "Personnalisation IA de l'expérience client en temps réel",
                    "examples": ["Adobe Experience Cloud", "Salesforce Einstein", "Dynamic Yield"],
                    "open_source": False,
                    "investment": "Très élevé (custom pricing)"
                }
            ]
        },
        "Analyse & Business Intelligence": {
            "INITIAL": [
                {
                    "name": "Tableur avancé & reporting basique",
                    "category": "Reporting",
                    "description": "Tableaux de bord Excel/Google Sheets avec visualisations simples",
                    "examples": ["Microsoft Excel", "Google Sheets", "LibreOffice Calc"],
                    "open_source": True,
                    "investment": "Minimal"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Outil de Business Intelligence",
                    "category": "BI & Analytics",
                    "description": "Dashboards interactifs, rapports automatisés, self-service analytics",
                    "examples": ["Power BI", "Tableau", "Metabase (open-source)", "Looker"],
                    "open_source": False,
                    "investment": "Faible à moyen (10-70€/user/mois)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme analytics avancée",
                    "category": "Advanced Analytics",
                    "description": "Analytics prédictif, data storytelling, collaboration data",
                    "examples": ["Tableau + Einstein Analytics", "Qlik Sense", "Sisense"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ],
            "AVANCE": [
                {
                    "name": "Plateforme IA & ML intégrée",
                    "category": "AI/ML Platform",
                    "description": "Modèles prédictifs, NLP, computer vision pour les décisions métier",
                    "examples": ["Databricks", "Google Vertex AI", "Azure Machine Learning"],
                    "open_source": False,
                    "investment": "Très élevé"
                }
            ]
        },
        "E-commerce & Vente Digitale": {
            "INITIAL": [
                {
                    "name": "Site vitrine & présence en ligne",
                    "category": "Web Presence",
                    "description": "Site web professionnel avec présentation des produits/services",
                    "examples": ["WordPress + WooCommerce", "Wix", "Squarespace"],
                    "open_source": True,
                    "investment": "Minimal (50-300€/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Plateforme e-commerce",
                    "category": "E-commerce",
                    "description": "Boutique en ligne avec paiement, catalogue, gestion commandes",
                    "examples": ["Shopify", "WooCommerce", "PrestaShop", "Magento Open Source"],
                    "open_source": False,
                    "investment": "Faible à moyen"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Commerce omnicanal",
                    "category": "Omnichannel Commerce",
                    "description": "Expérience unifiée web, mobile, physique avec click & collect",
                    "examples": ["Salesforce Commerce Cloud", "Adobe Commerce", "SAP Commerce"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        }
    },

    # ── AXE CANAUX DISTRIBUTION (Digital Banking) ────────────────────────────
    "CANAUX_DISTRIBUTION": {
        "Mobile & SMS Banking": {
            "INITIAL": [
                {
                    "name": "Solution SMS/USSD Banking",
                    "category": "Mobile Financial Services",
                    "description": "Services bancaires par SMS et menus USSD pour clients sans smartphone",
                    "examples": ["InfoBip SMS Banking", "Comviva Mobiquity", "Ericsson Digital BSS", "Telepin USSD"],
                    "open_source": False,
                    "investment": "Faible à moyen (selon volume SMS)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Application Mobile Banking native",
                    "category": "Mobile Banking App",
                    "description": "App iOS/Android avec authentification biométrique, virements et paiements",
                    "examples": ["Backbase Mobile", "Temenos Infinity Mobile", "Oracle FLEXCUBE Mobile", "Solution interne React Native"],
                    "open_source": False,
                    "investment": "Moyen à élevé (200k-1M€ développement)"
                },
                {
                    "name": "Intégration Mobile Money",
                    "category": "Mobile Money Integration",
                    "description": "Connecteurs avec les wallets mobile money régionaux (interopérabilité)",
                    "examples": ["Orange Money API", "Wave API", "MTN MoMo API", "GIM-UEMOA Switch"],
                    "open_source": False,
                    "investment": "Faible (APIs partenaires)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme Digital Banking omnicanale",
                    "category": "Digital Banking Platform",
                    "description": "Plateforme unifiée web/mobile avec parcours client sans rupture",
                    "examples": ["Backbase Engagement Banking", "Finastra Digital Banking", "SAP Digital Banking"],
                    "open_source": False,
                    "investment": "Élevé (1-5M€)"
                }
            ],
            "AVANCE": [
                {
                    "name": "Super-App financière",
                    "category": "Financial Super App",
                    "description": "Application tout-en-un banking, assurance, investissement, marketplace",
                    "examples": ["Backbase Super App", "Mambu + composants", "Solution maison microservices"],
                    "open_source": False,
                    "investment": "Très élevé (custom)"
                }
            ]
        },
        "KYC & Onboarding Digital": {
            "INITIAL": [
                {
                    "name": "Formulaires d'inscription en ligne",
                    "category": "Digital Onboarding",
                    "description": "Collecte de données client via formulaires web avec upload de documents",
                    "examples": ["Typeform", "JotForm", "Solution interne", "HubSpot Forms"],
                    "open_source": False,
                    "investment": "Minimal"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Plateforme KYC & vérification d'identité (e-KYC)",
                    "category": "Identity Verification",
                    "description": "Vérification d'identité par IA : OCR documents, reconnaissance faciale, liveness check",
                    "examples": ["Smile ID (Afrique)", "Onfido", "Jumio", "Shufti Pro"],
                    "open_source": False,
                    "investment": "Faible à moyen (pay-per-check)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme AML/KYC intégrée",
                    "category": "Compliance & KYC Platform",
                    "description": "Gestion complète KYC/AML avec screening PEP/sanctions, scoring de risque client",
                    "examples": ["ComplyAdvantage", "Dow Jones Risk & Compliance", "Acuris Risk Intelligence", "Fenergo"],
                    "open_source": False,
                    "investment": "Moyen à élevé"
                }
            ]
        },
        "Agency Banking": {
            "BASIQUE": [
                {
                    "name": "Plateforme Agent Banking",
                    "category": "Agency Banking",
                    "description": "Solution pour réseau d'agents avec gestion des transactions, des limites et du float",
                    "examples": ["Craft Silicon Agent Banking", "Interswitch AgentBanking", "Temenos AgentBanking", "CR2 BankWorld Agent"],
                    "open_source": False,
                    "investment": "Moyen"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Réseau ATM/POS intelligent",
                    "category": "Self-Service Banking",
                    "description": "Gestion de parc ATM/POS avec monitoring temps réel et cash management prédictif",
                    "examples": ["NCR Atleos", "Diebold Nixdorf", "Nautilus Hyosung", "CR2 ATM"],
                    "open_source": False,
                    "investment": "Élevé (hardware + software)"
                }
            ]
        }
    },

    # ── AXE OFFRES DIGITALES ─────────────────────────────────────────────────
    "OFFRES_DIGITALES": {
        "Core Banking & Produits": {
            "INITIAL": [
                {
                    "name": "Core Banking System classique",
                    "category": "Core Banking",
                    "description": "Système central de gestion bancaire (comptes, crédits, dépôts)",
                    "examples": ["Temenos T24/Transact", "Oracle FLEXCUBE", "Misys FusionBanking", "BankPerfect"],
                    "open_source": False,
                    "investment": "Élevé (licensing + implémentation)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Core Banking Cloud-native (moderne)",
                    "category": "Modern Core Banking",
                    "description": "Core banking en microservices sur cloud pour agilité produit maximale",
                    "examples": ["Mambu (cloud-native)", "Thought Machine Vault", "10x Banking", "Finxact"],
                    "open_source": False,
                    "investment": "Élevé (SaaS)"
                }
            ]
        },
        "Paiements & Monnaie Digitale": {
            "INITIAL": [
                {
                    "name": "Passerelle de paiement locale",
                    "category": "Payment Gateway",
                    "description": "Acceptation des paiements en ligne (CB, mobile money) pour le contexte local",
                    "examples": ["CinetPay (UEMOA)", "Paytech (Sénégal)", "Stripe Africa", "PayDunya"],
                    "open_source": False,
                    "investment": "Faible (commissions sur transactions)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Switch de paiement interbancaire",
                    "category": "Interbank Payment Switch",
                    "description": "Connexion aux réseaux interbancaires pour paiements et virements régionaux",
                    "examples": ["GIM-UEMOA", "BCEAO SIMT", "Visa/Mastercard Processing", "Interswitch"],
                    "open_source": False,
                    "investment": "Moyen (membership + frais)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme de paiement en temps réel (RTP)",
                    "category": "Real-Time Payments",
                    "description": "Virement instantané 24/7 avec règlement en temps réel",
                    "examples": ["Montran RTP", "ACI Worldwide", "Finastra Payments Hub", "Temenos Payment Hub"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ],
            "AVANCE": [
                {
                    "name": "CBDC & Monnaie numérique de banque centrale",
                    "category": "Digital Currency",
                    "description": "Intégration avec les initiatives de monnaie digitale (e-CFA BCEAO en développement)",
                    "examples": ["Hyperledger Fabric", "R3 Corda", "ConsenSys Quorum", "Projet e-Naira (Nigeria)"],
                    "open_source": True,
                    "investment": "Variable (R&D + partenariats)"
                }
            ]
        },
        "Open Banking & BaaS": {
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme API Open Banking",
                    "category": "Open Banking / PSD2",
                    "description": "Exposition des APIs bancaires sécurisées pour les partenaires fintech",
                    "examples": ["Axway API Management", "MuleSoft", "Kong API Gateway", "Tyk (open-source)"],
                    "open_source": True,
                    "investment": "Moyen"
                }
            ],
            "AVANCE": [
                {
                    "name": "Banking-as-a-Service (BaaS) Platform",
                    "category": "BaaS",
                    "description": "Infrastructure bancaire exposée via APIs pour les non-banques et fintechs",
                    "examples": ["Treezor (BaaS)", "Railsbank", "Mambu BaaS", "Solarisbank"],
                    "open_source": False,
                    "investment": "Très élevé (licensing + infra)"
                }
            ]
        }
    },

    # ── AXE MARKETING & COMMUNICATION ────────────────────────────────────────
    "MARKETING_COMMUNICATION": {
        "Marketing Digital": {
            "INITIAL": [
                {
                    "name": "Présence réseaux sociaux et outils basiques",
                    "category": "Social Media",
                    "description": "Gestion des pages sociales et communication digitale de base",
                    "examples": ["Meta Business Suite", "LinkedIn Company Pages", "Hootsuite (gratuit)", "Buffer"],
                    "open_source": False,
                    "investment": "Minimal"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Plateforme Marketing Automation",
                    "category": "Marketing Automation",
                    "description": "Automatisation des emails, SMS marketing, campagnes digitales",
                    "examples": ["HubSpot Marketing", "Mailchimp", "Brevo (ex-Sendinblue)", "ActiveCampaign"],
                    "open_source": False,
                    "investment": "Faible à moyen (50-500€/mois)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Customer Data Platform (CDP)",
                    "category": "CDP",
                    "description": "Unification des données client pour la personnalisation à grande échelle",
                    "examples": ["Segment", "Tealium", "Adobe Real-Time CDP", "Bloomreach"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        }
    },

    # ── AXE RH & CULTURE DIGITALE ────────────────────────────────────────────
    "RH_CULTURE_DIGITALE": {
        "SIRH & Formation": {
            "INITIAL": [
                {
                    "name": "SIRH de base",
                    "category": "HR Information System",
                    "description": "Gestion administrative RH : paie, congés, absences",
                    "examples": ["Sage Paie", "Cegid HR", "OrangeHRM (open-source)", "Kintone"],
                    "open_source": True,
                    "investment": "Faible à moyen"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Plateforme e-learning (LMS)",
                    "category": "Learning Management System",
                    "description": "Formation en ligne, suivi des compétences et certifications",
                    "examples": ["Moodle (open-source)", "360Learning", "Cornerstone OnDemand", "Talentsoft"],
                    "open_source": True,
                    "investment": "Faible à moyen"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme SIRH complète + People Analytics",
                    "category": "HCM Suite",
                    "description": "Suite RH complète avec analytics prédictif des talents",
                    "examples": ["SAP SuccessFactors", "Workday HCM", "Oracle HCM Cloud", "ADP Workforce Now"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        }
    },

    # ── AXE PROCESSUS ────────────────────────────────────────────────────────
    "PROCESS": {
        "ERP & Gestion Intégrée": {
            "INITIAL": [
                {
                    "name": "Logiciel de comptabilité & gestion de base",
                    "category": "Accounting Software",
                    "description": "Comptabilité, facturation, gestion des stocks basique",
                    "examples": ["Sage 50", "QuickBooks", "Ciel Compta", "Wave (gratuit)"],
                    "open_source": False,
                    "investment": "Minimal (50-200€/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "ERP PME",
                    "category": "ERP",
                    "description": "Gestion intégrée finance, achats, stocks, RH pour PME",
                    "examples": ["Odoo (open-source)", "Sage 100", "Cegid", "Dolibarr (open-source)"],
                    "open_source": True,
                    "investment": "Faible à moyen (200-2000€/mois)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "ERP Enterprise",
                    "category": "ERP Enterprise",
                    "description": "ERP complet pour grandes entreprises, multi-sites, multi-devises",
                    "examples": ["SAP S/4HANA", "Oracle ERP Cloud", "Microsoft Dynamics 365 F&O"],
                    "open_source": False,
                    "investment": "Très élevé (custom)"
                }
            ]
        },
        "Automatisation & RPA": {
            "INITIAL": [
                {
                    "name": "Macros & automatisation basique",
                    "category": "Task Automation",
                    "description": "Automatisation des tâches répétitives Office et web basique",
                    "examples": ["Microsoft Power Automate (Desktop)", "Zapier", "Make (Integromat)"],
                    "open_source": False,
                    "investment": "Minimal (15-70€/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Plateforme RPA",
                    "category": "Robotic Process Automation",
                    "description": "Robots logiciels pour automatiser les processus métier structurés",
                    "examples": ["UiPath Community", "Automation Anywhere", "Blue Prism"],
                    "open_source": False,
                    "investment": "Moyen à élevé"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Hyperautomation Platform",
                    "category": "Intelligent Process Automation",
                    "description": "RPA + IA + Process Mining pour l'automatisation intelligente",
                    "examples": ["UiPath Platform", "SS&C Blue Prism", "Microsoft Power Platform"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        },
        "Gestion de Projet & Collaboration": {
            "INITIAL": [
                {
                    "name": "Outils de collaboration basiques",
                    "category": "Collaboration",
                    "description": "Messagerie, visioconférence, partage de fichiers",
                    "examples": ["Microsoft Teams", "Google Workspace", "Slack (gratuit)"],
                    "open_source": False,
                    "investment": "Minimal (0-20€/user/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Outil de gestion de projet",
                    "category": "Project Management",
                    "description": "Suivi des tâches, planning, gestion des ressources",
                    "examples": ["Jira", "Asana", "Trello", "Monday.com", "ClickUp"],
                    "open_source": False,
                    "investment": "Faible (10-30€/user/mois)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme PPM (Portfolio & Program Management)",
                    "category": "PPM",
                    "description": "Gestion de portefeuille projets, ressources, budgets à l'échelle",
                    "examples": ["ServiceNow PPM", "Planview", "SAP Portfolio Management"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        }
    },

    # ── AXE SI ───────────────────────────────────────────────────────────────
    "INFORMATION_SYSTEM": {
        "Cybersécurité": {
            "INITIAL": [
                {
                    "name": "Protection endpoint basique",
                    "category": "Endpoint Security",
                    "description": "Antivirus, pare-feu, gestion des mises à jour",
                    "examples": ["Microsoft Defender", "Bitdefender", "ESET", "Malwarebytes"],
                    "open_source": False,
                    "investment": "Minimal (5-15€/poste/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "MFA & Identity Management",
                    "category": "IAM",
                    "description": "Authentification multifacteur, SSO, gestion centralisée des identités",
                    "examples": ["Microsoft Entra ID (Azure AD)", "Okta", "Keycloak (open-source)", "Duo Security"],
                    "open_source": True,
                    "investment": "Faible à moyen"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "SIEM & SOC",
                    "category": "Security Monitoring",
                    "description": "Détection des menaces en temps réel, corrélation d'événements",
                    "examples": ["Microsoft Sentinel", "Splunk", "IBM QRadar", "Elastic SIEM"],
                    "open_source": False,
                    "investment": "Élevé"
                },
                {
                    "name": "EDR (Endpoint Detection & Response)",
                    "category": "Advanced Endpoint Protection",
                    "description": "Détection et réponse aux menaces avancées sur les postes",
                    "examples": ["CrowdStrike Falcon", "SentinelOne", "Microsoft Defender for Endpoint"],
                    "open_source": False,
                    "investment": "Moyen à élevé"
                }
            ],
            "AVANCE": [
                {
                    "name": "Zero Trust Network Access",
                    "category": "Network Security",
                    "description": "Accès sécurisé basé sur l'identité, sans VPN traditionnel",
                    "examples": ["Zscaler ZPA", "Cloudflare Access", "Palo Alto Prisma Access"],
                    "open_source": False,
                    "investment": "Élevé"
                }
            ]
        },
        "Cloud & Infrastructure": {
            "INITIAL": [
                {
                    "name": "Hébergement web basique",
                    "category": "Web Hosting",
                    "description": "Hébergement mutualisé ou VPS pour les applications",
                    "examples": ["OVHcloud", "Hostinger", "PlanetHoster", "Infomaniak"],
                    "open_source": False,
                    "investment": "Minimal (10-100€/mois)"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Infrastructure Cloud IaaS",
                    "category": "Cloud Infrastructure",
                    "description": "Serveurs, stockage et réseau cloud à la demande",
                    "examples": ["AWS EC2/S3", "Microsoft Azure VMs", "Google Compute Engine", "OVHcloud Public Cloud"],
                    "open_source": False,
                    "investment": "Variable (pay-as-you-go)"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Plateforme Cloud PaaS & Containers",
                    "category": "Platform as a Service",
                    "description": "Kubernetes, microservices, CI/CD natif cloud",
                    "examples": ["Azure Kubernetes Service", "AWS EKS", "Google GKE", "Red Hat OpenShift"],
                    "open_source": True,
                    "investment": "Moyen à élevé"
                }
            ],
            "AVANCE": [
                {
                    "name": "Architecture cloud-native multi-cloud",
                    "category": "Multi-Cloud Architecture",
                    "description": "Résilience multi-cloud, serverless, FinOps",
                    "examples": ["Terraform", "HashiCorp Vault", "AWS Multi-Region", "Azure Arc"],
                    "open_source": True,
                    "investment": "Élevé"
                }
            ]
        },
        "Data & Analytics": {
            "INITIAL": [
                {
                    "name": "Stockage et partage de données basiques",
                    "category": "File Storage",
                    "description": "Stockage centralisé des fichiers et documents",
                    "examples": ["SharePoint", "Google Drive", "Dropbox Business", "Nextcloud (open-source)"],
                    "open_source": True,
                    "investment": "Minimal"
                }
            ],
            "BASIQUE": [
                {
                    "name": "Base de données relationnelle & ETL",
                    "category": "Database & ETL",
                    "description": "Bases de données structurées et intégration de données",
                    "examples": ["PostgreSQL (open-source)", "MySQL", "Talend Open Studio", "Apache Airflow"],
                    "open_source": True,
                    "investment": "Faible"
                }
            ],
            "INTERMEDIAIRE": [
                {
                    "name": "Data Warehouse / Data Lakehouse",
                    "category": "Data Platform",
                    "description": "Centralisation, transformation et analyse des données à grande échelle",
                    "examples": ["Snowflake", "Google BigQuery", "Databricks", "Azure Synapse Analytics"],
                    "open_source": False,
                    "investment": "Moyen à élevé"
                }
            ],
            "AVANCE": [
                {
                    "name": "Plateforme MLOps & AI Platform",
                    "category": "MLOps",
                    "description": "Déploiement et monitoring des modèles IA en production",
                    "examples": ["MLflow (open-source)", "Kubeflow", "AWS SageMaker", "Azure ML Studio"],
                    "open_source": True,
                    "investment": "Élevé"
                }
            ]
        }
    }
}


def get_technologies(axis: str, maturity_level: str, sub_axis: str = None) -> list[dict]:
    """Return relevant technologies for an axis and maturity level."""
    axis_upper = axis.upper()
    level_upper = maturity_level.upper()
    result = []

    if axis_upper not in TECHNOLOGY_STACK:
        return result

    axis_data = TECHNOLOGY_STACK[axis_upper]
    for sub_axis_name, levels in axis_data.items():
        if sub_axis and sub_axis.lower() not in sub_axis_name.lower():
            continue
        if level_upper in levels:
            for tech in levels[level_upper]:
                result.append({**tech, "sub_axis": sub_axis_name})

    return result


def format_technologies_for_prompt(axis: str, maturity_level: str) -> str:
    """Format technologies as a knowledge block for injection into AI prompts."""
    techs = get_technologies(axis, maturity_level)
    if not techs:
        return ""

    lines = [f"\nTECHNOLOGIES RECOMMANDÉES — Axe {axis} (niveau {maturity_level}) :"]
    for tech in techs[:6]:  # limit to 6 to avoid prompt bloat
        lines.append(f"\n▸ [{tech['sub_axis']}] {tech['name']} ({tech['category']})")
        lines.append(f"  {tech['description']}")
        lines.append(f"  Exemples : {', '.join(tech['examples'][:3])}")
        lines.append(f"  Investissement : {tech.get('investment', 'Variable')}")
        if tech.get("open_source"):
            lines.append("  ✓ Options open-source disponibles")

    return "\n".join(lines)


def get_tech_summary(axis: str, maturity_level: str) -> str:
    """Short one-line summary of key tools for a given context."""
    techs = get_technologies(axis, maturity_level)
    if not techs:
        return ""
    examples = []
    for tech in techs[:3]:
        examples.extend(tech["examples"][:2])
    return f"Outils de référence pour ce niveau : {', '.join(examples[:5])}"
