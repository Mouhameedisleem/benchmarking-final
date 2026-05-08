import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface AxisScore { axis: string; score: number; }
interface SubAxisScore { axis: string; subAxis: string; score: number; }

@Component({
  selector: 'app-score-result',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width:980px;">

      <!-- Header -->
      <div class="d-flex align-items-center mb-4">
        <a routerLink="/companies" class="btn btn-sm btn-outline-secondary me-3">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </a>
        <div class="flex-grow-1">
          <h4 class="mb-0 fw-bold">Résultats de l'évaluation</h4>
          <small class="text-muted" *ngIf="companyName">{{ companyName }}</small>
        </div>
        <span *ngIf="validated" class="badge bg-success fs-6 px-3 py-2">
          <i class="fas fa-check-circle me-1"></i>Validée
        </span>
        <span *ngIf="!validated && pendingReview" class="badge bg-warning text-dark fs-6 px-3 py-2">
          En attente de validation
        </span>
        <span *ngIf="!validated && !pendingReview" class="badge bg-secondary fs-6 px-3 py-2">
          En cours
        </span>
      </div>

      <!-- Loading -->
      <div *ngIf="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Chargement des résultats…</p>
      </div>

      <!-- Error -->
      <div *ngIf="error && !loading" class="alert alert-danger">
        <i class="fas fa-exclamation-circle me-2"></i>{{ error }}
      </div>

      <!-- Content -->
      <div *ngIf="!loading && !error">

        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4">
          <li class="nav-item">
            <button class="nav-link" [class.active]="tab==='scores'" (click)="tab='scores'">
              <i class="fas fa-chart-bar me-1"></i>Scores
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" [class.active]="tab==='recs'" (click)="tab='recs'">
              <i class="fas fa-lightbulb me-1"></i>Recommandations
              <span class="badge bg-primary ms-1">{{ recommendations.length }}</span>
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" [class.active]="tab==='bench'" (click)="tab='bench'">
              <i class="fas fa-globe me-1"></i>Benchmarking
            </button>
          </li>
        </ul>

        <!-- ── TAB: SCORES ── -->
        <div *ngIf="tab==='scores'">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="card border-0 shadow-sm rounded-4 text-center p-4 h-100">
                <div class="text-muted small mb-1">Score global</div>
                <div class="display-4 fw-bold" [style.color]="scoreColor(globalScore)">
                  {{ globalScore | number:'1.0-1' }}
                </div>
                <div class="text-muted small">/100</div>
                <div class="badge mt-2 px-3 py-2 rounded-pill"
                     [style.background]="maturityBg(maturityLevel)"
                     [style.color]="maturityColor(maturityLevel)"
                     style="font-size:13px;">
                  {{ maturityLabel(maturityLevel) }}
                </div>
              </div>
            </div>
            <div class="col-md-8">
              <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
                <div class="fw-semibold mb-3">Scores par axe</div>
                <div *ngFor="let a of axisBars" class="mb-3">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="small fw-semibold" [style.color]="a.score > 0 ? a.color : '#9ca3af'">{{ a.label }}</span>
                    <span *ngIf="a.score > 0" class="small text-muted">{{ a.score | number:'1.0-1' }}/100</span>
                    <span *ngIf="a.score === 0" class="badge bg-light text-secondary" style="font-size:10px;">Non évalué</span>
                  </div>
                  <div class="progress rounded-pill" style="height:10px;">
                    <div class="progress-bar rounded-pill"
                         [style.width]="a.score > 0 ? a.score+'%' : '100%'"
                         [style.background]="a.score > 0 ? a.color : '#f3f4f6'"
                         [style.opacity]="a.score > 0 ? '1' : '0.5'">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div *ngIf="subAxisScores.length > 0" class="card border-0 shadow-sm rounded-4 mt-3 p-4">
            <div class="fw-semibold mb-3">Détail par sous-axe</div>
            <div class="row g-2">
              <div *ngFor="let s of subAxisScores" class="col-md-6">
                <div class="d-flex align-items-center gap-2">
                  <span class="badge rounded-pill flex-shrink-0"
                        style="font-size:10px;width:80px;text-align:center;white-space:normal;"
                        [style.background]="axisColor(s.axis)+'20'"
                        [style.color]="axisColor(s.axis)">
                    {{ axisLabel(s.axis) }}
                  </span>
                  <span class="small text-muted flex-grow-1 text-truncate" style="max-width:160px;">{{ s.subAxis }}</span>
                  <div class="progress flex-grow-1 rounded-pill" style="height:6px;">
                    <div class="progress-bar rounded-pill"
                         [style.width]="s.score+'%'"
                         [style.background]="axisColor(s.axis)">
                    </div>
                  </div>
                  <span class="small fw-bold" style="min-width:36px;text-align:right;">{{ s.score | number:'1.0-0' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ── TAB: RECOMMENDATIONS ── -->
        <div *ngIf="tab==='recs'">
          <div *ngIf="recommendations.length === 0" class="text-center text-muted py-5">
            <i class="fas fa-inbox fa-2x mb-3 d-block"></i>
            Aucune recommandation disponible.
          </div>
          <div *ngFor="let r of recommendations" class="card border-0 shadow-sm rounded-3 mb-3">
            <div class="card-body p-3 d-flex gap-3 align-items-start">
              <div class="flex-shrink-0">
                <span class="badge rounded-pill d-block text-center mb-1" style="width:70px;font-size:11px;"
                      [style.background]="priorityColor(r.priority)+'20'"
                      [style.color]="priorityColor(r.priority)">
                  {{ r.priority }}
                </span>
                <span class="badge rounded-pill d-block text-center" style="font-size:10px;width:80px;white-space:normal;"
                      [style.background]="axisColor(r.axis)+'20'"
                      [style.color]="axisColor(r.axis)">
                  {{ axisLabel(r.axis) }}
                </span>
              </div>
              <div class="flex-grow-1">
                <div class="fw-semibold mb-1">{{ r.title }}</div>
                <p class="text-muted small mb-1">{{ r.description }}</p>
                <p class="text-muted small mb-0 fst-italic">{{ r.bestPractice }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- ── TAB: BENCHMARKING ── -->
        <div *ngIf="tab==='bench'">
          <div *ngIf="!benchmark" class="text-center text-muted py-5">
            <i class="fas fa-chart-line fa-2x mb-3 d-block"></i>
            Données de benchmarking non disponibles.
          </div>
          <div *ngIf="benchmark">
            <div class="row g-3 mb-3" *ngIf="benchmark.sectorBenchmark">
              <div class="col-md-4">
                <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
                  <div class="text-muted small mb-1">Moyenne nationale</div>
                  <div class="fs-3 fw-bold text-primary">{{ benchmark.sectorBenchmark.nationalAverage | number:'1.0-1' }}</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
                  <div class="text-muted small mb-1">Moyenne internationale</div>
                  <div class="fs-3 fw-bold text-success">{{ benchmark.sectorBenchmark.internationalAverage | number:'1.0-1' }}</div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="card border-0 shadow-sm rounded-4 p-3 text-center">
                  <div class="text-muted small mb-1">Positionnement</div>
                  <div class="fw-bold text-primary" style="font-size:15px;">{{ benchmark.sectorBenchmark.positioningLabel }}</div>
                  <div class="text-muted small">Percentile {{ benchmark.sectorBenchmark.companyPercentile }}e</div>
                </div>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 p-4 mb-3" *ngIf="benchmark.axisBenchmarks?.length">
              <div class="fw-semibold mb-3">Comparaison par axe</div>
              <div class="table-responsive">
                <table class="table table-sm align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>Axe</th>
                      <th class="text-center">Votre score</th>
                      <th class="text-center">Moy. sectorielle</th>
                      <th class="text-center">Top quartile</th>
                      <th class="text-center">Écart moy.</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr *ngFor="let ab of benchmark.axisBenchmarks">
                      <td class="fw-semibold">{{ ab.axisLabel || ab.axis }}</td>
                      <td class="text-center fw-bold text-primary">{{ ab.companyScore | number:'1.0-1' }}</td>
                      <td class="text-center">{{ ab.sectorAverage | number:'1.0-1' }}</td>
                      <td class="text-center">{{ ab.topQuartile | number:'1.0-1' }}</td>
                      <td class="text-center">
                        <span [class]="ab.gapToAverage >= 0 ? 'text-success fw-semibold' : 'text-danger fw-semibold'">
                          {{ ab.gapToAverage >= 0 ? '+' : '' }}{{ ab.gapToAverage | number:'1.0-1' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 p-4" *ngIf="benchmark.trends?.length">
              <div class="fw-semibold mb-3">Tendances sectorielles</div>
              <div class="row g-2">
                <div *ngFor="let t of benchmark.trends" class="col-md-6">
                  <div class="p-3 rounded-3 border h-100">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <span class="fw-semibold small">{{ t.title }}</span>
                      <span class="badge ms-2 flex-shrink-0" style="font-size:10px;"
                            [style.background]="t.impactLevel==='ÉLEVÉ'||t.impactLevel==='ELEVE'||t.impactLevel==='HIGH' ? '#fef9c3' : '#f0fdf4'"
                            [style.color]="t.impactLevel==='ÉLEVÉ'||t.impactLevel==='ELEVE'||t.impactLevel==='HIGH' ? '#854d0e' : '#166534'">
                        {{ t.impactLevel }}
                      </span>
                    </div>
                    <p class="text-muted small mb-1">{{ t.description }}</p>
                    <div class="text-muted" style="font-size:11px;">{{ t.horizon }} · Adoption : {{ t.adoptionRate }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  `
})
export class ScoreResultComponent implements OnInit {
  tab = 'scores';
  loading = true;
  error = '';

  companyName = '';
  pendingReview = false;
  validated = false;
  globalScore = 0;
  maturityLevel = '';
  recommendations: any[] = [];
  subAxisScores: SubAxisScore[] = [];
  benchmark: any = null;
  axisBars: { label: string; score: number; color: string }[] = [];

  private readonly axisColors: Record<string, string> = {
    METIER: '#0d6efd',              BUSINESS: '#0d6efd',
    PROCESSUS: '#198754',           PROCESS: '#198754',
    SI: '#6366f1',                  INFORMATION_SYSTEM: '#6366f1',
    CANAUX_DISTRIBUTION: '#0891b2',
    MARKETING_COMMUNICATION: '#d97706',
    RH_CULTURE_DIGITALE: '#7c3aed',
    OFFRES_DIGITALES: '#059669'
  };

  readonly axisLabels: Record<string, string> = {
    METIER: 'Métier',
    PROCESSUS: 'Processus',
    SI: 'Système d\'Information',
    CANAUX_DISTRIBUTION: 'Canaux & UX',
    MARKETING_COMMUNICATION: 'Marketing & Communication',
    RH_CULTURE_DIGITALE: 'RH & Culture Digitale',
    OFFRES_DIGITALES: 'Offres Digitales'
  };

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('evaluationId'));
    this.http.get<any>(`${environment.apiUrl}/evaluations/${id}/full-review`).subscribe({
      next: (data) => {
        const ev = data.evaluation;
        this.companyName = ev.companyName;
        this.pendingReview = data.pendingReview ?? false;
        this.validated = data.validated ?? false;
        this.globalScore = ev.globalScore;
        this.maturityLevel = ev.maturityLevel;
        this.subAxisScores = ev.scoresBySubAxis || [];
        const allAxes = [
          { key: 'METIER',                   label: 'Métier',                    color: '#0d6efd'  },
          { key: 'PROCESSUS',                label: 'Processus',                 color: '#198754'  },
          { key: 'SI',                       label: 'Système d\'Information',    color: '#6366f1'  },
          { key: 'CANAUX_DISTRIBUTION',      label: 'Canaux & UX',               color: '#0891b2'  },
          { key: 'MARKETING_COMMUNICATION',  label: 'Marketing & Communication', color: '#d97706'  },
          { key: 'RH_CULTURE_DIGITALE',      label: 'RH & Culture Digitale',     color: '#7c3aed'  },
          { key: 'OFFRES_DIGITALES',         label: 'Offres Digitales',          color: '#059669'  },
        ];
        this.axisBars = allAxes
          .map(a => ({
            label: a.label,
            score: (ev.scoresByAxis || []).find((s: AxisScore) => s.axis === a.key)?.score || 0,
            color: a.color
          }))
          ;
        this.recommendations = data.recommendations || [];
        this.benchmark = data.benchmark && Object.keys(data.benchmark).length > 0 ? data.benchmark : null;
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.error?.message || 'Erreur lors du chargement des résultats.';
        this.loading = false;
      }
    });
  }

  scoreColor(score: number): string {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#eab308';
    if (score >= 20) return '#f97316';
    return '#ef4444';
  }

  axisColor(axis: string): string { return this.axisColors[axis] ?? '#6c757d'; }

  axisLabel(axis: string): string { return this.axisLabels[axis] ?? axis; }

  priorityColor(p: string): string {
    return { HAUTE: '#dc2626', MOYENNE: '#d97706', BASSE: '#16a34a' }[p] ?? '#6c757d';
  }

  maturityLabel(level: string): string {
    return { INITIAL: 'Initial', BASIQUE: 'Basique', INTERMEDIAIRE: 'Intermédiaire', AVANCE: 'Avancé', OPTIMISE: 'Optimisé' }[level] ?? level;
  }

  maturityColor(level: string): string {
    return { INITIAL: '#ef4444', BASIQUE: '#f97316', INTERMEDIAIRE: '#ca8a04', AVANCE: '#3b82f6', OPTIMISE: '#16a34a' }[level] ?? '#6c757d';
  }

  maturityBg(level: string): string {
    return { INITIAL: '#fef2f2', BASIQUE: '#fff7ed', INTERMEDIAIRE: '#fefce8', AVANCE: '#eff6ff', OPTIMISE: '#f0fdf4' }[level] ?? '#f1f5f9';
  }
}