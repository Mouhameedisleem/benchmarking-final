"""
Regulatory & Compliance Knowledge Base
Maps sectors and regions to applicable regulations, standards, and compliance requirements.
Sources: EUR-Lex, ANSSI, CNIL, HACA (Maroc), INPDP (Tunisie), ANPDP (Algérie), ISO, IEC.
"""

# ─── GLOBAL REGULATIONS (applicable everywhere) ────────────────────────────

GLOBAL_REGULATIONS: list[dict] = [
    {
        "id": "RGPD",
        "name": "RGPD — Règlement Général sur la Protection des Données",
        "short": "RGPD / GDPR",
        "scope": "Protection des données personnelles",
        "applies_to": ["all"],
        "regions": ["europe", "maghreb", "africa"],
        "axis": ["INFORMATION_SYSTEM", "PROCESS"],
        "requirements": [
            "Registre des activités de traitement",
            "Nomination d'un DPO si traitement à grande échelle",
            "Politique de confidentialité et consentement",
            "Droit à l'effacement et à la portabilité des données",
            "Notification de violation sous 72h",
            "Privacy by design et privacy by default"
        ],
        "maturity_impact": "Un score SI < 50 indique probablement des non-conformités RGPD.",
        "reference": "Règlement (UE) 2016/679 — CNIL.fr"
    },
    {
        "id": "ISO27001",
        "name": "ISO/IEC 27001 — Système de Management de la Sécurité de l'Information",
        "short": "ISO 27001",
        "scope": "Cybersécurité et sécurité de l'information",
        "applies_to": ["all"],
        "regions": ["global"],
        "axis": ["INFORMATION_SYSTEM"],
        "requirements": [
            "Analyse des risques de sécurité (SMSI)",
            "Politique de sécurité de l'information",
            "Contrôles d'accès et gestion des identités",
            "Continuité d'activité et plan de reprise (PRA/PCA)",
            "Audit et tests de pénétration réguliers",
            "Formation et sensibilisation du personnel"
        ],
        "maturity_impact": "Niveau AVANCÉ requis pour certification ISO 27001.",
        "reference": "ISO/IEC 27001:2022 — iso.org"
    },
]

# ─── SECTOR-SPECIFIC REGULATIONS ───────────────────────────────────────────

SECTOR_REGULATIONS: dict[str, list[dict]] = {
    "finance": [
        {
            "id": "DORA",
            "name": "DORA — Digital Operational Resilience Act",
            "short": "DORA (UE)",
            "scope": "Résilience opérationnelle numérique du secteur financier",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Gestion des risques liés aux TIC (tests de résilience)",
                "Gestion et notification des incidents TIC",
                "Tests de résilience opérationnelle numérique (TLPT)",
                "Gestion du risque tiers lié aux TIC",
                "Partage d'informations sur les cybermenaces"
            ],
            "deadline": "Applicable depuis janvier 2025",
            "maturity_impact": "Score SI minimum requis : 65/100 pour conformité DORA.",
            "reference": "Règlement (UE) 2022/2554 — eur-lex.europa.eu"
        },
        {
            "id": "BALE4",
            "name": "Bâle IV — Réforme des exigences en fonds propres",
            "short": "Bâle IV",
            "scope": "Gouvernance et risques bancaires",
            "regions": ["europe", "global"],
            "axis": ["BUSINESS", "PROCESS"],
            "requirements": [
                "Calcul standardisé du risque de crédit",
                "Modélisation interne des risques opérationnels",
                "Ratio de levier et NSFR",
                "Reporting réglementaire renforcé (FINREP, COREP)"
            ],
            "deadline": "Transposition progressive 2025-2028",
            "maturity_impact": "Gouvernance des processus (PROCESS) doit atteindre 60/100.",
            "reference": "Comité de Bâle sur le contrôle bancaire (BCBS)"
        },
        {
            "id": "DSP2",
            "name": "DSP2 — Directive sur les Services de Paiement",
            "short": "DSP2",
            "scope": "Open banking, authentification forte (SCA)",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM", "BUSINESS"],
            "requirements": [
                "Authentification forte du client (SCA/2FA)",
                "APIs open banking sécurisées (PSD2 APIs)",
                "Accès des tiers aux comptes (XS2A)",
                "Protection contre la fraude au paiement"
            ],
            "deadline": "En vigueur — DSP3 en préparation",
            "maturity_impact": "Exige un niveau SI INTERMÉDIAIRE minimum.",
            "reference": "Directive 2015/2366/UE — Banque de France"
        }
    ],
    "banque": [
        {
            "id": "DORA",
            "name": "DORA — Digital Operational Resilience Act",
            "short": "DORA (UE)",
            "scope": "Résilience opérationnelle numérique",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Tests de résilience opérationnelle numérique",
                "Gestion des incidents TIC",
                "Gestion du risque fournisseur TIC",
                "Cartographie des systèmes critiques"
            ],
            "deadline": "Applicable depuis janvier 2025",
            "maturity_impact": "Score SI minimum requis : 65/100.",
            "reference": "Règlement (UE) 2022/2554"
        }
    ],
    "sante": [
        {
            "id": "HDS",
            "name": "HDS — Hébergement de Données de Santé",
            "short": "HDS (France)",
            "scope": "Hébergement et traitement des données de santé",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Certification HDS obligatoire pour hébergement de données de santé",
                "Traçabilité des accès aux données patients",
                "Chiffrement des données au repos et en transit",
                "Plan de continuité et reprise d'activité (PRA santé)",
                "Pseudonymisation des données pour la recherche"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "Niveau SI AVANCÉ requis. Non-conformité = interdiction d'exercice.",
            "reference": "Code de la santé publique, Art. L. 1111-8 — esante.gouv.fr"
        },
        {
            "id": "ESPACE_SANTE",
            "name": "Mon Espace Santé — DMP et interopérabilité",
            "short": "Mon Espace Santé",
            "scope": "Dossier Médical Partagé et interopérabilité des SI de santé",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Alimentation du Dossier Médical Partagé (DMP)",
                "Interopérabilité avec les standards HL7 FHIR",
                "Messagerie sécurisée de santé (MSSanté)",
                "Agenda en ligne et téléconsultation"
            ],
            "deadline": "Déploiement progressif 2024-2026",
            "maturity_impact": "Exige niveau INTERMÉDIAIRE minimum en axe SI.",
            "reference": "SÉGUR DU NUMÉRIQUE EN SANTÉ — esante.gouv.fr"
        },
        {
            "id": "SMSI_SANTE",
            "name": "Politique Générale de Sécurité des SI de Santé (PGSSI-S)",
            "short": "PGSSI-S",
            "scope": "Sécurité des systèmes d'information de santé",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Authentification forte des professionnels de santé (e-CPS)",
                "Identitovigilance et identité nationale de santé (INS)",
                "Habilitations et contrôle des accès par profil",
                "Plan de gestion des crises cyber (CERT Santé)"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "",
            "reference": "ANS — Agence du Numérique en Santé"
        }
    ],
    "energie": [
        {
            "id": "NIS2",
            "name": "NIS2 — Directive sur la sécurité des réseaux et systèmes d'information",
            "short": "NIS2 (UE)",
            "scope": "Cybersécurité des infrastructures critiques et essentielles",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Mesures de gestion des risques cybersécurité",
                "Notification d'incidents sous 24h (alerte) / 72h (rapport)",
                "Sécurité de la chaîne d'approvisionnement",
                "Formation obligatoire des dirigeants à la cybersécurité",
                "Tests de résilience et plans de réponse aux incidents"
            ],
            "deadline": "Transposition nationale octobre 2024",
            "maturity_impact": "Score SI minimum 60/100. Les entités 'essentielles' doivent atteindre 70/100.",
            "reference": "Directive (UE) 2022/2555 — ANSSI.gouv.fr"
        }
    ],
    "telecom": [
        {
            "id": "NIS2",
            "name": "NIS2 — Directive Réseaux et SI",
            "short": "NIS2 (UE)",
            "scope": "Cybersécurité des opérateurs de télécommunications",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Notification d'incidents cyber significatifs",
                "Sécurité des réseaux de communication",
                "Gestion des risques fournisseurs (Huawei, équipements 5G)",
                "Chiffrement des communications"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "",
            "reference": "Directive (UE) 2022/2555 — ARCEP"
        },
        {
            "id": "ARCEP",
            "name": "Obligations ARCEP — Neutralité du net et qualité de service",
            "short": "ARCEP",
            "scope": "Régulation des télécommunications (France)",
            "regions": ["europe"],
            "axis": ["PROCESS", "BUSINESS"],
            "requirements": [
                "Rapports de qualité de service (débit, latence, disponibilité)",
                "Respect de la neutralité du net",
                "Couverture réseau et déploiement 5G",
                "Portabilité des numéros"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "",
            "reference": "arcep.fr"
        }
    ],
    "industrie": [
        {
            "id": "NIS2",
            "name": "NIS2 — Cybersécurité des OIV et OSE",
            "short": "NIS2 (UE)",
            "scope": "Opérateurs d'importance vitale et services essentiels",
            "regions": ["europe"],
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Sécurisation des systèmes SCADA/OT",
                "Ségrégation des réseaux IT/OT",
                "Tests d'intrusion sur les systèmes industriels",
                "Plan de continuité pour la production"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "Critique pour les OIV. Score SI minimum 65/100.",
            "reference": "ANSSI — Guide sécurité des systèmes industriels"
        },
        {
            "id": "ISO50001",
            "name": "ISO 50001 — Management de l'énergie",
            "short": "ISO 50001",
            "scope": "Efficacité énergétique et développement durable",
            "regions": ["global"],
            "axis": ["PROCESS"],
            "requirements": [
                "Système de management de l'énergie (SMÉ)",
                "Audit énergétique et tableau de bord",
                "Objectifs de réduction de consommation",
                "Rapport RSE et empreinte carbone"
            ],
            "deadline": "Recommandé",
            "maturity_impact": "",
            "reference": "iso.org/iso-50001"
        }
    ],
    "assurance": [
        {
            "id": "SOLV2",
            "name": "Solvabilité II — Directive assurance européenne",
            "short": "Solvabilité II",
            "scope": "Gouvernance, risques et capital des assureurs",
            "regions": ["europe"],
            "axis": ["PROCESS", "BUSINESS"],
            "requirements": [
                "Calcul du Solvency Capital Requirement (SCR)",
                "Gouvernance et gestion des risques (ORSA)",
                "Reporting réglementaire (QRT, SFCR, RSR)",
                "Exigences d'honorabilité et compétences des dirigeants"
            ],
            "deadline": "En vigueur — révision 2024",
            "maturity_impact": "Axe PROCESSUS doit atteindre 60/100 pour conformité.",
            "reference": "Directive 2009/138/CE — ACPR"
        }
    ],
    "banque_uemoa": [
        {
            "id": "BCEAO_INSTRUC_008",
            "name": "Instruction BCEAO 008-05-2015 — Monnaie électronique dans l'UEMOA",
            "short": "BCEAO 008-05-2015",
            "scope": "Émission et gestion de la monnaie électronique",
            "regions": ["uemoa", "west_africa"],
            "axis": ["BUSINESS", "INFORMATION_SYSTEM", "OFFRES_DIGITALES"],
            "requirements": [
                "Agrément BCEAO obligatoire pour l'émission de monnaie électronique",
                "Ségrégation des fonds clients (cantonnement) à 100%",
                "Interopérabilité technique entre émetteurs de monnaie électronique",
                "Plafonds de transactions définis (solde max, transactions journalières)",
                "Reporting mensuel des transactions à la BCEAO",
                "KYC simplifié pour les comptes de faible valeur (low-KYC)"
            ],
            "deadline": "En vigueur depuis 2015",
            "maturity_impact": "Requis pour tout service de mobile money ou paiement digital dans l'UEMOA.",
            "reference": "BCEAO — bceao.int"
        },
        {
            "id": "LOI_2013_015",
            "name": "Loi 2013-015 — Cybersécurité et Protection des données dans l'UEMOA",
            "short": "Loi 2013-015 UEMOA",
            "scope": "Cybercriminalité et protection des données personnelles",
            "regions": ["uemoa", "west_africa"],
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Protection des systèmes d'information contre les cyberattaques",
                "Signalement des incidents de sécurité informatique aux autorités",
                "Protection des données personnelles des clients",
                "Obligations de confidentialité et de sécurité des transactions"
            ],
            "deadline": "En vigueur",
            "maturity_impact": "Score SI minimum requis : 50/100 pour les opérateurs financiers.",
            "reference": "Loi uniforme UEMOA sur la cybersécurité"
        },
        {
            "id": "BCEAO_CIRCULAIRE_003",
            "name": "Circulaire BCEAO 003-2011 — Conditions d'exercice du crédit",
            "short": "Circulaire BCEAO 003",
            "scope": "Réglementation des activités de crédit et bancaires",
            "regions": ["uemoa"],
            "axis": ["BUSINESS", "PROCESS"],
            "requirements": [
                "Conditions minimales de fonds propres pour les établissements de crédit",
                "Normes prudentielles (coefficient de solvabilité, liquidité)",
                "Obligations de reporting trimestriel à la BCEAO",
                "Politique de provisionnement des créances douteuses",
                "Respect des ratios de la Commission Bancaire UMOA"
            ],
            "deadline": "En vigueur — révisions périodiques",
            "maturity_impact": "Gouvernance des processus financiers doit atteindre 55/100.",
            "reference": "Commission Bancaire UMOA — umoa-titres.uemoa.int"
        },
        {
            "id": "BCEAO_OPEN_BANKING",
            "name": "Cadre BCEAO pour l'Interopérabilité et l'Open Banking (UEMOA)",
            "short": "BCEAO Open Banking",
            "scope": "Interopérabilité des systèmes de paiement et open banking",
            "regions": ["uemoa"],
            "axis": ["INFORMATION_SYSTEM", "OFFRES_DIGITALES", "CANAUX_DISTRIBUTION"],
            "requirements": [
                "Connexion obligatoire au GIM-UEMOA (Groupement Interbancaire Monétique)",
                "Compatibilité avec le SIMT (Système Interbancaire de Monnaie Électronique BCEAO)",
                "Interopérabilité technique avec les opérateurs de mobile money",
                "APIs sécurisées pour l'accès des tiers autorisés (fintech partenaires)",
                "Standards de sécurité ISO 8583 / ISO 20022 pour les paiements"
            ],
            "deadline": "En déploiement progressif 2023-2026",
            "maturity_impact": "Exige un niveau SI INTERMÉDIAIRE minimum pour la conformité.",
            "reference": "BCEAO — Stratégie de Digitalisation Financière UEMOA 2025"
        }
    ],
}

# ─── REGIONAL REGULATIONS ───────────────────────────────────────────────────

REGIONAL_REGULATIONS: dict[str, list[dict]] = {
    "maroc": [
        {
            "id": "LOI09_08",
            "name": "Loi 09-08 — Protection des données personnelles (Maroc)",
            "short": "Loi 09-08",
            "scope": "Protection des données personnelles",
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Déclaration des traitements de données à la CNDP",
                "Droit d'accès, de rectification et d'opposition",
                "Transferts internationaux de données encadrés",
                "Nomination d'un correspondant informatique et libertés"
            ],
            "maturity_impact": "",
            "reference": "Commission Nationale de Contrôle de la Protection des Données — cndp.ma"
        },
        {
            "id": "LOI07_03",
            "name": "Loi 07-03 — Cybercriminalité (Maroc)",
            "short": "Loi 07-03",
            "scope": "Lutte contre la cybercriminalité",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Protection des systèmes informatiques contre les intrusions",
                "Signalement des cyberattaques aux autorités",
                "Conservation des logs d'accès"
            ],
            "maturity_impact": "",
            "reference": "DGSSI — Direction Générale de la Sécurité des Systèmes d'Information"
        },
        {
            "id": "DGSSI_MA",
            "name": "Directive DGSSI — Sécurité des SI au Maroc",
            "short": "DGSSI",
            "scope": "Cybersécurité nationale",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Référentiel général de sécurité marocain (RGS-MA)",
                "Homologation des SI sensibles",
                "maCERT — notification des incidents"
            ],
            "maturity_impact": "",
            "reference": "dgssi.gov.ma"
        }
    ],
    "tunisie": [
        {
            "id": "LOI2004_63",
            "name": "Loi 2004-63 — Protection des données personnelles (Tunisie)",
            "short": "Loi 2004-63",
            "scope": "Protection des données personnelles",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Déclaration préalable auprès de l'INPDP",
                "Droits des personnes concernées (accès, rectification)",
                "Sécurisation des traitements de données"
            ],
            "maturity_impact": "",
            "reference": "Instance Nationale de Protection des Données Personnelles — inpdp.nat.tn"
        },
        {
            "id": "ANSI_TN",
            "name": "Décret 2004-1248 — Cybersécurité nationale (Tunisie)",
            "short": "ANSI Tunisie",
            "scope": "Sécurité des systèmes d'information",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Audit de sécurité obligatoire pour les SI de l'État",
                "Certification des produits de sécurité",
                "tCERT — réponse aux incidents"
            ],
            "maturity_impact": "",
            "reference": "Agence Nationale de Sécurité Informatique — ansi.tn"
        }
    ],
    "algerie": [
        {
            "id": "LOI18_07",
            "name": "Loi 18-07 — Protection des données personnelles (Algérie)",
            "short": "Loi 18-07",
            "scope": "Protection des données personnelles",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Déclaration des traitements à l'ANPDP",
                "Droit à l'information et au consentement",
                "Obligation de sécurité des données"
            ],
            "maturity_impact": "",
            "reference": "Autorité Nationale de Protection des Données Personnelles — anpdp.dz"
        }
    ],
    "senegal": [
        {
            "id": "LOI2008_12",
            "name": "Loi 2008-12 — Protection des données à caractère personnel (Sénégal)",
            "short": "Loi 2008-12 CDP",
            "scope": "Protection des données personnelles",
            "axis": ["INFORMATION_SYSTEM", "PROCESS"],
            "requirements": [
                "Déclaration des traitements à la CDP (Commission des Données Personnelles)",
                "Droit d'accès, de rectification et de suppression des données",
                "Obligation de sécurité et de confidentialité des données",
                "Encadrement des transferts de données hors du Sénégal"
            ],
            "maturity_impact": "",
            "reference": "Commission des Données Personnelles Sénégal — cdp.sn"
        },
        {
            "id": "BCEAO_SN",
            "name": "Réglementations BCEAO applicables au Sénégal",
            "short": "BCEAO / UEMOA",
            "scope": "Services financiers et paiements digitaux",
            "axis": ["BUSINESS", "INFORMATION_SYSTEM", "OFFRES_DIGITALES"],
            "requirements": [
                "Conformité aux instructions BCEAO sur la monnaie électronique",
                "Connexion obligatoire au GIM-UEMOA pour les opérations interbancaires",
                "Respect des normes prudentielles de la Commission Bancaire UMOA",
                "Reporting réglementaire automatisé à la BCEAO"
            ],
            "maturity_impact": "Score SI minimum 50/100 pour les opérateurs financiers.",
            "reference": "BCEAO — bceao.int, Commission Bancaire UMOA"
        }
    ],
    "cote_ivoire": [
        {
            "id": "ARTCI_CI",
            "name": "Loi sur les transactions électroniques (Côte d'Ivoire)",
            "short": "ARTCI — Loi TIC",
            "scope": "Transactions électroniques, cybersécurité et données personnelles",
            "axis": ["INFORMATION_SYSTEM", "BUSINESS"],
            "requirements": [
                "Enregistrement auprès de l'ARTCI pour les services en ligne",
                "Conditions de validité des contrats électroniques",
                "Protection des données personnelles (Loi sur la protection des données)",
                "Sécurisation des paiements en ligne"
            ],
            "maturity_impact": "",
            "reference": "ARTCI — artci.ci"
        },
        {
            "id": "BCEAO_CI",
            "name": "Réglementations BCEAO applicables en Côte d'Ivoire",
            "short": "BCEAO / UEMOA",
            "scope": "Services financiers et paiements digitaux",
            "axis": ["BUSINESS", "INFORMATION_SYSTEM", "OFFRES_DIGITALES"],
            "requirements": [
                "Conformité aux instructions BCEAO sur la monnaie électronique (008-05-2015)",
                "Agrément BCEAO pour l'émission de monnaie électronique",
                "Connexion au GIM-UEMOA",
                "Respect des normes AML/CFT (lutte contre le blanchiment)"
            ],
            "maturity_impact": "Requis pour les opérations de mobile money et banking digital.",
            "reference": "BCEAO — bceao.int"
        }
    ],
    "france": [
        {
            "id": "ANSSI_RGS",
            "name": "RGS — Référentiel Général de Sécurité (France)",
            "short": "RGS v2",
            "scope": "Sécurité des SI pour les organismes publics",
            "axis": ["INFORMATION_SYSTEM"],
            "requirements": [
                "Homologation des téléservices",
                "Authentification forte des agents (RGS **)",
                "Qualification des produits de sécurité",
                "PSSI (Politique de Sécurité des SI)"
            ],
            "maturity_impact": "",
            "reference": "ANSSI — ssi.gouv.fr"
        }
    ],
}

# Country to region key mapping
COUNTRY_TO_REGION: dict[str, str] = {
    "maroc": "maroc",
    "morocco": "maroc",
    "tunisie": "tunisie",
    "tunisia": "tunisie",
    "algérie": "algerie",
    "algerie": "algerie",
    "algeria": "algerie",
    "france": "france",
    "belgique": "france",  # EU GDPR similar
    "suisse": "france",
    "sénégal": "senegal",
    "senegal": "senegal",
    "côte d'ivoire": "cote_ivoire",
    "cote d'ivoire": "cote_ivoire",
    "cote_ivoire": "cote_ivoire",
    "ivory coast": "cote_ivoire",
    "mali": "senegal",       # UEMOA — BCEAO applies
    "burkina faso": "senegal",
    "niger": "senegal",
    "bénin": "senegal",
    "benin": "senegal",
    "togo": "senegal",
    "guinée-bissau": "senegal",
    "guinee-bissau": "senegal",
}

# UEMOA countries (West Africa) — BCEAO regulations apply to banking sector
UEMOA_COUNTRIES: set[str] = {
    "sénégal", "senegal", "côte d'ivoire", "cote d'ivoire", "cote_ivoire",
    "mali", "burkina faso", "niger", "bénin", "benin", "togo", "guinée-bissau", "guinee-bissau"
}


def get_regulations(sector: str, country: str) -> list[dict]:
    """Return all applicable regulations for a given sector and country."""
    result = []

    # 1. Always add global regulations
    result.extend(GLOBAL_REGULATIONS)

    # 2. Add sector-specific regulations
    sector_key = sector.lower().strip()
    sector_aliases = {
        "banking": "banque", "bank": "banque", "banque": "banque",
        "healthcare": "sante", "santé": "sante",
        "manufacturing": "industrie", "insurance": "assurance",
        "energy": "energie", "utilities": "energie",
        "telecom": "telecom", "telecommunications": "telecom"
    }
    sector_key = sector_aliases.get(sector_key, sector_key)

    if sector_key in SECTOR_REGULATIONS:
        result.extend(SECTOR_REGULATIONS[sector_key])

    # 3. For banking/finance in UEMOA countries, add BCEAO-specific regulations
    country_lower = country.lower().strip()
    if sector_key in ("banque", "finance") and country_lower in UEMOA_COUNTRIES:
        result.extend(SECTOR_REGULATIONS.get("banque_uemoa", []))

    # 4. Add country/region regulations
    country_key = COUNTRY_TO_REGION.get(country_lower, None)
    if country_key and country_key in REGIONAL_REGULATIONS:
        result.extend(REGIONAL_REGULATIONS[country_key])

    # Deduplicate by id
    seen = set()
    deduped = []
    for reg in result:
        if reg["id"] not in seen:
            seen.add(reg["id"])
            deduped.append(reg)

    return deduped


def format_regulations_for_prompt(sector: str, country: str) -> str:
    """Format regulations as a knowledge block for AI prompts."""
    regs = get_regulations(sector, country)
    if not regs:
        return ""

    lines = [f"\nRÉGLEMENTATIONS APPLICABLES — {sector.upper()} / {country.upper()} :"]
    for reg in regs:
        lines.append(f"\n▸ {reg['name']} ({reg['short']})")
        lines.append(f"  Périmètre : {reg['scope']}")
        lines.append(f"  Axes concernés : {', '.join(reg['axis'])}")
        lines.append(f"  Exigences clés : {' | '.join(reg['requirements'][:3])}")
        if reg.get("maturity_impact"):
            lines.append(f"  ⚠ Impact maturité : {reg['maturity_impact']}")
        lines.append(f"  Référence : {reg['reference']}")

    return "\n".join(lines)
