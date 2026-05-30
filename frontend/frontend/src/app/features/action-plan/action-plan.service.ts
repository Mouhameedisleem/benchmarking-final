import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ActionPlanTask {
  id: number;
  evaluationId: number;
  companyName: string;
  title: string;
  description: string;
  axe: string;
  priority: 'HAUTE' | 'MOYENNE' | 'BASSE';
  phase: string;
  responsible: string;
  deadline: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  createdAt: string;
  updatedAt: string;
}

export interface ActionPlanRequest {
  title?: string;
  description?: string;
  axe?: string;
  priority?: string;
  phase?: string;
  responsible?: string;
  deadline?: string;
  status?: 'TODO' | 'IN_PROGRESS' | 'DONE';
}

@Injectable({ providedIn: 'root' })
export class ActionPlanService {
  private readonly base = `${environment.apiUrl}/action-plans`;

  constructor(private http: HttpClient) {}

  generate(evaluationId: number, recommendations: any[]): Observable<ActionPlanTask[]> {
    return this.http.post<ActionPlanTask[]>(`${this.base}/generate/${evaluationId}`, recommendations);
  }

  getByEvaluation(evaluationId: number): Observable<ActionPlanTask[]> {
    return this.http.get<ActionPlanTask[]>(`${this.base}/${evaluationId}`);
  }

  exists(evaluationId: number): Observable<{ exists: boolean }> {
    return this.http.get<{ exists: boolean }>(`${this.base}/${evaluationId}/exists`);
  }

  update(taskId: number, request: ActionPlanRequest): Observable<ActionPlanTask> {
    return this.http.put<ActionPlanTask>(`${this.base}/task/${taskId}`, request);
  }

  delete(taskId: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/task/${taskId}`);
  }

  exportExcel(evaluationId: number): Observable<Blob> {
    return this.http.get(`${this.base}/${evaluationId}/export`, { responseType: 'blob' });
  }
}
