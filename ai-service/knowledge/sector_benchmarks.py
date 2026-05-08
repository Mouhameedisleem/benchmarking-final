"""
Sector Benchmarks Knowledge Base
Average digital maturity scores by sector and region, based on:
- McKinsey Digital Quotient Industry Reports
- Gartner Digital Business Maturity Benchmarks
- WEF Digital Transformation Initiative
- Accenture Technology Vision Reports
- IDC EMEA Digital Transformation Spending Guide
"""

# Format:
# {
#   "sector_key": {
#     "global_avg": float (0-100),
#     "africa_avg": float,
#     "europe_avg": float,
#     "maghreb_avg": float,
#     "leaders_threshold": float,  # top 25% score
#     "laggards_threshold": float, # bottom 25% score
#     "business_avg": float,
#     "process_avg": float,
#     "si_avg": float,
#     "yoy_growth": float,  # average yearly score increase in %
#     "key_challenges": [str],
#     "source": str
#   }
# }

SECTOR_BENCHMARKS: dict[str, dict] = {
    "finance": {
        "label": "Finance & Banque",
        "global_avg": 68.0,
        "europe_avg": 74.0,
        "africa_avg": 52.0,
        "maghreb_avg": 55.0,
        "uemoa_avg": 42.0,
        "leaders_threshold": 82.0,
        "laggards_threshold": 48.0,
        "business_avg": 70.0,
        "process_avg": 65.0,
        "si_avg": 69.0,
        "yoy_growth": 4.2,
        "key_challenges": [
            "Modernisation des systèmes legacy (core banking)",
            "Conformité réglementaire (DORA, RGPD, BCEAO)",
            "Adoption de l'open banking et des API",
            "Cybersécurité face aux fraudes et cyberattaques"
        ],
        "source": "McKinsey Global Banking Report 2024, Gartner Banking Maturity, Hsys Digital Benchmark 2026"
    },
    "banque": {
        "label": "Banque",
        "global_avg": 68.0,
        "europe_avg": 74.0,
        "africa_avg": 52.0,
        "maghreb_avg": 55.0,
        "uemoa_avg": 42.0,
        "leaders_threshold": 82.0,
        "laggards_threshold": 48.0,
        "business_avg": 70.0,
        "process_avg": 65.0,
        "si_avg": 69.0,
        "canaux_distribution_avg": 45.0,
        "marketing_communication_avg": 38.0,
        "rh_culture_digitale_avg": 35.0,
        "offres_digitales_avg": 40.0,
        "yoy_growth": 5.8,
        "key_challenges": [
            "Modernisation du core banking (migration systèmes legacy)",
            "Conformité réglementaire BCEAO et développement du mobile money",
            "Développement de l'inclusion financière et bancarisation digitale",
            "Adoption de l'open banking et interopérabilité avec le mobile money",
            "Gestion des risques cyber et conformité AML/KYC",
            "Développement des compétences digitales internes"
        ],
        "source": "McKinsey Global Banking Report 2024, Hsys Digital Benchmark 2026, GSMA State of Mobile Money Africa"
    },
    "sante": {
        "label": "Santé",
        "global_avg": 52.0,
        "europe_avg": 60.0,
        "africa_avg": 36.0,
        "maghreb_avg": 38.0,
        "leaders_threshold": 72.0,
        "laggards_threshold": 35.0,
        "business_avg": 50.0,
        "process_avg": 54.0,
        "si_avg": 52.0,
        "yoy_growth": 5.8,
        "key_challenges": [
            "Numérisation du dossier patient (DMP/HDS)",
            "Interopérabilité des systèmes de santé",
            "Télémédecine et santé connectée",
            "Protection des données de santé (HDS, RGPD)"
        ],
        "source": "WEF Digital Health Report 2024, Accenture Health Tech Vision"
    },
    "industrie": {
        "label": "Industrie & Manufacturing",
        "global_avg": 55.0,
        "europe_avg": 63.0,
        "africa_avg": 38.0,
        "maghreb_avg": 40.0,
        "leaders_threshold": 75.0,
        "laggards_threshold": 37.0,
        "business_avg": 54.0,
        "process_avg": 58.0,
        "si_avg": 53.0,
        "yoy_growth": 6.1,
        "key_challenges": [
            "Transition vers l'Industrie 4.0 et IoT",
            "Digitalisation de la supply chain",
            "Maintenance prédictive avec l'IA",
            "Formation des équipes aux technologies digitales"
        ],
        "source": "McKinsey Industry 4.0 Report, WEF Manufacturing Maturity"
    },
    "retail": {
        "label": "Commerce & Distribution",
        "global_avg": 60.0,
        "europe_avg": 67.0,
        "africa_avg": 42.0,
        "maghreb_avg": 44.0,
        "leaders_threshold": 78.0,
        "laggards_threshold": 42.0,
        "business_avg": 65.0,
        "process_avg": 57.0,
        "si_avg": 58.0,
        "yoy_growth": 5.3,
        "key_challenges": [
            "Commerce omnicanal et expérience client digitale",
            "Personnalisation par l'IA et big data",
            "Logistique et gestion des stocks en temps réel",
            "Concurrence des pure players e-commerce"
        ],
        "source": "Gartner Retail Technology Report, McKinsey Consumer"
    },
    "education": {
        "label": "Éducation & Formation",
        "global_avg": 45.0,
        "europe_avg": 55.0,
        "africa_avg": 30.0,
        "maghreb_avg": 32.0,
        "leaders_threshold": 65.0,
        "laggards_threshold": 28.0,
        "business_avg": 44.0,
        "process_avg": 46.0,
        "si_avg": 45.0,
        "yoy_growth": 7.2,
        "key_challenges": [
            "Adoption des plateformes LMS et e-learning",
            "Compétences digitales des enseignants",
            "Personnalisation pédagogique par l'IA",
            "Infrastructure numérique et connectivité"
        ],
        "source": "WEF Future of Jobs 2024, UNESCO ICT in Education"
    },
    "telecom": {
        "label": "Télécommunications",
        "global_avg": 72.0,
        "europe_avg": 78.0,
        "africa_avg": 60.0,
        "maghreb_avg": 62.0,
        "leaders_threshold": 88.0,
        "laggards_threshold": 56.0,
        "business_avg": 74.0,
        "process_avg": 70.0,
        "si_avg": 72.0,
        "yoy_growth": 3.5,
        "key_challenges": [
            "Déploiement 5G et nouvelles architectures réseau",
            "Monétisation des données et services à valeur ajoutée",
            "Virtualisation du réseau (SDN/NFV)",
            "Cybersécurité et résilience des infrastructures critiques"
        ],
        "source": "Gartner Telecom Tech Report 2024, Ericsson Mobility Report"
    },
    "energie": {
        "label": "Énergie & Utilities",
        "global_avg": 50.0,
        "europe_avg": 59.0,
        "africa_avg": 33.0,
        "maghreb_avg": 37.0,
        "leaders_threshold": 70.0,
        "laggards_threshold": 32.0,
        "business_avg": 49.0,
        "process_avg": 52.0,
        "si_avg": 49.0,
        "yoy_growth": 5.9,
        "key_challenges": [
            "Smart grid et compteurs intelligents",
            "Transition énergétique et énergies renouvelables",
            "Optimisation de la consommation par l'IoT et l'IA",
            "Cybersécurité des infrastructures critiques"
        ],
        "source": "IEA Digital Energy Report 2024, Accenture Energy Vision"
    },
    "assurance": {
        "label": "Assurance",
        "global_avg": 62.0,
        "europe_avg": 70.0,
        "africa_avg": 44.0,
        "maghreb_avg": 46.0,
        "leaders_threshold": 80.0,
        "laggards_threshold": 45.0,
        "business_avg": 64.0,
        "process_avg": 60.0,
        "si_avg": 62.0,
        "yoy_growth": 4.8,
        "key_challenges": [
            "Transformation vers l'InsurTech et produits digitaux",
            "Underwriting automatisé par l'IA",
            "Expérience client omnicanale",
            "Conformité Solvabilité II et RGPD"
        ],
        "source": "McKinsey Insurance Report 2024, Gartner InsurTech"
    },
    "logistique": {
        "label": "Logistique & Transport",
        "global_avg": 53.0,
        "europe_avg": 61.0,
        "africa_avg": 36.0,
        "maghreb_avg": 38.0,
        "leaders_threshold": 73.0,
        "laggards_threshold": 36.0,
        "business_avg": 52.0,
        "process_avg": 56.0,
        "si_avg": 51.0,
        "yoy_growth": 5.7,
        "key_challenges": [
            "Traçabilité en temps réel et blockchain",
            "Optimisation des routes par l'IA",
            "Entrepôts automatisés et robotique",
            "Transition vers la logistique verte"
        ],
        "source": "McKinsey Supply Chain Report 2024, Gartner Logistics"
    },
    "agriculture": {
        "label": "Agriculture & Agroalimentaire",
        "global_avg": 38.0,
        "europe_avg": 46.0,
        "africa_avg": 24.0,
        "maghreb_avg": 27.0,
        "leaders_threshold": 58.0,
        "laggards_threshold": 22.0,
        "business_avg": 37.0,
        "process_avg": 39.0,
        "si_avg": 38.0,
        "yoy_growth": 6.5,
        "key_challenges": [
            "Agriculture de précision et IoT agricole",
            "Traçabilité alimentaire et blockchain",
            "Gestion de l'eau et ressources naturelles",
            "Plateformes de vente directe et e-commerce"
        ],
        "source": "FAO Digital Agriculture Report, WEF Agritech"
    },
    "tourisme": {
        "label": "Tourisme & Hôtellerie",
        "global_avg": 56.0,
        "europe_avg": 64.0,
        "africa_avg": 39.0,
        "maghreb_avg": 43.0,
        "leaders_threshold": 76.0,
        "laggards_threshold": 38.0,
        "business_avg": 60.0,
        "process_avg": 52.0,
        "si_avg": 56.0,
        "yoy_growth": 6.8,
        "key_challenges": [
            "Expérience digitale client (réservation, check-in)",
            "Revenue management et pricing dynamique",
            "Personnalisation par la data et l'IA",
            "Marketing digital et réseaux sociaux"
        ],
        "source": "UNWTO Digital Tourism Report 2024"
    },
    "btp": {
        "label": "BTP & Construction",
        "global_avg": 41.0,
        "europe_avg": 50.0,
        "africa_avg": 27.0,
        "maghreb_avg": 30.0,
        "leaders_threshold": 62.0,
        "laggards_threshold": 25.0,
        "business_avg": 40.0,
        "process_avg": 43.0,
        "si_avg": 40.0,
        "yoy_growth": 5.2,
        "key_challenges": [
            "Adoption du BIM (Building Information Modeling)",
            "Drones et relevés topographiques digitaux",
            "Gestion de projet digitale (ERP chantier)",
            "Sécurité et suivi des travailleurs en temps réel"
        ],
        "source": "McKinsey Construction Report, WEF Built Environment"
    },
}

# Countries to region mapping
COUNTRY_REGION_MAP: dict[str, str] = {
    "france": "europe_avg",
    "belgique": "europe_avg",
    "suisse": "europe_avg",
    "luxembourg": "europe_avg",
    "allemagne": "europe_avg",
    "espagne": "europe_avg",
    "italie": "europe_avg",
    "maroc": "maghreb_avg",
    "tunisie": "maghreb_avg",
    "algérie": "maghreb_avg",
    "algerie": "maghreb_avg",
    "libye": "maghreb_avg",
    "mauritanie": "maghreb_avg",
    "sénégal": "uemoa_avg",
    "senegal": "uemoa_avg",
    "côte d'ivoire": "uemoa_avg",
    "cote d'ivoire": "uemoa_avg",
    "cote_ivoire": "uemoa_avg",
    "ivory coast": "uemoa_avg",
    "mali": "uemoa_avg",
    "burkina faso": "uemoa_avg",
    "niger": "uemoa_avg",
    "bénin": "uemoa_avg",
    "benin": "uemoa_avg",
    "togo": "uemoa_avg",
    "guinée-bissau": "uemoa_avg",
    "cameroun": "africa_avg",
    "kenya": "africa_avg",
    "nigeria": "africa_avg",
    "ghana": "africa_avg",
    "afrique du sud": "africa_avg",
}

# Sector name normalization
SECTOR_ALIASES: dict[str, str] = {
    "banking": "banque",
    "bank": "banque",
    "fintech": "finance",
    "financial services": "finance",
    "healthcare": "sante",
    "santé": "sante",
    "health": "sante",
    "manufacturing": "industrie",
    "industrie 4.0": "industrie",
    "e-commerce": "retail",
    "commerce": "retail",
    "distribution": "retail",
    "energy": "energie",
    "utilities": "energie",
    "insurance": "assurance",
    "transport": "logistique",
    "supply chain": "logistique",
    "construction": "btp",
    "immobilier": "btp",
    "hospitality": "tourisme",
    "hotel": "tourisme",
    "hôtellerie": "tourisme",
}


def get_sector_key(sector: str) -> str:
    """Normalize sector name to a known key."""
    normalized = sector.lower().strip()
    if normalized in SECTOR_BENCHMARKS:
        return normalized
    if normalized in SECTOR_ALIASES:
        return SECTOR_ALIASES[normalized]
    # Fuzzy: find first key that appears in the sector string
    for key in SECTOR_BENCHMARKS:
        if key in normalized or normalized in key:
            return key
    return None


def get_benchmark(sector: str, country: str) -> dict | None:
    """Return benchmark data for a sector, with region-specific average."""
    key = get_sector_key(sector)
    if key is None:
        return None
    bench = SECTOR_BENCHMARKS[key].copy()

    # Select the right regional average
    country_lower = country.lower().strip()
    region_key = COUNTRY_REGION_MAP.get(country_lower, "global_avg")
    bench["regional_avg"] = bench.get(region_key, bench["global_avg"])
    bench["region_label"] = {
        "europe_avg": "Europe",
        "africa_avg": "Afrique",
        "maghreb_avg": "Maghreb",
        "uemoa_avg": "UEMOA (Afrique de l'Ouest)",
        "global_avg": "Mondial"
    }.get(region_key, "Mondial")

    return bench


def format_benchmark_for_prompt(sector: str, country: str, company_score: float = None) -> str:
    """Format benchmark data for injection into AI prompts."""
    bench = get_benchmark(sector, country)
    if not bench:
        return ""

    lines = [
        f"\nBENCHMARK SECTORIEL — {bench['label']} ({bench['region_label']}) :",
        f"- Moyenne régionale : {bench['regional_avg']:.0f}/100",
        f"- Moyenne mondiale : {bench['global_avg']:.0f}/100",
        f"- Entreprises leaders (top 25%) : {bench['leaders_threshold']:.0f}/100",
        f"- Entreprises en retard (bottom 25%) : {bench['laggards_threshold']:.0f}/100",
        f"- Croissance annuelle moyenne du secteur : +{bench['yoy_growth']:.1f}%/an",
        f"- Score axe Métier moyen : {bench['business_avg']:.0f}/100",
        f"- Score axe Processus moyen : {bench['process_avg']:.0f}/100",
        f"- Score axe SI moyen : {bench['si_avg']:.0f}/100",
        f"- Défis clés du secteur : {', '.join(bench['key_challenges'])}",
        f"- Source : {bench['source']}",
    ]

    if company_score is not None:
        gap = company_score - bench["regional_avg"]
        position = "au-dessus" if gap >= 0 else "en dessous"
        lines.append(f"\n→ L'entreprise est à {abs(gap):.1f} points {position} de la moyenne régionale.")
        if company_score >= bench["leaders_threshold"]:
            lines.append("→ Positionnement : LEADER (top 25% du secteur)")
        elif company_score >= bench["regional_avg"]:
            lines.append("→ Positionnement : AU-DESSUS DE LA MOYENNE sectorielle")
        elif company_score >= bench["laggards_threshold"]:
            lines.append("→ Positionnement : EN DESSOUS DE LA MOYENNE sectorielle")
        else:
            lines.append("→ Positionnement : EN RETARD (bottom 25% du secteur)")

    return "\n".join(lines)
