import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { CompanyService } from '../../../core/services/company.service';

interface CompanyReport {
  company: any;
  evaluation: any | null;
  recommendations: any[];
  showRecs: boolean;
  loading: boolean;
  benchmark: any | null;
  benchmarkError: boolean;
  showBenchmark: boolean;
  benchmarkLoading: boolean;
}

@Component({
  selector: 'app-consultant-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  styles: [`
    .stat-card { border-radius: 16px; transition: transform .15s; }
    .stat-card:hover { transform: translateY(-3px); }

    .company-card { border-radius: 16px; overflow: hidden; transition: box-shadow .2s; }
    .company-card:hover { box-shadow: 0 8px 30px rgba(0,0,0,.12) !important; }

    .accent-bar { width: 5px; border-radius: 3px; flex-shrink: 0; }

    .maturity-step {
      width: 28px; height: 28px; border-radius: 50%; border: 2px solid #dee2e6;
      display: flex; align-items: center; justify-content: center;
      font-size: 10px; font-weight: 700; color: #adb5bd;
      background: #fff; position: relative; z-index: 1;
    }
    .maturity-step.active { border-color: currentColor; color: #fff; }
    .maturity-line { height: 2px; flex: 1; background: #dee2e6; margin-top: 13px; }
    .maturity-line.active { background: linear-gradient(90deg, var(--start), var(--end)); }

    .axis-bar { height: 10px; border-radius: 5px; background: #e9ecef; overflow: hidden; }
    .axis-fill { height: 100%; border-radius: 5px; transition: width .6s ease; }

    .rec-item { border-radius: 10px; border-left: 4px solid transparent; }

    .badge-haute { background: #dc3545; }
    .badge-moyenne { background: #fd7e14; }
    .badge-basse { background: #6c757d; }

    .filter-btn { border-radius: 20px; padding: 4px 14px; font-size: .8rem; }
    .filter-btn.active { font-weight: 600; }

    .gauge-track { fill: none; stroke: #e9ecef; }
    .gauge-fill  { fill: none; stroke-linecap: round; transition: stroke-dasharray .7s ease; }
  `],
  template: `
    <div class="container-fluid py-4 px-4" style="max-width:1200px;margin:auto;">

      <!-- ── Page header ── -->
      <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-2">
        <div>
          <h3 class="fw-bold mb-0">Analyse des entreprises</h3>
          <small class="text-muted">Scores · Recommandations IA · Complétude des questionnaires</small>
        </div>
        <a routerLink="/consultant/dashboard" class="btn btn-outline-secondary btn-sm rounded-pill px-3">
          <i class="fas fa-arrow-left me-1"></i>Dashboard
        </a>
      </div>

      <!-- ── Loading ── -->
      <div *ngIf="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" style="width:3rem;height:3rem;"></div>
        <p class="text-muted mt-2">Chargement des données…</p>
      </div>

      <ng-container *ngIf="!isLoading">

        <!-- ── KPI row ── -->
        <div class="row g-3 mb-4">
          <div class="col-6 col-md-3">
            <div class="stat-card p-3 text-center" style="background:linear-gradient(135deg,#e3f2fd,#bbdefb);border:none;">
              <div class="fs-1 fw-bold text-primary">{{ reports.length }}</div>
              <div class="small text-primary fw-semibold">Entreprises</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="stat-card p-3 text-center" style="background:linear-gradient(135deg,#e8f5e9,#c8e6c9);border:none;">
              <div class="fs-1 fw-bold text-success">{{ completedCount }}</div>
              <div class="small text-success fw-semibold">Complétés</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="stat-card p-3 text-center" style="background:linear-gradient(135deg,#fff8e1,#ffecb3);border:none;">
              <div class="fs-1 fw-bold text-warning">{{ inProgressCount }}</div>
              <div class="small text-warning fw-semibold">En cours</div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="stat-card p-3 text-center" style="background:linear-gradient(135deg,#f3f4f6,#e5e7eb);border:none;">
              <div class="fs-1 fw-bold text-secondary">{{ notStartedCount }}</div>
              <div class="small text-secondary fw-semibold">Non commencés</div>
            </div>
          </div>
        </div>

        <!-- ── Filters + search ── -->
        <div class="d-flex align-items-center gap-2 mb-4 flex-wrap">
          <div class="input-group" style="max-width:260px;">
            <span class="input-group-text bg-white border-end-0">
              <i class="fas fa-search text-muted"></i>
            </span>
            <input type="text" class="form-control border-start-0 ps-0"
                   placeholder="Rechercher une entreprise…"
                   [(ngModel)]="searchTerm">
          </div>
          <button *ngFor="let f of filters"
                  class="btn btn-sm filter-btn"
                  [class.btn-primary]="activeFilter === f.value"
                  [class.btn-outline-secondary]="activeFilter !== f.value"
                  [class.active]="activeFilter === f.value"
                  (click)="activeFilter = f.value">
            {{ f.label }}
          </button>
        </div>

        <!-- ── Empty ── -->
        <div *ngIf="filtered.length === 0" class="text-center py-5 text-muted">
          <i class="fas fa-search fa-3x mb-3 opacity-25"></i>
          <p>Aucun résultat pour ces critères.</p>
        </div>

        <!-- ── Company cards ── -->
        <div *ngFor="let report of filtered" class="company-card card border-0 shadow-sm mb-4">

          <!-- Card header -->
          <div class="card-header border-0 py-3 px-4"
               style="background:linear-gradient(135deg,#f8f9fa,#fff);">
            <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
              <div class="d-flex align-items-center gap-3">
                <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 fw-bold text-white"
                     [style.background]="getCompanyColor(report.company.name)"
                     style="width:46px;height:46px;font-size:1.1rem;">
                  {{ report.company.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <div class="fw-bold fs-5">{{ report.company.name }}</div>
                  <div class="text-muted small">
                    <i class="fas fa-industry me-1"></i>{{ getSectorName(report.company.sector) }}
                    <span class="mx-1">·</span>
                    <i class="fas fa-users me-1"></i>{{ report.company.size || '—' }}
                    <span class="mx-1">·</span>
                    <i class="fas fa-map-marker-alt me-1"></i>{{ report.company.country || '—' }}
                  </div>
                </div>
              </div>
              <span class="badge rounded-pill px-3 py-2 fs-6"
                    [ngClass]="getStatusBadge(report.evaluation?.status)">
                <i class="me-1" [ngClass]="getStatusIcon(report.evaluation?.status)"></i>
                {{ getStatusLabel(report.evaluation?.status) }}
              </span>
            </div>

            <!-- Completion bar -->
            <div class="mt-3">
              <div class="d-flex justify-content-between small text-muted mb-1">
                <span><i class="fas fa-tasks me-1"></i>Complétude du questionnaire</span>
                <span class="fw-semibold">{{ getCompletionPct(report.evaluation) }}%</span>
              </div>
              <div class="progress" style="height:8px;border-radius:4px;">
                <div class="progress-bar"
                     [style.width.%]="getCompletionPct(report.evaluation)"
                     [ngClass]="getProgressColor(report.evaluation?.status)"
                     style="transition:width .7s ease;border-radius:4px;">
                </div>
              </div>
            </div>
          </div>

          <!-- Card body -->
          <div class="card-body px-4 py-3">

            <!-- No evaluation -->
            <div *ngIf="!report.evaluation"
                 class="d-flex align-items-center gap-3 py-3 text-muted">
              <i class="fas fa-clipboard-list fa-2x opacity-25"></i>
              <div>
                <div class="fw-semibold">Aucune évaluation disponible</div>
                <small>Cette entreprise n'a pas encore commencé le questionnaire.</small>
              </div>
            </div>

            <!-- Score + axes -->
            <div *ngIf="report.evaluation" class="row align-items-center g-4">

              <!-- Left: SVG Gauge -->
              <div class="col-md-4 text-center">
                <svg viewBox="0 0 120 120" style="width:140px;height:140px;">
                  <!-- Track -->
                  <circle class="gauge-track" cx="60" cy="60" r="50" stroke-width="12"/>
                  <!-- Fill -->
                  <circle class="gauge-fill"
                          cx="60" cy="60" r="50" stroke-width="12"
                          [attr.stroke]="getScoreStroke(report.evaluation.globalScore)"
                          [attr.stroke-dasharray]="getDashArray(report.evaluation.globalScore)"
                          transform="rotate(-90 60 60)"/>
                  <!-- Score number -->
                  <text x="60" y="54" text-anchor="middle"
                        font-size="22" font-weight="800"
                        [attr.fill]="getScoreStroke(report.evaluation.globalScore)">
                    {{ report.evaluation.globalScore != null ? (report.evaluation.globalScore | number:'1.0-0') : '—' }}
                  </text>
                  <text x="60" y="70" text-anchor="middle" font-size="10" fill="#9ca3af">/100</text>
                </svg>
                <div class="fw-semibold text-muted small mt-1">Score global</div>

                <!-- Maturity badge -->
                <span *ngIf="report.evaluation.maturityLevel"
                      class="badge rounded-pill px-3 py-2 mt-2"
                      [ngClass]="getMaturityBadge(report.evaluation.maturityLevel)">
                  <i class="fas fa-star me-1"></i>
                  {{ getMaturityLabel(report.evaluation.maturityLevel) }}
                </span>
              </div>

              <!-- Right: Axes + Maturity stepper -->
              <div class="col-md-8">

                <!-- Maturity stepper -->
                <div *ngIf="report.evaluation.maturityLevel" class="mb-3">
                  <div class="small text-muted fw-semibold mb-2">Niveau de maturité</div>
                  <div class="d-flex align-items-center">
                    <ng-container *ngFor="let step of maturitySteps; let i = index; let last = last">
                      <div class="maturity-step"
                           [class.active]="isMaturityActive(report.evaluation.maturityLevel, i)"
                           [style.background]="isMaturityActive(report.evaluation.maturityLevel, i) ? step.color : ''"
                           [style.border-color]="isMaturityActive(report.evaluation.maturityLevel, i) ? step.color : ''"
                           [style.color]="isMaturityActive(report.evaluation.maturityLevel, i) ? '#fff' : ''"
                           [title]="step.label">
                        {{ i + 1 }}
                      </div>
                      <div *ngIf="!last" class="maturity-line flex-grow-1"
                           [style.background]="isMaturityActive(report.evaluation.maturityLevel, i + 1) ? step.color : '#dee2e6'">
                      </div>
                    </ng-container>
                  </div>
                  <div class="d-flex justify-content-between mt-1" style="font-size:9px;color:#9ca3af;">
                    <span *ngFor="let step of maturitySteps">{{ step.label }}</span>
                  </div>
                </div>

                <!-- Axis scores -->
                <div class="small text-muted fw-semibold mb-2">Scores par axe</div>
                <div *ngFor="let axis of report.evaluation.scoresByAxis || []" class="mb-2">
                  <div class="d-flex justify-content-between small mb-1">
                    <span class="fw-semibold">
                      <i class="me-1" [ngClass]="getAxisIcon(axis.axis)"></i>
                      {{ getAxisLabel(axis.axis) }}
                    </span>
                    <span class="fw-bold" [style.color]="getAxisFill(axis.axis)">
                      {{ axis.score | number:'1.0-0' }}%
                    </span>
                  </div>
                  <div class="axis-bar">
                    <div class="axis-fill" [style.width.%]="axis.score" [style.background]="getAxisFill(axis.axis)"></div>
                  </div>
                </div>
                <div *ngIf="!report.evaluation.scoresByAxis?.length" class="text-muted small">
                  Scores par axe non disponibles.
                </div>
              </div>
            </div>
          </div>

          <!-- Recommendations footer -->
          <div *ngIf="report.evaluation?.status === 'COMPLETED'" class="card-footer border-0 bg-white px-4 pb-4 pt-0">
            <button class="btn btn-sm rounded-pill px-3"
                    [class.btn-outline-primary]="!report.showRecs"
                    [class.btn-primary]="report.showRecs"
                    (click)="toggleRecs(report)"
                    [disabled]="report.loading">
              <span *ngIf="report.loading" class="spinner-border spinner-border-sm me-1"></span>
              <i *ngIf="!report.loading" class="fas fa-robot me-1"></i>
              {{ report.showRecs ? 'Masquer' : 'Afficher' }} les recommandations IA
              <span *ngIf="report.recommendations.length" class="badge bg-white text-primary ms-1">
                {{ report.recommendations.length }}
              </span>
            </button>

            <!-- Recommendations list -->
            <div *ngIf="report.showRecs" class="mt-3">
              <div *ngIf="!report.recommendations.length && !report.loading"
                   class="text-muted small text-center py-2">
                Aucune recommandation disponible.
              </div>

              <!-- Group by axis -->
              <ng-container *ngFor="let axisGroup of groupByAxis(report.recommendations)">
                <div class="small fw-bold text-uppercase mb-2 mt-3" style="letter-spacing:.08em;"
                     [style.color]="getAxisFill(axisGroup.axis)">
                  <i class="me-1" [ngClass]="getAxisIcon(axisGroup.axis)"></i>
                  {{ getAxisLabel(axisGroup.axis) }}
                </div>
                <div *ngFor="let rec of axisGroup.items" class="rec-item p-3 mb-2"
                     [style.border-left-color]="getPriorityColor(rec.priority)"
                     [style.background]="getPriorityBg(rec.priority)">
                  <div class="d-flex align-items-start gap-2">
                    <span class="badge rounded-pill flex-shrink-0 mt-1" [style.background]="getPriorityColor(rec.priority)">
                      {{ rec.priority }}
                    </span>
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

            <!-- ── Benchmark button ── -->
            <div class="mt-3 pt-3 border-top">
              <button class="btn btn-sm rounded-pill px-3"
                      [class.btn-outline-success]="!report.showBenchmark"
                      [class.btn-success]="report.showBenchmark"
                      (click)="toggleBenchmark(report)"
                      [disabled]="report.benchmarkLoading">
                <span *ngIf="report.benchmarkLoading" class="spinner-border spinner-border-sm me-1"></span>
                <i *ngIf="!report.benchmarkLoading" class="fas fa-chart-bar me-1"></i>
                {{ report.showBenchmark ? 'Masquer' : 'Voir' }} le benchmarking sectoriel
              </button>

              <!-- ── Benchmark panel ── -->
              <div *ngIf="report.showBenchmark" class="mt-3">

                <!-- Error / unavailable state -->
                <div *ngIf="report.benchmarkError || !report.benchmark"
                     class="d-flex align-items-start gap-3 p-3 rounded-3"
                     style="background:#fff8e1;border:1px solid #ffc107;">
                  <i class="fas fa-exclamation-triangle text-warning fs-5 mt-1"></i>
                  <div>
                    <div class="fw-semibold text-warning small">Service de benchmarking indisponible</div>
                    <div class="text-muted small mt-1">
                      Assurez-vous que le service IA Python est en cours d'exécution
                      (<code style="font-size:.75rem;">uvicorn main:app --port 8000</code>), puis réessayez.
                    </div>
                    <button class="btn btn-sm btn-outline-warning mt-2 rounded-pill" (click)="retryBenchmark(report)">
                      <i class="fas fa-redo me-1"></i>Réessayer
                    </button>
                  </div>
                </div>

              </div>
              <div *ngIf="report.showBenchmark && report.benchmark" class="mt-3">

                <!-- Executive summary -->
                <div class="rounded-3 p-3 mb-3" style="background:#f0fdf4;border-left:4px solid #198754;">
                  <div class="small fw-bold text-success mb-1" style="letter-spacing:.06em;">
                    <i class="fas fa-file-alt me-1"></i>SYNTHÈSE EXÉCUTIVE
                  </div>
                  <p class="mb-0 small text-muted">{{ report.benchmark.executive_summary }}</p>
                </div>

                <!-- Sector positioning -->
                <div *ngIf="report.benchmark.sector_benchmark" class="mb-3">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-globe me-1"></i>POSITIONNEMENT SECTORIEL
                  </div>
                  <div class="row g-2 mb-2">
                    <div class="col-6 col-md-3">
                      <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                        <div class="fw-bold" [style.color]="getScoreStroke(report.evaluation.globalScore)">
                          {{ report.evaluation.globalScore | number:'1.0-0' }}
                        </div>
                        <div style="font-size:.7rem;color:#6b7280;">Score entreprise</div>
                      </div>
                    </div>
                    <div class="col-6 col-md-3">
                      <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                        <div class="fw-bold text-warning">{{ report.benchmark.sector_benchmark.national_average | number:'1.0-0' }}</div>
                        <div style="font-size:.7rem;color:#6b7280;">Moy. nationale</div>
                      </div>
                    </div>
                    <div class="col-6 col-md-3">
                      <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                        <div class="fw-bold text-primary">{{ report.benchmark.sector_benchmark.international_average | number:'1.0-0' }}</div>
                        <div style="font-size:.7rem;color:#6b7280;">Moy. internationale</div>
                      </div>
                    </div>
                    <div class="col-6 col-md-3">
                      <div class="rounded-3 p-2 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;">
                        <div class="fw-bold text-success">{{ report.benchmark.sector_benchmark.top_quartile_score | number:'1.0-0' }}</div>
                        <div style="font-size:.7rem;color:#6b7280;">Top quartile</div>
                      </div>
                    </div>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <span class="badge rounded-pill px-3 py-2"
                          [style.background]="getBenchmarkPositionColor(report.benchmark.sector_benchmark.positioning_label)"
                          style="color:#fff;">
                      <i class="fas fa-map-marker-alt me-1"></i>
                      {{ report.benchmark.sector_benchmark.positioning_label }}
                      — {{ report.benchmark.sector_benchmark.company_percentile }}e percentile
                    </span>
                    <small class="text-muted">Source : {{ report.benchmark.sector_benchmark.source }}</small>
                  </div>
                </div>

                <!-- Axis benchmarks -->
                <div *ngIf="report.benchmark.axis_benchmarks?.length" class="mb-3">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-th-list me-1"></i>GAPS PAR AXE VS BENCHMARK
                  </div>
                  <div *ngFor="let ab of report.benchmark.axis_benchmarks" class="mb-2">
                    <div class="d-flex justify-content-between small mb-1">
                      <span class="fw-semibold">
                        <i class="me-1" [ngClass]="getAxisIcon(ab.axis)"></i>{{ ab.axis_label }}
                      </span>
                      <span class="text-muted">
                        Entreprise: <strong [style.color]="getScoreStroke(ab.company_score)">{{ ab.company_score | number:'1.0-0' }}</strong>
                        &nbsp;|&nbsp;Secteur: <strong>{{ ab.sector_average | number:'1.0-0' }}</strong>
                        &nbsp;|&nbsp;Top: <strong class="text-success">{{ ab.top_quartile | number:'1.0-0' }}</strong>
                      </span>
                    </div>
                    <div class="position-relative axis-bar">
                      <!-- Sector average marker -->
                      <div class="position-absolute top-0 bottom-0" style="width:2px;background:#fd7e14;z-index:2;"
                           [style.left.%]="ab.sector_average"></div>
                      <!-- Top quartile marker -->
                      <div class="position-absolute top-0 bottom-0" style="width:2px;background:#198754;z-index:2;"
                           [style.left.%]="ab.top_quartile"></div>
                      <!-- Company fill -->
                      <div class="axis-fill" [style.width.%]="ab.company_score" [style.background]="getAxisFill(ab.axis)"></div>
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
                <div *ngIf="report.benchmark.trends?.length" class="mb-3">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-bolt me-1"></i>TENDANCES SECTORIELLES (2024-2025)
                  </div>
                  <div *ngFor="let trend of report.benchmark.trends"
                       class="d-flex gap-3 p-3 rounded-3 mb-2"
                       style="background:#f8fafc;border:1px solid #e2e8f0;">
                    <div class="flex-shrink-0">
                      <span class="badge rounded-pill" [style.background]="getImpactColor(trend.impact_level)">
                        {{ trend.impact_level }}
                      </span>
                    </div>
                    <div>
                      <div class="fw-semibold small">{{ trend.title }}</div>
                      <div class="text-muted small mt-1">{{ trend.description }}</div>
                      <div class="mt-1 d-flex gap-2 flex-wrap" style="font-size:.7rem;">
                        <span class="text-muted"><i class="fas fa-clock me-1"></i>{{ trend.horizon }}</span>
                        <span *ngIf="trend.adoption_rate" class="text-muted"><i class="fas fa-chart-pie me-1"></i>Adoption: {{ trend.adoption_rate }}</span>
                        <span *ngIf="trend.source" class="text-muted"><i class="fas fa-book me-1"></i>{{ trend.source }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Sector leaders — 3-level hierarchy -->
                <div *ngIf="report.benchmark.sector_leaders?.length" class="mb-3">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-trophy me-1"></i>LEADERS DU SECTEUR
                  </div>
                  <div *ngFor="let group of leadersByLevel(report.benchmark)" class="mb-3">
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
                <div *ngIf="report.benchmark.improvement_roadmap?.length">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-route me-1"></i>FEUILLE DE ROUTE D'AMÉLIORATION
                  </div>
                  <div *ngFor="let phase of report.benchmark.improvement_roadmap; let i = index"
                       class="d-flex gap-3 mb-3">
                    <div class="flex-shrink-0 d-flex flex-column align-items-center">
                      <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold"
                           style="width:32px;height:32px;font-size:.8rem;"
                           [style.background]="['#6366f1','#0891b2','#059669'][i] || '#6c757d'">
                        {{ i + 1 }}
                      </div>
                      <div *ngIf="i < report.benchmark.improvement_roadmap.length - 1"
                           style="width:2px;flex:1;min-height:20px;background:#e2e8f0;margin-top:4px;"></div>
                    </div>
                    <div class="pb-2">
                      <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
                        <span class="fw-bold small">{{ phase.phase }}</span>
                        <span class="badge rounded-pill" style="font-size:.65rem;"
                              [style.background]="getInvestmentColor(phase.investment_level)">
                          Investissement {{ phase.investment_level }}
                        </span>
                        <span class="badge rounded-pill bg-success" style="font-size:.65rem;">
                          {{ phase.expected_score_gain }}
                        </span>
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
                <div *ngIf="report.benchmark.key_insights?.length" class="mt-2">
                  <div class="small fw-bold mb-2" style="color:#059669;letter-spacing:.06em;">
                    <i class="fas fa-lightbulb me-1"></i>INSIGHTS CLÉS
                  </div>
                  <ul class="mb-0 ps-3" style="font-size:.82rem;">
                    <li *ngFor="let insight of report.benchmark.key_insights" class="text-muted mb-1">
                      {{ insight }}
                    </li>
                  </ul>
                </div>

              </div>
            </div>

          </div>

        </div>
      </ng-container>
    </div>
  `
})
export class ConsultantAnalysisComponent implements OnInit {
  reports: CompanyReport[] = [];
  isLoading = true;
  searchTerm = '';
  activeFilter = 'ALL';

  filters = [
    { label: 'Tous', value: 'ALL' },
    { label: 'Complétés', value: 'COMPLETED' },
    { label: 'En cours', value: 'IN_PROGRESS' },
    { label: 'Non commencés', value: 'NONE' }
  ];

  maturitySteps = [
    { key: 'INITIAL',       label: 'Initial',       color: '#dc3545' },
    { key: 'BASIQUE',       label: 'Basique',       color: '#fd7e14' },
    { key: 'INTERMEDIAIRE', label: 'Interm.',       color: '#ffc107' },
    { key: 'AVANCE',        label: 'Avancé',        color: '#0d6efd' },
    { key: 'OPTIMISE',      label: 'Optimisé',      color: '#198754' }
  ];

  private readonly apiUrl = environment.apiUrl;
  private companyColors = ['#6366f1','#0891b2','#059669','#d97706','#dc2626','#7c3aed','#db2777'];

  constructor(private http: HttpClient, private companyService: CompanyService) {}

  ngOnInit() {
    this.companyService.getCompanies().pipe(
      switchMap(companies => {
        if (!companies.length) return of([]);
        return forkJoin(
          companies.map(company =>
            this.http.get<any>(`${this.apiUrl}/evaluations/latest?companyId=${company.id}`).pipe(
              catchError(() => of(null)),
              switchMap(evaluation => of({ company, evaluation, recommendations: [], showRecs: false, loading: false, benchmark: null, benchmarkError: false, showBenchmark: false, benchmarkLoading: false } as CompanyReport))
            )
          )
        );
      })
    ).subscribe({
      next: (reports) => { this.reports = reports; this.isLoading = false; },
      error: () => { this.isLoading = false; }
    });
  }

  get filtered(): CompanyReport[] {
    return this.reports.filter(r => {
      const matchSearch = !this.searchTerm ||
        r.company.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchFilter =
        this.activeFilter === 'ALL' ||
        (this.activeFilter === 'NONE'      && !r.evaluation) ||
        (this.activeFilter !== 'NONE'      && r.evaluation?.status === this.activeFilter);
      return matchSearch && matchFilter;
    });
  }

  get completedCount()  { return this.reports.filter(r => r.evaluation?.status === 'COMPLETED').length; }
  get inProgressCount() { return this.reports.filter(r => r.evaluation?.status === 'IN_PROGRESS').length; }
  get notStartedCount() { return this.reports.filter(r => !r.evaluation).length; }

  toggleRecs(report: CompanyReport) {
    if (report.showRecs) { report.showRecs = false; return; }
    if (report.recommendations.length) { report.showRecs = true; return; }
    report.loading = true;
    this.http.get<any[]>(`${this.apiUrl}/evaluations/${report.evaluation.evaluationId}/recommendations`).pipe(
      catchError(() => of([]))
    ).subscribe(recs => {
      report.recommendations = recs;
      report.loading = false;
      report.showRecs = true;
    });
  }

  toggleBenchmark(report: CompanyReport) {
    if (report.showBenchmark) { report.showBenchmark = false; return; }
    if (report.benchmark || report.benchmarkError) { report.showBenchmark = true; return; }
    report.benchmarkLoading = true;
    report.benchmarkError = false;
    this.http.get<any>(`${this.apiUrl}/evaluations/${report.evaluation.evaluationId}/benchmark`).pipe(
      catchError(() => of(null))
    ).subscribe(data => {
      report.benchmark = data;
      report.benchmarkError = !data;
      report.benchmarkLoading = false;
      report.showBenchmark = true;
    });
  }

  retryBenchmark(report: CompanyReport) {
    report.benchmark = null;
    report.benchmarkError = false;
    report.showBenchmark = false;
    this.toggleBenchmark(report);
  }

  getBenchmarkPositionColor(label: string): string {
    if (!label) return '#6c757d';
    if (label.includes('Top')) return '#198754';
    if (label.includes('dessus')) return '#0d6efd';
    if (label.includes('moyenne')) return '#fd7e14';
    return '#dc3545';
  }

  getImpactColor(level: string): string {
    const map: any = { ELEVE: '#dc3545', MOYEN: '#fd7e14', FAIBLE: '#6c757d' };
    return map[level] || '#6c757d';
  }

  getInvestmentColor(level: string): string {
    const map: any = { 'Faible': '#198754', 'Modéré': '#fd7e14', 'Élevé': '#dc3545' };
    return map[level] || '#6c757d';
  }

  groupByAxis(recs: any[]): { axis: string; items: any[] }[] {
    const axes = ['METIER', 'PROCESSUS', 'SI'];
    return axes
      .map(axis => ({ axis, items: recs.filter(r => r.axis === axis) }))
      .filter(g => g.items.length > 0);
  }

  // ─── SVG gauge helpers ───
  getDashArray(score?: number): string {
    if (score == null) return '0 314';
    const c = 2 * Math.PI * 50; // r=50
    const filled = (score / 100) * c;
    return `${filled} ${c - filled}`;
  }

  getScoreStroke(score?: number): string {
    if (score == null) return '#9ca3af';
    if (score >= 75) return '#198754';
    if (score >= 50) return '#fd7e14';
    return '#dc3545';
  }

  // ─── Maturity stepper ───
  isMaturityActive(level: string, stepIndex: number): boolean {
    const idx = this.maturitySteps.findIndex(s => s.key === level);
    return stepIndex <= idx;
  }

  getMaturityLabel(level: string): string {
    return this.maturitySteps.find(s => s.key === level)?.label || level;
  }

  getMaturityBadge(level: string): string {
    const map: any = {
      INITIAL: 'bg-danger', BASIQUE: 'bg-warning text-dark',
      INTERMEDIAIRE: 'bg-info text-dark', AVANCE: 'bg-primary', OPTIMISE: 'bg-success'
    };
    return map[level] || 'bg-secondary';
  }

  // ─── Axis ───
  getAxisLabel(axis: string): string {
    const map: any = { METIER: 'Métier', PROCESSUS: 'Processus', SI: "Système d'info" };
    return map[axis] || axis;
  }

  getAxisIcon(axis: string): string {
    const map: any = { METIER: 'fas fa-briefcase', PROCESSUS: 'fas fa-cogs', SI: 'fas fa-server' };
    return map[axis] || 'fas fa-chart-bar';
  }

  getAxisFill(axis: string): string {
    const map: any = { METIER: '#6366f1', PROCESSUS: '#059669', SI: '#0891b2' };
    return map[axis] || '#6c757d';
  }

  // ─── Status ───
  getStatusLabel(status?: string): string {
    if (!status) return 'Non commencé';
    return status === 'COMPLETED' ? 'Complété' : 'En cours';
  }

  getStatusBadge(status?: string): string {
    if (!status) return 'bg-secondary';
    return status === 'COMPLETED' ? 'bg-success' : 'bg-warning text-dark';
  }

  getStatusIcon(status?: string): string {
    if (!status) return 'fas fa-minus-circle';
    return status === 'COMPLETED' ? 'fas fa-check-circle' : 'fas fa-clock';
  }

  getCompletionPct(eval_: any): number {
    if (!eval_) return 0;
    return eval_.status === 'COMPLETED' ? 100 : 50;
  }

  getProgressColor(status?: string): string {
    if (!status) return 'bg-secondary';
    return status === 'COMPLETED' ? 'bg-success' : 'bg-warning';
  }

  // ─── Recommendations ───
  getPriorityColor(p: string): string {
    const map: any = { HAUTE: '#dc3545', MOYENNE: '#fd7e14', BASSE: '#6c757d' };
    return map[p] || '#6c757d';
  }

  getPriorityBg(p: string): string {
    const map: any = { HAUTE: '#fff5f5', MOYENNE: '#fff8f1', BASSE: '#f9fafb' };
    return map[p] || '#f9fafb';
  }

  // ─── Company avatar color ───
  getCompanyColor(name: string): string {
    const i = name.charCodeAt(0) % this.companyColors.length;
    return this.companyColors[i];
  }

  // ─── Sector ───
  getSectorName(sector: string): string {
    const map: any = {
      banking:'Banque', insurance:'Assurance', industry:'Industrie',
      retail:'Commerce', healthcare:'Santé', education:'Éducation',
      tech:'Technologies', transport:'Transport', energy:'Énergie', construction:'Construction'
    };
    return map[sector] || sector || '—';
  }

  leadersByLevel(benchmark: any): { level: string; label: string; icon: string; color: string; bg: string; border: string; leaders: any[] }[] {
    const all: any[] = benchmark?.sector_leaders || [];
    const groups = [
      { level: 'NATIONAL', label: 'Leaders Nationaux',  icon: 'fas fa-flag',         color: '#0891b2', bg: 'linear-gradient(135deg,#f0f9ff,#e0f2fe)', border: '#bae6fd' },
      { level: 'REGIONAL', label: 'Leaders Régionaux',  icon: 'fas fa-globe-africa',  color: '#7c3aed', bg: 'linear-gradient(135deg,#faf5ff,#ede9fe)', border: '#ddd6fe' },
      { level: 'GLOBAL',   label: 'Leaders Mondiaux',   icon: 'fas fa-trophy',        color: '#059669', bg: 'linear-gradient(135deg,#f0fdf4,#dcfce7)', border: '#bbf7d0' },
    ];
    return groups
      .map(g => ({ ...g, leaders: all.filter(l => (l.level || 'GLOBAL') === g.level) }))
      .filter(g => g.leaders.length > 0);
  }
}
