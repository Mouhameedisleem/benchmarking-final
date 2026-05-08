import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface EvaluationSummary {
  evaluationId: number;
  companyId: number;
  companyName: string;
  consultantName?: string;
  globalScore: number;
  businessScore?: number;
  processScore?: number;
  siScore?: number;
  maturityLevel: string;
  status: 'IN_PROGRESS' | 'PENDING_REVIEW' | 'VALIDATED';
  createdAt: string;
}

@Injectable({ providedIn: 'root' })
export class EvaluationService {
  private readonly apiUrl = `${environment.apiUrl}/evaluations`;

  constructor(private http: HttpClient) {}

  getAllEvaluations(): Observable<EvaluationSummary[]> {
    return this.http.get<EvaluationSummary[]>(`${this.apiUrl}/all`);
  }

  getPendingReviews(): Observable<EvaluationSummary[]> {
    return this.http.get<EvaluationSummary[]>(`${this.apiUrl}/pending-review`);
  }

  getEvaluation(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  getLatestEvaluation(companyId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/latest?companyId=${companyId}`);
  }

  getFullReview(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}/full-review`);
  }

  getMaturityLabel(level: string): string {
    const labels: Record<string, string> = {
      INITIAL: 'Initial',
      BASIQUE: 'Basique',
      INTERMEDIAIRE: 'Intermédiaire',
      AVANCE: 'Avancé',
      OPTIMISE: 'Optimisé'
    };
    return labels[level] ?? level;
  }

  getMaturityColor(level: string): string {
    const colors: Record<string, string> = {
      INITIAL: '#ef4444',
      BASIQUE: '#f97316',
      INTERMEDIAIRE: '#eab308',
      AVANCE: '#3b82f6',
      OPTIMISE: '#22c55e'
    };
    return colors[level] ?? '#94a3b8';
  }

  getScoreColor(score: number): string {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#eab308';
    if (score >= 20) return '#f97316';
    return '#ef4444';
  }
}
