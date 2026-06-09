"""
Benchmarking Engine
Positions the company against national and international sector benchmarks.
Primary path: LLM-grounded analysis via Mistral (Gartner, McKinsey, WEF, OECD, BCG).
Fallback path: deterministic rule-based benchmark when the LLM is unavailable.
"""
import asyncio
import json
import os
from services.llm_client import call_llm as call_groq, extract_json, TaskType
from knowledge.sub_axis_data import get_sub_axis_data, format_sub_axis_for_prompt
from knowledge.sub_axis_extra import get_sub_axis_extra_fuzzy
from knowledge.country_context import get_country_context


# ── Verifiable source URL mapping ─────────────────────────────────────────────

_ORG_URLS: dict[str, str] = {
    "mckinsey":     "https://www.mckinsey.com",
    "gartner":      "https://www.gartner.com",
    "wef":          "https://www.weforum.org",
    "bcg":          "https://www.bcg.com",
    "idc":          "https://www.idc.com",
    "oecd":         "https://www.oecd.org",
    "ocde":         "https://www.oecd.org",
    "iea":          "https://www.iea.org",
    "irena":        "https://www.irena.org",
    "unesco":       "https://www.unesco.org",
    "bce":          "https://www.ecb.europa.eu",
    "bceao":        "https://www.bceao.int",
    "bloombergnef": "https://about.bnef.com",
    "cbre":         "https://www.cbre.com",
    "cerema":       "https://www.cerema.fr",
    "cncf":         "https://www.cncf.io",
    "ibm":          "https://www.ibm.com",
    "salesforce":   "https://www.salesforce.com",
    "siemens":      "https://www.siemens.com",
    "eiopa":        "https://www.eiopa.europa.eu",
    "edSurge":      "https://www.edsurge.com",
    "nejm":         "https://www.nejm.org",
    "ifr":          "https://ifr.org",
    "uitp":         "https://www.uitp.org",
    "ans":          "https://esante.gouv.fr",
}


def _get_source_url(source: str) -> str:
    """Derive a verifiable organisation URL from a source citation string."""
    if not source:
        return ""
    s = source.lower()
    for key, url in _ORG_URLS.items():
        if key in s:
            return url
    return ""


# ── Sector name aliases (French & English → canonical key) ───────────────────

_SECTOR_ALIAS: dict[str, str] = {
    # French → English key
    "banque": "banking", "bancaire": "banking", "banques": "banking",
    "finance": "banking", "financier": "banking", "financière": "banking",
    "assurance": "insurance", "assurances": "insurance", "assureur": "insurance",
    "industrie": "industry", "industriel": "industry", "industrielle": "industry",
    "manufacture": "industry", "fabrication": "industry", "production": "industry",
    "commerce": "retail", "distribution": "retail", "vente": "retail",
    "détail": "retail", "detail": "retail",
    "santé": "healthcare", "sante": "healthcare", "médical": "healthcare",
    "medical": "healthcare", "hôpital": "healthcare", "hopital": "healthcare",
    "pharmacie": "healthcare", "clinique": "healthcare",
    "technologie": "tech", "technologies": "tech", "informatique": "tech",
    "numérique": "tech", "numerique": "tech", "logiciel": "tech",
    "software": "tech", "it": "tech", "ict": "tech", "digital": "tech",
    "éducation": "education", "education": "education", "enseignement": "education",
    "formation": "education", "université": "education", "universite": "education",
    "transport": "transport", "logistique": "transport", "mobilité": "transport",
    "mobilite": "transport", "fret": "transport", "livraison": "transport",
    "énergie": "energy", "energie": "energy", "énergétique": "energy",
    "electricite": "energy", "électricité": "energy", "pétrole": "energy",
    "petrole": "energy", "gaz": "energy",
    "construction": "construction", "btp": "construction",
    "immobilier": "construction", "bâtiment": "construction", "batiment": "construction",
    "travaux": "construction",
    # English pass-through
    "banking": "banking", "insurance": "insurance", "industry": "industry",
    "retail": "retail", "healthcare": "healthcare", "tech": "tech",
    "education": "education", "energy": "energy",
    # Telecom / media (map to tech as closest)
    "telecom": "tech", "télécommunication": "tech", "telecommunication": "tech",
    "media": "tech", "médias": "tech",
    # Agriculture / agroalimentaire
    "agriculture": "industry", "agroalimentaire": "industry", "agro": "industry",
    # Public sector
    "public": "education", "administration": "education", "gouvernement": "education",
    # Beauty / cosmetics → retail
    "beauty": "retail", "cosmetic": "retail", "cosmétique": "retail", "beauté": "retail",
    "mode": "retail", "fashion": "retail", "luxe": "retail", "luxury": "retail",
    # Short forms
    "edu": "education", "educ": "education",
    "health": "healthcare", "medical": "healthcare",
    "trans": "transport", "log": "transport",
    "bank": "banking", "fin": "banking",
    "ins": "insurance",
    "manu": "industry", "ind": "industry",
    "eng": "energy", "ener": "energy",
    "const": "construction", "immo": "construction",
}


def _resolve_sector(sector: str) -> str:
    """Map any sector string (French or English) to a canonical _SECTOR_DATA key."""
    if not sector:
        return "default"
    normalized = sector.lower().strip()
    # Try whole string first
    if normalized in _SECTOR_ALIAS:
        return _SECTOR_ALIAS[normalized]
    # Try each word
    for word in normalized.replace("-", " ").replace("_", " ").split():
        if word in _SECTOR_ALIAS:
            return _SECTOR_ALIAS[word]
    # Try prefix matching (e.g. "banqu" → "banque")
    for alias, key in _SECTOR_ALIAS.items():
        if normalized.startswith(alias[:4]) and len(alias) >= 4:
            return key
    return "default"


# ── Sector reference data (Gartner DTI / McKinsey Digital Index 2023-2024) ────

_SECTOR_DATA = {
    "banking":     {"nat": 57, "intl": 68, "top": 83, "source": "McKinsey Global Banking Report 2024"},
    "insurance":   {"nat": 50, "intl": 62, "top": 78, "source": "Gartner Insurance Digital Maturity 2024"},
    "industry":    {"nat": 44, "intl": 57, "top": 74, "source": "WEF Advanced Manufacturing 2024"},
    "retail":      {"nat": 53, "intl": 66, "top": 81, "source": "McKinsey Retail Digital Index 2024"},
    "healthcare":  {"nat": 42, "intl": 55, "top": 72, "source": "Gartner Healthcare IT Maturity 2024"},
    "tech":        {"nat": 66, "intl": 76, "top": 89, "source": "IDC Digital Transformation Survey 2024"},
    "education":   {"nat": 38, "intl": 50, "top": 68, "source": "OECD Education Digital Readiness 2024"},
    "transport":   {"nat": 47, "intl": 60, "top": 76, "source": "WEF Mobility Futures Report 2024"},
    "energy":      {"nat": 49, "intl": 63, "top": 79, "source": "IEA Digital Energy Transformation 2024"},
    "construction":{"nat": 35, "intl": 48, "top": 66, "source": "McKinsey Construction Productivity 2024"},
}
_DEFAULT_DATA = {"nat": 50, "intl": 63, "top": 78, "source": "Gartner Digital Business Survey 2024"}

# ── Country → Geographic region mapping ───────────────────────────────────────

_COUNTRY_TO_REGION: dict[str, str] = {
    # UEMOA
    "senegal": "UEMOA", "sénégal": "UEMOA",
    "mali": "UEMOA", "burkina faso": "UEMOA", "burkina": "UEMOA",
    "côte d'ivoire": "UEMOA", "cote d'ivoire": "UEMOA", "ivory coast": "UEMOA",
    "guinée-bissau": "UEMOA", "guinee-bissau": "UEMOA",
    "bénin": "UEMOA", "benin": "UEMOA", "togo": "UEMOA", "niger": "UEMOA",
    # MENA
    "egypt": "MENA", "égypte": "MENA", "egypte": "MENA",
    "morocco": "MENA", "maroc": "MENA",
    "tunisia": "MENA", "tunisie": "MENA",
    "algeria": "MENA", "algérie": "MENA", "algerie": "MENA",
    "lebanon": "MENA", "liban": "MENA",
    "jordan": "MENA", "jordanie": "MENA",
    "saudi arabia": "MENA", "arabie saoudite": "MENA",
    "uae": "MENA", "émirats arabes unis": "MENA", "emirats arabes unis": "MENA",
    "qatar": "MENA", "kuwait": "MENA", "bahrain": "MENA", "oman": "MENA",
    "iraq": "MENA", "irak": "MENA", "libya": "MENA", "libye": "MENA",
    # Sub-Saharan Africa (non-UEMOA)
    "kenya": "SSA", "nigeria": "SSA", "nigéria": "SSA",
    "ghana": "SSA", "ethiopia": "SSA", "éthiopie": "SSA",
    "tanzania": "SSA", "tanzanie": "SSA", "rwanda": "SSA",
    "south africa": "SSA", "afrique du sud": "SSA",
    "uganda": "SSA", "ouganda": "SSA",
    "cameroon": "SSA", "cameroun": "SSA",
    # Europe
    "france": "Europe", "germany": "Europe", "allemagne": "Europe",
    "spain": "Europe", "espagne": "Europe",
    "italy": "Europe", "italie": "Europe",
    "united kingdom": "Europe", "royaume-uni": "Europe", "uk": "Europe",
    "netherlands": "Europe", "pays-bas": "Europe",
    "belgium": "Europe", "belgique": "Europe",
    "portugal": "Europe", "switzerland": "Europe", "suisse": "Europe",
    "sweden": "Europe", "suède": "Europe", "suede": "Europe",
    "norway": "Europe", "norvège": "Europe",
    "denmark": "Europe", "danemark": "Europe",
    "poland": "Europe", "pologne": "Europe",
    "austria": "Europe", "autriche": "Europe",
    # North America
    "usa": "North America", "united states": "North America",
    "états-unis": "North America", "etats-unis": "North America",
    "canada": "North America",
    # APAC
    "china": "APAC", "chine": "APAC",
    "japan": "APAC", "japon": "APAC",
    "india": "APAC", "inde": "APAC",
    "singapore": "APAC", "singapour": "APAC",
    "australia": "APAC", "australie": "APAC",
    "south korea": "APAC", "corée du sud": "APAC", "coree du sud": "APAC",
    "indonesia": "APAC", "indonésie": "APAC",
    "malaysia": "APAC", "malaisie": "APAC",
    "thailand": "APAC", "thaïlande": "APAC",
    "vietnam": "APAC", "viêt nam": "APAC", "philippines": "APAC",
    # LATAM
    "brazil": "LATAM", "brésil": "LATAM", "bresil": "LATAM",
    "mexico": "LATAM", "mexique": "LATAM",
    "argentina": "LATAM", "argentine": "LATAM",
    "colombia": "LATAM", "colombie": "LATAM",
    "chile": "LATAM", "chili": "LATAM",
    "peru": "LATAM", "pérou": "LATAM", "perou": "LATAM",
}


def _resolve_region(country: str) -> str:
    """Map a country name to its geographic region for benchmarking context."""
    if not country:
        return "Afrique"
    c = country.lower().strip()
    if c in _COUNTRY_TO_REGION:
        return _COUNTRY_TO_REGION[c]
    for key, region in _COUNTRY_TO_REGION.items():
        if key in c or c in key:
            return region
    return "International"


_SECTOR_TRENDS = {
    "banking": [
        {"title": "IA Générative dans les services financiers",
         "description": "Les banques intègrent ChatGPT et Claude pour l'analyse de risque, le KYC automatisé et le conseil client. 68% des grandes banques mondiales pilotent des cas d'usage IA générative.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "68% des grandes banques", "source": "McKinsey 2024"},
        {"title": "Open Banking & API Economy",
         "description": "La directive DSP2 et son évolution DSP3 accélèrent l'ouverture des systèmes bancaires. Les API banking permettent de nouveaux modèles de revenus en partenariat avec les fintechs.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "55% des banques européennes", "source": "Gartner 2024"},
        {"title": "Instant Payment généralisé",
         "description": "Le virement instantané devient la norme en Europe (règlement UE 2024). Les banques doivent adapter leurs systèmes de paiement en temps réel 24/7.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "72% des banques UE", "source": "BCE 2024"},
        {"title": "Cloud hybride bancaire",
         "description": "Migration progressive vers le cloud souverain pour les workloads critiques. Réduction des coûts d'infrastructure et flexibilité accrue pour les nouvelles offres.",
         "impact_level": "MOYEN", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "42% des banques", "source": "IDC 2024"},
    ],
    "insurance": [
        {"title": "InsurTech & tarification dynamique",
         "description": "L'utilisation de l'IA et de la télématique permet une tarification en temps réel basée sur les comportements réels des assurés. Les assureurs leaders réduisent les fraudes de 30%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "45% des assureurs", "source": "Gartner 2024"},
        {"title": "Automatisation des sinistres par IA",
         "description": "Les processus de déclaration et d'indemnisation sont automatisés grâce à l'IA, réduisant les délais de traitement de 60% et améliorant la satisfaction client.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "38% des assureurs", "source": "McKinsey 2024"},
        {"title": "Assurance paramétrique & IoT",
         "description": "Les capteurs IoT et les contrats paramétriques permettent des indemnisations automatiques déclenchées par des événements mesurables (météo, capteurs industriels).",
         "impact_level": "MOYEN", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "22% des assureurs", "source": "BCG 2024"},
        {"title": "Cloud & modernisation des systèmes legacy",
         "description": "La migration des SI core insurance vers le cloud réduit les coûts opérationnels de 20-40% et accélère la mise sur marché de nouveaux produits.",
         "impact_level": "ELEVE", "horizon": "Long terme (3-5 ans)", "adoption_rate": "31% des assureurs", "source": "IDC 2024"},
        {"title": "Conformité IFRS 17 & réglementation Solvabilité II",
         "description": "La mise en conformité avec IFRS 17 nécessite une refonte des systèmes de reporting et d'évaluation des contrats d'assurance, avec des investissements SI significatifs.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "100% des assureurs UE", "source": "EIOPA 2024"},
    ],
    "industry": [
        {"title": "Industrie 4.0 & jumeaux numériques",
         "description": "Le jumeau numérique des usines permet de simuler, optimiser et prédire les défaillances en temps réel. Réduction des arrêts non planifiés de 25-40%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "34% des industriels", "source": "WEF 2024"},
        {"title": "Maintenance prédictive par IA",
         "description": "L'IA appliquée aux données capteurs permet d'anticiper les pannes avant qu'elles surviennent, réduisant les coûts de maintenance de 15-25%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "41% des usines connectées", "source": "McKinsey 2024"},
        {"title": "Robotique collaborative (Cobots)",
         "description": "Les robots collaboratifs travaillant aux côtés des opérateurs humains augmentent la productivité de 20-30% tout en réduisant les TMS et accidents.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "28% des sites industriels", "source": "IFR 2024"},
        {"title": "Supply Chain digitale & résilience",
         "description": "La digitalisation de la chaîne d'approvisionnement avec visibilité end-to-end permet de réduire les ruptures de stock de 35% et d'optimiser les stocks de 20%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "47% des industriels", "source": "Gartner 2024"},
        {"title": "Transition énergétique & usine verte",
         "description": "La décarbonation industrielle est une priorité stratégique. Les usines leaders réduisent leur empreinte carbone de 30-50% via l'efficience énergétique et les énergies renouvelables.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "39% des industriels", "source": "IEA 2024"},
    ],
    "retail": [
        {"title": "Commerce unifié & omnicanal seamless",
         "description": "L'intégration physique-digital (BOPIS, ROPIS, clienteling) devient le standard. Les retailers omnicanaux génèrent 3x plus de revenus que les pure players.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "67% des enseignes", "source": "Salesforce 2024"},
        {"title": "Personnalisation IA & recommandation en temps réel",
         "description": "Les moteurs de recommandation IA augmentent le panier moyen de 15-25%. La personnalisation temps réel devient le différenciateur majeur face à Amazon.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "58% des e-commerçants", "source": "McKinsey 2024"},
        {"title": "Quick Commerce & livraison ultra-rapide",
         "description": "La livraison en moins de 2h devient la norme dans les grandes villes. Les dark stores et micro-fulfilment centers restructurent la logistique urbaine.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "43% des retailers urbains", "source": "BCG 2024"},
        {"title": "Social Commerce & live shopping",
         "description": "Les ventes via TikTok, Instagram et les lives shopping représentent 20% du e-commerce en Asie et progressent de 40% en Europe.",
         "impact_level": "MOYEN", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "31% des marques", "source": "Gartner 2024"},
        {"title": "Automatisation entrepôts & logistique robotisée",
         "description": "Les robots de picking et les systèmes WMS intelligents réduisent les coûts logistiques de 25% et la préparation de commande de 60%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "29% des centres logistiques", "source": "IDC 2024"},
    ],
    "healthcare": [
        {"title": "Santé numérique & télémédecine généralisée",
         "description": "La télémédecine est passée de 1% à 15% des consultations post-Covid. Les plateformes de santé digitale réduisent les délais d'accès aux soins de 40%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "72% des établissements", "source": "OCDE 2024"},
        {"title": "IA diagnostique & aide à la décision clinique",
         "description": "Les algorithmes d'IA atteignent des taux de précision diagnostique supérieurs aux radiologues pour certaines pathologies (cancer du poumon : 94% vs 86%).",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "38% des CHU", "source": "Gartner 2024"},
        {"title": "Dossier Patient Informatisé (DPI) interopérable",
         "description": "L'interopérabilité des systèmes de santé via FHIR et les Espaces Numériques de Santé (ENS) permet la continuité des soins et réduit les erreurs médicales.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "61% des établissements", "source": "ANSM 2024"},
        {"title": "Cybersécurité & protection des données de santé",
         "description": "Les attaques ransomware contre les hôpitaux ont triplé en 3 ans. La certification HDS et la conformité RGPD santé sont des impératifs réglementaires.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "55% des établissements", "source": "ANS 2024"},
        {"title": "Médecine de précision & génomique",
         "description": "Le séquençage génomique à coût décroissant et les biomarqueurs IA permettent des traitements personnalisés, réduisant les effets indésirables de 30%.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "18% des centres spécialisés", "source": "WEF 2024"},
    ],
    "tech": [
        {"title": "IA générative & LLM en production",
         "description": "L'intégration de LLMs dans les produits SaaS devient le standard concurrentiel. Les entreprises tech leaders déploient des copilotes IA dans 80% de leurs produits.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "76% des éditeurs SaaS", "source": "IDC 2024"},
        {"title": "Platform Engineering & Developer Experience",
         "description": "Les Internal Developer Platforms (IDP) standardisent les workflows DevOps et réduisent le time-to-market de 40%. L'IDP devient le facteur d'attraction des talents.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "58% des DSI tech", "source": "Gartner 2024"},
        {"title": "FinOps & optimisation cloud",
         "description": "La maîtrise des coûts cloud devient critique avec la hausse des prix AWS/Azure/GCP. Les pratiques FinOps réduisent les dépenses cloud de 20-35%.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "49% des entreprises cloud-native", "source": "CNCF 2024"},
        {"title": "Architecture composable & API-first",
         "description": "La MACH architecture (Microservices, API-first, Cloud-native, Headless) permet une agilité maximale pour assembler des services best-of-breed.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "44% des éditeurs", "source": "Gartner 2024"},
        {"title": "Quantum Computing & cryptographie post-quantique",
         "description": "La préparation à l'ère post-quantique exige dès maintenant une migration vers des algorithmes cryptographiques résistants aux ordinateurs quantiques.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "12% des entreprises tech", "source": "IBM Research 2024"},
    ],
    "education": [
        {"title": "IA générative & apprentissage personnalisé",
         "description": "Les tuteurs IA (ChatGPT, Khan Academy AI) adaptent le contenu pédagogique au rythme individuel de chaque apprenant, améliorant les résultats de 30-40%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "52% des établissements", "source": "OCDE 2024"},
        {"title": "EdTech & plateformes LMS nouvelle génération",
         "description": "Les LMS enrichis (Moodle 4.x, Canvas, Brightspace) intègrent analytics, IA et micro-certifications. Le marché EdTech croît de 16% par an.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "68% des universités", "source": "UNESCO 2024"},
        {"title": "Micro-certifications & formation continue",
         "description": "Les badges numériques et nano-diplômes répondent aux besoins de requalification rapide. 65% des employés auront besoin d'une reconversion d'ici 2027.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "44% des établissements", "source": "WEF 2024"},
        {"title": "Réalité virtuelle & immersive learning",
         "description": "Les simulations VR réduisent le temps d'apprentissage de 40% dans les domaines techniques (chirurgie, maintenance industrielle, formation professionnelle).",
         "impact_level": "MOYEN", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "19% des établissements", "source": "Gartner 2024"},
        {"title": "Accessibilité numérique & inclusion",
         "description": "Les technologies adaptatives (sous-titrage IA, synthèse vocale, interfaces inclusives) permettent à 15% de population en situation de handicap d'accéder à l'éducation digitale.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "37% des plateformes éducatives", "source": "UNESCO 2024"},
    ],
    "transport": [
        {"title": "Mobilité autonome & connectée",
         "description": "Les véhicules connectés (C-V2X) et semi-autonomes transforment la logistique urbaine. Les flottes autonomes réduisent les coûts de transport de 30-45%.",
         "impact_level": "ELEVE", "horizon": "Long terme (3-5 ans)", "adoption_rate": "18% des flottes commerciales", "source": "WEF 2024"},
        {"title": "Optimisation IA des tournées & TMS intelligent",
         "description": "Les TMS alimentés par IA optimisent les routes en temps réel, réduisant les kilomètres parcourus de 15-20% et les émissions CO2 de 25%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "53% des transporteurs", "source": "Gartner 2024"},
        {"title": "Plateforme multimodale & MaaS",
         "description": "La Mobility as a Service (MaaS) intègre tous les modes de transport dans une expérience digitale unifiée. Les apps MaaS captent 35% des déplacements urbains.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "41% des opérateurs urbains", "source": "UITP 2024"},
        {"title": "Électrification des flottes & infrastructure de recharge",
         "description": "La transition vers des flottes 100% électriques est accélérée par les réglementations européennes (fin des moteurs thermiques en 2035) et la baisse du TCO.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "29% des flottes d'entreprise", "source": "IEA 2024"},
        {"title": "Traçabilité temps réel & IoT logistique",
         "description": "Les capteurs IoT et la blockchain permettent une visibilité end-to-end de la supply chain, réduisant les pertes et litiges de 40%.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "47% des opérateurs logistiques", "source": "McKinsey 2024"},
    ],
    "energy": [
        {"title": "Smart Grid & gestion intelligente des réseaux",
         "description": "Les réseaux électriques intelligents intègrent l'IA pour équilibrer production et consommation en temps réel, essentiels pour l'intégration des ENR.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "44% des opérateurs réseaux", "source": "IEA 2024"},
        {"title": "Transition vers les énergies renouvelables",
         "description": "La parité réseau du solaire et de l'éolien est atteinte dans 90% des marchés mondiaux. Les ENR représenteront 50% du mix électrique mondial en 2030.",
         "impact_level": "ELEVE", "horizon": "Long terme (3-5 ans)", "adoption_rate": "68% des énergéticiens", "source": "IRENA 2024"},
        {"title": "Jumeaux numériques pour actifs énergétiques",
         "description": "Les jumeaux numériques des centrales et réseaux permettent d'optimiser les performances et anticiper les défaillances, réduisant les OPEX de 20%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "31% des opérateurs", "source": "Siemens Energy 2024"},
        {"title": "Stockage d'énergie & batteries",
         "description": "La chute des coûts des batteries (−89% en 10 ans) rend le stockage stationnaire économiquement viable, révolutionnant la gestion de l'intermittence.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "37% des producteurs ENR", "source": "BloombergNEF 2024"},
        {"title": "Hydrogène vert & décarbonation industrielle",
         "description": "L'hydrogène vert devient la solution de décarbonation des industries lourdes. Les investissements mondiaux atteignent 500 Mds$ d'ici 2030.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "14% des industriels", "source": "IEA 2024"},
    ],
    "construction": [
        {"title": "BIM (Building Information Modeling) & construction digitale",
         "description": "Le BIM 5D/6D devient obligatoire dans les marchés publics européens. Il réduit les délais de construction de 20% et les coûts de 15%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "58% des grandes entreprises BTP", "source": "McKinsey 2024"},
        {"title": "Construction modulaire & impression 3D",
         "description": "La préfabrication hors-site et l'impression 3D de bâtiments réduisent les délais de 50% et les déchets de chantier de 60%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "22% des constructeurs", "source": "WEF 2024"},
        {"title": "Drones & robotique de chantier",
         "description": "Les drones pour la surveillance et le relevé topographique, et les robots maçons augmentent la productivité de 30% et réduisent les accidents du travail de 40%.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "35% des chantiers", "source": "Gartner 2024"},
        {"title": "PropTech & gestion immobilière intelligente",
         "description": "Les plateformes PropTech de gestion des actifs immobiliers et les bâtiments intelligents (Smart Building) réduisent les charges d'exploitation de 25-30%.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "41% des gestionnaires immobiliers", "source": "CBRE 2024"},
        {"title": "Construction durable & économie circulaire",
         "description": "La RE2020 et les certifications HQE/BREEAM imposent une conception bas-carbone. Le réemploi et la déconstruction sélective deviennent des avantages compétitifs.",
         "impact_level": "ELEVE", "horizon": "Long terme (3-5 ans)", "adoption_rate": "48% des promoteurs", "source": "Cerema 2024"},
    ],
    "default": [
        {"title": "IA Générative et automatisation cognitive",
         "description": "L'adoption de l'IA générative transforme les processus métier, de la relation client à l'analyse décisionnelle. Les entreprises leaders réduisent leurs coûts opérationnels de 25-35%.",
         "impact_level": "ELEVE", "horizon": "Court terme (0-12 mois)", "adoption_rate": "52% des entreprises", "source": "McKinsey 2024"},
        {"title": "Cloud & Architecture microservices",
         "description": "La migration vers le cloud hybride et les architectures microservices devient un impératif compétitif. Elle permet l'agilité nécessaire pour lancer de nouveaux produits en semaines plutôt qu'en mois.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "61% des entreprises", "source": "Gartner 2024"},
        {"title": "Cybersécurité Zero Trust",
         "description": "La généralisation du télétravail et la multiplication des cyberattaques poussent les entreprises à adopter le modèle Zero Trust. Les budgets cybersécurité croissent de 15% par an.",
         "impact_level": "ELEVE", "horizon": "Moyen terme (1-3 ans)", "adoption_rate": "44% des entreprises", "source": "IDC 2024"},
        {"title": "Expérience client omnicanale",
         "description": "Les clients exigent une expérience fluide et personnalisée sur tous les canaux. Les entreprises leaders investissent dans le CRM unifié et l'analyse comportementale temps réel.",
         "impact_level": "MOYEN", "horizon": "Court terme (0-12 mois)", "adoption_rate": "67% des entreprises", "source": "Salesforce 2024"},
        {"title": "Data Mesh & gouvernance des données",
         "description": "La gouvernance décentralisée des données avec une architecture Data Mesh permet une exploitation plus agile des actifs données tout en garantissant conformité et qualité.",
         "impact_level": "MOYEN", "horizon": "Long terme (3-5 ans)", "adoption_rate": "28% des entreprises", "source": "Gartner 2024"},
    ]
}

_SECTOR_LEADERS = {
    "banking": [
        {"company": "DBS Bank", "country": "Singapour", "estimated_score": 91, "key_practice": "Banque 100% cloud-native avec IA embarquée dans tous les processus", "differentiator": "Digital bank of the year 5 années consécutives (Euromoney)", "source": "Gartner 2024"},
        {"company": "ING Group", "country": "Pays-Bas", "estimated_score": 86, "key_practice": "Plateforme de banking-as-a-service et API ouverte à 200+ fintechs", "differentiator": "Architecture agile Spotify transformée en modèle bancaire", "source": "McKinsey 2024"},
        {"company": "Capitec Bank", "country": "Afrique du Sud", "estimated_score": 83, "key_practice": "Digitalisation complète avec 8M+ clients actifs sur mobile", "differentiator": "Leader en inclusion financière digitale sur marchés émergents", "source": "BCG 2024"},
    ],
    "insurance": [
        {"company": "AXA", "country": "France", "estimated_score": 84, "key_practice": "Plateforme IA pour la détection de fraude et tarification comportementale", "differentiator": "Leader en InsurTech avec 500M€ investis dans la transformation digitale", "source": "Gartner 2024"},
        {"company": "Lemonade", "country": "USA", "estimated_score": 88, "key_practice": "Assurance 100% IA — souscription et indemnisation en moins de 3 secondes", "differentiator": "Modèle InsurTech natif avec NPS de 70 vs 15 pour les assureurs traditionnels", "source": "BCG 2024"},
        {"company": "Ping An Insurance", "country": "Chine", "estimated_score": 91, "key_practice": "IA diagnostique intégrée et santé connectée avec 200M+ clients", "differentiator": "Écosystème finance-santé-auto le plus intégré au monde", "source": "McKinsey 2024"},
    ],
    "industry": [
        {"company": "Siemens AG", "country": "Allemagne", "estimated_score": 91, "key_practice": "Jumeau numérique pour 300+ usines mondiales via la plateforme MindSphere", "differentiator": "Pionnier de l'Industrie 4.0 et référence mondiale en automatisation intelligente", "source": "WEF 2024"},
        {"company": "Schneider Electric", "country": "France", "estimated_score": 87, "key_practice": "EcoStruxure IoT connectant 800 000 actifs industriels en temps réel", "differentiator": "Leader de l'efficience énergétique industrielle et de l'usine durable", "source": "Gartner 2024"},
        {"company": "Haier Group", "country": "Chine", "estimated_score": 85, "key_practice": "Modèle RenDanHeYi — micro-entreprises autonomes pilotées par la donnée client", "differentiator": "Organisation industrielle la plus agile au monde selon MIT Sloan", "source": "IDC 2024"},
    ],
    "retail": [
        {"company": "Amazon", "country": "USA", "estimated_score": 95, "key_practice": "Personnalisation IA sur 350M produits, logistique robotisée dans 1 000+ entrepôts", "differentiator": "Référence absolue en e-commerce — 40% du marché US en ligne", "source": "McKinsey 2024"},
        {"company": "Alibaba / Tmall", "country": "Chine", "estimated_score": 93, "key_practice": "New Retail fusionnant physique et digital via IA, AR et paiement facial", "differentiator": "Écosystème commerce le plus avancé — 1,3 Mds€ de ventes en 5 min (11.11)", "source": "BCG 2024"},
        {"company": "Zara / Inditex", "country": "Espagne", "estimated_score": 86, "key_practice": "Supply chain ultra-réactive (2 semaines design-to-store) pilotée par la donnée", "differentiator": "Modèle fast-fashion le plus efficace — 0 stock mort grâce au RFID et IA", "source": "Gartner 2024"},
    ],
    "healthcare": [
        {"company": "Mayo Clinic", "country": "USA", "estimated_score": 89, "key_practice": "Plateforme IA diagnostique traitant 1M+ dossiers patients avec 94% de précision", "differentiator": "Leader mondial en IA médicale avec 300 algorithmes certifiés FDA", "source": "NEJM 2024"},
        {"company": "Philips Healthcare", "country": "Pays-Bas", "estimated_score": 87, "key_practice": "Écosystème de santé connectée avec monitoring continu et alertes prédictives", "differentiator": "Pionnier du continuum de soins digital — de la maison à l'hôpital", "source": "Gartner 2024"},
        {"company": "Ramsay Santé", "country": "France", "estimated_score": 81, "key_practice": "DPI unifié sur 400 établissements avec IA pour la gestion des lits et planification", "differentiator": "Leader européen en digitalisation des soins et télémédecine", "source": "ANS 2024"},
    ],
    "tech": [
        {"company": "Microsoft", "country": "USA", "estimated_score": 96, "key_practice": "Copilot IA intégré à toute la suite Microsoft 365 et Azure OpenAI Service", "differentiator": "Plus grande plateforme cloud et IA d'entreprise — 200M utilisateurs Copilot", "source": "IDC 2024"},
        {"company": "Salesforce", "country": "USA", "estimated_score": 92, "key_practice": "Einstein AI natif dans le CRM avec Data Cloud unifiant toutes les données client", "differentiator": "Leader du CRM IA — plateforme #1 de la relation client intelligente", "source": "Gartner 2024"},
        {"company": "SAP", "country": "Allemagne", "estimated_score": 88, "key_practice": "SAP Business AI embarqué dans tous les processus ERP et supply chain", "differentiator": "Plus grand écosystème ERP mondial — 87% des transactions mondiales transitent par SAP", "source": "IDC 2024"},
    ],
    "education": [
        {"company": "Coursera", "country": "USA", "estimated_score": 88, "key_practice": "Plateforme IA adaptative avec 7 000+ cours et micro-certifications reconnues", "differentiator": "Leader mondial de la formation en ligne — 148M apprenants dans 190 pays", "source": "UNESCO 2024"},
        {"company": "Duolingo", "country": "USA", "estimated_score": 91, "key_practice": "Apprentissage adaptatif par IA avec gamification et personnalisation totale", "differentiator": "App éducative la plus téléchargée au monde — DAU de 37M avec 94% de rétention", "source": "EdSurge 2024"},
        {"company": "Universidad UNED", "country": "Espagne", "estimated_score": 83, "key_practice": "Université 100% distance avec IA pour l'accompagnement personnalisé de 300 000 étudiants", "differentiator": "Modèle de référence européen pour l'enseignement supérieur à distance digitalisé", "source": "OCDE 2024"},
    ],
    "transport": [
        {"company": "UPS / UPS Orion", "country": "USA", "estimated_score": 89, "key_practice": "Algorithme IA Orion optimisant 55 000 routes — économie de 100M miles/an", "differentiator": "Leader de la logistique intelligente avec le plus grand réseau IoT de colis au monde", "source": "McKinsey 2024"},
        {"company": "SNCF", "country": "France", "estimated_score": 82, "key_practice": "Maintenance prédictive IA sur 16 000 km de voies et 16 000 trains connectés", "differentiator": "Référence européenne en maintenance ferroviaire prédictive et mobilité MaaS", "source": "UITP 2024"},
        {"company": "DB Schenker", "country": "Allemagne", "estimated_score": 85, "key_practice": "Plateforme digitale unifiée avec visibilité temps réel sur 2M d'expéditions/mois", "differentiator": "Leader mondial du transport & logistique digitalisé — TMS le plus avancé du secteur", "source": "Gartner 2024"},
    ],
    "energy": [
        {"company": "Enel Group", "country": "Italie", "estimated_score": 88, "key_practice": "Smart grid avec 45M compteurs intelligents et IA pour l'équilibrage réseau", "differentiator": "Leader mondial de la transition énergétique numérique avec 100% renouvelable en 2040", "source": "IEA 2024"},
        {"company": "Ørsted", "country": "Danemark", "estimated_score": 91, "key_practice": "Transformation de pétrolier à leader mondial de l'éolien offshore digital", "differentiator": "Cas de transformation sectorielle le plus cité — score ESG #1 mondial", "source": "WEF 2024"},
        {"company": "TotalEnergies", "country": "France", "estimated_score": 84, "key_practice": "Plateforme data lake industrielle et jumeaux numériques sur tous les actifs", "differentiator": "Leader de la transition multi-énergie avec la plus grande capacité solaire en France", "source": "IEA 2024"},
    ],
    "construction": [
        {"company": "Vinci", "country": "France", "estimated_score": 85, "key_practice": "BIM 6D sur tous les projets >50M€, drones et réalité augmentée sur chantier", "differentiator": "Leader mondial BTP avec le programme digital le plus avancé du secteur", "source": "McKinsey 2024"},
        {"company": "Skanska", "country": "Suède", "estimated_score": 88, "key_practice": "Construction zéro accident via IA et wearables, BIM et impression 3D béton", "differentiator": "Référence mondiale en construction durable et sécurité digitale des chantiers", "source": "WEF 2024"},
        {"company": "KATERRA", "country": "USA", "estimated_score": 82, "key_practice": "Construction modulaire hors-site avec supply chain verticalement intégrée et digitale", "differentiator": "Pionnier de la construction industrialisée — réduction de 40% des délais et coûts", "source": "Gartner 2024"},
    ],
    "default": [
        {"company": "Amazon", "country": "USA", "estimated_score": 93, "key_practice": "Plateforme cloud AWS et culture data-driven à toutes les strates", "differentiator": "Pionnier du cloud computing et de l'IA appliquée à grande échelle", "source": "Gartner 2024"},
        {"company": "Siemens AG", "country": "Allemagne", "estimated_score": 87, "key_practice": "Jumeau numérique industriel et usine 4.0 intégralement connectée", "differentiator": "Leader mondial de la transformation digitale industrielle", "source": "WEF 2024"},
        {"company": "Ping An Group", "country": "Chine", "estimated_score": 89, "key_practice": "IA et big data intégrés dans tous les produits financiers et santé", "differentiator": "2 000+ chercheurs en IA — plus grand investisseur FinTech mondial", "source": "McKinsey 2024"},
    ]
}

_MATURITY_ROADMAP = {
    "INITIAL": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Établir les fondations digitales", "actions": ["Cartographier les processus manuels prioritaires à automatiser", "Déployer un ERP/CRM cloud de base", "Former les équipes aux outils numériques essentiels"], "gain": "+10 à +15 points", "target": "BASIQUE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Digitaliser les processus cœur de métier", "actions": ["Mettre en place une architecture data centralisée", "Lancer la migration cloud des applications critiques", "Créer un portail client digital avec self-service"], "gain": "+15 à +20 points", "target": "INTERMEDIAIRE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Intégrer l'IA dans les décisions métier", "actions": ["Déployer des modèles prédictifs pour l'analyse de risque", "Automatiser 60% des processus de back-office", "Mettre en place une gouvernance données mature"], "gain": "+20 à +25 points", "target": "AVANCE", "investment": "Élevé"},
    ],
    "BASIQUE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Consolider la base digitale et éliminer les silos", "actions": ["Unifier les sources de données dans un data lake centralisé", "Déployer des APIs pour l'intégration inter-systèmes", "Automatiser les reportings et tableaux de bord"], "gain": "+8 à +12 points", "target": "INTERMEDIAIRE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Développer les capacités analytiques avancées", "actions": ["Implémenter une plateforme BI self-service pour tous les métiers", "Lancer des pilotes IA/ML sur les cas d'usage à fort ROI", "Transformer l'expérience client en omnicanal seamless"], "gain": "+12 à +18 points", "target": "AVANCE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Atteindre l'excellence opérationnelle digitale", "actions": ["Industrialiser les modèles IA validés en production", "Déployer une architecture microservices full cloud", "Certifier la gouvernance des données (ISO 27001, RGPD)"], "gain": "+15 à +20 points", "target": "OPTIMISE", "investment": "Élevé"},
    ],
    "INTERMEDIAIRE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Optimiser et automatiser les processus clés", "actions": ["Déployer l'automatisation RPA sur les tâches répétitives", "Renforcer la cybersécurité (Zero Trust, SOC)", "Lancer un programme d'innovation interne (lab digital)"], "gain": "+5 à +10 points", "target": "AVANCE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Intégrer l'IA générative dans les produits/services", "actions": ["Pilotes IA générative pour support client et production de contenu", "Moderniser le SI legacy vers une architecture API-first", "Mettre en place un programme de data literacy pour les managers"], "gain": "+10 à +15 points", "target": "AVANCE", "investment": "Élevé"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Devenir leader digital du secteur", "actions": ["Monétiser les données via de nouveaux modèles business", "Déployer des jumeaux numériques pour les opérations critiques", "Contribuer à des consortiums d'innovation sectorielle"], "gain": "+10 à +15 points", "target": "OPTIMISE", "investment": "Élevé"},
    ],
    "AVANCE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Industrialiser l'IA et les plateformes data", "actions": ["Déployer un MLOps pour la gestion du cycle de vie des modèles IA", "Étendre le Data Mesh à toutes les business units", "Lancer une offre data-as-a-service pour les partenaires"], "gain": "+5 à +8 points", "target": "OPTIMISE", "investment": "Élevé"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Créer de la valeur par l'innovation digitale", "actions": ["Développer des plateformes d'écosystème avec partenaires", "Adopter l'architecture Composable Enterprise (MACH)", "Mesurer et maximiser le ROI digital avec des OKRs data-driven"], "gain": "+5 à +7 points", "target": "OPTIMISE", "investment": "Modéré"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Rayonnement et leadership sectoriel", "actions": ["Partager les best practices via publications et conférences", "Nouer des partenariats R&D avec universités et startups", "Piloter des initiatives ESG digitales à impact mesurable"], "gain": "+3 à +5 points", "target": "OPTIMISE", "investment": "Faible"},
    ],
    "OPTIMISE": [
        {"phase": "Phase 1 — Court terme (0-6 mois)", "objective": "Maintenir l'avance technologique", "actions": ["Veille active sur les technologies émergentes (Quantum, Gen-AI)", "Benchmarking continu avec les leaders mondiaux", "Programme d'excellence continue (Kaizen digital)"], "gain": "+2 à +4 points", "target": "OPTIMISE", "investment": "Modéré"},
        {"phase": "Phase 2 — Moyen terme (6-18 mois)", "objective": "Exporter l'expertise digitale", "actions": ["Créer un centre d'excellence digital partageable", "Monétiser les actifs technologiques propriétaires", "Développer des partenariats stratégiques de co-innovation"], "gain": "+2 à +3 points", "target": "OPTIMISE", "investment": "Faible"},
        {"phase": "Phase 3 — Long terme (18-36 mois)", "objective": "Façonner l'avenir du secteur", "actions": ["Contribuer aux standards et régulations sectorielles", "Investir dans les startups deep-tech du secteur", "Déployer des solutions ESG et d'impact digital mesurable"], "gain": "+2 à +3 points", "target": "OPTIMISE", "investment": "Faible"},
    ],
}


_VALID_POSITIONING_LABELS = {
    "Top quartile",
    "Au-dessus de la moyenne internationale",
    "Dans la moyenne",
    "En dessous de la moyenne",
}

# Per-axis sector average modifiers relative to the global nat_avg
# Based on Gartner DTI / McKinsey Digital Index 2023-2024 axis breakdowns
_AXIS_MODIFIERS: dict[str, dict[str, float]] = {
    "banking":      {"METIER": 1.15, "PROCESSUS": 1.05, "SI": 1.20, "CANAUX": 1.10, "MARKETING": 0.90, "RH": 0.95, "OFFRES": 1.15, "MODELE_OPERATIONNEL": 1.10, "IT_DATA": 1.20},
    "insurance":    {"METIER": 1.10, "PROCESSUS": 1.00, "SI": 1.15, "CANAUX": 0.95, "MARKETING": 0.90, "RH": 0.90, "OFFRES": 1.05, "MODELE_OPERATIONNEL": 1.05, "IT_DATA": 1.15},
    "industry":     {"METIER": 1.05, "PROCESSUS": 1.15, "SI": 1.00, "CANAUX": 0.85, "MARKETING": 0.80, "RH": 0.90, "OFFRES": 0.90, "MODELE_OPERATIONNEL": 1.15, "IT_DATA": 1.05},
    "retail":       {"METIER": 1.00, "PROCESSUS": 1.00, "SI": 1.05, "CANAUX": 1.25, "MARKETING": 1.20, "RH": 0.90, "OFFRES": 1.10, "MODELE_OPERATIONNEL": 1.00, "IT_DATA": 1.05},
    "healthcare":   {"METIER": 1.00, "PROCESSUS": 1.10, "SI": 1.15, "CANAUX": 0.90, "MARKETING": 0.85, "RH": 1.00, "OFFRES": 0.95, "MODELE_OPERATIONNEL": 1.05, "IT_DATA": 1.15},
    "tech":         {"METIER": 1.10, "PROCESSUS": 1.15, "SI": 1.20, "CANAUX": 1.10, "MARKETING": 1.05, "RH": 1.10, "OFFRES": 1.15, "MODELE_OPERATIONNEL": 1.15, "IT_DATA": 1.20},
    "education":    {"METIER": 0.95, "PROCESSUS": 0.90, "SI": 1.05, "CANAUX": 0.95, "MARKETING": 0.85, "RH": 1.00, "OFFRES": 0.90, "MODELE_OPERATIONNEL": 0.90, "IT_DATA": 1.00},
    "transport":    {"METIER": 1.00, "PROCESSUS": 1.10, "SI": 1.05, "CANAUX": 0.95, "MARKETING": 0.85, "RH": 0.90, "OFFRES": 0.90, "MODELE_OPERATIONNEL": 1.10, "IT_DATA": 1.05},
    "energy":       {"METIER": 1.05, "PROCESSUS": 1.10, "SI": 1.15, "CANAUX": 0.85, "MARKETING": 0.80, "RH": 0.95, "OFFRES": 0.90, "MODELE_OPERATIONNEL": 1.10, "IT_DATA": 1.15},
    "construction": {"METIER": 0.95, "PROCESSUS": 1.00, "SI": 0.95, "CANAUX": 0.85, "MARKETING": 0.80, "RH": 0.85, "OFFRES": 0.80, "MODELE_OPERATIONNEL": 0.95, "IT_DATA": 0.95},
    "default":      {"METIER": 1.00, "PROCESSUS": 1.00, "SI": 1.05, "CANAUX": 1.00, "MARKETING": 0.95, "RH": 0.95, "OFFRES": 0.95, "MODELE_OPERATIONNEL": 1.00, "IT_DATA": 1.05},
}

_VALID_IMPACT_LEVELS = {"ELEVE", "MOYEN", "FAIBLE"}
_VALID_INVESTMENT_LEVELS = {"Faible", "Modéré", "Élevé"}

# Maps request axis names (used in evaluation scores) → KB prefix in sub_axis_data.py
_AXIS_TO_KB_PREFIX: dict[str, str] = {
    "METIER":                        "BUSINESS",
    "BUSINESS":                      "BUSINESS",
    "PROCESSUS":                     "PROCESS",
    "PROCESS":                       "PROCESS",
    "SI":                            "INFORMATION_SYSTEM",
    "INFORMATION_SYSTEM":            "INFORMATION_SYSTEM",
    "CANAUX":                        "CANAUX_DISTRIBUTION",
    "CANAUX_DISTRIBUTION":           "CANAUX_DISTRIBUTION",
    "MARKETING":                     "MARKETING_COMMUNICATION",
    "MARKETING_COMMUNICATION":       "MARKETING_COMMUNICATION",
    "RH":                            "RH_CULTURE_DIGITALE",
    "RH_CULTURE_DIGITALE":           "RH_CULTURE_DIGITALE",
    "OFFRES":                        "OFFRES_DIGITALES",
    "OFFRES_DIGITALES":              "OFFRES_DIGITALES",
    "MODELE_OPERATIONNEL":           "MODELE_OPERATIONNEL_INNOVATION",
    "MODELE_OPERATIONNEL_INNOVATION":"MODELE_OPERATIONNEL_INNOVATION",
    "IT_DATA":                       "IT_DATA",
}


def _compute_positioning_label(score: float, nat: float, intl: float, top: float) -> str:
    if score >= top:
        return "Top quartile"
    if score >= intl:
        return "Au-dessus de la moyenne internationale"
    if score >= nat:
        return "Dans la moyenne"
    return "En dessous de la moyenne"


class BenchmarkingEngine:
    def __init__(self):
        # Use large model for benchmarks — output is cached, quality > speed
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def benchmark(self, request) -> dict:
        try:
            prompt = self._build_prompt(request)
            raw = await call_groq(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.5,
                model=self.model,
                task=TaskType.BENCHMARKING,
            )
            data = extract_json(raw)
            result = self._normalize(data, request)
        except Exception:
            result = self._fallback_benchmark(request)
        try:
            result["sub_axis_benchmarks"] = await self._build_sub_axis_benchmarks(request)
        except Exception:
            result["sub_axis_benchmarks"] = []
        return result

    # ── Fallback (rule-based) ──────────────────────────────────────────────────

    def _fallback_benchmark(self, request) -> dict:
        sector_key = _resolve_sector(request.sector)
        sd = _SECTOR_DATA.get(sector_key, _DEFAULT_DATA)

        score     = float(request.global_score)
        nat_avg   = float(sd["nat"])
        intl_avg  = float(sd["intl"])
        top_q     = float(sd["top"])

        # Percentile + label
        if score >= top_q:
            percentile = min(99, 75 + int((score - top_q) / max(1, 100 - top_q) * 24))
            label = "Top quartile"
        elif score >= intl_avg:
            percentile = 55 + int((score - intl_avg) / max(1, top_q - intl_avg) * 20)
            label = "Au-dessus de la moyenne internationale"
        elif score >= nat_avg:
            percentile = 35 + int((score - nat_avg) / max(1, intl_avg - nat_avg) * 20)
            label = "Dans la moyenne"
        else:
            percentile = max(5, int(score / nat_avg * 35))
            label = "En dessous de la moyenne"

        # Axis benchmarks — use per-axis modifiers for realistic sector averages
        axis_benchmarks = []
        axis_mods = _AXIS_MODIFIERS.get(sector_key, _AXIS_MODIFIERS["default"])
        all_axis_scores = [
            ("METIER",              "Métier",                           float(request.business_score)),
            ("PROCESSUS",           "Processus",                        float(request.process_score)),
            ("SI",                  "Système d'Information",            float(request.si_score)),
            ("CANAUX",              "Canaux & UX",                      float(getattr(request, "canaux_score", 0) or 0)),
            ("MARKETING",           "Marketing & Communication",        float(getattr(request, "marketing_score", 0) or 0)),
            ("RH",                  "RH & Culture Digitale",            float(getattr(request, "rh_score", 0) or 0)),
            ("OFFRES",              "Offres Digitales",                  float(getattr(request, "offres_score", 0) or 0)),
            ("MODELE_OPERATIONNEL", "Modèle Opérationnel & Innovation", float(getattr(request, "modele_operationnel_score", 0) or 0)),
            ("IT_DATA",             "IT & Data",                        float(getattr(request, "it_data_score", 0) or 0)),
        ]
        for axis_key_ab, axis_lbl, comp_score in all_axis_scores:
            if comp_score == 0:
                continue
            mod = axis_mods.get(axis_key_ab, 1.0)
            axis_nat  = round(nat_avg  * mod, 1)
            axis_top  = round(top_q    * mod, 1)
            axis_benchmarks.append({
                "axis":           axis_key_ab,
                "axis_label":     axis_lbl,
                "company_score":  comp_score,
                "sector_average": axis_nat,
                "top_quartile":   axis_top,
                "gap_to_average": round(comp_score - axis_nat, 1),
                "gap_to_top":     round(comp_score - axis_top, 1),
            })

        # Trends — use sector-specific if available, else default
        trends = [
            {**t, "source_url": _get_source_url(t.get("source", ""))}
            for t in _SECTOR_TRENDS.get(sector_key, _SECTOR_TRENDS["default"])[:5]
        ]

        # Leaders — use sector-specific if available, else default
        leaders = [
            {**l, "source_url": _get_source_url(l.get("source", ""))}
            for l in _SECTOR_LEADERS.get(sector_key, _SECTOR_LEADERS["default"])
        ]

        # Roadmap — pick by maturity level (fallback to INTERMEDIAIRE)
        maturity = (request.maturity_level or "INTERMEDIAIRE").upper()
        roadmap_template = _MATURITY_ROADMAP.get(maturity, _MATURITY_ROADMAP["INTERMEDIAIRE"])
        roadmap = [
            {
                "phase":               p["phase"],
                "objective":           p["objective"],
                "actions":             p["actions"],
                "expected_score_gain": p["gain"],
                "target_level":        p["target"],
                "investment_level":    p["investment"],
            }
            for p in roadmap_template
        ]

        gap_nat = round(score - nat_avg, 1)
        gap_top = round(top_q - score, 1)
        gap_str = f"{'+' if gap_nat >= 0 else ''}{gap_nat}"

        if gap_nat >= 0:
            gap_sentence = "l'entreprise se distingue positivement et doit capitaliser sur ses forces pour consolider son leadership."
        else:
            gap_sentence = f"des actions prioritaires permettraient de combler l'écart de {abs(gap_nat):.0f} points avec la moyenne sectorielle."

        executive_summary = (
            f"{request.company_name} affiche un score de maturité digitale de {score:.0f}/100, "
            f"se positionnant au {percentile}ème percentile du secteur {request.sector}. "
            f"Avec un écart de {gap_str} points par rapport à la moyenne nationale ({nat_avg:.0f}/100), "
            f"{gap_sentence} "
            f"Pour atteindre le top quartile ({top_q:.0f}/100), un gain de {max(0, gap_top):.0f} points est nécessaire."
        )

        return {
            "company_name":   request.company_name,
            "sector":         request.sector,
            "country":        request.country,
            "global_score":   score,
            "maturity_level": request.maturity_level,
            "executive_summary": executive_summary,
            "sector_benchmark": {
                "national_average":      nat_avg,
                "international_average": intl_avg,
                "top_quartile_score":    top_q,
                "company_percentile":    max(5, min(99, percentile)),
                "positioning_label":     label,
                "source":                sd["source"],
            },
            "axis_benchmarks":    axis_benchmarks,
            "trends":             trends,
            "sector_leaders":     leaders,
            "improvement_roadmap": roadmap,
            "sub_axis_benchmarks": [],
            "key_insights": [
                f"Score global {score:.0f}/100 — {label} dans le secteur {request.sector}.",
                f"Écart de {gap_str} pts vs moyenne nationale ; {max(0, gap_top):.0f} pts restants pour intégrer le top quartile.",
                "Axe prioritaire : renforcer les dimensions les plus en retard par rapport au benchmark sectoriel.",
            ],
        }

    # ── LLM prompts ────────────────────────────────────────────────────────────

    def _system_prompt(self) -> str:
        return (
            "Tu es un expert en benchmarking de maturité digitale avec une connaissance approfondie "
            "des écosystèmes numériques par pays ET par secteur. "
            "TES ANALYSES DOIVENT TOUJOURS distinguer 3 niveaux de leaders : "
            "NATIONAL (entreprises du même pays), REGIONAL (même zone géographique), GLOBAL (leaders mondiaux). "
            "Ne génère JAMAIS un benchmarking générique : identifie les acteurs RÉELS du pays et du secteur. "
            "Les réglementations citées doivent prioritairement être celles du pays concerné. "
            "Sources : Gartner, McKinsey, WEF, OECD, BCG, IDC (2022-2024). "
            "Réponds UNIQUEMENT en JSON valide, sans texte hors JSON."
        )

    def _build_prompt(self, req) -> str:
        canaux              = getattr(req, "canaux_score",              0) or 0
        marketing           = getattr(req, "marketing_score",           0) or 0
        rh                  = getattr(req, "rh_score",                  0) or 0
        offres              = getattr(req, "offres_score",              0) or 0
        modele_operationnel = getattr(req, "modele_operationnel_score", 0) or 0
        it_data             = getattr(req, "it_data_score",             0) or 0

        # Only include evaluated axes (score > 0) in the axis_benchmarks template
        axis_lines = [
            '    {{"axis":"METIER","axis_label":"Métier","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
            '    {{"axis":"PROCESSUS","axis_label":"Processus","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
            '    {{"axis":"SI","axis_label":"Système d\'Information","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}',
        ]
        if canaux > 0:
            axis_lines.append('    {{"axis":"CANAUX","axis_label":"Canaux & UX","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if marketing > 0:
            axis_lines.append('    {{"axis":"MARKETING","axis_label":"Marketing & Communication","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if rh > 0:
            axis_lines.append('    {{"axis":"RH","axis_label":"RH & Culture Digitale","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if offres > 0:
            axis_lines.append('    {{"axis":"OFFRES","axis_label":"Offres Digitales","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if modele_operationnel > 0:
            axis_lines.append('    {{"axis":"MODELE_OPERATIONNEL","axis_label":"Modèle Opérationnel & Innovation","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')
        if it_data > 0:
            axis_lines.append('    {{"axis":"IT_DATA","axis_label":"IT & Data","company_score":<float>,"sector_average":<float>,"top_quartile":<float>,"gap_to_average":<float>,"gap_to_top":<float>}}')

        axes_template = ",\n".join(axis_lines)

        # Pre-compute positioning label from scores so the LLM doesn't hallucinate it
        sector_key = _resolve_sector(req.sector)
        sd = _SECTOR_DATA.get(sector_key, _DEFAULT_DATA)
        nat_avg = float(sd["nat"])
        intl_avg = float(sd["intl"])
        top_q = float(sd["top"])
        computed_label = _compute_positioning_label(
            float(req.global_score), nat_avg, intl_avg, top_q
        )
        computed_percentile = self._compute_percentile(
            float(req.global_score), nat_avg, intl_avg, top_q
        )

        region = _resolve_region(req.country)

        consultant_section = ""
        if getattr(req, "consultant_prompt", None):
            consultant_section = f"""
DIRECTIVES DU CONSULTANT (adapter executive_summary, feuille de route et insights UNIQUEMENT) :
{req.consultant_prompt}

IMPORTANT : ces directives n'affectent PAS les valeurs numériques ni positioning_label.
"""

        return f"""Produis une analyse de benchmarking sectoriel STRICTEMENT au format JSON ci-dessous.

PROFIL : {req.company_name} | Secteur: {req.sector} | Pays: {req.country} | Région: {region}
SCORES :
- Global={req.global_score:.1f}/100 | Métier={req.business_score:.1f} | Processus={req.process_score:.1f} | SI={req.si_score:.1f}
- Canaux={canaux:.1f} | Marketing={marketing:.1f} | RH={rh:.1f} | Offres={offres:.1f}
- Modèle Opérationnel={modele_operationnel:.1f} | IT & Data={it_data:.1f}
MATURITÉ : {req.maturity_level}
{consultant_section}
CONTRAINTES ABSOLUES — ne pas dévier :
- positioning_label DOIT être exactement l'une de ces 4 valeurs : "Top quartile" | "Au-dessus de la moyenne internationale" | "Dans la moyenne" | "En dessous de la moyenne"
- La valeur correcte pour cette entreprise est : "{computed_label}" (percentile {computed_percentile})
- national_average = {nat_avg} | international_average = {intl_avg} | top_quartile_score = {top_q}
- company_percentile = {computed_percentile}
- impact_level DOIT être : "ELEVE" | "MOYEN" | "FAIBLE" (jamais autre chose)
- investment_level DOIT être : "Faible" | "Modéré" | "Élevé"
- Les company_score dans axis_benchmarks DOIVENT reprendre exactement les scores fournis ci-dessus
- Génère 5 tendances SECTORIELLES GÉNÉRALES du secteur {req.sector} en {req.country} / {region}
- Les tendances décrivent des phénomènes du marché, PAS les actions de {req.company_name}
- NE JAMAIS mentionner "{req.company_name}" dans les tendances — cite des acteurs TIERS (concurrents, leaders du secteur, études de marché)
- Chaque trend.description DOIT citer 1 entreprise EXTERNE (pas {req.company_name}) + 1 chiffre précis + 1 date
- Chaque sector_leader.key_practice DOIT contenir des chiffres mesurables et une date
- source DOIT être la référence complète : "Organisation Année — Titre du rapport"
- source_url DOIT être l'URL officielle de l'organisation source

RÈGLE CRITIQUE SUR LES LEADERS — hiérarchie OBLIGATOIRE :
- 2 leaders NATIONAUX : entreprises RÉELLES opérant en {req.country} dans le secteur {req.sector}
  (Si {req.country} a peu d'acteurs, prends les plus importants ou les filiales locales de groupes)
- 2 leaders RÉGIONAUX : entreprises RÉELLES de la région {region} (hors {req.country})
- 1 leader GLOBAL : référence mondiale du secteur {req.sector}
- Le champ "level" DOIT être "NATIONAL", "REGIONAL" ou "GLOBAL"
- Ne génère PAS de leaders génériques : nomme des entreprises vérifiables avec chiffres réels

FORMAT JSON OBLIGATOIRE :
{{
  "executive_summary": "3-4 phrases spécifiques à {req.company_name} dans le secteur {req.sector} en {req.country}.",
  "sector_benchmark": {{
    "national_average": {nat_avg},
    "international_average": {intl_avg},
    "top_quartile_score": {top_q},
    "company_percentile": {computed_percentile},
    "positioning_label": "{computed_label}",
    "source": "{sd['source']}"
  }},
  "axis_benchmarks": [
{axes_template}
  ],
  "trends": [
    {{"title":"<phénomène sectoriel {req.sector} / {req.country}>","description":"<acteur EXTERNE (pas {req.company_name}) + chiffre + date — ex: 'En 2023, Banque X a déployé Y, réduisant les coûts de 30%'>","impact_level":"ELEVE","horizon":"<horizon>","adoption_rate":"<taux chiffré>","source":"<Org Année — Rapport>","source_url":"<https://url>"}},
    {{"title":"...","description":"<acteur EXTERNE + chiffre + date>","impact_level":"MOYEN","horizon":"...","adoption_rate":"...","source":"...","source_url":"..."}},
    {{"title":"...","description":"<acteur EXTERNE + chiffre + date>","impact_level":"ELEVE","horizon":"...","adoption_rate":"...","source":"...","source_url":"..."}},
    {{"title":"...","description":"<acteur EXTERNE + chiffre + date>","impact_level":"MOYEN","horizon":"...","adoption_rate":"...","source":"...","source_url":"..."}},
    {{"title":"...","description":"<acteur EXTERNE + chiffre + date>","impact_level":"FAIBLE","horizon":"...","adoption_rate":"...","source":"...","source_url":"..."}}
  ],
  "sector_leaders": [
    {{"level":"NATIONAL","company":"<leader {req.sector} en {req.country}>","country":"{req.country}","estimated_score":<int>,"key_practice":"<chiffres+date>","differentiator":"...","source":"...","source_url":"..."}},
    {{"level":"NATIONAL","company":"<2ème acteur {req.sector} en {req.country}>","country":"{req.country}","estimated_score":<int>,"key_practice":"...","differentiator":"...","source":"...","source_url":"..."}},
    {{"level":"REGIONAL","company":"<leader {req.sector} en {region}>","country":"<pays {region}>","estimated_score":<int>,"key_practice":"...","differentiator":"...","source":"...","source_url":"..."}},
    {{"level":"REGIONAL","company":"<2ème acteur {req.sector} en {region}>","country":"<pays {region}>","estimated_score":<int>,"key_practice":"...","differentiator":"...","source":"...","source_url":"..."}},
    {{"level":"GLOBAL","company":"<leader mondial {req.sector}>","country":"<pays>","estimated_score":<int>,"key_practice":"...","differentiator":"...","source":"...","source_url":"..."}}
  ],
  "improvement_roadmap": [
    {{"phase":"Phase 1 — Court terme (0-6 mois)","objective":"...","actions":["...","...","..."],"expected_score_gain":"+X points","target_level":"...","investment_level":"Modéré"}},
    {{"phase":"Phase 2 — Moyen terme (6-18 mois)","objective":"...","actions":["...","...","..."],"expected_score_gain":"+X points","target_level":"...","investment_level":"Élevé"}},
    {{"phase":"Phase 3 — Long terme (18-36 mois)","objective":"...","actions":["...","...","..."],"expected_score_gain":"+X points","target_level":"...","investment_level":"Élevé"}}
  ],
  "key_insights": [
    "Insight 1 spécifique à {req.company_name} en {req.country}",
    "Insight 2 sur les axes prioritaires",
    "Insight 3 sur la feuille de route"
  ]
}}"""

    # ── Sub-axis benchmarks (hybrid: static KB + template analysis) ───────────

    async def _build_sub_axis_benchmarks(self, request) -> list[dict]:
        """Build per-sub-axis benchmarks from static KB enriched with LLM analysis + leaders."""
        sub_axis_scores = getattr(request, "sub_axis_scores", None) or []
        if not sub_axis_scores:
            return []

        company_name = getattr(request, "company_name", "")
        country      = getattr(request, "country", "")
        sector       = getattr(request, "sector", "")
        region       = _resolve_region(country)

        sector_key = _resolve_sector(sector)
        sd = _SECTOR_DATA.get(sector_key, _DEFAULT_DATA)
        nat_avg = float(sd["nat"])

        # Pre-load KB data so both LLM calls can use it
        country_kb = get_country_context(country, sector)   # non-empty for Maroc/Tunisie/Algérie/France/Allemagne
        sas_data: list[tuple[str, str, float, dict]] = []
        for sas in sub_axis_scores:
            axis     = str(sas.get("axis", "")).upper()
            sub_axis = str(sas.get("sub_axis", ""))
            score    = float(sas.get("score", 0))
            if not axis or not sub_axis:
                continue
            kb_prefix = _AXIS_TO_KB_PREFIX.get(axis, axis)

            # Step 1 — exact match (banking KB, fast path)
            kb = get_sub_axis_data(kb_prefix, sub_axis, sector=sector) or {}

            # Step 2 — fuzzy sector JSON if critical fields are missing
            # This handles AI-generated sub-axis names for non-banking sectors
            # (insurance, health, education, retail, etc.)
            missing_fields = (
                not kb.get("zoom_case_study")
                or not kb.get("cadre_juridique")
                or not kb.get("tendances")
                or not kb.get("leaders_nationaux")
            )
            if missing_fields:
                sector_kb = get_sub_axis_extra_fuzzy(kb_prefix, sub_axis, sector=sector)
                if sector_kb:
                    kb = {**sector_kb, **kb}

            # Step 3 — country-specific override for Maroc, Tunisie, Algérie, France, Allemagne
            # Replaces CIMA/UEMOA-centric cadre_juridique and leaders_nationaux with
            # country-accurate data. Preserves sector trends and other KB fields.
            if country_kb:
                if country_kb.get("cadre_juridique"):
                    kb["cadre_juridique"] = country_kb["cadre_juridique"]
                if country_kb.get("leaders_nationaux"):
                    kb["leaders_nationaux"] = country_kb["leaders_nationaux"]
                if country_kb.get("zoom_case_study") and not kb.get("zoom_case_study", {}).get("entreprise"):
                    kb["zoom_case_study"] = country_kb["zoom_case_study"]
                if country_kb.get("analyse_statique"):
                    kb["analyse_statique"] = country_kb["analyse_statique"]

            sas_data.append((axis, sub_axis, score, kb))

        sub_axis_names = [sa for _, sa, _, _ in sas_data]

        # Run sequentially to avoid hitting Groq's tokens-per-minute rate limit
        llm_leaders  = await self._generate_sub_axis_leaders(sub_axis_names, sector, country, region)
        llm_analyses = await self._generate_sub_axis_analyses(sas_data, sector, country, company_name, nat_avg)

        result = []
        for axis, sub_axis, score, kb in sas_data:
            llm_sa    = llm_leaders.get(sub_axis, {})
            nat_entry = llm_sa.get("national")
            reg_entry = llm_sa.get("regional")

            leaders_nat = ([nat_entry] if nat_entry else []) + kb.get("leaders_nationaux", [])
            leaders_reg = ([reg_entry] if reg_entry else []) + kb.get("leaders_regionaux", [])

            analyse = (
                llm_analyses.get(sub_axis)
                or self._template_analyse(
                    sub_axis, score, kb,
                    company_name=company_name,
                    country=country,
                    region=region,
                    nat_avg=nat_avg,
                )
            )

            result.append({
                "axis":                   axis,
                "sub_axis":               sub_axis,
                "company_score":          score,
                "tendances":              kb.get("tendances", []),
                "analyse_statique":       kb.get("analyse_statique", ""),
                "maturite_maximale":      kb.get("maturite_maximale", ""),
                "cadre_juridique":        kb.get("cadre_juridique", []),
                "ma_levees_fonds":        kb.get("ma_levees_fonds", []),
                "leaders_nationaux":      leaders_nat,
                "leaders_regionaux":      leaders_reg,
                "leaders_internationaux": kb.get("leaders_internationaux", []),
                "analyse_personnalisee":  analyse,
                "zoom_case_study":        self._select_zoom_by_score(
                    kb, score,
                    national_leader=nat_entry,
                    regional_leader=reg_entry,
                ),
                "comparatif_organisations": kb.get("comparatif_organisations", {}),
                "risques":                kb.get("risques", []),
                "opportunites":           kb.get("opportunites", []),
            })
        return result

    async def _generate_sub_axis_leaders(
        self,
        sub_axes: list[str],
        sector: str,
        country: str,
        region: str,
    ) -> dict:
        """LLM call — generates 1 national + 1 regional leader per sub-axis for this country+sector."""
        if not sub_axes:
            return {}
        axes_json = ", ".join(f'"{sa}"' for sa in sub_axes[:20])
        prompt = (
            f"Secteur: {sector} | Pays: {country} | Région: {region}\n\n"
            f"Pour chaque sous-axe, fournis UN leader national (opérant en {country}) "
            f"et UN leader régional ({region}, hors {country}) dans le secteur {sector}.\n"
            f"Sous-axes: [{axes_json}]\n\n"
            "Format JSON STRICT (même clés que les sous-axes fournis) :\n"
            '{"Nom du sous-axe": '
            '{"national": {"entreprise":"...","pays":"' + country + '","pratique":"... chiffre + date ...","source":"..."},'
            '"regional": {"entreprise":"...","pays":"<pays région>","pratique":"... chiffre + date ...","source":"..."}'
            "}, ...}"
        )
        try:
            raw = await call_groq(
                messages=[
                    {"role": "system", "content": "Expert benchmarking sectoriel. Réponds UNIQUEMENT en JSON valide."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                task=TaskType.BENCHMARKING,
            )
            return extract_json(raw)
        except Exception:
            return {}

    async def _generate_sub_axis_analyses(
        self,
        sas_data: list[tuple[str, str, float, dict]],
        sector: str,
        country: str,
        company_name: str,
        nat_avg: float,
    ) -> dict:
        """LLM call — generates a specific, non-generic analysis for each sub-axis.

        Returns {sub_axis_name: analysis_text}. Falls back to empty dict on error
        so _template_analyse is used as safety net.
        """
        if not sas_data:
            return {}

        name_label = company_name if company_name else "l'entreprise"
        lines = []
        for _, sub_axis, score, kb in sas_data[:20]:
            ctx_parts = []
            if kb.get("analyse_statique"):
                ctx_parts.append(kb["analyse_statique"][:200])
            if kb.get("maturite_maximale"):
                ctx_parts.append(f"Excellence: {kb['maturite_maximale'][:150]}")
            ctx = " | ".join(ctx_parts) if ctx_parts else "—"
            lines.append(
                f'- Sous-axe: "{sub_axis}" | Score: {score:.0f}/100 '
                f'(moy. nationale: {nat_avg:.0f}) | Contexte KB: {ctx}'
            )

        axes_block = "\n".join(lines)
        prompt = f"""Tu es expert en transformation digitale pour le secteur {sector} en {country}.

Pour chaque sous-axe ci-dessous, rédige une analyse personnalisée et UNIQUE de 2-3 phrases pour {name_label}.

RÈGLES STRICTES :
- Chaque analyse doit être DIFFÉRENTE des autres, même si les scores sont identiques
- Cite des pratiques, outils, réglementations ou technologies CONCRETS propres à CE sous-axe
- Mentionne l'écart précis par rapport à la moyenne sectorielle et ses implications opérationnelles
- Propose 1-2 actions prioritaires SPÉCIFIQUES à ce sous-axe (ex: "implémenter un CRM sectoriel", "adopter l'e-souscription")
- INTERDIT : formules génériques comme "consolider les acquis", "cibler les écarts", "plan de transformation structuré"
- Les clés JSON doivent être EXACTEMENT les noms des sous-axes fournis
- Adapte chaque analyse au contexte KB fourni pour ce sous-axe

SOUS-AXES À ANALYSER :
{axes_block}

Réponds UNIQUEMENT en JSON valide avec les noms de sous-axes comme clés :
{{"Nom exact du sous-axe": "Analyse unique et spécifique 2-3 phrases...", ...}}"""

        sub_axis_names = [sa for _, sa, _, _ in sas_data[:20]]
        try:
            raw = await call_groq(
                messages=[
                    {"role": "system", "content": "Expert benchmarking digital. Réponds UNIQUEMENT en JSON valide."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.65,
                task=TaskType.BENCHMARKING,
            )
            raw_dict = extract_json(raw)
            if not isinstance(raw_dict, dict):
                return {}
            # Fuzzy key matching: LLM sometimes returns slightly different key names
            matched: dict = {}
            for sa in sub_axis_names:
                if sa in raw_dict:
                    matched[sa] = raw_dict[sa]
                    continue
                sa_norm = sa.lower().strip()
                for k, v in raw_dict.items():
                    if k.lower().strip() == sa_norm:
                        matched[sa] = v
                        break
                if sa not in matched:
                    # Partial match fallback: check if sub-axis name is contained in key
                    for k, v in raw_dict.items():
                        if sa_norm in k.lower() or k.lower() in sa_norm:
                            matched[sa] = v
                            break
            return matched
        except Exception:
            return {}

    def _select_zoom_by_score(
        self,
        kb: dict,
        score: float,
        national_leader: dict | None = None,
        regional_leader: dict | None = None,
    ) -> dict:
        """Return a case study matched to the company's maturity level.

        Score >= 60 → global leader (aspirational top-tier)
        Score 35-59 → regional leader (attainable mid-term reference)
        Score < 35  → national leader (immediately relatable local model)

        LLM-generated national/regional leaders take priority over static KB entries.
        """
        def _leader_as_zoom(leader: dict) -> dict:
            pratique = leader.get("pratique", "")
            return {
                "entreprise": leader.get("entreprise", ""),
                "pays":       leader.get("pays", ""),
                "technologie": pratique[:80] if pratique else "",
                "description": pratique,
                "resultats":   "",
                "source":      leader.get("source", ""),
                "annee":       "2023",
            }

        if score >= 60:
            return kb.get("zoom_case_study", {})

        if score >= 35:
            if regional_leader:
                return _leader_as_zoom(regional_leader)
            leaders_r = kb.get("leaders_regionaux", [])
            if leaders_r:
                return _leader_as_zoom(leaders_r[0])
            return kb.get("zoom_case_study", {})

        if national_leader:
            return _leader_as_zoom(national_leader)
        leaders_n = kb.get("leaders_nationaux", [])
        if leaders_n:
            return _leader_as_zoom(leaders_n[0])
        leaders_r = kb.get("leaders_regionaux", [])
        if leaders_r:
            return _leader_as_zoom(leaders_r[0])
        return kb.get("zoom_case_study", {})

    def _template_analyse(
        self,
        sub_axis: str,
        score: float,
        kb: dict,
        company_name: str = "",
        country: str = "",
        region: str = "",
        nat_avg: float = 0.0,
    ) -> str:
        """Generate a personalized analysis mentioning company name, country, region, and sector gap."""
        if score >= 75:
            level  = "un niveau avancé"
            action = "consolider les acquis et viser l'excellence opérationnelle"
        elif score >= 50:
            level  = "un niveau intermédiaire"
            action = "cibler les écarts identifiés et accélérer le plan de transformation"
        elif score >= 25:
            level  = "un niveau basique"
            action = "engager un plan de transformation structuré sur 12-18 mois"
        else:
            level  = "un niveau initial"
            action = "poser les fondations digitales en priorité absolue"

        name_part    = company_name if company_name else "L'entreprise"
        geo_parts    = [p for p in [country, region] if p and p.lower() != country.lower()]
        country_part = f" ({country})" if country else ""
        region_label = f" / région {geo_parts[0]}" if geo_parts else ""

        gap_part = ""
        if nat_avg > 0:
            gap = score - nat_avg
            if gap > 5:
                gap_part = (
                    f" Ce score dépasse de {gap:.0f} pts la moyenne sectorielle nationale"
                    f" ({nat_avg:.0f}/100), positionnant {name_part} favorablement"
                    f" dans son marché{country_part}."
                )
            elif gap < -5:
                gap_part = (
                    f" Ce score est {abs(gap):.0f} pts en dessous de la moyenne sectorielle"
                    f" ({nat_avg:.0f}/100){region_label} — un écart prioritaire à combler."
                )
            else:
                gap_part = (
                    f" Ce score est proche de la moyenne sectorielle ({nat_avg:.0f}/100)"
                    f"{country_part}, avec une marge de progression identifiée."
                )

        excellence = ""
        if kb.get("maturite_maximale"):
            excerpt = kb["maturite_maximale"][:120].rstrip()
            excellence = f" L'excellence dans ce domaine implique : {excerpt}…"

        # Specific context from KB to make each sub-axis analysis unique
        specific_context = ""
        tendances = kb.get("tendances", [])
        analyse_statique = kb.get("analyse_statique", "")
        if tendances:
            t = tendances[0]
            titre = t.get("titre", "")
            desc  = t.get("description", "")[:110]
            if titre:
                specific_context = f" La tendance clé sur ce sous-axe est « {titre} » : {desc}…"
        elif analyse_statique:
            specific_context = f" {analyse_statique[:160].rstrip()}…"

        return (
            f"{name_part}{country_part} affiche {level} sur le sous-axe « {sub_axis} »"
            f" avec un score de {score:.0f}/100.{gap_part}"
            f"{specific_context}"
            f" La priorité est de {action}.{excellence}"
        )

    @staticmethod
    def _scrub_company_name(text: str, company_name: str) -> str:
        """Remove the evaluated company's name from trend text — trends must cite external actors."""
        if not text or not company_name:
            return text
        import re
        # Replace exact name (case-insensitive) with generic industry placeholder
        pattern = re.compile(re.escape(company_name), re.IGNORECASE)
        return pattern.sub("les acteurs du secteur", text)

    def _compute_percentile(self, score: float, nat: float, intl: float, top: float) -> int:
        if score >= top:
            return min(99, 75 + int((score - top) / max(1, 100 - top) * 24))
        if score >= intl:
            return 55 + int((score - intl) / max(1, top - intl) * 20)
        if score >= nat:
            return 35 + int((score - nat) / max(1, intl - nat) * 20)
        return max(5, int(score / max(1, nat) * 35))

    # ── Normalisation (LLM path) ───────────────────────────────────────────────

    def _normalize(self, data: dict, req) -> dict:
        sb = data.get("sector_benchmark", {})

        # Use reference sector data as ground truth for numeric values
        sector_key = _resolve_sector(req.sector)
        sd = _SECTOR_DATA.get(sector_key, _DEFAULT_DATA)
        nat_ref   = float(sd["nat"])
        intl_ref  = float(sd["intl"])
        top_ref   = float(sd["top"])

        # Accept LLM values only if they are plausible (non-zero and within range)
        nat_avg  = float(sb.get("national_average") or 0) or nat_ref
        intl_avg = float(sb.get("international_average") or 0) or intl_ref
        top_q    = float(sb.get("top_quartile_score") or 0) or top_ref

        # Always compute positioning label and percentile from actual scores — never trust LLM
        score = float(req.global_score)
        positioning_label = _compute_positioning_label(score, nat_avg, intl_avg, top_q)
        percentile = self._compute_percentile(score, nat_avg, intl_avg, top_q)

        sector_benchmark = {
            "national_average":      nat_avg,
            "international_average": intl_avg,
            "top_quartile_score":    top_q,
            "company_percentile":    max(5, min(99, percentile)),
            "positioning_label":     positioning_label,
            "source":                sb.get("source") or sd["source"],
        }

        # Map real scores from request for axis validation
        real_scores = {
            "METIER":              float(req.business_score),
            "PROCESSUS":           float(req.process_score),
            "SI":                  float(req.si_score),
            "CANAUX":              float(getattr(req, "canaux_score", 0) or 0),
            "MARKETING":           float(getattr(req, "marketing_score", 0) or 0),
            "RH":                  float(getattr(req, "rh_score", 0) or 0),
            "OFFRES":              float(getattr(req, "offres_score", 0) or 0),
            "MODELE_OPERATIONNEL": float(getattr(req, "modele_operationnel_score", 0) or 0),
            "IT_DATA":             float(getattr(req, "it_data_score", 0) or 0),
        }
        axis_benchmarks = []
        for ab in data.get("axis_benchmarks", []):
            axis = ab.get("axis", "").upper()
            # Always use real score from request — never trust LLM for company_score
            comp = real_scores.get(axis, float(ab.get("company_score", 0)))
            sec_avg = float(ab.get("sector_average") or nat_avg)
            top_val = float(ab.get("top_quartile") or top_q)
            axis_benchmarks.append({
                "axis":           axis,
                "axis_label":     ab.get("axis_label", axis),
                "company_score":  comp,
                "sector_average": sec_avg,
                "top_quartile":   top_val,
                "gap_to_average": round(comp - sec_avg, 1),
                "gap_to_top":     round(comp - top_val, 1),
            })

        company_name = req.company_name
        trends = [
            {
                "title":         self._scrub_company_name(t.get("title", ""), company_name),
                "description":   self._scrub_company_name(t.get("description", ""), company_name),
                "impact_level":  t.get("impact_level", "MOYEN") if t.get("impact_level") in _VALID_IMPACT_LEVELS else "MOYEN",
                "horizon":       t.get("horizon", "Moyen terme"),
                "adoption_rate": t.get("adoption_rate", ""),
                "source":        t.get("source", ""),
                "source_url":    t.get("source_url") or _get_source_url(t.get("source", "")),
            }
            for t in data.get("trends", [])
        ]

        leaders = [
            {
                "level":           l.get("level", "GLOBAL"),
                "company":         l.get("company", ""),
                "country":         l.get("country", ""),
                "estimated_score": int(l.get("estimated_score", 80)),
                "key_practice":    l.get("key_practice", ""),
                "differentiator":  l.get("differentiator", ""),
                "source":          l.get("source", ""),
                "source_url":      l.get("source_url") or _get_source_url(l.get("source", "")),
            }
            for l in data.get("sector_leaders", [])
        ]

        roadmap = [
            {
                "phase":               p.get("phase", ""),
                "objective":           p.get("objective", ""),
                "actions":             p.get("actions", []),
                "expected_score_gain": p.get("expected_score_gain", ""),
                "target_level":        p.get("target_level", ""),
                "investment_level":    p.get("investment_level", "Modéré"),
            }
            for p in data.get("improvement_roadmap", [])
        ]

        return {
            "company_name":      req.company_name,
            "sector":            req.sector,
            "country":           req.country,
            "global_score":      float(req.global_score),
            "maturity_level":    req.maturity_level,
            "executive_summary": data.get("executive_summary", ""),
            "sector_benchmark":  sector_benchmark,
            "axis_benchmarks":   axis_benchmarks,
            "trends":            trends,
            "sector_leaders":    leaders,
            "improvement_roadmap": roadmap,
            "sub_axis_benchmarks": [],
            "key_insights":      data.get("key_insights", []),
        }
