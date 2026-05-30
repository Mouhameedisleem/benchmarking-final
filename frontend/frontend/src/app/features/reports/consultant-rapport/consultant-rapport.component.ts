import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface AnswerSummary {
  questionId: number;
  questionText: string;
  axis: string;
  subAxis: string;
  answerValue: number;
  normalizedScore: number;
  weight: number;
  comment: string;
}

interface CompanyRapport {
  evaluationId: number;
  companyId: number;
  companyName: string;
  globalScore: number;
  maturityLevel: string;
  status: string;
  createdAt: string;
  answerSummaries: AnswerSummary[];
}

interface CompanyView {
  evaluationId: number;
  companyId: number;
  companyName: string;
  globalScore: number;
  maturityLevel: string;
  commentCount: number;
  visibleAnswers: number;
  axisGroups: { axis: string; answers: AnswerSummary[]; commentCount: number }[];
}

@Component({
  selector: 'app-consultant-rapport',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width:1100px;">

      <!-- Header -->
      <div class="d-flex align-items-center mb-4 gap-3">
        <a routerLink="/consultant/dashboard" class="btn btn-sm btn-outline-secondary">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </a>
        <div class="flex-grow-1">
          <h4 class="mb-0 fw-bold">
            <i class="fas fa-file-alt me-2" style="color:#1768e5;"></i>
            Rapport global des réponses
          </h4>
          <small class="text-muted">Vue consolidée des réponses de toutes les entreprises</small>
        </div>
      </div>

      <!-- Loading -->
      <div *ngIf="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Chargement des données…</p>
      </div>

      <!-- Error -->
      <div *ngIf="error && !loading" class="alert alert-danger rounded-3">
        <i class="fas fa-exclamation-circle me-2"></i>{{ error }}
      </div>

      <!-- Content -->
      <div *ngIf="!loading && !error">

        <!-- Summary cards -->
        <div class="row g-3 mb-4">
          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
              <div class="fw-bold fs-3" style="color:#1768e5;">{{ companies.length }}</div>
              <div class="text-muted small">Entreprises</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
              <div class="fw-bold fs-3 text-success">{{ totalAnswers }}</div>
              <div class="text-muted small">Réponses totales</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
              <div class="fw-bold fs-3 text-warning">{{ totalComments }}</div>
              <div class="text-muted small">Commentaires</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
              <div class="fw-bold fs-3" style="color:#0891b2;">{{ avgScore | number:'1.0-1' }}</div>
              <div class="text-muted small">Score moyen /100</div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="card border-0 shadow-sm rounded-3 p-3 mb-4">
          <div class="row g-2 align-items-center">
            <div class="col-md-4">
              <div class="input-group input-group-sm">
                <span class="input-group-text bg-white border-end-0 text-muted">
                  <i class="fas fa-search"></i>
                </span>
                <input type="text" class="form-control border-start-0 ps-0"
                       placeholder="Rechercher une entreprise…"
                       [(ngModel)]="searchCompany">
              </div>
            </div>
            <div class="col-md-3">
              <select class="form-select form-select-sm" [(ngModel)]="filterAxis">
                <option value="">Tous les axes</option>
                <option *ngFor="let ax of axes" [value]="ax.key">{{ ax.label }}</option>
              </select>
            </div>
            <div class="col-auto">
              <div class="form-check form-switch mb-0">
                <input class="form-check-input" type="checkbox" id="commentsOnly" [(ngModel)]="commentsOnly">
                <label class="form-check-label small" for="commentsOnly" style="cursor:pointer;">
                  <i class="fas fa-comment me-1 text-warning"></i>Avec commentaire
                </label>
              </div>
            </div>
            <div class="col-auto ms-auto d-flex gap-2 flex-wrap">
              <button class="btn btn-sm btn-outline-primary rounded-pill px-3" (click)="expandAll()">
                <i class="fas fa-expand-alt me-1"></i>Tout développer
              </button>
              <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" (click)="collapseAll()">
                <i class="fas fa-compress-alt me-1"></i>Tout réduire
              </button>
              <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" (click)="resetFilters()">
                <i class="fas fa-times me-1"></i>Réinitialiser
              </button>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div *ngIf="filteredCompanies.length === 0" class="text-center text-muted py-5">
          <i class="fas fa-search fa-2x mb-3 d-block opacity-25"></i>
          <p>Aucune entreprise ne correspond aux filtres sélectionnés.</p>
          <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" (click)="resetFilters()">
            Réinitialiser les filtres
          </button>
        </div>

        <!-- Companies list -->
        <div *ngFor="let co of filteredCompanies; trackBy: trackByEvalId" class="mb-3">
          <div class="card border-0 shadow-sm rounded-4 overflow-hidden">

            <!-- Company header -->
            <div class="d-flex align-items-center px-4 py-3 gap-3"
                 (click)="toggleCompany(co.evaluationId)"
                 style="cursor:pointer;background:#f8fafc;user-select:none;">
              <div class="rounded-circle d-flex align-items-center justify-content-center fw-bold flex-shrink-0"
                   style="width:42px;height:42px;background:#e8f0fe;color:#1768e5;font-size:15px;">
                {{ co.companyName.charAt(0).toUpperCase() }}
              </div>
              <div class="flex-grow-1">
                <div class="fw-semibold">{{ co.companyName }}</div>
                <div class="d-flex flex-wrap align-items-center gap-2 mt-1">
                  <span class="text-muted small">{{ co.visibleAnswers }} réponse(s)</span>
                  <span *ngIf="co.commentCount > 0" class="badge rounded-pill"
                        style="background:#fef9c3;color:#92400e;font-size:10px;">
                    <i class="fas fa-comment me-1"></i>{{ co.commentCount }} commentaire(s)
                  </span>
                </div>
              </div>
              <div class="text-center me-2 flex-shrink-0">
                <div class="fw-bold" style="color:#1768e5;font-size:20px;">
                  {{ co.globalScore | number:'1.0-1' }}<span class="text-muted fw-normal" style="font-size:12px;">/100</span>
                </div>
                <span class="badge rounded-pill px-2"
                      [style.background]="maturityColor(co.maturityLevel) + '20'"
                      [style.color]="maturityColor(co.maturityLevel)"
                      style="font-size:10px;">
                  {{ maturityLabel(co.maturityLevel) }}
                </span>
              </div>
              <i class="fas text-muted flex-shrink-0"
                 [class.fa-chevron-down]="!expandedMap[co.evaluationId]"
                 [class.fa-chevron-up]="expandedMap[co.evaluationId]"></i>
            </div>

            <!-- Expanded content -->
            <div *ngIf="expandedMap[co.evaluationId]">

              <div *ngIf="co.axisGroups.length === 0" class="text-center text-muted py-4 border-top">
                <i class="fas fa-inbox d-block mb-2 opacity-25"></i>
                Aucune réponse à afficher avec les filtres actuels.
              </div>

              <div *ngFor="let group of co.axisGroups; trackBy: trackByAxis; let last = last"
                   [class.border-bottom]="!last" class="border-top">

                <!-- Axis label bar -->
                <div class="px-4 py-2 d-flex align-items-center gap-2"
                     [style.background]="axisColor(group.axis) + '0a'">
                  <span class="badge rounded-pill px-2"
                        [style.background]="axisColor(group.axis) + '20'"
                        [style.color]="axisColor(group.axis)"
                        style="font-size:11px;font-weight:600;">
                    {{ axisLabel(group.axis) }}
                  </span>
                  <span class="text-muted" style="font-size:12px;">{{ group.answers.length }} question(s)</span>
                  <span *ngIf="group.commentCount > 0" class="badge rounded-pill"
                        style="background:#fef9c3;color:#92400e;font-size:10px;">
                    {{ group.commentCount }} commentaire(s)
                  </span>
                </div>

                <!-- Answers table -->
                <table class="table table-sm table-hover mb-0 align-middle" style="font-size:13px;">
                  <thead style="background:#fafafa;">
                    <tr>
                      <th class="ps-4 py-1 fw-normal text-muted" style="width:42%;font-size:11px;">Question</th>
                      <th class="text-center py-1 fw-normal text-muted" style="width:65px;font-size:11px;">Note</th>
                      <th class="text-center py-1 fw-normal text-muted" style="width:65px;font-size:11px;">Score</th>
                      <th class="py-1 fw-normal text-muted" style="font-size:11px;">Situation actuelle (commentaire)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr *ngFor="let a of group.answers"
                        [style.background]="a.comment ? '#fffbeb' : ''">
                      <td class="ps-4 py-2">
                        <div class="text-secondary" style="line-height:1.4;">{{ a.questionText }}</div>
                        <span *ngIf="a.subAxis" class="badge rounded-pill mt-1"
                              style="font-size:10px;background:#f1f5f9;color:#64748b;">
                          {{ a.subAxis }}
                        </span>
                      </td>
                      <td class="text-center py-2">
                        <span class="fw-bold" [style.color]="scoreColor(a.answerValue ?? 0)">
                          {{ a.answerValue ?? 0 }}/5
                        </span>
                      </td>
                      <td class="text-center py-2">
                        <span class="badge rounded-pill px-2"
                              [style.background]="scoreColor(a.answerValue ?? 0) + '20'"
                              [style.color]="scoreColor(a.answerValue ?? 0)"
                              style="font-size:11px;">
                          {{ (a.normalizedScore ?? 0) | number:'1.0-0' }}
                        </span>
                      </td>
                      <td class="py-2 pe-4">
                        <div *ngIf="a.comment" class="d-flex align-items-start gap-2">
                          <i class="fas fa-comment-dots flex-shrink-0 mt-1" style="color:#f59e0b;font-size:12px;"></i>
                          <span class="text-secondary" style="font-style:italic;line-height:1.5;">{{ a.comment }}</span>
                        </div>
                        <span *ngIf="!a.comment" class="text-muted" style="opacity:0.4;">—</span>
                      </td>
                    </tr>
                  </tbody>
                </table>

              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  `
})
export class ConsultantRapportComponent implements OnInit {
  companies: CompanyRapport[] = [];
  loading = true;
  error = '';

  searchCompany = '';
  filterAxis = '';
  commentsOnly = false;
  expandedMap: { [id: number]: boolean } = {};

  readonly axes = [
    { key: 'METIER',                         label: 'Métier' },
    { key: 'PROCESSUS',                      label: 'Processus' },
    { key: 'SI',                             label: 'SI' },
    { key: 'CANAUX_DISTRIBUTION',            label: 'Canaux & UX' },
    { key: 'MARKETING_COMMUNICATION',        label: 'Marketing' },
    { key: 'RH_CULTURE_DIGITALE',            label: 'RH & Culture' },
    { key: 'OFFRES_DIGITALES',               label: 'Offres Digitales' },
    { key: 'MODELE_OPERATIONNEL_INNOVATION', label: 'Modèle Opérationnel & Innovation' },
    { key: 'IT_DATA',                        label: 'IT & Data' },
  ];

  private readonly axisColors: Record<string, string> = {
    METIER: '#0d6efd', PROCESSUS: '#198754', SI: '#6366f1',
    CANAUX_DISTRIBUTION: '#0891b2', MARKETING_COMMUNICATION: '#d97706',
    RH_CULTURE_DIGITALE: '#7c3aed', OFFRES_DIGITALES: '#059669',
    MODELE_OPERATIONNEL_INNOVATION: '#f97316', IT_DATA: '#8b5cf6'
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<CompanyRapport[]>(`${environment.apiUrl}/evaluations/rapport`).subscribe({
      next: (data) => {
        this.companies = data;
        const map: { [id: number]: boolean } = {};
        data.forEach(co => { map[co.evaluationId] = true; });
        this.expandedMap = map;
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.error?.message || 'Erreur lors du chargement des données.';
        this.loading = false;
      }
    });
  }

  get totalAnswers(): number {
    return this.companies.reduce((sum, co) => sum + (co.answerSummaries?.length ?? 0), 0);
  }

  get totalComments(): number {
    return this.companies.reduce((sum, co) =>
      sum + (co.answerSummaries?.filter(a => a.comment?.trim().length > 0).length ?? 0), 0);
  }

  get avgScore(): number {
    if (!this.companies.length) return 0;
    return this.companies.reduce((sum, co) => sum + (co.globalScore ?? 0), 0) / this.companies.length;
  }

  get filteredCompanies(): CompanyView[] {
    return this.companies
      .filter(co => !this.searchCompany ||
        co.companyName.toLowerCase().includes(this.searchCompany.toLowerCase()))
      .map(co => {
        let answers = co.answerSummaries ?? [];
        if (this.filterAxis) answers = answers.filter(a => a.axis === this.filterAxis);
        if (this.commentsOnly) answers = answers.filter(a => a.comment?.trim().length > 0);

        const axisMap = new Map<string, AnswerSummary[]>();
        for (const a of answers) {
          const key = a.axis || 'AUTRE';
          if (!axisMap.has(key)) axisMap.set(key, []);
          axisMap.get(key)!.push(a);
        }

        const axisGroups = [...axisMap.entries()].map(([axis, ans]) => ({
          axis,
          answers: ans,
          commentCount: ans.filter(a => a.comment?.trim().length > 0).length
        }));

        return {
          evaluationId: co.evaluationId,
          companyId: co.companyId,
          companyName: co.companyName,
          globalScore: co.globalScore ?? 0,
          maturityLevel: co.maturityLevel,
          commentCount: (co.answerSummaries ?? []).filter(a => a.comment?.trim().length > 0).length,
          visibleAnswers: answers.length,
          axisGroups
        };
      })
      .filter(co => (!this.filterAxis && !this.commentsOnly) ? true : co.visibleAnswers > 0);
  }

  toggleCompany(id: number) {
    this.expandedMap = { ...this.expandedMap, [id]: !this.expandedMap[id] };
  }

  expandAll() {
    const m: { [id: number]: boolean } = {};
    this.companies.forEach(co => { m[co.evaluationId] = true; });
    this.expandedMap = m;
  }

  collapseAll() {
    this.expandedMap = {};
  }

  resetFilters() {
    this.searchCompany = '';
    this.filterAxis = '';
    this.commentsOnly = false;
  }

  trackByEvalId(_: number, co: CompanyView): number { return co.evaluationId; }
  trackByAxis(_: number, g: { axis: string }): string { return g.axis; }

  axisColor(axis: string): string { return this.axisColors[axis] ?? '#6c757d'; }

  axisLabel(axis: string): string {
    return this.axes.find(a => a.key === axis)?.label ?? axis;
  }

  scoreColor(v: number): string {
    if (v >= 5) return '#16a34a';
    if (v >= 4) return '#3b82f6';
    if (v >= 3) return '#d97706';
    if (v >= 2) return '#f97316';
    return '#dc2626';
  }

  maturityColor(level: string): string {
    const c: Record<string, string> = {
      INITIAL: '#ef4444', BASIQUE: '#f97316', INTERMEDIAIRE: '#eab308',
      AVANCE: '#3b82f6', OPTIMISE: '#22c55e'
    };
    return c[level] ?? '#94a3b8';
  }

  maturityLabel(level: string): string {
    const l: Record<string, string> = {
      INITIAL: 'Initial', BASIQUE: 'Basique', INTERMEDIAIRE: 'Intermédiaire',
      AVANCE: 'Avancé', OPTIMISE: 'Optimisé'
    };
    return l[level] ?? level;
  }
}
