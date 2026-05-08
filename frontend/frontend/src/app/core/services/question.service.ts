import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Question, SubAxis, SUB_AXES, CATEGORIES } from '../models/question.model';

@Injectable({
  providedIn: 'root'
})
export class QuestionService {
  
  private questions: Question[] = [
    // ========== METIER - CANAUX ==========
    {
      id: 1,
      content: "L'entreprise propose-t-elle une application mobile ?",
      axis: 'METIER',
      subAxis: 'canaux-digitaux',
      category: 'CANAUX',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN',
      helpText: "L'application mobile permet-elle d'accéder aux principaux services ?"
    },
    {
      id: 2,
      content: 'Les clients peuvent-ils effectuer des opérations courantes en ligne ?',
      axis: 'METIER',
      subAxis: 'canaux-digitaux',
      category: 'CANAUX',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5',
      helpText: "Évaluez la complétude des opérations disponibles en ligne"
    },
    {
      id: 3,
      content: 'Existe-t-il une stratégie omnicanale formalisée ?',
      axis: 'METIER',
      subAxis: 'omnicanalite',
      category: 'CANAUX',
      sector: 'banking',
      order: 3,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 4,
      content: 'Quel est le niveau de satisfaction client sur les canaux digitaux ?',
      axis: 'METIER',
      subAxis: 'modele-relationnel',
      category: 'CANAUX',
      order: 4,
      isActive: true,
      required: false,
      responseType: 'PERCENTAGE'
    },
    {
      id: 5,
      content: 'Les canaux physiques et digitaux sont-ils intégrés ?',
      axis: 'METIER',
      subAxis: 'omnicanalite',
      category: 'CANAUX',
      order: 5,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    
    // ========== METIER - SELFCARE ==========
    {
      id: 6,
      content: 'Les clients peuvent-ils gérer leurs informations personnelles en ligne ?',
      axis: 'METIER',
      subAxis: 'fonctionnalites-selfcare',
      category: 'SELFCARE',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 7,
      content: 'Existe-t-il un espace client avec des fonctionnalités avancées ?',
      axis: 'METIER',
      subAxis: 'fonctionnalites-selfcare',
      category: 'SELFCARE',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    {
      id: 8,
      content: "Les taux d'utilisation des fonctionnalités selfcare sont-ils suivis ?",
      axis: 'METIER',
      subAxis: 'pilotage-usage',
      category: 'SELFCARE',
      order: 3,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== METIER - MARKETING ==========
    {
      id: 9,
      content: "L'entreprise est-elle active sur les réseaux sociaux ?",
      axis: 'METIER',
      subAxis: 'communication-digitale',
      category: 'MARKETING',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    {
      id: 10,
      content: 'Existe-t-il une stratégie de marketing digital formalisée ?',
      axis: 'METIER',
      subAxis: 'marketing-digital',
      category: 'MARKETING',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 11,
      content: 'Des outils de mesure de la satisfaction client sont-ils déployés ?',
      axis: 'METIER',
      subAxis: 'satisfaction-client',
      category: 'MARKETING',
      order: 3,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    
    // ========== METIER - OFFRES DIGITALES ==========
    {
      id: 12,
      content: "L'entreprise propose-t-elle des offres 100% digitales ?",
      axis: 'METIER',
      subAxis: 'neo-banque',
      category: 'OFFRES',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 13,
      content: 'Des services de conseil automatisés sont-ils disponibles ?',
      axis: 'METIER',
      subAxis: 'robot-advisor',
      category: 'OFFRES',
      order: 2,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== METIER - OPEN BANKING ==========
    {
      id: 14,
      content: "L'entreprise expose-t-elle des APIs à des partenaires ?",
      axis: 'METIER',
      subAxis: 'monetisation-api',
      category: 'OPEN_BANKING',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 15,
      content: 'Existe-t-il des partenariats avec des fintechs ?',
      axis: 'METIER',
      subAxis: 'collaboration-fintechs',
      category: 'OPEN_BANKING',
      order: 2,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== PROCESSUS - AUTOMATISATION ==========
    {
      id: 16,
      content: 'Les processus sont-ils dématérialisés ?',
      axis: 'PROCESSUS',
      subAxis: 'dematerialisation',
      category: 'AUTOMATISATION',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    {
      id: 17,
      content: "Utilisez-vous des outils RPA pour automatiser les tâches ?",
      axis: 'PROCESSUS',
      subAxis: 'automatisation-rpa-ia',
      category: 'AUTOMATISATION',
      order: 2,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    {
      id: 18,
      content: 'Des workflows automatisés sont-ils en place ?',
      axis: 'PROCESSUS',
      subAxis: 'workflows',
      category: 'AUTOMATISATION',
      order: 3,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    
    // ========== PROCESSUS - GOUVERNANCE ==========
    {
      id: 19,
      content: 'Une stratégie digitale formalisée existe-t-elle ?',
      axis: 'PROCESSUS',
      subAxis: 'strategie-digitale',
      category: 'GOUVERNANCE',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 20,
      content: 'Des budgets spécifiques sont-ils alloués à la transformation digitale ?',
      axis: 'PROCESSUS',
      subAxis: 'budgets-pilotage',
      category: 'GOUVERNANCE',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    
    // ========== PROCESSUS - INNOVATION ==========
    {
      id: 21,
      content: "Existe-t-il des initiatives d'innovation interne (labs, hackathons) ?",
      axis: 'PROCESSUS',
      subAxis: 'innovation-interne',
      category: 'INNOVATION',
      order: 1,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    {
      id: 22,
      content: 'Une veille concurrentielle est-elle organisée ?',
      axis: 'PROCESSUS',
      subAxis: 'veille-concurrentielle',
      category: 'INNOVATION',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    
    // ========== PROCESSUS - CULTURE DIGITALE ==========
    {
      id: 23,
      content: "Des programmes d'acculturation digitale existent-ils ?",
      axis: 'PROCESSUS',
      subAxis: 'acculturation-digitale',
      category: 'CULTURE',
      order: 1,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    {
      id: 24,
      content: 'Les collaborateurs sont-ils formés aux nouveaux usages digitaux ?',
      axis: 'PROCESSUS',
      subAxis: 'formation-usages',
      category: 'CULTURE',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    
    // ========== PROCESSUS - COLLABORATIF ==========
    {
      id: 25,
      content: 'Des outils collaboratifs sont-ils déployés (Teams, Slack, etc.) ?',
      axis: 'PROCESSUS',
      subAxis: 'outils-collaboratifs',
      category: 'COLLABORATIF',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 26,
      content: 'Le télétravail est-il encouragé et outillé ?',
      axis: 'PROCESSUS',
      subAxis: 'teletravail',
      category: 'COLLABORATIF',
      order: 2,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== PROCESSUS - AGILITE ==========
    {
      id: 27,
      content: 'Les équipes travaillent-elles en mode agile ?',
      axis: 'PROCESSUS',
      subAxis: 'methodes-agiles',
      category: 'AGILITE',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    {
      id: 28,
      content: 'Une digitale factory (UX) est-elle en place ?',
      axis: 'PROCESSUS',
      subAxis: 'digitale-factory',
      category: 'AGILITE',
      order: 2,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== SI - SOCLE IT ==========
    {
      id: 29,
      content: "L'infrastructure utilise-t-elle le cloud ?",
      axis: 'SI',
      subAxis: 'cloud',
      category: 'SOCLE_IT',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5',
      helpText: "Évaluez le niveau d'adoption du cloud (privé/public/hybride)"
    },
    {
      id: 30,
      content: 'Exposez-vous des APIs à des partenaires ?',
      axis: 'SI',
      subAxis: 'couche-api',
      category: 'SOCLE_IT',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 31,
      content: 'Une politique de cybersécurité formalisée existe-t-elle ?',
      axis: 'SI',
      subAxis: 'cybersecurite',
      category: 'SOCLE_IT',
      order: 3,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 32,
      content: 'Investissez-vous dans les nouvelles technologies (IA, IoT) ?',
      axis: 'SI',
      subAxis: 'nouvelles-technologies',
      category: 'SOCLE_IT',
      order: 4,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== SI - DATA ==========
    {
      id: 33,
      content: 'Existe-t-il une gouvernance des données ?',
      axis: 'SI',
      subAxis: 'gouvernance-donnee',
      category: 'DATA',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'BOOLEAN'
    },
    {
      id: 34,
      content: "Les données sont-elles accessibles pour l'analyse ?",
      axis: 'SI',
      subAxis: 'accessibilite-exploitation',
      category: 'DATA',
      order: 2,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5'
    },
    {
      id: 35,
      content: 'Une équipe dédiée à la data existe-t-elle ?',
      axis: 'SI',
      subAxis: 'equipe-dediee',
      category: 'DATA',
      order: 3,
      isActive: true,
      required: false,
      responseType: 'BOOLEAN'
    },
    
    // ========== SI - POSTE DE TRAVAIL ==========
    {
      id: 36,
      content: "Les conseillers disposent-ils d'outils d'aide à la relation client ?",
      axis: 'SI',
      subAxis: 'assistance-conseiller',
      category: 'POSTE_TRAVAIL',
      order: 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5',
      helpText: "CRM, knowledge base, outils de suggestion"
    }
  ];

  private subAxes: SubAxis[] = SUB_AXES;

  constructor() {}

  getQuestions(): Observable<Question[]> {
    return of(this.questions);
  }

  getQuestionsByAxis(axis: string): Observable<Question[]> {
    const filtered = this.questions.filter(q => q.axis === axis && q.isActive);
    return of(filtered);
  }

  getQuestionsForCompany(sector?: string, country?: string): Observable<Question[]> {
    const filtered = this.questions.filter(q => 
      q.isActive && 
      (!q.sector || q.sector === sector) &&
      (!q.country || q.country === country)
    );
    return of(filtered);
  }

  getQuestion(id: number): Observable<Question | undefined> {
    const question = this.questions.find(q => q.id === id);
    return of(question);
  }

  addQuestion(question: Question): Observable<Question> {
    const newQuestion = {
      ...question,
      id: this.questions.length + 1,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.questions.push(newQuestion);
    return of(newQuestion);
  }

  updateQuestion(id: number, questionData: Partial<Question>): Observable<Question | undefined> {
    const index = this.questions.findIndex(q => q.id === id);
    if (index !== -1) {
      this.questions[index] = {
        ...this.questions[index],
        ...questionData,
        updatedAt: new Date()
      };
      return of(this.questions[index]);
    }
    return of(undefined);
  }

  deleteQuestion(id: number): Observable<boolean> {
    const index = this.questions.findIndex(q => q.id === id);
    if (index !== -1) {
      this.questions[index].isActive = false;
      return of(true);
    }
    return of(false);
  }

  getSubAxes(): Observable<SubAxis[]> {
    return of(this.subAxes);
  }

  getSubAxesByAxis(axis: string): Observable<SubAxis[]> {
    const filtered = this.subAxes.filter(s => s.axis === axis);
    return of(filtered);
  }

  getCategories(): Observable<any[]> {
    return of(CATEGORIES);
  }

  getAxisOptions(): { value: string; label: string }[] {
    return [
      { value: 'METIER', label: 'Métier' },
      { value: 'PROCESSUS', label: 'Processus' },
      { value: 'SI', label: "Système d'information" }
    ];
  }
}