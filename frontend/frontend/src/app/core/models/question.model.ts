/**
 * Modèle de données pour les questions du questionnaire
 * Basé sur le document de benchmark avec 15 catégories et sous-axes
 */

// ==================== INTERFACES PRINCIPALES ====================

/**
 * Interface représentant une question
 */
export interface Question {
  id?: number;
  content: string;
  axis: 'METIER' | 'PROCESSUS' | 'SI' | 'CANAUX_DISTRIBUTION' | 'MARKETING_COMMUNICATION' | 'RH_CULTURE_DIGITALE' | 'OFFRES_DIGITALES' | 'MODELE_OPERATIONNEL_INNOVATION' | 'IT_DATA';
  category: string;
  subAxis: string;
  subAxisLabel?: string;
  sector?: string;           // null pour tous les secteurs
  country?: string;          // null pour tous les pays
  order: number;
  isActive: boolean;
  weight?: number;           // Pondération optionnelle (défaut: 1)
  helpText?: string;         // Texte d'aide pour la question
  responseType?: 'BOOLEAN' | 'SCALE_1_5' | 'TEXT' | 'PERCENTAGE' | 'MULTIPLE_CHOICE';
  options?: string[];        // Options pour les choix multiples
  minValue?: number;         // Valeur minimale (pour échelle)
  maxValue?: number;         // Valeur maximale (pour échelle)
  step?: number;             // Pas d'incrémentation
  required: boolean;         // Question obligatoire ou non
  benchmark?: {              // Données de benchmark pour cette question
    sectorAverage?: number;
    topPerformer?: string;
    trend?: string;
  };
  createdAt?: Date;
  updatedAt?: Date;
}

/**
 * Interface représentant une réponse à une question
 */
export interface QuestionResponse {
  questionId: number;
  value: number | string | boolean | string[];
  comment?: string;
  confidence?: number;       // Niveau de confiance dans la réponse (1-5)
  attachments?: string[];    // Pièces jointes optionnelles
  respondedAt?: Date;
}

/**
 * Interface représentant une section du questionnaire (catégorie)
 */
export interface QuestionSection {
  category: string;
  categoryLabel: string;
  axis: string;
  icon?: string;
  description?: string;
  questions: Question[];
  progress: {
    answered: number;
    total: number;
    percentage: number;
    mandatoryAnswered: number;
    mandatoryTotal: number;
  };
  order: number;
  isActive: boolean;
}

/**
 * Interface représentant l'état complet du questionnaire
 */
export interface QuestionnaireState {
  evaluationId?: number;
  companyId: number;
  companyName: string;
  companySector?: string;
  companyCountry?: string;
  currentSection: number;
  sections: QuestionSection[];
  responses: { [key: number]: QuestionResponse };
  completed: boolean;
  startedAt: Date;
  completedAt?: Date;
  lastSavedAt?: Date;
  timeSpent?: number;        // Temps passé en secondes
  metadata?: {
    device?: string;
    browser?: string;
    ip?: string;
  };
}

// ==================== SOUS-AXES ====================

/**
 * Interface représentant un sous-axe d'évaluation
 */
export interface SubAxis {
  id: string;
  name: string;
  axis: 'METIER' | 'PROCESSUS' | 'SI' | 'CANAUX_DISTRIBUTION' | 'MARKETING_COMMUNICATION' | 'RH_CULTURE_DIGITALE' | 'OFFRES_DIGITALES' | 'MODELE_OPERATIONNEL_INNOVATION' | 'IT_DATA';
  category: string;
  description?: string;
  helpText?: string;
  weight?: number;           // Pondération dans le calcul du score
  examples?: string[];       // Exemples concrets
  benchmark?: {              // Données de benchmark
    sectorAverage?: number;
    topPerformer?: string;
    trend?: string;
  };
}

/**
 * Interface représentant une catégorie (axe principal)
 */
export interface Category {
  id: string;
  name: string;
  axis: 'METIER' | 'PROCESSUS' | 'SI' | 'CANAUX_DISTRIBUTION' | 'MARKETING_COMMUNICATION' | 'RH_CULTURE_DIGITALE' | 'OFFRES_DIGITALES' | 'MODELE_OPERATIONNEL_INNOVATION' | 'IT_DATA';
  description?: string;
  icon?: string;
  color?: string;
  order: number;
  isActive?: boolean;
  weight?: number;           // Pondération de la catégorie
}

// ==================== DONNÉES STATIQUES ====================

/**
 * Catégories avec icônes (basées sur le document de benchmark)
 */
export const CATEGORIES: Category[] = [
  // AXE METIER
  { 
    id: 'CANAUX', 
    name: 'Canaux de distribution & expérience client', 
    axis: 'METIER', 
    icon: '📱', 
    color: '#0d6efd',
    description: 'Évaluation des canaux de distribution et de l\'expérience client multicanal',
    order: 1,
    weight: 1.2
  },
  { 
    id: 'SELFCARE', 
    name: 'Selfcare client', 
    axis: 'METIER', 
    icon: '🤳', 
    color: '#0d6efd',
    description: 'Autonomie du client dans la gestion de ses services',
    order: 2,
    weight: 1.0
  },
  { 
    id: 'MARKETING', 
    name: 'Marketing & communication digitale', 
    axis: 'METIER', 
    icon: '📢', 
    color: '#0d6efd',
    description: 'Stratégie et outils de marketing digital',
    order: 3,
    weight: 0.9
  },
  { 
    id: 'OFFRES', 
    name: 'Offres digitales', 
    axis: 'METIER', 
    icon: '💳', 
    color: '#0d6efd',
    description: 'Développement d\'offres et services digitaux',
    order: 4,
    weight: 1.1
  },
  { 
    id: 'OPEN_BANKING', 
    name: 'Open banking', 
    axis: 'METIER', 
    icon: '🔓', 
    color: '#0d6efd',
    description: 'Ouverture des données et collaboration avec des tiers',
    order: 5,
    weight: 1.0
  },
  
  // AXE PROCESSUS
  { 
    id: 'AUTOMATISATION', 
    name: 'Simplification & automatisation des processus', 
    axis: 'PROCESSUS', 
    icon: '⚙️', 
    color: '#198754',
    description: 'Automatisation et optimisation des processus métier',
    order: 6,
    weight: 1.1
  },
  { 
    id: 'GOUVERNANCE', 
    name: 'Gouvernance de la transformation digitale', 
    axis: 'PROCESSUS', 
    icon: '📊', 
    color: '#198754',
    description: 'Pilotage et gouvernance de la transformation',
    order: 7,
    weight: 1.0
  },
  { 
    id: 'INNOVATION', 
    name: 'Développement de l\'innovation', 
    axis: 'PROCESSUS', 
    icon: '💡', 
    color: '#198754',
    description: 'Capacité d\'innovation et veille technologique',
    order: 8,
    weight: 0.9
  },
  { 
    id: 'CULTURE', 
    name: 'Culture digitale', 
    axis: 'PROCESSUS', 
    icon: '🌱', 
    color: '#198754',
    description: 'Acculturation et formation aux usages digitaux',
    order: 9,
    weight: 0.9
  },
  { 
    id: 'COLLABORATIF', 
    name: 'Collaboratif & digital working', 
    axis: 'PROCESSUS', 
    icon: '👥', 
    color: '#198754',
    description: 'Outils collaboratifs et nouvelles méthodes de travail',
    order: 10,
    weight: 0.8
  },
  { 
    id: 'RH', 
    name: 'Digitalisation de la fonction RH', 
    axis: 'PROCESSUS', 
    icon: '👔', 
    color: '#198754',
    description: 'Impact du digital sur les RH et les métiers',
    order: 11,
    weight: 0.8
  },
  { 
    id: 'AGILITE', 
    name: 'Agilité', 
    axis: 'PROCESSUS', 
    icon: '🔄', 
    color: '#198754',
    description: 'Méthodes agiles et organisation associée',
    order: 12,
    weight: 1.0
  },
  
  // AXE SI
  { 
    id: 'SOCLE_IT', 
    name: 'Socle IT', 
    axis: 'SI', 
    icon: '💻', 
    color: '#6f42c1',
    description: 'Infrastructure technique et architecture',
    order: 13,
    weight: 1.2
  },
  { 
    id: 'DATA', 
    name: 'Data', 
    axis: 'SI', 
    icon: '📊', 
    color: '#6f42c1',
    description: 'Gouvernance et exploitation des données',
    order: 14,
    weight: 1.1
  },
  {
    id: 'POSTE_TRAVAIL',
    name: 'Poste de travail du banquier',
    axis: 'SI',
    icon: '🖥️',
    color: '#6f42c1',
    description: 'Équipement et assistance technologique des collaborateurs',
    order: 15,
    weight: 0.9
  },

  // AXE MODELE_OPERATIONNEL_INNOVATION
  {
    id: 'MODELE_OPERATIONNEL',
    name: 'Modèle opérationnel & innovation',
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    icon: '🏭',
    color: '#f97316',
    description: 'Simplification des processus, gouvernance digitale et capacité d\'innovation',
    order: 16,
    weight: 1.1
  },

  // AXE IT_DATA
  {
    id: 'IT_DATA',
    name: 'IT & Data',
    axis: 'IT_DATA',
    icon: '🗄️',
    color: '#8b5cf6',
    description: 'Infrastructure IT, socle technique et exploitation des données',
    order: 17,
    weight: 1.2
  }
];

/**
 * Sous-axes détaillés (basés sur le document de benchmark)
 */
export const SUB_AXES: SubAxis[] = [
  // ========== METIER - CANAUX ==========
  { 
    id: 'canaux-digitaux', 
    name: 'Canaux digitaux (web/mobile)', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Évaluez la maturité de vos canaux web et mobile',
    weight: 1.0,
    examples: ['Application mobile', 'Site web responsive', 'Espace client']
  },
  { 
    id: 'canaux-physiques', 
    name: 'Canaux physiques', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Agences, points de vente, guichets',
    weight: 0.8
  },
  { 
    id: 'canaux-distants', 
    name: 'Canaux distants', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Téléphone, chat, email, visioconférence',
    weight: 0.8
  },
  { 
    id: 'omnicanalite', 
    name: 'Omnicanalité', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Cohérence et continuité entre les différents canaux',
    weight: 1.2,
    examples: ['Panier commun web/mobile', 'Historique unifié', 'Parcours fluide']
  },
  { 
    id: 'modele-relationnel', 
    name: 'Modèle relationnel', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Stratégie de relation client multicanal',
    weight: 1.0
  },
  { 
    id: 'tarification', 
    name: 'Tarification', 
    axis: 'METIER', 
    category: 'CANAUX',
    helpText: 'Modèles tarifaires selon les canaux',
    weight: 0.9
  },
  
  // ========== METIER - SELFCARE ==========
  { 
    id: 'fonctionnalites-selfcare', 
    name: 'Fonctionnalités selfcare', 
    axis: 'METIER', 
    category: 'SELFCARE',
    helpText: 'Développement des fonctionnalités en libre-service',
    weight: 1.0,
    examples: ['Consultation solde', 'Virements', 'Opposition carte']
  },
  { 
    id: 'pilotage-usage', 
    name: 'Pilotage de l\'usage', 
    axis: 'METIER', 
    category: 'SELFCARE',
    helpText: 'Analyse et optimisation de l\'utilisation des canaux selfcare',
    weight: 0.9
  },
  { 
    id: 'accompagnement-clients', 
    name: 'Accompagnement des clients', 
    axis: 'METIER', 
    category: 'SELFCARE',
    helpText: 'Support et assistance pour l\'utilisation des outils selfcare',
    weight: 0.9
  },
  
  // ========== METIER - MARKETING ==========
  { 
    id: 'communication-digitale', 
    name: 'Communication digitale', 
    axis: 'METIER', 
    category: 'MARKETING',
    helpText: 'Stratégie de communication sur les canaux digitaux',
    weight: 1.0,
    examples: ['Réseaux sociaux', 'Emailing', 'Publicité en ligne']
  },
  { 
    id: 'marketing-digital', 
    name: 'Marketing digital', 
    axis: 'METIER', 
    category: 'MARKETING',
    helpText: 'Outils et techniques de marketing en ligne',
    weight: 1.0,
    examples: ['SEO/SEA', 'Lead management', 'Marketing automation']
  },
  { 
    id: 'ecoute-client', 
    name: 'Dispositifs d\'écoute client', 
    axis: 'METIER', 
    category: 'MARKETING',
    helpText: 'Collecte et analyse des avis et retours clients',
    weight: 1.1
  },
  { 
    id: 'satisfaction-client', 
    name: 'Mesure de la satisfaction', 
    axis: 'METIER', 
    category: 'MARKETING',
    helpText: 'Outils de mesure de la satisfaction client (NPS, CSAT)',
    weight: 1.0
  },
  
  // ========== METIER - OFFRES DIGITALES ==========
  { 
    id: 'neo-banque', 
    name: 'Offres de type néo-banque', 
    axis: 'METIER', 
    category: 'OFFRES',
    helpText: 'Développement d\'offres 100% digitales',
    weight: 1.1
  },
  { 
    id: 'robot-advisor', 
    name: 'Services de conseil automatisés', 
    axis: 'METIER', 
    category: 'OFFRES',
    helpText: 'Robot-advisor, coach financier automatisé',
    weight: 1.0
  },
  { 
    id: 'coach-automatise', 
    name: 'Coach automatisé', 
    axis: 'METIER', 
    category: 'OFFRES',
    helpText: 'Services de conseil personnalisés automatisés',
    weight: 0.9
  },
  { 
    id: 'digitalisation-offres', 
    name: 'Digitalisation des offres', 
    axis: 'METIER', 
    category: 'OFFRES',
    helpText: 'Transformation digitale des offres existantes',
    weight: 1.0
  },
  
  // ========== METIER - OPEN BANKING ==========
  { 
    id: 'offres-segmentees', 
    name: 'Offres par segment', 
    axis: 'METIER', 
    category: 'OPEN_BANKING',
    helpText: 'Développement d\'offres spécifiques par segment de clientèle',
    weight: 1.0
  },
  { 
    id: 'moments-de-vie', 
    name: 'Accompagnement des moments de vie', 
    axis: 'METIER', 
    category: 'OPEN_BANKING',
    helpText: 'Services adaptés aux moments clés de la vie des clients',
    weight: 1.1
  },
  { 
    id: 'coach-extra-financier', 
    name: 'Coach extra-financier', 
    axis: 'METIER', 
    category: 'OPEN_BANKING',
    helpText: 'Services de conseil au-delà du financier',
    weight: 0.9
  },
  { 
    id: 'collaboration-fintechs', 
    name: 'Collaboration avec fintechs', 
    axis: 'METIER', 
    category: 'OPEN_BANKING',
    helpText: 'Partenariats et collaborations avec l\'écosystème fintech',
    weight: 1.0
  },
  { 
    id: 'monetisation-api', 
    name: 'Monétisation des données/APIs', 
    axis: 'METIER', 
    category: 'OPEN_BANKING',
    helpText: 'Valorisation économique des données et APIs',
    weight: 1.0
  },
  
  // ========== PROCESSUS - AUTOMATISATION ==========
  { 
    id: 'dematerialisation', 
    name: 'Dématérialisation', 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION',
    helpText: 'Suppression des supports papier au profit du numérique',
    weight: 1.0,
    examples: ['Signature électronique', 'Archivage numérique', 'Factures dématérialisées']
  },
  { 
    id: 'workflows', 
    name: 'Mise en place de workflows', 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION',
    helpText: 'Automatisation des circuits de validation et processus',
    weight: 1.0
  },
  { 
    id: 'automatisation-rpa-ia', 
    name: 'Automatisation par RPA et IA', 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION',
    helpText: 'Utilisation de robots et d\'IA pour automatiser les tâches',
    weight: 1.2,
    examples: ['RPA', 'Traitement automatique', 'IA générative']
  },
  
  // ========== PROCESSUS - GOUVERNANCE ==========
  { 
    id: 'strategie-digitale', 
    name: 'Stratégie et feuille de route digitale', 
    axis: 'PROCESSUS', 
    category: 'GOUVERNANCE',
    helpText: 'Définition d\'une vision et d\'un plan d\'action digital',
    weight: 1.1
  },
  { 
    id: 'budgets-pilotage', 
    name: 'Budgets et pilotage dédiés', 
    axis: 'PROCESSUS', 
    category: 'GOUVERNANCE',
    helpText: 'Allocation de ressources et suivi de la transformation',
    weight: 1.0
  },
  { 
    id: 'gouvernance-dediee', 
    name: 'Gouvernance dédiée', 
    axis: 'PROCESSUS', 
    category: 'GOUVERNANCE',
    helpText: 'Structure de gouvernance spécifique à la transformation digitale',
    weight: 1.0
  },
  
  // ========== PROCESSUS - INNOVATION ==========
  { 
    id: 'innovation-interne', 
    name: 'Innovation en interne', 
    axis: 'PROCESSUS', 
    category: 'INNOVATION',
    helpText: 'Labs, hackathons, programmes d\'innovation interne',
    weight: 1.0,
    examples: ['Labs', 'Hackathons', 'Programme intrapreneurial']
  },
  { 
    id: 'lien-fintechs', 
    name: 'Liens avec l\'écosystème fintech', 
    axis: 'PROCESSUS', 
    category: 'INNOVATION',
    helpText: 'Collaboration avec les startups et fintechs',
    weight: 1.0
  },
  { 
    id: 'veille-concurrentielle', 
    name: 'Veille concurrentielle', 
    axis: 'PROCESSUS', 
    category: 'INNOVATION',
    helpText: 'Analyse des innovations concurrentes et tendances',
    weight: 0.9
  },
  
  // ========== PROCESSUS - CULTURE DIGITALE ==========
  { 
    id: 'acculturation-digitale', 
    name: 'Acculturation digitale', 
    axis: 'PROCESSUS', 
    category: 'CULTURE',
    helpText: 'Sensibilisation et adoption de la culture digitale',
    weight: 1.0
  },
  { 
    id: 'formation-usages', 
    name: 'Formation aux nouveaux usages', 
    axis: 'PROCESSUS', 
    category: 'CULTURE',
    helpText: 'Programmes de formation aux outils et usages digitaux',
    weight: 1.0
  },
  { 
    id: 'accompagnement-postures', 
    name: 'Accompagnement des nouvelles postures', 
    axis: 'PROCESSUS', 
    category: 'CULTURE',
    helpText: 'Accompagnement au changement et évolution des métiers',
    weight: 0.9
  },
  
  // ========== PROCESSUS - COLLABORATIF ==========
  { 
    id: 'outils-collaboratifs', 
    name: 'Outils collaboratifs', 
    axis: 'PROCESSUS', 
    category: 'COLLABORATIF',
    helpText: 'Déploiement d\'outils de travail collaboratif',
    weight: 1.0,
    examples: ['Teams', 'Slack', 'SharePoint', 'Notion']
  },
  { 
    id: 'teletravail', 
    name: 'Télétravail', 
    axis: 'PROCESSUS', 
    category: 'COLLABORATIF',
    helpText: 'Politique et outils pour le travail à distance',
    weight: 0.9
  },
  
  // ========== PROCESSUS - RH ==========
  { 
    id: 'digitalisation-rh', 
    name: 'Digitalisation de la fonction RH', 
    axis: 'PROCESSUS', 
    category: 'RH',
    helpText: 'Outils digitaux pour la gestion des RH',
    weight: 0.9,
    examples: ['SIRH', 'E-learning', 'Recrutement digital']
  },
  { 
    id: 'impact-metiers', 
    name: 'Impact du digital sur les métiers', 
    axis: 'PROCESSUS', 
    category: 'RH',
    helpText: 'Analyse et adaptation des métiers à la transformation digitale',
    weight: 0.9
  },
  
  // ========== PROCESSUS - AGILITE ==========
  { 
    id: 'methodes-agiles', 
    name: 'Méthodes agiles', 
    axis: 'PROCESSUS', 
    category: 'AGILITE',
    helpText: 'Déploiement de méthodes agiles (Scrum, Kanban)',
    weight: 1.1,
    examples: ['Scrum', 'Kanban', 'SAFe']
  },
  { 
    id: 'organisations-associees', 
    name: 'Organisations associées', 
    axis: 'PROCESSUS', 
    category: 'AGILITE',
    helpText: 'Structures organisationnelles adaptées à l\'agilité',
    weight: 1.0
  },
  { 
    id: 'digitale-factory', 
    name: 'Digitale factory (UX & co)', 
    axis: 'PROCESSUS', 
    category: 'AGILITE',
    helpText: 'Mise en place d\'une factory digitale avec approche UX',
    weight: 1.0
  },
  
  // ========== SI - SOCLE IT ==========
  { 
    id: 'cloud', 
    name: 'Cloud (privé/public, IaaS/PaaS/SaaS)', 
    axis: 'SI', 
    category: 'SOCLE_IT',
    helpText: 'Adoption du cloud computing',
    weight: 1.2,
    examples: ['AWS', 'Azure', 'GCP', 'Cloud privé']
  },
  { 
    id: 'architecture-modulaire', 
    name: 'Architecture modulaire (micro-services)', 
    axis: 'SI', 
    category: 'SOCLE_IT',
    helpText: 'Architecture orientée services et micro-services',
    weight: 1.1
  },
  { 
    id: 'couche-api', 
    name: 'Couche API', 
    axis: 'SI', 
    category: 'SOCLE_IT',
    helpText: 'Exposition et consommation d\'APIs',
    weight: 1.0,
    examples: ['API Management', 'API Gateway']
  },
  { 
    id: 'cybersecurite', 
    name: 'Cybersécurité', 
    axis: 'SI', 
    category: 'SOCLE_IT',
    helpText: 'Politique et outils de sécurité informatique',
    weight: 1.2
  },
  { 
    id: 'nouvelles-technologies', 
    name: 'Investissement dans les nouvelles technologies', 
    axis: 'SI', 
    category: 'SOCLE_IT',
    helpText: 'Veille et adoption de technologies émergentes (IA, IoT, Blockchain)',
    weight: 1.0
  },
  
  // ========== SI - DATA ==========
  { 
    id: 'acquisition-donnees', 
    name: 'Acquisition de données', 
    axis: 'SI', 
    category: 'DATA',
    helpText: 'Collecte de données internes et externes',
    weight: 1.0
  },
  { 
    id: 'mise-qualite', 
    name: 'Mise en qualité des données', 
    axis: 'SI', 
    category: 'DATA',
    helpText: 'Processus de nettoyage et validation des données',
    weight: 1.1
  },
  { 
    id: 'accessibilite-exploitation', 
    name: 'Accessibilité et exploitation des données', 
    axis: 'SI', 
    category: 'DATA',
    helpText: 'Outils et processus pour l\'exploitation des données',
    weight: 1.0
  },
  { 
    id: 'gouvernance-donnee', 
    name: 'Gouvernance de la donnée', 
    axis: 'SI', 
    category: 'DATA',
    helpText: 'Politique et organisation de la gouvernance des données',
    weight: 1.1
  },
  { 
    id: 'equipe-dediee', 
    name: 'Équipe dédiée à la data', 
    axis: 'SI', 
    category: 'DATA',
    helpText: 'Mise en place d\'une équipe data (Data Office, CDO)',
    weight: 1.0
  },
  
  // ========== SI - POSTE DE TRAVAIL ==========
  {
    id: 'assistance-conseiller',
    name: 'Assistance du conseiller par la technologie',
    axis: 'SI',
    category: 'POSTE_TRAVAIL',
    helpText: 'Outils d\'aide à la relation client pour les conseillers',
    weight: 1.0,
    examples: ['CRM', 'Knowledge base', 'Salesforce']
  },

  // ========== MODELE_OPERATIONNEL_INNOVATION ==========
  {
    id: 'simplification-processus',
    name: 'Simplification & automatisation des processus',
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    helpText: 'Pipelines automatisés, 0 ressaisie, workflows digitaux',
    weight: 1.1,
    examples: ['n8n', 'Make', 'Power Automate', 'ODK → ERP']
  },
  {
    id: 'gouvernance-mod-op',
    name: 'Gouvernance digitale & conformité',
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    helpText: 'Comité de pilotage, PRA/PCA, conformité réglementaire',
    weight: 1.0,
    examples: ['RGPD / APDP CI', 'PRA testé annuellement', 'Budget digital 2-3% CA']
  },
  {
    id: 'innovation-mod-op',
    name: 'Innovation digitale & R&D',
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    helpText: 'Partenariats R&D, IoT, IA sectorielle, veille technologique',
    weight: 1.0,
    examples: ['IoT capteurs', 'IA prédictive', 'FIRCA / subventions']
  },

  // ========== IT_DATA ==========
  {
    id: 'socle-it',
    name: 'Socle IT & infrastructure',
    axis: 'IT_DATA',
    category: 'IT_DATA',
    helpText: 'Disponibilité, redondance, connectivité, alimentation de secours',
    weight: 1.2,
    examples: ['UPS', 'Dual-SIM 4G', 'Cloud hybride', 'Monitoring UptimeRobot']
  },
  {
    id: 'data-analytics',
    name: 'Data & analytics',
    axis: 'IT_DATA',
    category: 'IT_DATA',
    helpText: 'Collecte, qualité, exploitation et gouvernance des données',
    weight: 1.1,
    examples: ['Lac de données', 'ML prévisionnel', 'Dashboard temps réel', 'NDVI / API']
  }
];

// ==================== QUESTIONS PRÉDÉFINIES ====================

/**
 * Questions prédéfinies par catégorie
 */
export const DEFAULT_QUESTIONS: Partial<Question>[] = [
  // ========== CANAUX ==========
  { 
    content: "L'entreprise propose-t-elle une application mobile ?", 
    axis: 'METIER', 
    category: 'CANAUX', 
    subAxis: 'canaux-digitaux', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true,
    helpText: "L'application mobile permet-elle d'accéder aux principaux services ?",
    weight: 1.0
  },
  { 
    content: "Les clients peuvent-ils effectuer des opérations courantes en ligne ?", 
    axis: 'METIER', 
    category: 'CANAUX', 
    subAxis: 'canaux-digitaux', 
    order: 2, 
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Évaluez la complétude des opérations disponibles en ligne",
    weight: 1.0,
    minValue: 1,
    maxValue: 5
  },
  { 
    content: "Existe-t-il une stratégie omnicanale formalisée ?", 
    axis: 'METIER', 
    category: 'CANAUX', 
    subAxis: 'omnicanalite', 
    order: 3, 
    responseType: 'BOOLEAN',
    required: true,
    helpText: "La stratégie assure-t-elle une continuité entre les canaux ?",
    weight: 1.2
  },
  { 
    content: "Quel est le niveau de satisfaction client sur les canaux digitaux ?", 
    axis: 'METIER', 
    category: 'CANAUX', 
    subAxis: 'modele-relationnel', 
    order: 4, 
    responseType: 'PERCENTAGE',
    required: false,
    helpText: "Basé sur les enquêtes de satisfaction NPS/CSAT",
    weight: 1.0,
    minValue: 0,
    maxValue: 100,
    step: 5
  },
  { 
    content: "Les canaux physiques et digitaux sont-ils intégrés ?", 
    axis: 'METIER', 
    category: 'CANAUX', 
    subAxis: 'omnicanalite', 
    order: 5, 
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Les informations sont-elles partagées entre les canaux ?",
    weight: 1.1
  },
  
  // ========== SELFCARE ==========
  { 
    content: "Les clients peuvent-ils gérer leurs informations personnelles en ligne ?", 
    axis: 'METIER', 
    category: 'SELFCARE', 
    subAxis: 'fonctionnalites-selfcare', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Existe-t-il un espace client avec des fonctionnalités avancées ?", 
    axis: 'METIER', 
    category: 'SELFCARE', 
    subAxis: 'fonctionnalites-selfcare', 
    order: 2, 
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Historique, chat, personnalisation, etc."
  },
  { 
    content: "Les taux d'utilisation des fonctionnalités selfcare sont-ils suivis ?", 
    axis: 'METIER', 
    category: 'SELFCARE', 
    subAxis: 'pilotage-usage', 
    order: 3, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== MARKETING ==========
  { 
    content: "L'entreprise est-elle active sur les réseaux sociaux ?", 
    axis: 'METIER', 
    category: 'MARKETING', 
    subAxis: 'communication-digitale', 
    order: 1, 
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Fréquence de publication, engagement, communautés"
  },
  { 
    content: "Existe-t-il une stratégie de marketing digital formalisée ?", 
    axis: 'METIER', 
    category: 'MARKETING', 
    subAxis: 'marketing-digital', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Des outils de mesure de la satisfaction client sont-ils déployés ?", 
    axis: 'METIER', 
    category: 'MARKETING', 
    subAxis: 'satisfaction-client', 
    order: 3, 
    responseType: 'BOOLEAN',
    required: true
  },
  
  // ========== OFFRES DIGITALES ==========
  { 
    content: "L'entreprise propose-t-elle des offres 100% digitales ?", 
    axis: 'METIER', 
    category: 'OFFRES', 
    subAxis: 'neo-banque', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Des services de conseil automatisés sont-ils disponibles ?", 
    axis: 'METIER', 
    category: 'OFFRES', 
    subAxis: 'robot-advisor', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== OPEN BANKING ==========
  { 
    content: "L'entreprise expose-t-elle des APIs à des partenaires ?", 
    axis: 'METIER', 
    category: 'OPEN_BANKING', 
    subAxis: 'monetisation-api', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Existe-t-il des partenariats avec des fintechs ?", 
    axis: 'METIER', 
    category: 'OPEN_BANKING', 
    subAxis: 'collaboration-fintechs', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== AUTOMATISATION ==========
  { 
    content: "Les processus sont-ils dématérialisés ?", 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION', 
    subAxis: 'dematerialisation', 
    order: 1, 
    responseType: 'SCALE_1_5',
    required: true
  },
  { 
    content: "Utilisez-vous des outils RPA pour automatiser les tâches ?", 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION', 
    subAxis: 'automatisation-rpa-ia', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  { 
    content: "Des workflows automatisés sont-ils en place ?", 
    axis: 'PROCESSUS', 
    category: 'AUTOMATISATION', 
    subAxis: 'workflows', 
    order: 3, 
    responseType: 'SCALE_1_5',
    required: true
  },
  
  // ========== GOUVERNANCE ==========
  { 
    content: "Une stratégie digitale formalisée existe-t-elle ?", 
    axis: 'PROCESSUS', 
    category: 'GOUVERNANCE', 
    subAxis: 'strategie-digitale', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Des budgets spécifiques sont-ils alloués à la transformation digitale ?", 
    axis: 'PROCESSUS', 
    category: 'GOUVERNANCE', 
    subAxis: 'budgets-pilotage', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: true
  },
  
  // ========== INNOVATION ==========
  { 
    content: "Existe-t-il des initiatives d'innovation interne (labs, hackathons) ?", 
    axis: 'PROCESSUS', 
    category: 'INNOVATION', 
    subAxis: 'innovation-interne', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: false
  },
  { 
    content: "Une veille concurrentielle est-elle organisée ?", 
    axis: 'PROCESSUS', 
    category: 'INNOVATION', 
    subAxis: 'veille-concurrentielle', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: true
  },
  
  // ========== CULTURE DIGITALE ==========
  { 
    content: "Des programmes d'acculturation digitale existent-ils ?", 
    axis: 'PROCESSUS', 
    category: 'CULTURE', 
    subAxis: 'acculturation-digitale', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: false
  },
  { 
    content: "Les collaborateurs sont-ils formés aux nouveaux usages digitaux ?", 
    axis: 'PROCESSUS', 
    category: 'CULTURE', 
    subAxis: 'formation-usages', 
    order: 2, 
    responseType: 'SCALE_1_5',
    required: true
  },
  
  // ========== COLLABORATIF ==========
  { 
    content: "Des outils collaboratifs sont-ils déployés (Teams, Slack, etc.) ?", 
    axis: 'PROCESSUS', 
    category: 'COLLABORATIF', 
    subAxis: 'outils-collaboratifs', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Le télétravail est-il encouragé et outillé ?", 
    axis: 'PROCESSUS', 
    category: 'COLLABORATIF', 
    subAxis: 'teletravail', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== RH ==========
  { 
    content: "La fonction RH dispose-t-elle d'outils digitaux (SIRH) ?", 
    axis: 'PROCESSUS', 
    category: 'RH', 
    subAxis: 'digitalisation-rh', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "L'impact du digital sur les métiers est-il évalué ?", 
    axis: 'PROCESSUS', 
    category: 'RH', 
    subAxis: 'impact-metiers', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== AGILITE ==========
  { 
    content: "Les équipes travaillent-elles en mode agile ?", 
    axis: 'PROCESSUS', 
    category: 'AGILITE', 
    subAxis: 'methodes-agiles', 
    order: 1, 
    responseType: 'SCALE_1_5',
    required: true
  },
  { 
    content: "Une digitale factory (UX) est-elle en place ?", 
    axis: 'PROCESSUS', 
    category: 'AGILITE', 
    subAxis: 'digitale-factory', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== SOCLE IT ==========
  { 
    content: "L'infrastructure utilise-t-elle le cloud ?", 
    axis: 'SI', 
    category: 'SOCLE_IT', 
    subAxis: 'cloud', 
    order: 1, 
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Évaluez le niveau d'adoption du cloud (privé/public/hybride)"
  },
  { 
    content: "Exposez-vous des APIs à des partenaires ?", 
    axis: 'SI', 
    category: 'SOCLE_IT', 
    subAxis: 'couche-api', 
    order: 2, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Une politique de cybersécurité formalisée existe-t-elle ?", 
    axis: 'SI', 
    category: 'SOCLE_IT', 
    subAxis: 'cybersecurite', 
    order: 3, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Investissez-vous dans les nouvelles technologies (IA, IoT) ?", 
    axis: 'SI', 
    category: 'SOCLE_IT', 
    subAxis: 'nouvelles-technologies', 
    order: 4, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== DATA ==========
  { 
    content: "Existe-t-il une gouvernance des données ?", 
    axis: 'SI', 
    category: 'DATA', 
    subAxis: 'gouvernance-donnee', 
    order: 1, 
    responseType: 'BOOLEAN',
    required: true
  },
  { 
    content: "Les données sont-elles accessibles pour l'analyse ?", 
    axis: 'SI', 
    category: 'DATA', 
    subAxis: 'accessibilite-exploitation', 
    order: 2, 
    responseType: 'SCALE_1_5',
    required: true
  },
  { 
    content: "Une équipe dédiée à la data existe-t-elle ?", 
    axis: 'SI', 
    category: 'DATA', 
    subAxis: 'equipe-dediee', 
    order: 3, 
    responseType: 'BOOLEAN',
    required: false
  },
  
  // ========== POSTE DE TRAVAIL ==========
  {
    content: "Les conseillers disposent-ils d'outils d'aide à la relation client ?",
    axis: 'SI',
    category: 'POSTE_TRAVAIL',
    subAxis: 'assistance-conseiller',
    order: 1,
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "CRM, knowledge base, outils de suggestion"
  },

  // ========== MODELE_OPERATIONNEL_INNOVATION ==========
  {
    content: "Les processus métier clés sont-ils automatisés de bout en bout (0 ressaisie manuelle) ?",
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    subAxis: 'simplification-processus',
    order: 1,
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Évaluez le niveau d'automatisation des processus opérationnels",
    weight: 1.1
  },
  {
    content: "Une politique de gouvernance digitale et de conformité réglementaire est-elle formalisée ?",
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    subAxis: 'gouvernance-mod-op',
    order: 2,
    responseType: 'BOOLEAN',
    required: true,
    helpText: "PRA testé, conformité RGPD/APDP, comité de pilotage actif",
    weight: 1.0
  },
  {
    content: "Des initiatives d'innovation digitale (IoT, IA, R&D) sont-elles engagées ?",
    axis: 'MODELE_OPERATIONNEL_INNOVATION',
    category: 'MODELE_OPERATIONNEL',
    subAxis: 'innovation-mod-op',
    order: 3,
    responseType: 'BOOLEAN',
    required: false,
    helpText: "Partenariats R&D, pilotes IoT, IA prédictive, brevets",
    weight: 1.0
  },

  // ========== IT_DATA ==========
  {
    content: "L'infrastructure IT est-elle fiable, redondante et disponible en permanence ?",
    axis: 'IT_DATA',
    category: 'IT_DATA',
    subAxis: 'socle-it',
    order: 1,
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Alimentation secourue, connectivité multi-opérateurs, monitoring",
    weight: 1.2
  },
  {
    content: "Des outils d'analyse de données et d'aide à la décision sont-ils déployés ?",
    axis: 'IT_DATA',
    category: 'IT_DATA',
    subAxis: 'data-analytics',
    order: 2,
    responseType: 'SCALE_1_5',
    required: true,
    helpText: "Tableaux de bord, ML prédictif, lac de données, analytique en temps réel",
    weight: 1.1
  },
  {
    content: "Une stratégie de gouvernance des données est-elle définie et appliquée ?",
    axis: 'IT_DATA',
    category: 'IT_DATA',
    subAxis: 'data-analytics',
    order: 3,
    responseType: 'BOOLEAN',
    required: true,
    helpText: "Politique de qualité, de sécurité et de valorisation des données",
    weight: 1.0
  }
];

// ==================== FONCTIONS UTILITAIRES ====================

/**
 * Récupère les sous-axes par catégorie
 */
export function getSubAxesByCategory(category: string): SubAxis[] {
  return SUB_AXES.filter(subAxis => subAxis.category === category);
}

/**
 * Récupère les sous-axes par axe
 */
export function getSubAxesByAxis(axis: string): SubAxis[] {
  return SUB_AXES.filter(subAxis => subAxis.axis === axis);
}

/**
 * Récupère les sous-axes par ID
 */
export function getSubAxisById(id: string): SubAxis | undefined {
  return SUB_AXES.find(subAxis => subAxis.id === id);
}

/**
 * Récupère les catégories par axe
 */
export function getCategoriesByAxis(axis: string): Category[] {
  return CATEGORIES.filter(cat => cat.axis === axis);
}

/**
 * Récupère une catégorie par ID
 */
export function getCategoryById(id: string): Category | undefined {
  return CATEGORIES.find(cat => cat.id === id);
}

/**
 * Calcule le nombre total de questions
 */
export function getTotalQuestions(): number {
  return DEFAULT_QUESTIONS.length;
}

/**
 * Récupère les questions par catégorie
 */
export function getQuestionsByCategory(category: string): Partial<Question>[] {
  return DEFAULT_QUESTIONS.filter(q => q.category === category);
}

/**
 * Génère un libellé de sous-axe à partir de son ID
 */
export function getSubAxisLabel(subAxisId: string): string {
  const subAxis = getSubAxisById(subAxisId);
  return subAxis?.name || subAxisId;
}

/**
 * Vérifie si un sous-axe existe
 */
export function subAxisExists(subAxisId: string): boolean {
  return SUB_AXES.some(sub => sub.id === subAxisId);
}

/**
 * Récupère la progression par défaut pour une section
 */
export function getDefaultSectionProgress(total: number): { answered: number; total: number; percentage: number } {
  return {
    answered: 0,
    total,
    percentage: 0
  };
}