import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

interface MaturityLevel { level: number | string; desc: string; }
interface Framework {
  key: string;
  name: string;
  authority: string;
  category: string;
  categoryColor: string;
  icon: string;
  iconBg: string;
  focus: string;
  maturityLevels: MaturityLevel[];
  domains: { name: string; criteria: string[] }[];
}

const FRAMEWORKS: Framework[] = [
  {
    key: 'GARTNER_DMM',
    name: 'Digital Maturity Model',
    authority: 'Gartner Research',
    category: 'Stratégie',
    categoryColor: '#6366f1',
    icon: 'fas fa-chess-king',
    iconBg: 'linear-gradient(135deg,#6366f1,#818cf8)',
    focus: 'Transformation digitale globale : stratégie, culture, technologie et expérience client.',
    maturityLevels: [
      { level: 1, desc: 'Absent — Aucune stratégie digitale. Initiatives isolées.' },
      { level: 2, desc: 'Opportuniste — Expérimentations ad-hoc. Pas de vision partagée.' },
      { level: 3, desc: 'Répétable — Stratégie digitale établie. Processus standardisés émergents.' },
      { level: 4, desc: 'Géré — KPIs digitaux définis et suivis. Décisions data-driven.' },
      { level: 5, desc: 'Optimisant — Innovation continue. IA/ML intégrée. Leader marché.' }
    ],
    domains: [
      { name: 'Stratégie Digitale', criteria: ['Feuille de route pluriannuelle','Budget digital > 30% IT','CDO au comité exécutif','Alignement stratégie business','Stratégie API & écosystème'] },
      { name: 'Expérience Client', criteria: ['Parcours client omnicanal','Plateforme de données clients (CDP)','Personnalisation IA/ML à l\'échelle','NPS mesuré et actionné','Taux d\'auto-service digital'] },
      { name: 'Culture & Talents', criteria: ['Programmes de formation digitale','Certifications compétences digitales','Culture d\'innovation (KPIs)','Adoption Agile / DevOps','Gestion du changement digital'] },
      { name: 'Architecture & Tech', criteria: ['Taux cloud adoption','API-first architecture','Microservices & conteneurisation','Roadmap modernisation legacy','Zero-trust cybersécurité'] },
      { name: 'Data & Analytics', criteria: ['Gouvernance des données','Self-service analytics','Traitement temps réel','IA/ML en production','Stratégie de monétisation data'] }
    ]
  },
  {
    key: 'MCKINSEY_DQ',
    name: 'Digital Quotient (DQ)',
    authority: 'McKinsey & Company',
    category: 'Stratégie',
    categoryColor: '#6366f1',
    icon: 'fas fa-chart-line',
    iconBg: 'linear-gradient(135deg,#0891b2,#22d3ee)',
    focus: 'Mesure des capacités digitales sur 4 axes — validé dans 150+ entreprises mondiales.',
    maturityLevels: [
      { level: 1, desc: 'Retardataire — En dessous de la moyenne du secteur.' },
      { level: 2, desc: 'Suiveur — Réactif aux tendances. Pas de stratégie claire.' },
      { level: 3, desc: 'Candidat — Investissements actifs. Lacunes subsistantes.' },
      { level: 4, desc: 'Challenger — Capacités solides. Compétition efficace.' },
      { level: 5, desc: 'Leader — Référence sectorielle. Définit les standards.' }
    ],
    domains: [
      { name: 'Stratégie & Innovation', criteria: ['Ambition digitale portée au CA','Pipeline innovation > 2% CA en R&D','Cycles stratégiques agiles (trimestriels)','Framework build-buy-partner','Planification scénarios disruption'] },
      { name: 'Talents & Culture', criteria: ['Programmes recrutement digital','Culture expérimentation — fail fast','Squads cross-fonctionnels','Fluence digitale des dirigeants','Autonomie et outillage employés'] },
      { name: 'Organisation Agile', criteria: ['Agilité à l\'échelle — équipes produit','Pipeline DevOps & livraison continue','Digital Factory ou Centre d\'Excellence','Décisions plates pour digital','Framework OKR en place'] },
      { name: 'Capacités Technologiques', criteria: ['Architecture data moderne (data lake/mesh)','Factory IA/ML systématique','Modernisation ERP/CRM','Cybersécurité comme levier business','Participation ecosystème API ouvert'] }
    ]
  },
  {
    key: 'MIT_CISR',
    name: 'Digital Maturity Model',
    authority: 'MIT — CISR',
    category: 'Stratégie',
    categoryColor: '#6366f1',
    icon: 'fas fa-university',
    iconBg: 'linear-gradient(135deg,#7c3aed,#a78bfa)',
    focus: 'Modèle bidimensionnel : digitalisation de l\'expérience client vs digitalisation opérationnelle.',
    maturityLevels: [
      { level: 'Débutant', desc: 'Faible sur les deux dimensions. Transformation non engagée.' },
      { level: 'Fashionista', desc: 'Fort côté client digital MAIS socle opérationnel faible.' },
      { level: 'Conservateur', desc: 'Forte digitalisation opérationnelle MAIS faible expérience client digital.' },
      { level: 'Digirati', desc: 'Leader sur les deux dimensions. Résultats supérieurs.' }
    ],
    domains: [
      { name: 'Expérience Client Digitale', criteria: ['> 50% revenus via canaux digitaux','Parcours client entièrement digital','Interactions personnalisées (data clients)','Mobile-first, satisfaction > 80%','Partenaires écosystème numériques'] },
      { name: 'Digitalisation Opérationnelle', criteria: ['Processus clés automatisés (RPA/IA)','Visibilité opérationnelle temps réel','Plateforme partagée multi-BU','Flux data sans intervention manuelle','Maintenance prédictive IoT/IA'] },
      { name: 'Information & Insights', criteria: ['Source unique de vérité opérationnelle','Tableaux de bord temps réel managers','Analytique prédictive en production','Qualité data avec SLA définis','Sources données externes intégrées'] }
    ]
  },
  {
    key: 'CMMI',
    name: 'Capability Maturity Model Integration',
    authority: 'CMMI Institute / ISACA',
    category: 'Processus',
    categoryColor: '#059669',
    icon: 'fas fa-cogs',
    iconBg: 'linear-gradient(135deg,#059669,#34d399)',
    focus: 'Maturité des processus pour les organisations de développement et de prestation de services.',
    maturityLevels: [
      { level: 1, desc: 'Initial — Processus imprévisibles, mal contrôlés, réactifs.' },
      { level: 2, desc: 'Géré — Projets gérés avec pratiques définies. Réactif.' },
      { level: 3, desc: 'Défini — Proactif. Standards à l\'échelle organisation. Processus compris.' },
      { level: 4, desc: 'Géré quantitativement — Mesure et contrôle statistiques.' },
      { level: 5, desc: 'Optimisant — Amélioration continue basée sur la quantification.' }
    ],
    domains: [
      { name: 'Gestion des Processus', criteria: ['Bibliothèque de processus standard (OPD)','Plans d\'amélioration processus (OPF)','Gestion quantitative de projet','Analyse causale et résolution','Modèles de performance processus'] },
      { name: 'Gestion de Projet', criteria: ['Gestion exigences + traçabilité','Planification projet (WBS, risques)','Suivi valeur acquise (Earned Value)','Gestion intégrée des parties prenantes','Risk management — identification & mitigation'] },
      { name: 'Ingénierie', criteria: ['Développement des exigences','Solution technique documentée','Intégration produit & interfaces','Vérification — revues, tests','Validation — tests d\'acceptation client'] },
      { name: 'Support & Qualité', criteria: ['Configuration management (git/versionning)','Audits qualité processus et produits','Mesure et analyse — collecte données','Prise de décision formelle (critères)','Analyse des causes racines'] }
    ]
  },
  {
    key: 'ISO_27001',
    name: 'ISO/IEC 27001:2022',
    authority: 'ISO — Organisation Internationale de Normalisation',
    category: 'Sécurité',
    categoryColor: '#dc2626',
    icon: 'fas fa-shield-alt',
    iconBg: 'linear-gradient(135deg,#dc2626,#f87171)',
    focus: 'Management de la sécurité de l\'information, cybersécurité et protection de la vie privée.',
    maturityLevels: [
      { level: 1, desc: 'Inexistant — Aucun contrôle. Réponses ad-hoc aux incidents.' },
      { level: 2, desc: 'Initial — Quelques contrôles mais pas systématiquement gérés.' },
      { level: 3, desc: 'Défini — SMSI documenté. Politiques en place. Évaluations régulières.' },
      { level: 4, desc: 'Géré — Contrôles surveillés. Incidents tracés. Audits conduits.' },
      { level: 5, desc: 'Optimisant — Amélioration continue. Threat intelligence. Security-by-design.' }
    ],
    domains: [
      { name: 'Gouvernance Sécurité', criteria: ['Politique sécurité approuvée par la direction','Rôle CISO défini','Processus d\'évaluation des risques (ISO 27005)','Déclaration d\'applicabilité (SoA)','Revue SMSI annuelle (management review)'] },
      { name: 'Contrôle d\'Accès & Identité', criteria: ['RBAC implémenté','MFA pour les systèmes critiques','PAM (Privileged Access Management)','Revue des accès (trimestrielle / annuelle)','Architecture Zero-Trust appliquée'] },
      { name: 'Gestion des Incidents', criteria: ['Plan de réponse incidents documenté et testé','MTTD et MTTR suivis','SOC ou monitoring équivalent','Procédures classification et escalade','Revues post-incidents (lessons learned)'] },
      { name: 'Protection des Données', criteria: ['Politique de classification des données','Chiffrement au repos et en transit','DLP (Data Loss Prevention)','Programme conformité RGPD','Procédures rétention et destruction sécurisée'] },
      { name: 'Continuité d\'Activité', criteria: ['BIA (Business Impact Analysis) complète','RTO et RPO définis','Plan DR testé annuellement','Stratégie backup 3-2-1','Gestion du risque fournisseurs (supply chain)'] }
    ]
  },
  {
    key: 'COBIT_2019',
    name: 'COBIT 2019',
    authority: 'ISACA',
    category: 'Gouvernance IT',
    categoryColor: '#d97706',
    icon: 'fas fa-sitemap',
    iconBg: 'linear-gradient(135deg,#d97706,#fbbf24)',
    focus: 'Gouvernance et management des SI — optimisation valeur, risques et ressources IT.',
    maturityLevels: [
      { level: 0, desc: 'Incomplet — Processus non réalisé ou n\'atteint pas son objectif.' },
      { level: 1, desc: 'Initial — Objectif atteint de façon informelle. Pas de planification.' },
      { level: 2, desc: 'Géré — Processus planifié, surveillé et ajusté.' },
      { level: 3, desc: 'Défini — Processus ajusté à partir d\'un processus standard.' },
      { level: 4, desc: 'Géré quantitativement — Performance contrôlée statistiquement.' },
      { level: 5, desc: 'Optimisant — Amélioration continue fondée sur la compréhension quantitative.' }
    ],
    domains: [
      { name: 'Gouvernance IT (EDM)', criteria: ['Stratégie IT alignée sur le business (EDM01)','Bénéfices investissements IT suivis (EDM02)','Appétit au risque IT défini (EDM03)','Optimisation ressources — stratégie sourcing (EDM04)','Transparence — reporting IT au CA (EDM05)'] },
      { name: 'Alignement Stratégique (APO)', criteria: ['Stratégie & roadmap IT (APO02)','Architecture d\'entreprise gérée (APO03)','Budget IT et gestion des coûts (APO06)','Framework de risk management IT (APO12)','Management sécurité SI (APO13)'] },
      { name: 'Build & Run (BAI/DSS)', criteria: ['Gestion du changement — CAB (BAI06)','Assets & CMDB (BAI09)','Service desk & incidents — ITIL (DSS02)','Problem management — élimination causes (DSS03)','Continuité — BCP/DRP (DSS04)'] }
    ]
  },
  {
    key: 'WEF_DTI',
    name: 'Digital Transformation Initiative',
    authority: 'World Economic Forum',
    category: 'Innovation',
    categoryColor: '#0891b2',
    icon: 'fas fa-globe',
    iconBg: 'linear-gradient(135deg,#0891b2,#67e8f9)',
    focus: 'Transformation digitale au niveau industrie — impact économique et sociétal.',
    maturityLevels: [
      { level: 1, desc: 'Naissant — Transformation digitale non prioritaire. Opérations traditionnelles.' },
      { level: 2, desc: 'Émergent — Projets digitaux démarrés. Prise de conscience du leadership.' },
      { level: 3, desc: 'En développement — Programmes actifs. Adaptation des modèles business.' },
      { level: 4, desc: 'Maturant — Digital intégré dans les opérations core. Valeur capturée.' },
      { level: 5, desc: 'Leader — Opérations digital-native. Nouveaux modèles. Constructeur d\'écosystème.' }
    ],
    domains: [
      { name: 'Adoption Technologique', criteria: ['Taux adoption cloud','Déploiement IoT dans les opérations','Cas d\'usage IA en production','Blockchain pour traçabilité et confiance','Readiness 5G / edge computing'] },
      { name: 'Capital Humain', criteria: ['Évaluation du déficit de compétences digitales','Investissement reskilling/upskilling par employé','Pipeline STEM et partenariats académiques','Programme de leadership digital','Enablement télétravail & hybride'] },
      { name: 'Infrastructure Digitale', criteria: ['Fiabilité réseau (SLA > 99,9%)','Cybersécurité : % du budget IT (10-15%)','Infrastructure identité & authentification','Open data et APIs disponibles','Green IT / infrastructure durable'] },
      { name: 'Écosystème Innovation', criteria: ['Investissement R&D technologies digitales','Programmes collaboration startups','Propriété intellectuelle (brevets digitaux)','Partenariats académiques & recherche','Participation aux organismes de normalisation digitale'] }
    ]
  },
  {
    key: 'SECTOR_BENCHMARKS',
    name: 'Benchmarks Sectoriels',
    authority: 'Agrégation IA Benchmark — Gartner, IDC, McKinsey, WEF',
    category: 'Benchmarking',
    categoryColor: '#7c3aed',
    icon: 'fas fa-chart-bar',
    iconBg: 'linear-gradient(135deg,#7c3aed,#c084fc)',
    focus: 'Positionnement d\'une entreprise par rapport aux moyennes régionales et mondiales de son secteur (13 secteurs × 4 régions).',
    maturityLevels: [
      { level: 'Maghreb', desc: 'Benchmarks locaux — Maroc, Tunisie, Algérie. Calibrés sur les marchés MENA.' },
      { level: 'Afrique', desc: 'Benchmarks africains — hors Maghreb. Sources AfDB, IFC, WEF Afrique.' },
      { level: 'Europe', desc: 'Benchmarks européens — normes EU, Eurostat, ECB pour le secteur financier.' },
      { level: 'Global', desc: 'Benchmarks mondiaux — Fortune 500, études Gartner / IDC / McKinsey.' }
    ],
    domains: [
      { name: 'Finance & Banque', criteria: ['Score moyen Maghreb : 52 | Europe : 68 | Global : 72','Seuil leaders : 78 | Retardataires : 35','Indicateurs : digital banking, open API, core banking cloud','Sources : BCG, McKinsey Banking Pools, BIS'] },
      { name: 'Santé & Médical', criteria: ['Score moyen Maghreb : 38 | Europe : 61 | Global : 65','Seuil leaders : 75 | Retardataires : 25','Indicateurs : e-santé, HIS, télémédecine, PACS','Sources : WHO, Deloitte Health Tech, KPMG Healthcare'] },
      { name: 'Industrie & Manufacturing', criteria: ['Score moyen Maghreb : 43 | Europe : 64 | Global : 67','Seuil leaders : 76 | Retardataires : 30','Indicateurs : Industrie 4.0, IIoT, MES/ERP, automatisation','Sources : WEF Manufacturing, Capgemini, Accenture Industry X'] },
      { name: 'Commerce & Retail', criteria: ['Score moyen Maghreb : 40 | Europe : 66 | Global : 70','Seuil leaders : 80 | Retardataires : 28','Indicateurs : e-commerce, omnicanal, CRM, supply chain digitale','Sources : Salesforce State of Commerce, Forrester Retail'] },
      { name: 'Éducation & Formation', criteria: ['Score moyen Maghreb : 35 | Europe : 58 | Global : 62','Seuil leaders : 72 | Retardataires : 22','Indicateurs : LMS, e-learning, plateforme collaborative, analytics pédagogique'] },
      { name: 'Énergie & Utilities', criteria: ['Score moyen Maghreb : 42 | Europe : 65 | Global : 68','Seuil leaders : 77 | Retardataires : 32','Indicateurs : smart grid, SCADA, GIS, prédictif maintenance','Sources : IEA Digital Energy, Accenture Utilities'] }
    ]
  },
  {
    key: 'REGULATIONS',
    name: 'Cadre Réglementaire',
    authority: 'UE, ISO, ANSI, DGSSI, CNDP — Réglementations numériques',
    category: 'Réglementaire',
    categoryColor: '#b91c1c',
    icon: 'fas fa-gavel',
    iconBg: 'linear-gradient(135deg,#b91c1c,#f87171)',
    focus: 'Référentiel des obligations légales et réglementaires applicables à la transformation digitale — régulations globales, sectorielles et régionales.',
    maturityLevels: [
      { level: 'Global', desc: 'RGPD (protection données UE), ISO/IEC 27001 (SMSI) — applicables à toutes les entreprises.' },
      { level: 'Sectoriel', desc: 'DORA + Bâle IV (finance), HDS (santé France), NIS2 (énergie/télécom), Solvabilité II (assurance).' },
      { level: 'Maroc', desc: 'Loi 09-08 (protection données), DGSSI (cybersécurité), directives BAM pour le secteur bancaire.' },
      { level: 'Tunisie', desc: 'Loi 2004-63 (protection données personnelles), ANSI (agence sécurité informatique), Banque Centrale.' },
      { level: 'Algérie', desc: 'Loi 18-07 (protection données), ANPDP, réglementations ARPCE pour les télécoms.' },
      { level: 'France / UE', desc: 'RGS (référentiel général de sécurité), ANSSI, RGPD, eIDAS, DSP2, DMA/DSA.' }
    ],
    domains: [
      { name: 'Réglementations Universelles', criteria: ['RGPD — Règlement Général sur la Protection des Données (UE 2016/679)','ISO/IEC 27001:2022 — Management de la sécurité de l\'information','ISO/IEC 27701 — Extension vie privée (PIMS)','ISO 31000 — Management des risques','Charte des Nations Unies sur la cybersécurité'] },
      { name: 'Finance & Banque', criteria: ['DORA — Digital Operational Resilience Act (UE 2022/2554, applicable jan. 2025)','Bâle IV — Exigences fonds propres et risques opérationnels (BRI)','DSP2 — Directive Services de Paiement révisée (PSD2)','MiCA — Marchés des crypto-actifs (UE)','Réglementation BAM (Maroc) / BCT (Tunisie) open banking'] },
      { name: 'Santé & Médical', criteria: ['HDS — Hébergement de Données de Santé (France/ANAP)','PGSSI-S — Politique Générale de Sécurité des SI de Santé','HIPAA — Health Insurance Portability and Accountability Act (USA)','MDR — Règlement Dispositifs Médicaux (UE 2017/745)','Données de santé : règles CNIL et CNDP'] },
      { name: 'Énergie & Télécom', criteria: ['NIS2 — Directive Sécurité des Réseaux et Systèmes d\'Information (UE 2022/2555)','Directive CER — Résilience des entités critiques (UE 2022/2557)','Réglementation ANRT (Maroc) / INT (Tunisie)','Cybersécurité OT/SCADA — IEC 62443','Sécurité des infrastructures critiques — NIST SP 800-82'] },
      { name: 'Régulations Régionales MENA', criteria: ['Maroc : Loi 09-08 (CNDP), Loi 05-20 cybersécurité, directives DGSSI','Tunisie : Loi 2004-63 (INPDP), cadre ANSI, Loi 2019-38 sur la startups','Algérie : Loi 18-07 sur la protection des données, Loi 09-04 lutte cybercriminalité','Égypte : Loi 151/2020 sur la protection des données personnelles','Sénégal : Loi 2008-12 — Commission de Protection des Données Personnelles (CDP)'] }
    ]
  },
  {
    key: 'BEST_PRACTICES',
    name: 'Meilleures Pratiques IA',
    authority: 'IA Benchmark — Synthèse Gartner, IDC, McKinsey, MIT, BCG',
    category: 'Pratiques',
    categoryColor: '#0891b2',
    icon: 'fas fa-star',
    iconBg: 'linear-gradient(135deg,#0891b2,#67e8f9)',
    focus: 'Référentiel de bonnes pratiques structurées par axe (Métier, Processus, SI) et par niveau de maturité — actions concrètes, KPIs et délais de mise en œuvre.',
    maturityLevels: [
      { level: 'Initial (Niv. 1)', desc: 'Pratiques fondamentales — poser les bases. Actions rapides à fort impact. Délai : 0-3 mois.' },
      { level: 'Basique (Niv. 2)', desc: 'Structuration et standardisation des processus existants. Délai : 3-6 mois.' },
      { level: 'Intermédiaire (Niv. 3)', desc: 'Intégration et automatisation partielle. Mise en place des indicateurs. Délai : 6-12 mois.' },
      { level: 'Avancé (Niv. 4)', desc: 'Optimisation continue, IA/ML exploitée, architecture scalable. Délai : 12-18 mois.' },
      { level: 'Optimisé (Niv. 5)', desc: 'Innovation permanente, leadership sectoriel, écosystème digital mature. Délai : 18-36 mois.' }
    ],
    domains: [
      { name: 'Axe Métier (BUSINESS)', criteria: ['Niv.1 : Cartographier les besoins clients, définir la vision digitale, audit des données','Niv.2 : Lancer un MVP e-commerce/CRM, former les équipes vente (CRM basique)','Niv.3 : Analytique prédictive clients, segmentation IA, marketplace B2B ou B2C','Niv.4 : IA pour recommandation produit, pricing dynamique, personalization avancée','Niv.5 : Modèle data-driven à l\'échelle, monétisation données, leadership innovation sectorielle'] },
      { name: 'Axe Processus (PROCESS)', criteria: ['Niv.1 : Documenter les processus critiques, identifier les goulots d\'étranglement','Niv.2 : BPM / modélisation BPMN, standardiser les SLA internes, ticketing','Niv.3 : RPA pour tâches répétitives (Robotic Process Automation), workflows intégrés','Niv.4 : Process mining, automatisation intelligente (IPA), orchestration end-to-end','Niv.5 : Processus auto-optimisants via IA, intégration écosystème, agilité complète'] },
      { name: 'Axe Système d\'Information (SI)', criteria: ['Niv.1 : Inventaire SI, classification des actifs, antivirus + firewall, MFA, sauvegardes','Niv.2 : SIEM basique, EDR, patch management, SOC externalisé, PCA documenté','Niv.3 : Zero-trust architecture, cloud hybride sécurisé, SOAR, micro-segmentation','Niv.4 : Threat intelligence, red teaming régulier, plateforme cyber unifiée (XDR)','Niv.5 : IA pour détection anomalies, cyber-résilience complète, auto-remédiation'] },
      { name: 'KPIs clés associés', criteria: ['Délai moyen de mise en œuvre par niveau : 3/6/12/18/36 mois','Taux d\'adoption numérique des employés (cible > 80% au niv. 3)','NPS digital (satisfaction parcours numérique)','MTTD / MTTR incidents cybersécurité','% de processus automatisés (cible > 60% au niv. 4)','ROI des initiatives digitales (cible > 150% à 3 ans)'] }
    ]
  },
  {
    key: 'TECH_STACK',
    name: 'Technologies & Outils IA',
    authority: 'IA Benchmark — Gartner Magic Quadrant, G2, Forrester Wave',
    category: 'Technologies',
    categoryColor: '#059669',
    icon: 'fas fa-microchip',
    iconBg: 'linear-gradient(135deg,#059669,#34d399)',
    focus: 'Cartographie des technologies recommandées par axe et niveau de maturité — outils open-source et commerciaux, avec estimation d\'investissement.',
    maturityLevels: [
      { level: 'Débutant', desc: 'Outils gratuits ou low-cost, SaaS simples, formation minimale requise. Budget < 5K€/an.' },
      { level: 'En développement', desc: 'Solutions mid-market, intégration API, formation équipe dédiée. Budget 5K–50K€/an.' },
      { level: 'Intermédiaire', desc: 'Plateformes enterprise, intégrations complexes, équipe technique. Budget 50K–200K€/an.' },
      { level: 'Avancé', desc: 'Suites enterprise, IA native, architecture microservices. Budget 200K–1M€/an.' },
      { level: 'Expert', desc: 'Plateformes best-in-class, IA/ML custom, équipes dédiées. Budget > 1M€/an.' }
    ],
    domains: [
      { name: 'CRM & Relation Client (Métier)', criteria: ['Débutant : HubSpot Free, Zoho CRM Free, Notion CRM (open-source)','Intermédiaire : Salesforce Sales Cloud, Microsoft Dynamics 365, Pipedrive','Avancé : Salesforce Einstein AI, Adobe Experience Cloud, Oracle CX','BI / Analytics : Power BI, Tableau, Metabase (open-source), Apache Superset','E-commerce : WooCommerce, PrestaShop (OSS), Shopify, Magento, Salesforce Commerce'] },
      { name: 'BPM & Automatisation (Processus)', criteria: ['Débutant : Trello, Notion, Jira Free, monday.com (gestion projets)','Intermédiaire : Bizagi, Camunda (OSS), Activiti, ProcessMaker','RPA : UiPath Community, Blue Prism, Automation Anywhere, n8n (OSS)','ERP : Odoo (OSS), SAP Business One, Microsoft Dynamics ERP, Oracle NetSuite','Gestion de projet : Jira, Asana, ClickUp, OpenProject (OSS)'] },
      { name: 'Cybersécurité (SI)', criteria: ['Débutant : Wazuh (OSS SIEM), ClamAV, pfSense, Bitwarden (gestion mots de passe)','Intermédiaire : Splunk, IBM QRadar, Palo Alto Cortex, CrowdStrike Falcon','Avancé : Microsoft Sentinel, Darktrace IA, SentinelOne XDR, Tenable Nessus','IAM : Keycloak (OSS), Okta, Azure AD, Ping Identity, HashiCorp Vault','Threat Intelligence : MISP (OSS), ThreatConnect, Recorded Future, AlienVault OTX'] },
      { name: 'Cloud & Infrastructure (SI)', criteria: ['Cloud public : AWS, Microsoft Azure, Google Cloud Platform, OVHcloud','Containerisation : Docker, Kubernetes, OpenShift, Rancher (OSS)','CI/CD : GitLab CI, GitHub Actions, Jenkins (OSS), ArgoCD','Monitoring : Prometheus + Grafana (OSS), Datadog, New Relic, Dynatrace','Data & IA : Databricks, Snowflake, Apache Spark (OSS), dbt, MLflow (OSS)'] }
    ]
  }
];

const SECTOR_MAP: { sector: string; icon: string; frameworks: string[] }[] = [
  { sector: 'Banque / Finance',     icon: '🏦', frameworks: ['GARTNER_DMM','MCKINSEY_DQ','ISO_27001','COBIT_2019','SECTOR_BENCHMARKS','REGULATIONS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Assurance',            icon: '🛡️', frameworks: ['GARTNER_DMM','ISO_27001','COBIT_2019','MCKINSEY_DQ','REGULATIONS','SECTOR_BENCHMARKS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Santé',                icon: '🏥', frameworks: ['CMMI','ISO_27001','GARTNER_DMM','WEF_DTI','REGULATIONS','SECTOR_BENCHMARKS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Industrie',            icon: '🏭', frameworks: ['CMMI','WEF_DTI','GARTNER_DMM','MIT_CISR','SECTOR_BENCHMARKS','REGULATIONS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Commerce / Retail',    icon: '🛒', frameworks: ['GARTNER_DMM','MIT_CISR','MCKINSEY_DQ','WEF_DTI','SECTOR_BENCHMARKS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Technologies',         icon: '💻', frameworks: ['MCKINSEY_DQ','GARTNER_DMM','CMMI','MIT_CISR','BEST_PRACTICES','TECH_STACK','SECTOR_BENCHMARKS'] },
  { sector: 'Éducation',            icon: '📚', frameworks: ['CMMI','WEF_DTI','GARTNER_DMM','MIT_CISR','SECTOR_BENCHMARKS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Transport',            icon: '🚚', frameworks: ['WEF_DTI','CMMI','GARTNER_DMM','MIT_CISR','REGULATIONS','SECTOR_BENCHMARKS','BEST_PRACTICES'] },
  { sector: 'Énergie',              icon: '⚡', frameworks: ['WEF_DTI','CMMI','ISO_27001','GARTNER_DMM','REGULATIONS','SECTOR_BENCHMARKS','BEST_PRACTICES','TECH_STACK'] },
  { sector: 'Secteur Public',       icon: '🏛️', frameworks: ['COBIT_2019','CMMI','ISO_27001','WEF_DTI','REGULATIONS','BEST_PRACTICES','TECH_STACK'] }
];

@Component({
  selector: 'app-consultant-frameworks',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  styles: [`
    .fw-card {
      border-radius: 16px; cursor: pointer;
      transition: transform .18s, box-shadow .18s;
      border: 2px solid transparent;
    }
    .fw-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,.12) !important; }
    .fw-card.selected { border-color: var(--sel-color); box-shadow: 0 0 0 4px color-mix(in srgb, var(--sel-color) 15%, transparent); }

    .fw-icon { width:52px; height:52px; border-radius:14px; display:flex; align-items:center; justify-content:center; }

    .category-pill { border-radius:20px; font-size:.72rem; font-weight:700; padding:3px 10px; }

    .maturity-row { border-radius:8px; padding:8px 12px; margin-bottom:6px; }

    .domain-tag { border-radius:20px; font-size:.75rem; padding:3px 10px; border:1px solid; display:inline-block; margin:2px; }

    .criteria-list li { font-size:.8rem; color:#4b5563; padding:2px 0; }

    .detail-panel {
      position: sticky; top: 80px;
      border-radius:16px; max-height: calc(100vh - 120px); overflow-y:auto;
    }

    .sector-table th, .sector-table td { font-size:.78rem; vertical-align:middle; }
    .sector-table .check { font-size:1rem; }

    .filter-chip { border-radius:20px; padding:5px 16px; font-size:.82rem; cursor:pointer; transition: all .15s; }
    .filter-chip.active { font-weight:700; color:#fff; }

    ::-webkit-scrollbar { width:5px; }
    ::-webkit-scrollbar-thumb { background:#d1d5db; border-radius:10px; }
  `],
  template: `
    <div class="container-fluid py-4 px-4" style="max-width:1400px;margin:auto;">

      <!-- ── Header banner ── -->
      <div class="rounded-4 p-4 mb-4 text-white"
           style="background:linear-gradient(135deg,#1e1b4b 0%,#3730a3 50%,#0891b2 100%);">
        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
          <div>
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="bg-white bg-opacity-20 rounded-3 p-2">
                <i class="fas fa-brain fa-lg"></i>
              </div>
              <div>
                <h3 class="fw-bold mb-0">Référentiels de l'Agent IA</h3>
                <small class="opacity-75">Base de connaissance utilisée pour évaluer la maturité digitale des entreprises</small>
              </div>
            </div>
            <div class="d-flex gap-3 flex-wrap mt-3">
              <div class="bg-white bg-opacity-10 rounded-3 px-3 py-2 text-center">
                <div class="fw-bold fs-4">{{ frameworks.length }}</div>
                <div style="font-size:.75rem;opacity:.8;">Référentiels</div>
              </div>
              <div class="bg-white bg-opacity-10 rounded-3 px-3 py-2 text-center">
                <div class="fw-bold fs-4">{{ totalDomains }}</div>
                <div style="font-size:.75rem;opacity:.8;">Domaines d'évaluation</div>
              </div>
              <div class="bg-white bg-opacity-10 rounded-3 px-3 py-2 text-center">
                <div class="fw-bold fs-4">{{ totalCriteria }}</div>
                <div style="font-size:.75rem;opacity:.8;">Critères d'évaluation</div>
              </div>
              <div class="bg-white bg-opacity-10 rounded-3 px-3 py-2 text-center">
                <div class="fw-bold fs-4">{{ sectorMap.length }}</div>
                <div style="font-size:.75rem;opacity:.8;">Secteurs couverts</div>
              </div>
            </div>
          </div>
          <a routerLink="/consultant/dashboard" class="btn btn-light btn-sm rounded-pill px-3 align-self-start">
            <i class="fas fa-arrow-left me-1"></i>Dashboard
          </a>
        </div>
      </div>

      <!-- ── Filters + search ── -->
      <div class="d-flex align-items-center gap-2 mb-4 flex-wrap">
        <div class="input-group flex-grow-0" style="min-width:220px;max-width:280px;">
          <span class="input-group-text bg-white border-end-0">
            <i class="fas fa-search text-muted"></i>
          </span>
          <input type="text" class="form-control border-start-0 ps-0"
                 placeholder="Rechercher…"
                 [(ngModel)]="search">
        </div>
        <div class="d-flex gap-2 flex-wrap">
          <span *ngFor="let cat of categories"
                class="filter-chip"
                [class.active]="activeCategory === cat.value"
                [style.background]="activeCategory === cat.value ? cat.color : '#f3f4f6'"
                [style.color]="activeCategory === cat.value ? '#fff' : '#374151'"
                [style.border]="'2px solid ' + (activeCategory === cat.value ? cat.color : 'transparent')"
                (click)="activeCategory = cat.value">
            {{ cat.label }}
            <span class="ms-1 opacity-75">({{ countByCategory(cat.value) }})</span>
          </span>
        </div>
      </div>

      <!-- ── Main layout: grid + detail panel ── -->
      <div class="row g-0">

        <!-- Grid of framework cards -->
        <div [class]="selected ? 'col-lg-6 pe-lg-3' : 'col-12'">
          <div class="row g-3">
            <div *ngFor="let fw of filtered" [class]="selected ? 'col-12' : 'col-md-6 col-xl-4'">
              <div class="fw-card card border-0 shadow-sm h-100"
                   [class.selected]="selected?.key === fw.key"
                   [style.--sel-color]="fw.categoryColor"
                   (click)="select(fw)">
                <div class="card-body p-4">
                  <div class="d-flex align-items-start justify-content-between mb-3">
                    <div class="fw-icon text-white" [style.background]="fw.iconBg">
                      <i [class]="fw.icon"></i>
                    </div>
                    <span class="category-pill text-white" [style.background]="fw.categoryColor">
                      {{ fw.category }}
                    </span>
                  </div>
                  <div class="fw-bold mb-1">{{ fw.name }}</div>
                  <div class="small text-muted mb-3">
                    <i class="fas fa-building me-1 opacity-50"></i>{{ fw.authority }}
                  </div>
                  <p class="text-muted small mb-3" style="line-height:1.5;">{{ fw.focus }}</p>
                  <div class="d-flex gap-3 small text-muted border-top pt-3">
                    <span><i class="fas fa-layer-group me-1"></i>{{ fw.maturityLevels.length }} niveaux</span>
                    <span><i class="fas fa-th-list me-1"></i>{{ fw.domains.length }} domaines</span>
                    <span><i class="fas fa-check-circle me-1"></i>{{ countCriteria(fw) }} critères</span>
                  </div>
                </div>
                <div class="card-footer border-0 bg-transparent px-4 pb-3">
                  <button class="btn btn-sm w-100 rounded-pill"
                          [style.background]="selected?.key === fw.key ? fw.categoryColor : ''"
                          [style.color]="selected?.key === fw.key ? '#fff' : fw.categoryColor"
                          [style.border]="'1.5px solid ' + fw.categoryColor">
                    <i class="me-1" [class]="selected?.key === fw.key ? 'fas fa-times' : 'fas fa-eye'"></i>
                    {{ selected?.key === fw.key ? 'Fermer le détail' : 'Voir le détail' }}
                  </button>
                </div>
              </div>
            </div>

            <div *ngIf="filtered.length === 0" class="col-12 text-center py-5 text-muted">
              <i class="fas fa-search fa-2x mb-3 opacity-25"></i>
              <p>Aucun framework trouvé.</p>
            </div>
          </div>
        </div>

        <!-- Detail side panel -->
        <div *ngIf="selected" class="col-lg-6 ps-lg-1 mt-3 mt-lg-0">
          <div class="detail-panel card border-0 shadow">
            <!-- Panel header -->
            <div class="p-4 text-white rounded-top-4" [style.background]="selected.iconBg">
              <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-3">
                  <div class="bg-white bg-opacity-25 rounded-3 p-2">
                    <i [class]="selected.icon + ' fa-lg'"></i>
                  </div>
                  <div>
                    <div class="fw-bold fs-5">{{ selected.name }}</div>
                    <div class="opacity-75 small">{{ selected.authority }}</div>
                  </div>
                </div>
                <button class="btn btn-sm bg-white bg-opacity-20 text-white border-0 rounded-circle"
                        style="width:32px;height:32px;"
                        (click)="selected = null">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>

            <div class="card-body p-4">

              <!-- Focus -->
              <div class="rounded-3 p-3 mb-4" style="background:#f8fafc;border-left:4px solid"
                   [style.border-left-color]="selected.categoryColor">
                <div class="small fw-bold text-uppercase mb-1" [style.color]="selected.categoryColor"
                     style="letter-spacing:.06em;">Objectif du framework</div>
                <p class="mb-0 text-muted small">{{ selected.focus }}</p>
              </div>

              <!-- Maturity levels -->
              <div class="fw-bold mb-3 d-flex align-items-center gap-2">
                <i class="fas fa-layer-group" [style.color]="selected.categoryColor"></i>
                Niveaux de maturité
              </div>
              <div *ngFor="let lv of selected.maturityLevels; let i = index" class="maturity-row"
                   [style.background]="getMaturityRowBg(i, selected.maturityLevels.length)">
                <div class="d-flex align-items-start gap-3">
                  <div class="rounded-circle d-flex align-items-center justify-content-center fw-bold text-white flex-shrink-0"
                       style="width:28px;height:28px;font-size:.8rem;"
                       [style.background]="getMaturityColor(i, selected.maturityLevels.length)">
                    {{ lv.level }}
                  </div>
                  <div class="small text-muted" style="line-height:1.5;">{{ lv.desc }}</div>
                </div>
              </div>

              <!-- Domains -->
              <div class="fw-bold mt-4 mb-3 d-flex align-items-center gap-2">
                <i class="fas fa-th-list" [style.color]="selected.categoryColor"></i>
                Domaines & Critères d'évaluation
              </div>
              <div *ngFor="let domain of selected.domains; let di = index" class="mb-3">
                <div class="d-flex align-items-center gap-2 mb-2 cursor-pointer"
                     (click)="toggleDomain(di)" style="cursor:pointer;">
                  <div class="rounded-2 p-1" [style.background]="selected.categoryColor + '20'">
                    <i class="fas fa-folder-open fa-sm" [style.color]="selected.categoryColor"></i>
                  </div>
                  <span class="fw-semibold small">{{ domain.name }}</span>
                  <span class="badge rounded-pill ms-auto" [style.background]="selected.categoryColor + '20'"
                        [style.color]="selected.categoryColor">
                    {{ domain.criteria.length }} critères
                  </span>
                  <i class="fas fa-sm" [class]="openDomains.has(di) ? 'fa-chevron-up' : 'fa-chevron-down'"
                     [style.color]="selected.categoryColor"></i>
                </div>
                <ul *ngIf="openDomains.has(di)" class="criteria-list ps-4 mb-0 list-unstyled">
                  <li *ngFor="let c of domain.criteria" class="d-flex align-items-start gap-2 py-1">
                    <i class="fas fa-check-circle mt-1 flex-shrink-0" style="color:#9ca3af;font-size:.7rem;"></i>
                    {{ c }}
                  </li>
                </ul>
              </div>

            </div>
          </div>
        </div>
      </div>

      <!-- ── Sector applicability table ── -->
      <div class="card border-0 shadow-sm mt-5 rounded-4 overflow-hidden">
        <div class="card-header border-0 py-3 px-4"
             style="background:linear-gradient(90deg,#f8fafc,#fff);">
          <div class="fw-bold d-flex align-items-center gap-2">
            <i class="fas fa-th text-primary"></i>
            Applicabilité par secteur
          </div>
          <small class="text-muted">Les frameworks utilisés par l'IA pour chaque secteur d'activité</small>
        </div>
        <div class="table-responsive">
          <table class="table sector-table mb-0 align-middle">
            <thead style="background:#f8fafc;">
              <tr>
                <th class="ps-4 py-3" style="min-width:170px;">Secteur</th>
                <th *ngFor="let fw of frameworks" class="text-center py-3" style="min-width:90px;">
                  <div class="d-flex flex-column align-items-center gap-1">
                    <div class="rounded-2 p-1" [style.background]="fw.iconBg" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center;">
                      <i [class]="fw.icon" class="text-white" style="font-size:.7rem;"></i>
                    </div>
                    <span style="font-size:.68rem;line-height:1.2;max-width:80px;" class="text-center text-muted">
                      {{ fw.name.split(' ').slice(0,2).join(' ') }}
                    </span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let row of sectorMap; let odd = odd"
                  [style.background]="odd ? '#fafafa' : '#fff'">
                <td class="ps-4 py-2 fw-semibold small">
                  <span class="me-2">{{ row.icon }}</span>{{ row.sector }}
                </td>
                <td *ngFor="let fw of frameworks" class="text-center py-2">
                  <span *ngIf="row.frameworks.includes(fw.key)" class="check"
                        [style.color]="fw.categoryColor">✓</span>
                  <span *ngIf="!row.frameworks.includes(fw.key)" class="text-muted opacity-25">·</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  `
})
export class ConsultantFrameworksComponent implements OnInit {
  frameworks = FRAMEWORKS;
  sectorMap  = SECTOR_MAP;
  search = '';
  activeCategory = 'ALL';
  selected: Framework | null = null;
  openDomains = new Set<number>();

  categories = [
    { label: 'Tous',           value: 'ALL',            color: '#374151' },
    { label: 'Stratégie',      value: 'Stratégie',      color: '#6366f1' },
    { label: 'Processus',      value: 'Processus',      color: '#059669' },
    { label: 'Sécurité',       value: 'Sécurité',       color: '#dc2626' },
    { label: 'Gouvernance',    value: 'Gouvernance IT',  color: '#d97706' },
    { label: 'Innovation',     value: 'Innovation',     color: '#0891b2' },
    { label: 'Benchmarking',   value: 'Benchmarking',   color: '#7c3aed' },
    { label: 'Réglementaire',  value: 'Réglementaire',  color: '#b91c1c' },
    { label: 'Pratiques',      value: 'Pratiques',      color: '#0891b2' },
    { label: 'Technologies',   value: 'Technologies',   color: '#059669' }
  ];

  ngOnInit() {}

  get filtered(): Framework[] {
    return this.frameworks.filter(fw => {
      const matchSearch = !this.search ||
        fw.name.toLowerCase().includes(this.search.toLowerCase()) ||
        fw.authority.toLowerCase().includes(this.search.toLowerCase());
      const matchCat = this.activeCategory === 'ALL' || fw.category === this.activeCategory;
      return matchSearch && matchCat;
    });
  }

  get totalDomains(): number {
    return this.frameworks.reduce((s, fw) => s + fw.domains.length, 0);
  }

  get totalCriteria(): number {
    return this.frameworks.reduce((s, fw) => s + this.countCriteria(fw), 0);
  }

  countByCategory(cat: string): number {
    if (cat === 'ALL') return this.frameworks.length;
    return this.frameworks.filter(fw => fw.category === cat).length;
  }

  countCriteria(fw: Framework): number {
    return fw.domains.reduce((s, d) => s + d.criteria.length, 0);
  }

  select(fw: Framework) {
    if (this.selected?.key === fw.key) { this.selected = null; return; }
    this.selected = fw;
    this.openDomains.clear();
    // Open first domain by default
    this.openDomains.add(0);
  }

  toggleDomain(i: number) {
    this.openDomains.has(i) ? this.openDomains.delete(i) : this.openDomains.add(i);
  }

  getMaturityColor(i: number, total: number): string {
    const colors = ['#dc2626','#f97316','#eab308','#3b82f6','#059669','#6366f1'];
    return colors[Math.min(i, colors.length - 1)];
  }

  getMaturityRowBg(i: number, total: number): string {
    const alpha = Math.round((0.04 + i * 0.015) * 255).toString(16).padStart(2,'0');
    const colors = ['#dc2626','#f97316','#eab308','#3b82f6','#059669','#6366f1'];
    return colors[Math.min(i, colors.length - 1)] + '12';
  }
}
