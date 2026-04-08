"""
Digital Maturity Frameworks Knowledge Base
Sources: Gartner, McKinsey, MIT CISR, CMMI Institute, ISO, ISACA (COBIT), WEF
Each framework includes: maturity levels, key domains, assessment criteria.
This knowledge is injected into AI prompts to ground generated questions.
"""

FRAMEWORKS = {

    "GARTNER_DMM": {
        "name": "Gartner Digital Maturity Model",
        "authority": "Gartner Research",
        "focus": "Overall digital business transformation across strategy, culture, technology and customer",
        "maturity_levels": {
            1: "Absent — No formal digital strategy. Initiatives are isolated and uncoordinated.",
            2: "Opportunistic — Ad-hoc digital experiments. No shared vision. Budget-driven.",
            3: "Repeatable — Digital strategy exists. Some processes standardized. Governance emerging.",
            4: "Managed — Digital KPIs defined and tracked. Cross-functional teams. Data-driven decisions.",
            5: "Optimizing — Continuous innovation. AI/ML embedded. Ecosystem partnerships. Market leader."
        },
        "domains": {
            "Digital Strategy": [
                "Existence of a formal multi-year digital transformation roadmap",
                "Digital budget as % of total IT investment (target: >30%)",
                "C-suite ownership of digital strategy (CDO or equivalent)",
                "Alignment of digital strategy with business objectives",
                "Ecosystem and platform strategy (partnerships, APIs, marketplaces)"
            ],
            "Customer Experience": [
                "Omnichannel customer journey mapping and optimization",
                "Real-time customer data platform (CDP) in use",
                "Personalization at scale using AI/ML",
                "Net Promoter Score (NPS) tracked and acted upon",
                "Digital self-service rate (% transactions handled digitally)"
            ],
            "Workforce & Culture": [
                "Digital literacy training programs for all employees",
                "Percentage of workforce with digital skills certifications",
                "Innovation culture KPIs (number of digital experiments per quarter)",
                "Agile/DevOps adoption across IT and business teams",
                "Change management capability for digital transformation"
            ],
            "Technology & Architecture": [
                "Cloud adoption rate (% workloads in cloud)",
                "API-first architecture and integration strategy",
                "Microservices and containerization adoption",
                "Legacy system modernization roadmap",
                "Cybersecurity posture and zero-trust architecture"
            ],
            "Data & Analytics": [
                "Enterprise data governance policy in place",
                "Self-service analytics tools available to business users",
                "Real-time data processing capabilities",
                "AI/ML models in production use",
                "Data monetization strategy"
            ]
        }
    },

    "MCKINSEY_DQ": {
        "name": "McKinsey Digital Quotient (DQ)",
        "authority": "McKinsey & Company",
        "focus": "Measures digital capability across strategy, culture, organization and capabilities — proven in 150+ companies",
        "maturity_levels": {
            1: "Digital Laggard — Below industry average. Significant transformation needed.",
            2: "Digital Follower — Reacting to digital trends. No clear strategy.",
            3: "Digital Contender — Active investment in digital. Strategy in place but gaps remain.",
            4: "Digital Challenger — Strong digital capabilities. Competing effectively.",
            5: "Digital Leader — Industry benchmark. Setting digital standards."
        },
        "domains": {
            "Strategy & Innovation": [
                "Digital ambition set at board level with explicit targets",
                "Innovation pipeline with dedicated funding (>2% revenue in digital R&D)",
                "Agile strategic planning cycles (quarterly vs annual)",
                "Build-buy-partner decision framework for digital capabilities",
                "Scenario planning for digital disruption risks"
            ],
            "Talent & Culture": [
                "Digital talent acquisition and retention programs",
                "Culture of experimentation — fail fast, learn fast",
                "Cross-functional digital squads (business + tech + data)",
                "Leader digital fluency — executives can engage with technical topics",
                "Employee digital enablement (tools, training, autonomy)"
            ],
            "Organization & Ways of Working": [
                "Agile at scale — product teams with end-to-end accountability",
                "DevOps and continuous delivery pipeline",
                "Digital factory or center of excellence established",
                "Flat decision-making for digital initiatives",
                "OKR (Objectives and Key Results) framework in use"
            ],
            "Technology & Capabilities": [
                "Modern data architecture (data lake / data mesh)",
                "AI/ML factory — systematic model development and deployment",
                "Core system modernization (ERP, CRM on modern platforms)",
                "Cybersecurity as business enabler (not just compliance)",
                "Open banking / open API ecosystem participation"
            ]
        }
    },

    "MIT_CISR": {
        "name": "MIT CISR Digital Maturity Model",
        "authority": "MIT Center for Information Systems Research",
        "focus": "Two-dimensional model: Customer Experience digitalization vs Operational digitalization",
        "maturity_levels": {
            1: "Beginner — Low digital customer experience AND low operational digitalization.",
            2: "Fashionista — High customer-facing digital BUT low operational backbone.",
            3: "Conservative — Strong operational digitalization BUT low customer digital experience.",
            4: "Digirati — High on both dimensions. Digital leader generating superior results."
        },
        "domains": {
            "Digital Customer Experience": [
                "Digital channels generate >50% of revenue or interactions",
                "Customer journey is fully digital end-to-end",
                "Personalized digital interactions using customer data",
                "Mobile-first experience with >80% satisfaction score",
                "Digital ecosystem partners enhance customer value"
            ],
            "Operational Digitalization": [
                "Core business processes are automated (RPA or AI-driven)",
                "Real-time operational visibility across the value chain",
                "Shared digital platform used by multiple business units",
                "Data flows seamlessly between systems without manual intervention",
                "Predictive maintenance or operations using IoT/AI"
            ],
            "Information & Insight": [
                "Single source of truth for key operational data",
                "Real-time dashboards available to front-line managers",
                "Predictive analytics in production for key business outcomes",
                "Data quality monitored with SLAs defined",
                "External data sources integrated (market, economic, social)"
            ]
        }
    },

    "CMMI": {
        "name": "Capability Maturity Model Integration (CMMI)",
        "authority": "CMMI Institute / ISACA",
        "focus": "Process maturity for development and service delivery organizations",
        "maturity_levels": {
            1: "Initial — Processes unpredictable, poorly controlled, reactive.",
            2: "Managed — Projects managed using defined practices. Reactive.",
            3: "Defined — Proactive. Organization-wide standards. Processes characterized and understood.",
            4: "Quantitatively Managed — Measured and controlled using statistical methods.",
            5: "Optimizing — Focus on continuous process improvement using quantitative feedback."
        },
        "domains": {
            "Process Management": [
                "Organizational process definition (OPD) — standard process library",
                "Organizational process focus (OPF) — process improvement plans",
                "Quantitative project management using statistical control",
                "Causal analysis and resolution for defects",
                "Process performance baselines and models"
            ],
            "Project Management": [
                "Requirements management — traceability and change control",
                "Project planning with WBS, schedule, and risk register",
                "Project monitoring — earned value or equivalent KPIs",
                "Integrated project management across stakeholders",
                "Risk management — identification, mitigation, monitoring"
            ],
            "Engineering": [
                "Requirements development — elicitation, analysis, validation",
                "Technical solution — architecture and design decisions documented",
                "Product integration — assembly and interface management",
                "Verification — peer reviews, testing protocols",
                "Validation — acceptance testing against customer needs"
            ],
            "Support": [
                "Configuration management — version control, change control board",
                "Quality assurance — process and product audits",
                "Measurement and analysis — defined measures, data collection",
                "Decision analysis — formal criteria for decisions",
                "Causal analysis — root cause identification"
            ]
        }
    },

    "ISO_27001": {
        "name": "ISO/IEC 27001:2022 — Information Security Management",
        "authority": "International Organization for Standardization (ISO)",
        "focus": "Information security, cybersecurity, and privacy protection",
        "maturity_levels": {
            1: "Non-existent — No security controls. Ad-hoc responses to incidents.",
            2: "Initial — Some controls in place but not systematically managed.",
            3: "Defined — ISMS documented. Policies in place. Regular risk assessments.",
            4: "Managed — Controls monitored. Incidents tracked. Audits conducted.",
            5: "Optimizing — Continuous improvement. Threat intelligence. Security-by-design."
        },
        "domains": {
            "Information Security Governance": [
                "Information security policy approved by top management",
                "Chief Information Security Officer (CISO) role defined",
                "Information security risk assessment process (ISO 27005)",
                "Statement of Applicability (SoA) maintained",
                "Management review of ISMS performance (annual minimum)"
            ],
            "Access Control & Identity": [
                "Role-Based Access Control (RBAC) implemented",
                "Multi-factor authentication (MFA) for critical systems",
                "Privileged access management (PAM) solution in place",
                "Access review cycle (quarterly for privileged, annual for all)",
                "Zero-trust architecture principles applied"
            ],
            "Incident Management": [
                "Security incident response plan documented and tested",
                "Mean Time to Detect (MTTD) and Respond (MTTR) tracked",
                "Security Operations Center (SOC) or equivalent monitoring",
                "Incident classification and escalation procedures",
                "Post-incident review and lessons learned process"
            ],
            "Data Protection": [
                "Data classification policy (public / internal / confidential / secret)",
                "Encryption at rest and in transit for sensitive data",
                "Data Loss Prevention (DLP) controls",
                "GDPR/local regulation compliance program",
                "Data retention and secure disposal procedures"
            ],
            "Business Continuity": [
                "Business Impact Analysis (BIA) completed",
                "Recovery Time Objective (RTO) and Recovery Point Objective (RPO) defined",
                "Disaster recovery plan tested (annual minimum)",
                "Backup strategy — 3-2-1 rule applied",
                "Supply chain security — third-party risk management"
            ]
        }
    },

    "COBIT_2019": {
        "name": "COBIT 2019 — IT Governance Framework",
        "authority": "ISACA",
        "focus": "Enterprise IT governance, risk management and value delivery from IT investments",
        "maturity_levels": {
            0: "Incomplete — Process not performed or fails to achieve its purpose.",
            1: "Initial — Process achieves its purpose informally. No planning.",
            2: "Managed — Process is planned, monitored and adjusted.",
            3: "Defined — Process is tailored from a defined standard process.",
            4: "Quantitatively Managed — Process performance controlled using statistics.",
            5: "Optimizing — Continuous improvement using quantitative understanding."
        },
        "domains": {
            "IT Governance (EDM)": [
                "IT strategy aligned with business strategy (EDM01)",
                "Benefits realization from IT investments tracked (EDM02)",
                "IT risk appetite defined and communicated (EDM03)",
                "IT resource optimization — sourcing strategy (EDM04)",
                "Stakeholder transparency — IT reporting to board (EDM05)"
            ],
            "IT Management — Alignment (APO)": [
                "IT strategy and roadmap (APO02)",
                "Enterprise architecture managed (APO03)",
                "IT budget and cost management (APO06)",
                "IT risk management framework (APO12)",
                "IT security management (APO13)"
            ],
            "IT Management — Build & Run (BAI/DSS)": [
                "Change management — CAB process (BAI06)",
                "Asset and configuration management — CMDB (BAI09)",
                "Service desk and incident management — ITIL aligned (DSS02)",
                "Problem management — root cause elimination (DSS03)",
                "Continuity management — BCP/DRP (DSS04)"
            ]
        }
    },

    "WEF_DTI": {
        "name": "WEF Digital Transformation Initiative",
        "authority": "World Economic Forum",
        "focus": "Industry-level digital transformation measuring economic and societal impact",
        "maturity_levels": {
            1: "Nascent — Digital transformation not yet a priority. Traditional operations.",
            2: "Emerging — Digital projects starting. Leadership awareness building.",
            3: "Developing — Digital programs active. Business model adaptation underway.",
            4: "Maturing — Digital integrated in core operations. Value being captured.",
            5: "Leading — Digital-native operations. New business models. Ecosystem builder."
        },
        "domains": {
            "Technology Adoption": [
                "Cloud computing adoption rate across the organization",
                "Internet of Things (IoT) deployment in operations",
                "Artificial Intelligence use cases in production",
                "Blockchain / distributed ledger for trust and traceability",
                "5G / edge computing readiness"
            ],
            "Human Capital": [
                "Digital skills gap assessment conducted",
                "Reskilling/upskilling investment per employee (annual)",
                "STEM talent pipeline and partnerships with universities",
                "Digital leadership development program",
                "Remote and hybrid work digital enablement"
            ],
            "Digital Infrastructure": [
                "Network infrastructure capacity and reliability (SLA >99.9%)",
                "Cybersecurity investment as % of IT budget (benchmark: 10-15%)",
                "Digital identity and authentication infrastructure",
                "Open data and API ecosystem availability",
                "Green IT / sustainable digital infrastructure"
            ],
            "Innovation Ecosystem": [
                "R&D investment in digital technologies",
                "Startup/scale-up collaboration programs",
                "Intellectual property (patents) in digital technologies",
                "Academic / research institution partnerships",
                "Participation in digital standards bodies"
            ]
        }
    }
}


# Maps sectors to most relevant frameworks
SECTOR_FRAMEWORK_MAP = {
    "finance": ["GARTNER_DMM", "MCKINSEY_DQ", "ISO_27001", "COBIT_2019"],
    "banque": ["GARTNER_DMM", "MCKINSEY_DQ", "ISO_27001", "COBIT_2019"],
    "banking": ["GARTNER_DMM", "MCKINSEY_DQ", "ISO_27001", "COBIT_2019"],
    "assurance": ["GARTNER_DMM", "ISO_27001", "COBIT_2019", "MCKINSEY_DQ"],
    "insurance": ["GARTNER_DMM", "ISO_27001", "COBIT_2019", "MCKINSEY_DQ"],
    "santé": ["CMMI", "ISO_27001", "GARTNER_DMM", "WEF_DTI"],
    "healthcare": ["CMMI", "ISO_27001", "GARTNER_DMM", "WEF_DTI"],
    "industrie": ["CMMI", "WEF_DTI", "GARTNER_DMM", "MIT_CISR"],
    "manufacturing": ["CMMI", "WEF_DTI", "GARTNER_DMM", "MIT_CISR"],
    "retail": ["GARTNER_DMM", "MIT_CISR", "MCKINSEY_DQ", "WEF_DTI"],
    "commerce": ["GARTNER_DMM", "MIT_CISR", "MCKINSEY_DQ", "WEF_DTI"],
    "telecom": ["GARTNER_DMM", "MCKINSEY_DQ", "MIT_CISR", "COBIT_2019"],
    "éducation": ["CMMI", "WEF_DTI", "GARTNER_DMM", "MIT_CISR"],
    "education": ["CMMI", "WEF_DTI", "GARTNER_DMM", "MIT_CISR"],
    "public": ["COBIT_2019", "CMMI", "ISO_27001", "WEF_DTI"],
    "gouvernement": ["COBIT_2019", "CMMI", "ISO_27001", "WEF_DTI"],
    "energie": ["WEF_DTI", "CMMI", "ISO_27001", "GARTNER_DMM"],
    "energy": ["WEF_DTI", "CMMI", "ISO_27001", "GARTNER_DMM"],
    "transport": ["WEF_DTI", "CMMI", "GARTNER_DMM", "MIT_CISR"],
    "logistique": ["WEF_DTI", "CMMI", "GARTNER_DMM", "MIT_CISR"],
    "default": ["GARTNER_DMM", "MCKINSEY_DQ", "MIT_CISR", "ISO_27001"]
}


def get_frameworks_for_sector(sector: str, max_frameworks: int = 3) -> list[dict]:
    """Returns the top N framework objects relevant for a given sector."""
    sector_lower = sector.lower().strip()
    framework_keys = None

    for key in SECTOR_FRAMEWORK_MAP:
        if key in sector_lower or sector_lower in key:
            framework_keys = SECTOR_FRAMEWORK_MAP[key]
            break

    if not framework_keys:
        framework_keys = SECTOR_FRAMEWORK_MAP["default"]

    selected = []
    for key in framework_keys[:max_frameworks]:
        if key in FRAMEWORKS:
            selected.append({"key": key, **FRAMEWORKS[key]})

    return selected


def format_frameworks_for_prompt(frameworks: list[dict]) -> str:
    """Formats framework knowledge as a structured string for injection into prompts."""
    lines = []
    for fw in frameworks:
        lines.append(f"\n## {fw['name']} ({fw['authority']})")
        lines.append(f"Focus: {fw['focus']}")
        lines.append("\nMaturity Levels:")
        for level, desc in fw["maturity_levels"].items():
            lines.append(f"  Level {level}: {desc}")
        lines.append("\nKey Assessment Domains & Criteria:")
        for domain, criteria in fw["domains"].items():
            lines.append(f"\n  [{domain}]")
            for c in criteria:
                lines.append(f"    • {c}")
    return "\n".join(lines)
