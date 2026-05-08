import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Company } from '../models/company.model';

export interface Trend {
  id: string;
  title: string;
  description: string;
  category: string;
  subAxis: string;
  region: 'national' | 'regional' | 'international';
  source?: string;
  data?: any;
  stats?: {
    percentage?: number;
    value?: string;
    year?: number;
  };
  examples?: {
    company: string;
    country: string;
    description: string;
  }[];
}

export interface LeaderExample {
  company: string;
  country: string;
  category: string;
  subAxis: string;
  description: string;
  innovation: string;
  source: string;
  year?: number;
}

export interface LegalFramework {
  id: string;
  title: string;
  description: string;
  country: string;
  region?: string;
  type: 'law' | 'regulation' | 'circular' | 'initiative';
  impact: 'opportunity' | 'constraint' | 'neutral';
  summary: string;
  source: string;
  date: Date;
  articles?: {
    number: string;
    content: string;
  }[];
}

@Injectable({
  providedIn: 'root'
})
export class BenchmarkService {
  
  // Données mockées pour les tendances
  private trends: Trend[] = [
    {
      id: 'trend-1',
      title: 'Affichage du solde en temps réel',
      description: 'Progression de l\'affichage instantané des transactions sur mobile',
      category: 'CANAUX',
      subAxis: 'canaux-digitaux',
      region: 'international',
      stats: {
        percentage: 28,
        value: '28% des banques traditionnelles'
      },
      examples: [
        {
          company: 'U Itim',
          country: 'France',
          description: 'Offre premium avec affichage instantané'
        },
        {
          company: 'Kapsul',
          country: 'France',
          description: 'Affichage en temps réel dès 2020'
        }
      ]
    },
    {
      id: 'trend-2',
      title: 'Déploiement de l\'Instant Payment',
      description: 'Service largement déployé et plébiscité par les clients',
      category: 'CANAUX',
      subAxis: 'canaux-digitaux',
      region: 'international',
      stats: {
        percentage: 68,
        value: '68% des banques testées'
      },
      examples: [
        {
          company: 'Acteur majeur français',
          country: 'France',
          description: '2 300 000 virements instantanés, soit 9% des virements externes'
        }
      ]
    }
  ];

  // Données mockées pour les leaders
  private leaders: LeaderExample[] = [
    {
      company: 'Capital One',
      country: 'USA',
      category: 'IA',
      subAxis: 'ia-iot',
      description: 'Assistant virtuel Eno capable d\'identifier risques et besoins',
      innovation: 'Chatbot enrichi par Machine Learning, mode supervisé, relation émotionnelle',
      source: 'Capital One',
      year: 2024
    },
    {
      company: 'N26',
      country: 'Allemagne',
      category: 'CANAUX',
      subAxis: 'canaux-digitaux',
      description: 'Modification du PIN CB directement dans l\'application',
      innovation: 'Utilisation immédiate de la carte sans attendre',
      source: 'N26',
      year: 2024
    },
    {
      company: 'Boursorama',
      country: 'France',
      category: 'CANAUX',
      subAxis: 'canaux-digitaux',
      description: 'Ajout de la carte dans le wallet immédiatement',
      innovation: 'Pas d\'attente de réception physique',
      source: 'Boursorama',
      year: 2024
    }
  ];

  // Données mockées pour le cadre légal
  private legalFrameworks: LegalFramework[] = [
    {
      id: 'legal-1',
      title: 'Initiative UEMOA',
      description: 'Dématérialisation des procédures et digitalisation des paiements',
      country: 'UEMOA',
      type: 'initiative',
      impact: 'opportunity',
      summary: 'Les États membres de l\'UEMOA ont lancé plusieurs initiatives pour la dématérialisation',
      source: 'UEMOA',
      date: new Date('2023-01-01')
    }
  ];

  constructor() {}

  /**
   * Récupère les tendances par catégorie/sous-axe
   */
  getTrends(category?: string, subAxis?: string, region?: string): Observable<Trend[]> {
    let filtered = this.trends;
    
    if (category) {
      filtered = filtered.filter(t => t.category === category);
    }
    if (subAxis) {
      filtered = filtered.filter(t => t.subAxis === subAxis);
    }
    if (region) {
      filtered = filtered.filter(t => t.region === region);
    }
    
    return of(filtered);
  }

  /**
   * Récupère les exemples de leaders par catégorie/sous-axe
   */
  getLeaders(category?: string, subAxis?: string): Observable<LeaderExample[]> {
    let filtered = this.leaders;
    
    if (category) {
      filtered = filtered.filter(l => l.category === category);
    }
    if (subAxis) {
      filtered = filtered.filter(l => l.subAxis === subAxis);
    }
    
    return of(filtered);
  }

  /**
   * Récupère le cadre légal par pays
   */
  getLegalFramework(country: string): Observable<LegalFramework[]> {
    const filtered = this.legalFrameworks.filter(l => 
      l.country === country || l.country === 'UEMOA'
    );
    return of(filtered);
  }

  /**
   * Génère un rapport de benchmark complet pour une entreprise
   */
  generateBenchmarkReport(company: Company, score: any): Observable<any> {
    return of({
      company: company,
      score: score,
      trends: this.trends.filter(t => t.category === 'CANAUX'), // À adapter
      leaders: this.leaders,
      legal: this.legalFrameworks,
      recommendations: this.generateRecommendations(company, score)
    });
  }

  /**
   * Génère des recommandations basées sur le benchmark
   */
  private generateRecommendations(company: Company, score: any): any[] {
    const recommendations = [];
    
    // Exemple de recommandation basée sur les tendances
    if (score.scoresByAxis.METIER < 50) {
      recommendations.push({
        type: 'TENDANCE',
        title: 'Adopter l\'affichage en temps réel',
        description: 'Suivez la tendance des leaders en proposant l\'affichage instantané des transactions',
        examples: this.trends[0].examples
      });
    }
    
    // Exemple de recommandation basée sur les leaders
    if (company.sector === 'banking') {
      recommendations.push({
        type: 'LEADER',
        title: 'Inspirez-vous de Capital One',
        description: 'Développez un assistant virtuel enrichi par Machine Learning',
        example: this.leaders[0]
      });
    }
    
    return recommendations;
  }

  /**
   * Compare une entreprise avec les leaders du marché
   */
  compareWithLeaders(company: Company, score: any): any {
    return {
      company: {
        name: company.name,
        score: score.globalScore,
        level: score.maturityLevel
      },
      leaders: this.leaders.map(l => ({
        name: l.company,
        country: l.country,
        innovation: l.innovation
      })),
      gaps: this.identifyGaps(score)
    };
  }

  /**
   * Identifie les écarts par rapport aux leaders
   */
  private identifyGaps(score: any): any[] {
    const gaps = [];
    
    if (score.scoresByAxis.METIER < 70) {
      gaps.push({
        axis: 'METIER',
        gap: 'Expérience client digitale',
        suggestion: 'Inspirez-vous des fonctionnalités innovantes de N26 et Boursorama'
      });
    }
    
    if (score.scoresByAxis.SI < 60) {
      gaps.push({
        axis: 'SI',
        gap: 'Innovation technologique',
        suggestion: 'Développez des capacités d\'IA comme Capital One'
      });
    }
    
    return gaps;
  }
}