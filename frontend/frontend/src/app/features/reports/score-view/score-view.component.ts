import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../core/services/auth.service';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-score-view',
  standalone: true,
  imports: [CommonModule, RouterLink],
  styles: [`
    .gauge-track { fill: none; stroke: #e9ecef; }
    .gauge-fill  { fill: none; stroke-linecap: round; transition: stroke-dasharray .7s ease; }
    .axis-bar  { height: 10px; border-radius: 5px; background: #e9ecef; overflow: hidden; }
    .axis-fill { height: 100%; border-radius: 5px; transition: width .6s ease; }
    .maturity-step {
      width: 28px; height: 28px; border-radius: 50%; border: 2px solid #dee2e6;
      display: flex; align-items: center; justify-content: center;
      font-size: 10px; font-weight: 700; color: #adb5bd; background: #fff;
    }
    .maturity-step.active { border-color: currentColor; color: #fff; }
    .maturity-line { height: 2px; flex: 1; background: #dee2e6; margin-top: 13px; }
    .rec-item { border-radius: 10px; border-left: 4px solid transparent; }
  `],
  template: `
    <div class="container-fluid py-4 px-4" style="max-width:1100px;margin:auto;">

      <!-- Header -->
      <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-2">
        <div>
          <h3 class="fw-bold mb-0">Mes Résultats</h3>
          <small class="text-muted">Score de maturité · Recommandations IA · Benchmarking sectoriel</small>
        </div>
        <a routerLink="/client/dashboard" class="btn btn-outline-secondary btn-sm rounded-pill px-3">
          <i class="fas fa-arrow-left me-1"></i>Dashboard
        </a>
      </div>

      <!-- Loading -->
      <div *ngIf="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" style="width:3rem;height:3rem;"></div>
        <p class="text-muted mt-2">Chargement de vos résultats…</p>
      </div>

      <!-- No evaluation -->
      <div *ngIf="!isLoading && !evaluation"
           class="card border-0 shadow-sm text-center py-5">
        <div class="card-body">
          <i class="fas fa-clipboard-list fa-3x text-muted mb-3 opacity-25"></i>
          <h5 class="text-muted">Aucune évaluation disponible</h5>
          <p class="text-muted small mb-3">Commencez le questionnaire pour obtenir vos résultats de maturité digitale.</p>
          <a routerLink="/questionnaire" class="btn btn-primary rounded-pill px-4">
            <i class="fas fa-play me-1"></i>Commencer le questionnaire
          </a>
        </div>
      </div>

      <ng-container *ngIf="!isLoading && evaluation">

        <!-- Score + maturity card -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header border-0 py-3 px-4"
               style="background:linear-gradient(135deg,#f8f9fa,#fff);">
            <div class="d-flex align-items-center gap-3">
              <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 fw-bold text-white"
                   style="width:46px;height:46px;font-size:1.1rem;background:#1768e5;">
                {{ (currentUser?.companyName || 'E').charAt(0).toUpperCase() }}
              </div>
              <div>
                <div class="fw-bold fs-5">{{ currentUser?.companyName || 'Mon entreprise' }}</div>
                <div class="text-muted small">
                  <i class="fas fa-calendar-check me-1"></i>
                  Évaluation du {{ evaluation.createdAt | date:'dd/MM/yyyy' }}
                </div>
              </div>
            </div>
          </div>

          <div class="card-body px-4 py-3">
            <div class="row align-items-center g-4">

              <!-- SVG Gauge -->
              <div class="col-md-4 text-center">
                <svg viewBox="0 0 120 120" style="width:150px;height:150px;">
                  <circle class="gauge-track" cx="60" cy="60" r="50" stroke-width="12"/>
                  <circle class="gauge-fill"
                          cx="60" cy="60" r="50" stroke-width="12"
                          [attr.stroke]="scoreColor(evaluation.globalScore)"
                          [attr.stroke-dasharray]="dashArray(evaluation.globalScore)"
                          transform="rotate(-90 60 60)"/>
                  <text x="60" y="54" text-anchor="middle" font-size="22" font-weight="800"
                        [attr.fill]="scoreColor(evaluation.globalScore)">
                    {{ evaluation.globalScore | number:'1.0-0' }}
                  </text>
                  <text x="60" y="70" text-anchor="middle" font-size="10" fill="#9ca3af">/100</text>
                </svg>
                <div class="fw-semibold text-muted small mt-1">Score global</div>
                <span *ngIf="evaluation.maturityLevel" class="badge rounded-pill px-3 py-2 mt-2"
                      [ngClass]="maturityBadge(evaluation.maturityLevel)">
                  <i class="fas fa-star me-1"></i>{{ maturityLabel(evaluation.maturityLevel) }}
                </span>
              </div>

              <!-- Axes + maturity stepper -->
              <div class="col-md-8">
                <!-- Maturity stepper -->
                <div *ngIf="evaluation.maturityLevel" class="mb-3">
                  <div class="small text-muted fw-semibold mb-2">Niveau de maturité</div>
                  <div class="d-flex align-items-center">
                    <ng-container *ngFor="let step of maturitySteps; let i = index; let last = last">
                      <div class="maturity-step"
                           [class.active]="isMaturityActive(evaluation.maturityLevel, i)"
                           [style.background]="isMaturityActive(evaluation.maturityLevel, i) ? step.color : ''"
                           [style.border-color]="isMaturityActive(evaluation.maturityLevel, i) ? step.color : ''"
                           [style.color]="isMaturityActive(evaluation.maturityLevel, i) ? '#fff' : ''"
                           [title]="step.label">
                        {{ i + 1 }}
                      </div>
                      <div *ngIf="!last" class="maturity-line flex-grow-1"
                           [style.background]="isMaturityActive(evaluation.maturityLevel, i + 1) ? step.color : '#dee2e6'">
                      </div>
                    </ng-container>
                  </div>
                  <div class="d-flex justify-content-between mt-1" style="font-size:9px;color:#9ca3af;">
                    <span *ngFor="let step of maturitySteps">{{ step.label }}</span>
                  </div>
                </div>

                <!-- Axis scores -->
                <div class="small text-muted fw-semibold mb-2">Scores par axe</div>
                <div *ngFor="let axis of evaluation.scoresByAxis || []" class="mb-2">
                  <div class="d-flex justify-content-between small mb-1">
                    <span class="fw-semibold">
                      <i class="me-1" [ngClass]="axisIcon(axis.axis)"></i>{{ axisLabel(axis.axis) }}
                    </span>
                    <span class="fw-bold" [style.color]="axisColor(axis.axis)">{{ axis.score | number:'1.0-0' }}%</span>
                  </div>
                  <div class="axis-bar">
                    <div class="axis-fill" [style.width.%]="axis.score" [style.background]="axisColor(axis.axis)"></div>
                  </div>
                </div>

                <!-- AI maturity explanation -->
                <div *ngIf="evaluation.maturityExplanation" class="mt-3 p-3 rounded-3"
                     style="background:#f0f4ff;border-left:4px solid #1768e5;font-size:.85rem;">
                  <i class="fas fa-robot text-primary me-1"></i>
                  <span class="text-muted">{{ evaluation.maturityExplanation }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Download report -->
          <div class="card-footer border-0 bg-white px-4 pb-3 pt-0 d-flex gap-2 flex-wrap">
            <a routerLink="/client/report" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              <i class="fas fa-file-pdf me-1"></i>Télécharger le rapport PDF
            </a>
          </div>
        </div>

        <!-- Recommendations -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header border-0 bg-white py-3 px-4 d-flex align-items-center justify-content-between">
            <div class="fw-semibold">
              <i class="fas fa-robot text-primary me-2"></i>Recommandations IA
            </div>
            <button class="btn btn-sm rounded-pill px-3"
                    [class.btn-outline-primary]="!showRecs"
                    [class.btn-primary]="showRecs"
                    (click)="toggleRecs()"
                    [disabled]="recsLoading">
              <span *ngIf="recsLoading" class="spinner-border spinner-border-sm me-1"></span>
              <i *ngIf="!recsLoading" class="fas fa-robot me-1"></i>
              {{ showRecs ? 'Masquer' : 'Voir' }} les recommandations
              <span *ngIf="recommendations.length" class="badge bg-white text-primary ms-1">
                {{ recommendations.length }}
              </span>
            </button>
          </div>
          <div *ngIf="showRecs" class="card-body px-4 py-3">
            <div *ngIf="!recommendations.length && !recsLoading" class="text-muted small text-center py-2">
              Aucune recommandation disponible.
            </div>
            <ng-container *ngFor="let axisGroup of groupByAxis(recommendations)">
              <div class="small fw-bold text-uppercase mb-2 mt-3" style="letter-spacing:.08em;"
                   [style.color]="axisColor(axisGroup.axis)">
                <i class="me-1" [ngClass]="axisIcon(axisGroup.axis)"></i>{{ axisLabel(axisGroup.axis) }}
              </div>
              <div *ngFor="let rec of axisGroup.items" class="rec-item p-3 mb-2"
                   [style.border-left-color]="priorityColor(rec.priority)"
                   [style.background]="priorityBg(rec.priority)">
                <div class="d-flex align-items-start gap-2">
                  <span class="badge rounded-pill flex-shrink-0 mt-1"
                        [style.background]="priorityColor(rec.priority)">{{ rec.priority }}</span>
                  <div>
                    <div class="fw-semibold small">{{ rec.title }}</div>
                    <div class="text-muted small mt-1">{{ rec.description }}</div>
                    <div *ngIf="rec.bestPractice" class="small mt-1" style="color:#92400e;">
                      <i class="fas fa-lightbulb me-1 text-warning"></i>{{ rec.bestPractice }}
                    </div>
                  </div>
                </div>
              </div>
            </ng-container>
          </div>
        </div>

        <!-- Benchmark -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-header border-0 bg-white py-3 px-4 d-flex align-items-center justify-content-between">
            <div class="fw-semibold">
              <i class="fas fa-chart-bar text-success me-2"></i>Benchmarking Sectoriel IA
            </div>
            <button class="btn btn-sm rounded-pill px-3"
                    [class.btn-outline-success]="!showBenchmark"
                    [class.btn-success]="showBenchmark"
                    (click)="toggleBenchmark()"
                    [disabled]="benchmarkLoading">
              <span *ngIf="benchmarkLoading" class="spinner-border spinner-border-sm me-1"></span>
              <i *ngIf="!benchmarkLoading" class="fas fa-globe me-1"></i>
              {{ showBenchmark ? 'Masquer' : 'Voir' }} le benchmarking
            </button>
          </div>

          <!-- Error / unavailable state -->
          <div *ngIf="showBenchmark && (benchmarkError || !benchmark)" class="card-body px-4 py-3">
            <div class="d-flex align-items-start gap-3 p-3 rounded-3"
                 style="background:#fff8e1;border:1px solid #ffc107;">
              <i class="fas fa-exclamation-triangle text-warning fs-5 mt-1"></i>
              <div>
                <div class="fw-semibold text-warning small">Service de benchmarking indisponible</div>
                <div class="text-muted small mt-1">
                  Assurez-vous que le service IA Python est en cours d'exécution
                  (<code style="font-size:.75rem;">uvicorn main:app --port 8000</code>), puis réessayez.
                </div>
                <button class="btn btn-sm btn-outline-warning mt-2 rounded-pill" (click)="retryBenchmark()">
                  <i class="fas fa-redo me-1"></i>Réessayer
                </button>
              </div>
            </div>
          </div>

          <div *ngIf="showBenchmark && benchmark" class="card-body px-4 py-3">

            <!-- Executive summary -->
            <div class="rounded-3 p-3 mb-3" style="background:#f0fdf4;border-left:4px solid #198754;">
              <div class="small fw-bold text-success mb-1" style="letter-spacing:.06em;">
                <i class="fas fa-file-alt me-1"></i>SYNTHÈSE EXÉCUTIVE
              </div>
              <p class="mb-0 small text-muted">{{ benchmark.executive_summary }}</p>
            </div>

            <!-- Sector positioning -->
            <div *ngIf="benchmark.sector_benchmark" class="mb-3">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-globe me-1"></i>POSITIONNEMENT SECTORIEL
              </div>
              <div class="row g-2 mb-2">
                <div class="col-6 col-md-3">
                  <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                    <div class="fw-bold" [style.color]="scoreColor(evaluation.globalScore)">
                      {{ evaluation.globalScore | number:'1.0-0' }}
                    </div>
                    <div style="font-size:.7rem;color:#6b7280;">Votre score</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                    <div class="fw-bold text-warning">{{ benchmark.sector_benchmark.national_average | number:'1.0-0' }}</div>
                    <div style="font-size:.7rem;color:#6b7280;">Moy. nationale</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                    <div class="fw-bold text-primary">{{ benchmark.sector_benchmark.international_average | number:'1.0-0' }}</div>
                    <div style="font-size:.7rem;color:#6b7280;">Moy. internationale</div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                    <div class="fw-bold text-success">{{ benchmark.sector_benchmark.top_quartile_score | number:'1.0-0' }}</div>
                    <div style="font-size:.7rem;color:#6b7280;">Top quartile</div>
                  </div>
                </div>
              </div>
              <div class="d-flex align-items-center gap-2">
                <span class="badge rounded-pill px-3 py-2"
                      [style.background]="positionColor(benchmark.sector_benchmark.positioning_label)"
                      style="color:#fff;">
                  <i class="fas fa-map-marker-alt me-1"></i>
                  {{ benchmark.sector_benchmark.positioning_label }}
                  — {{ benchmark.sector_benchmark.company_percentile }}e percentile
                </span>
                <small class="text-muted">Source : {{ benchmark.sector_benchmark.source }}</small>
              </div>
            </div>

            <!-- Axis benchmarks -->
            <div *ngIf="benchmark.axis_benchmarks?.length" class="mb-3">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-th-list me-1"></i>GAPS PAR AXE VS BENCHMARK
              </div>
              <div *ngFor="let ab of benchmark.axis_benchmarks" class="mb-2">
                <div class="d-flex justify-content-between small mb-1">
                  <span class="fw-semibold">
                    <i class="me-1" [ngClass]="axisIcon(ab.axis)"></i>{{ ab.axis_label }}
                  </span>
                  <span class="text-muted">
                    Vous: <strong [style.color]="scoreColor(ab.company_score)">{{ ab.company_score | number:'1.0-0' }}</strong>
                    &nbsp;|&nbsp;Secteur: <strong>{{ ab.sector_average | number:'1.0-0' }}</strong>
                    &nbsp;|&nbsp;Top: <strong class="text-success">{{ ab.top_quartile | number:'1.0-0' }}</strong>
                  </span>
                </div>
                <div class="position-relative axis-bar">
                  <div class="position-absolute top-0 bottom-0" style="width:2px;background:#fd7e14;z-index:2;"
                       [style.left.%]="ab.sector_average"></div>
                  <div class="position-absolute top-0 bottom-0" style="width:2px;background:#198754;z-index:2;"
                       [style.left.%]="ab.top_quartile"></div>
                  <div class="axis-fill" [style.width.%]="ab.company_score" [style.background]="axisColor(ab.axis)"></div>
                </div>
                <div class="d-flex gap-3 mt-1" style="font-size:.68rem;color:#9ca3af;">
                  <span style="color:#fd7e14;">▏ Moy. secteur</span>
                  <span style="color:#198754;">▏ Top quartile</span>
                  <span *ngIf="ab.gap_to_average > 0" class="text-danger">Gap moy.: -{{ ab.gap_to_average | number:'1.0-0' }} pts</span>
                  <span *ngIf="ab.gap_to_average <= 0" class="text-success">+{{ (-ab.gap_to_average) | number:'1.0-0' }} pts au-dessus</span>
                </div>
              </div>
            </div>

            <!-- Trends -->
            <div *ngIf="benchmark.trends?.length" class="mb-3">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-bolt me-1"></i>TENDANCES SECTORIELLES
              </div>
              <div *ngFor="let trend of benchmark.trends"
                   class="d-flex gap-3 p-3 rounded-3 mb-2"
                   style="background:#f8fafc;border:1px solid #e2e8f0;">
                <div class="flex-shrink-0">
                  <span class="badge rounded-pill" [style.background]="impactColor(trend.impact_level)">
                    {{ trend.impact_level }}
                  </span>
                </div>
                <div>
                  <div class="fw-semibold small">{{ trend.title }}</div>
                  <div class="text-muted small mt-1">{{ trend.description }}</div>
                  <div class="mt-1 d-flex gap-2 flex-wrap" style="font-size:.7rem;">
                    <span class="text-muted"><i class="fas fa-clock me-1"></i>{{ trend.horizon }}</span>
                    <span *ngIf="trend.adoption_rate" class="text-muted"><i class="fas fa-chart-pie me-1"></i>{{ trend.adoption_rate }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sector leaders — 3-level hierarchy -->
            <div *ngIf="benchmark.sector_leaders?.length" class="mb-3">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-trophy me-1"></i>LEADERS DU SECTEUR
              </div>
              <div *ngFor="let group of leadersByLevel()" class="mb-3">
                <div class="small fw-semibold mb-2 d-flex align-items-center gap-1"
                     [style.color]="group.color">
                  <i [class]="group.icon"></i> {{ group.label }}
                </div>
                <div class="row g-2">
                  <div *ngFor="let leader of group.leaders" class="col-md-4">
                    <div class="p-3 rounded-3 h-100"
                         [style.background]="group.bg"
                         [style.border]="'1px solid ' + group.border">
                      <div class="d-flex align-items-center gap-2 mb-2">
                        <div class="text-white rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                             [style.background]="group.color"
                             style="width:32px;height:32px;font-size:.75rem;font-weight:700;">
                          {{ leader.estimated_score }}
                        </div>
                        <div>
                          <div class="fw-bold small">{{ leader.company }}</div>
                          <div style="font-size:.7rem;color:#6b7280;">{{ leader.country }}</div>
                        </div>
                      </div>
                      <div class="small text-muted">{{ leader.key_practice }}</div>
                      <div *ngIf="leader.differentiator" class="mt-1 small" [style.color]="group.color">
                        <i class="fas fa-star me-1"></i>{{ leader.differentiator }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Roadmap -->
            <div *ngIf="benchmark.improvement_roadmap?.length">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-route me-1"></i>FEUILLE DE ROUTE D'AMÉLIORATION
              </div>
              <div *ngFor="let phase of benchmark.improvement_roadmap; let i = index" class="d-flex gap-3 mb-3">
                <div class="flex-shrink-0 d-flex flex-column align-items-center">
                  <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold"
                       style="width:32px;height:32px;font-size:.8rem;"
                       [style.background]="['#6366f1','#0891b2','#059669'][i] || '#6c757d'">
                    {{ i + 1 }}
                  </div>
                  <div *ngIf="i < benchmark.improvement_roadmap.length - 1"
                       style="width:2px;flex:1;min-height:20px;background:#e2e8f0;margin-top:4px;"></div>
                </div>
                <div class="pb-2">
                  <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
                    <span class="fw-bold small">{{ phase.phase }}</span>
                    <span class="badge rounded-pill" style="font-size:.65rem;"
                          [style.background]="investmentColor(phase.investment_level)">
                      Investissement {{ phase.investment_level }}
                    </span>
                    <span class="badge rounded-pill bg-success" style="font-size:.65rem;">{{ phase.expected_score_gain }}</span>
                  </div>
                  <div class="text-muted small mb-1">{{ phase.objective }}</div>
                  <ul class="mb-0 ps-3" style="font-size:.78rem;color:#4b5563;">
                    <li *ngFor="let action of phase.actions">{{ action }}</li>
                  </ul>
                  <div class="mt-1 small" style="color:#059669;">
                    <i class="fas fa-flag me-1"></i>Cible : {{ phase.target_level }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Key insights -->
            <div *ngIf="benchmark.key_insights?.length" class="mt-2">
              <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                <i class="fas fa-lightbulb me-1"></i>INSIGHTS CLÉS
              </div>
              <ul class="mb-0 ps-3" style="font-size:.82rem;">
                <li *ngFor="let insight of benchmark.key_insights" class="text-muted mb-1">{{ insight }}</li>
              </ul>
            </div>

          </div>
        </div>

      </ng-container>
    </div>
  `
})
export class ScoreViewComponent implements OnInit {
  isLoading = true;
  evaluation: any = null;
  currentUser: any = null;

  showRecs = false;
  recsLoading = false;
  recommendations: any[] = [];

  showBenchmark = false;
  benchmarkLoading = false;
  benchmark: any = null;
  benchmarkError = false;

  maturitySteps = [
    { key: 'INITIAL',       label: 'Initial',   color: '#dc3545' },
    { key: 'BASIQUE',       label: 'Basique',   color: '#fd7e14' },
    { key: 'INTERMEDIAIRE', label: 'Interm.',   color: '#ffc107' },
    { key: 'AVANCE',        label: 'Avancé',    color: '#0d6efd' },
    { key: 'OPTIMISE',      label: 'Optimisé',  color: '#198754' }
  ];

  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private authService: AuthService) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    const companyId = this.currentUser?.companyId;
    if (!companyId) { this.isLoading = false; return; }

    this.http.get<any>(`${this.apiUrl}/evaluations/latest?companyId=${companyId}`).pipe(
      catchError(() => of(null))
    ).subscribe(ev => {
      this.evaluation = ev;
      this.isLoading = false;
    });
  }

  toggleRecs() {
    if (this.showRecs) { this.showRecs = false; return; }
    if (this.recommendations.length) { this.showRecs = true; return; }
    this.recsLoading = true;
    this.http.get<any[]>(`${this.apiUrl}/evaluations/${this.evaluation.evaluationId}/recommendations`).pipe(
      catchError(() => of([]))
    ).subscribe(recs => {
      this.recommendations = recs;
      this.recsLoading = false;
      this.showRecs = true;
    });
  }

  toggleBenchmark() {
    if (this.showBenchmark) { this.showBenchmark = false; return; }
    if (this.benchmark || this.benchmarkError) { this.showBenchmark = true; return; }
    this.benchmarkLoading = true;
    this.benchmarkError = false;
    this.http.get<any>(`${this.apiUrl}/evaluations/${this.evaluation.evaluationId}/benchmark`).pipe(
      catchError(() => of(null))
    ).subscribe(data => {
      this.benchmark = data;
      this.benchmarkError = !data;
      this.benchmarkLoading = false;
      this.showBenchmark = true;
    });
  }

  retryBenchmark() {
    this.benchmark = null;
    this.benchmarkError = false;
    this.showBenchmark = false;
    this.toggleBenchmark();
  }

  dashArray(score?: number): string {
    if (score == null) return '0 314';
    const c = 2 * Math.PI * 50;
    return `${(score / 100) * c} ${c - (score / 100) * c}`;
  }

  scoreColor(score?: number): string {
    if (score == null) return '#9ca3af';
    if (score >= 75) return '#198754';
    if (score >= 50) return '#fd7e14';
    return '#dc3545';
  }

  maturityLabel(level: string): string {
    return this.maturitySteps.find(s => s.key === level)?.label || level;
  }

  maturityBadge(level: string): string {
    const m: any = { INITIAL:'bg-danger', BASIQUE:'bg-warning text-dark',
      INTERMEDIAIRE:'bg-info text-dark', AVANCE:'bg-primary', OPTIMISE:'bg-success' };
    return m[level] || 'bg-secondary';
  }

  isMaturityActive(level: string, idx: number): boolean {
    const active = this.maturitySteps.findIndex(s => s.key === level);
    return idx <= active;
  }

  axisLabel(a: string): string {
    const m: any = { METIER:'Métier', PROCESSUS:'Processus', SI:"Système d'info" };
    return m[a] || a;
  }

  axisIcon(a: string): string {
    const m: any = { METIER:'fas fa-briefcase', PROCESSUS:'fas fa-cogs', SI:'fas fa-server' };
    return m[a] || 'fas fa-chart-bar';
  }

  axisColor(a: string): string {
    const m: any = { METIER:'#6366f1', PROCESSUS:'#059669', SI:'#0891b2' };
    return m[a] || '#6c757d';
  }

  groupByAxis(recs: any[]) {
    return ['METIER','PROCESSUS','SI']
      .map(axis => ({ axis, items: recs.filter(r => r.axis === axis) }))
      .filter(g => g.items.length > 0);
  }

  priorityColor(p: string): string {
    const m: any = { HAUTE:'#dc3545', MOYENNE:'#fd7e14', BASSE:'#6c757d' };
    return m[p] || '#6c757d';
  }

  priorityBg(p: string): string {
    const m: any = { HAUTE:'#fff5f5', MOYENNE:'#fff8f1', BASSE:'#f9fafb' };
    return m[p] || '#f9fafb';
  }

  positionColor(label: string): string {
    if (!label) return '#6c757d';
    if (label.includes('Top')) return '#198754';
    if (label.includes('dessus')) return '#0d6efd';
    if (label.includes('moyenne')) return '#fd7e14';
    return '#dc3545';
  }

  impactColor(level: string): string {
    const m: any = { ELEVE:'#dc3545', MOYEN:'#fd7e14', FAIBLE:'#6c757d' };
    return m[level] || '#6c757d';
  }

  investmentColor(level: string): string {
    const m: any = { 'Faible':'#198754', 'Modéré':'#fd7e14', 'Élevé':'#dc3545' };
    return m[level] || '#6c757d';
  }

  leadersByLevel(): { level: string; label: string; icon: string; color: string; bg: string; border: string; leaders: any[] }[] {
    const all: any[] = this.benchmark?.sector_leaders || [];
    const groups = [
      { level: 'NATIONAL',  label: 'Leaders Nationaux',    icon: 'fas fa-flag',   color: '#0891b2', bg: 'linear-gradient(135deg,#f0f9ff,#e0f2fe)', border: '#bae6fd' },
      { level: 'REGIONAL',  label: 'Leaders Régionaux',    icon: 'fas fa-globe-africa', color: '#7c3aed', bg: 'linear-gradient(135deg,#faf5ff,#ede9fe)', border: '#ddd6fe' },
      { level: 'GLOBAL',    label: 'Leaders Mondiaux',     icon: 'fas fa-trophy', color: '#059669', bg: 'linear-gradient(135deg,#f0fdf4,#dcfce7)', border: '#bbf7d0' },
    ];
    return groups
      .map(g => ({ ...g, leaders: all.filter(l => (l.level || 'GLOBAL') === g.level) }))
      .filter(g => g.leaders.length > 0);
  }
}
