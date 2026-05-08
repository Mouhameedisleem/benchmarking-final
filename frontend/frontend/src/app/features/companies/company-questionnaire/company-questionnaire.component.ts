import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface QuestionItem {
  id: number;
  text: string;
  axis: string;
  subAxis: string;
  weight: number;
  displayOrder: number;
  options: string[];
}

interface QuestionGroup {
  axis: string;
  axisLabel: string;
  axisColor: string;
  questions: QuestionItem[];
}

@Component({
  selector: 'app-company-questionnaire',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width:960px;">

      <!-- Header -->
      <div class="d-flex align-items-center mb-4 gap-3">
        <a [routerLink]="['/companies']" class="btn btn-sm btn-outline-secondary">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </a>
        <div class="flex-grow-1">
          <h4 class="mb-0 fw-bold">
            <i class="fas fa-clipboard-list text-primary me-2"></i>
            Questionnaire — {{ companyName }}
          </h4>
          <small class="text-muted" *ngIf="sector">Secteur : {{ sector }}</small>
        </div>
        <a [routerLink]="['/companies', companyId, 'setup']" class="btn btn-sm btn-outline-primary">
          <i class="fas fa-sync me-1"></i>Reconfigurer
        </a>
      </div>

      <!-- Loading -->
      <div class="text-center py-5" *ngIf="isLoading">
        <div class="spinner-border text-primary"></div>
        <p class="mt-2 text-muted">Chargement du questionnaire...</p>
      </div>

      <!-- No questionnaire -->
      <div *ngIf="!isLoading && !hasQuestionnaire" class="card border-0 shadow-sm rounded-4 text-center p-5">
        <i class="fas fa-clipboard fa-3x text-muted mb-3"></i>
        <h5 class="text-muted">Aucun questionnaire configuré</h5>
        <p class="text-muted small mb-4">Ce questionnaire n'a pas encore été généré pour cette entreprise.</p>
        <a [routerLink]="['/companies', companyId, 'setup']" class="btn btn-primary">
          <i class="fas fa-robot me-2"></i>Générer le questionnaire IA
        </a>
      </div>

      <!-- Stats bar -->
      <div *ngIf="!isLoading && hasQuestionnaire" class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-3 text-center p-3">
            <div class="fw-bold fs-4 text-primary">{{ totalQuestions }}</div>
            <div class="small text-muted">Questions au total</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-3 text-center p-3">
            <div class="fw-bold fs-4 text-success">{{ groups.length }}</div>
            <div class="small text-muted">Axes évalués</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm rounded-3 text-center p-3">
            <div class="fw-bold fs-4 text-warning">{{ sector }}</div>
            <div class="small text-muted">Secteur</div>
          </div>
        </div>
      </div>

      <!-- Questions grouped by axis -->
      <div *ngIf="!isLoading && hasQuestionnaire">
        <div *ngFor="let group of groups" class="card border-0 shadow-sm rounded-4 mb-4">
          <!-- Axis header -->
          <div class="card-header border-0 rounded-top-4 d-flex align-items-center gap-2 px-4 py-3"
               [style.background]="group.axisColor + '15'">
            <span class="fw-bold" style="font-size:15px;" [style.color]="group.axisColor">
              {{ group.axisLabel }}
            </span>
            <span class="badge rounded-pill ms-auto"
                  [style.background]="group.axisColor + '25'"
                  [style.color]="group.axisColor">
              {{ group.questions.length }} question{{ group.questions.length > 1 ? 's' : '' }}
            </span>
          </div>

          <div class="card-body px-4 pb-4 pt-2">
            <div *ngFor="let q of group.questions; let i = index"
                 class="py-3"
                 [class.border-bottom]="i < group.questions.length - 1">
              <!-- Question text -->
              <div class="d-flex gap-2 align-items-start mb-2">
                <span class="badge rounded-pill flex-shrink-0 mt-1"
                      style="font-size:11px;padding:4px 8px;"
                      [style.background]="group.axisColor + '20'"
                      [style.color]="group.axisColor">
                  {{ q.displayOrder }}
                </span>
                <div class="flex-grow-1">
                  <p class="mb-1 fw-semibold" style="font-size:14px;">{{ q.text }}</p>
                  <small class="text-muted">
                    <i class="fas fa-tag me-1"></i>{{ q.subAxis }}
                    <span class="ms-3"><i class="fas fa-weight-hanging me-1"></i>Poids : {{ q.weight }}/5</span>
                  </small>
                </div>
              </div>

              <!-- Maturity options preview -->
              <div *ngIf="q.options && q.options.length === 5" class="ms-4 mt-2">
                <div class="d-flex flex-wrap gap-1">
                  <span *ngFor="let opt of q.options; let idx = index"
                        class="badge rounded-pill"
                        style="font-size:11px;font-weight:400;padding:4px 10px;background:#f1f5f9;color:#475569;border:1px solid #e2e8f0;">
                    <strong style="color:#1e40af;">{{ idx + 1 }}</strong> — {{ opt }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  `
})
export class CompanyQuestionnaireComponent implements OnInit {
  companyId!: number;
  companyName = '';
  sector = '';
  isLoading = true;
  hasQuestionnaire = false;
  groups: QuestionGroup[] = [];
  totalQuestions = 0;

  private readonly axisConfig: Record<string, { label: string; color: string }> = {
    BUSINESS: { label: 'Axe Métier', color: '#0d6efd' },
    PROCESS: { label: 'Axe Processus', color: '#198754' },
    INFORMATION_SYSTEM: { label: 'Axe Système d\'information', color: '#6366f1' },
    METIER: { label: 'Axe Métier', color: '#0d6efd' },
    PROCESSUS: { label: 'Axe Processus', color: '#198754' },
    SI: { label: 'Axe Système d\'information', color: '#6366f1' }
  };

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    this.companyId = Number(this.route.snapshot.paramMap.get('id'));
    this.http.get<any>(`${environment.apiUrl}/companies/${this.companyId}`).subscribe({
      next: (company) => {
        this.companyName = company.name;
        this.sector = company.sector;
        this.loadQuestionnaire();
      },
      error: () => { this.isLoading = false; }
    });
  }

  private loadQuestionnaire() {
    this.http.get<any[]>(`${environment.apiUrl}/questionnaires?companyId=${this.companyId}`).subscribe({
      next: (questionnaires) => {
        const active = questionnaires.find(q => q.active) || questionnaires[0];
        if (!active || !active.questions?.length) {
          this.hasQuestionnaire = false;
          this.isLoading = false;
          return;
        }
        this.hasQuestionnaire = true;
        const questions: QuestionItem[] = (active.questions as any[]).map(q => ({
          id: q.id,
          text: q.text,
          axis: q.axis,
          subAxis: q.subAxis || '',
          weight: q.weight || 1,
          displayOrder: q.displayOrder || 0,
          options: q.options || []
        }));
        this.totalQuestions = questions.length;
        this.groups = this.buildGroups(questions);
        this.isLoading = false;
      },
      error: () => {
        this.hasQuestionnaire = false;
        this.isLoading = false;
      }
    });
  }

  private buildGroups(questions: QuestionItem[]): QuestionGroup[] {
    const map = new Map<string, QuestionItem[]>();
    for (const q of questions.sort((a, b) => a.displayOrder - b.displayOrder)) {
      if (!map.has(q.axis)) map.set(q.axis, []);
      map.get(q.axis)!.push(q);
    }
    return Array.from(map.entries()).map(([axis, qs]) => ({
      axis,
      axisLabel: this.axisConfig[axis]?.label || axis,
      axisColor: this.axisConfig[axis]?.color || '#6c757d',
      questions: qs
    }));
  }
}
