import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface Recommendation {
  axis: string;
  priority: string;
  title: string;
  description: string;
  bestPractice: string;
  editing?: boolean;
}

interface AxisScore { axis: string; score: number; }
interface SubAxisScore { axis: string; subAxis: string; score: number; }
interface SectorBenchmark {
  nationalAverage: number; internationalAverage: number;
  topQuartileScore: number; companyPercentile: number;
  positioningLabel: string; source: string;
}
interface AxisBenchmark {
  axis: string; axisLabel: string; companyScore: number;
  sectorAverage: number; topQuartile: number;
  gapToAverage: number; gapToTop: number;
}
interface Trend { title: string; description: string; impactLevel: string; horizon: string; adoptionRate: string; source: string; }

@Component({
  selector: 'app-consultant-review',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width:980px;">

      <!-- Header -->
      <div class="d-flex align-items-center mb-4">
        <a routerLink="/consultant/dashboard" class="btn btn-sm btn-outline-secondary me-3">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </a>
        <div class="flex-grow-1">
          <h4 class="mb-0 fw-bold">Revue de l'évaluation</h4>
          <small class="text-muted">{{ companyName }} — Validez et envoyez les résultats</small>
        </div>
        <span *ngIf="pendingReview && !validated" class="badge bg-warning text-dark fs-6 px-3 py-2">En attente de validation</span>
        <span *ngIf="validated" class="badge bg-success fs-6 px-3 py-2">Envoyé</span>
      </div>

      <!-- Loading -->
      <div *ngIf="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Chargement des données…</p>
      </div>

      <!-- Error -->
      <div *ngIf="error && !loading" class="alert alert-danger">{{ error }}</div>

      <!-- AI Pending Banner -->
      <div *ngIf="!loading && !error && aiPending"
           class="alert border-0 rounded-3 mb-4 d-flex align-items-center gap-3"
           style="background:#fef9c3;border-left:4px solid #f59e0b !important;">
        <i class="fas fa-robot fa-lg" style="color:#d97706;"></i>
        <div class="flex-grow-1">
          <div class="fw-semibold" style="color:#92400e;">Analyses IA non générées</div>
          <div class="small text-muted">Les recommandations et le benchmarking n'ont pas encore été générés pour cette évaluation.</div>
        </div>
        <button class="btn btn-sm px-3 rounded-pill fw-semibold"
                style="background:#f59e0b;color:#fff;"
                (click)="generateInitial()"
                [disabled]="initialGenerating">
          <span *ngIf="initialGenerating" class="spinner-border spinner-border-sm me-2" style="width:12px;height:12px;"></span>
          <i *ngIf="!initialGenerating" class="fas fa-magic me-1"></i>
          {{ initialGenerating ? 'Génération en cours (1-2 min)…' : 'Générer les analyses IA' }}
        </button>
        <span *ngIf="initialGenerateError" class="text-danger small ms-2">{{ initialGenerateError }}</span>
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
                <div class="display-4 fw-black" style="color:#1768e5;">{{ globalScore | number:'1.0-1' }}</div>
                <div class="text-muted small">/100</div>
                <div class="badge mt-2 px-3 py-2 rounded-pill" style="background:#e8f0fe;color:#1768e5;font-size:13px;">
                  {{ maturityLevel }}
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
                  <span class="badge rounded-pill flex-shrink-0" style="font-size:10px;width:60px;text-align:center;"
                        [style.background]="getAxisColor(s.axis)+'20'" [style.color]="getAxisColor(s.axis)">
                    {{ s.axis }}
                  </span>
                  <span class="small text-muted flex-grow-1 text-truncate" style="max-width:160px;">{{ s.subAxis }}</span>
                  <div class="progress flex-grow-1 rounded-pill" style="height:6px;">
                    <div class="progress-bar rounded-pill" [style.width]="s.score+'%'" [style.background]="getAxisColor(s.axis)"></div>
                  </div>
                  <span class="small fw-bold" style="min-width:36px;text-align:right;">{{ s.score | number:'1.0-0' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ── TAB: RECOMMENDATIONS ── -->
        <div *ngIf="tab==='recs'">

          <!-- Consultant Prompt Panel -->
          <div class="card border-0 shadow-sm rounded-3 mb-4" style="border-left:4px solid #6366f1 !important;">
            <div class="card-body p-3">
              <div class="d-flex align-items-center gap-2 mb-0"
                   style="cursor:pointer;user-select:none;"
                   (click)="showPromptPanel = !showPromptPanel">
                <div class="rounded-2 d-flex align-items-center justify-content-center flex-shrink-0"
                     style="width:32px;height:32px;background:#ede9fe;">
                  <i class="fas fa-magic" style="color:#6366f1;font-size:13px;"></i>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold small" style="color:#4f46e5;">Régénérer avec directives IA</div>
                  <div class="text-muted" style="font-size:11px;">Donnez des instructions précises à l'IA pour personnaliser les recommandations</div>
                </div>
                <i class="fas text-muted"
                   [class.fa-chevron-down]="!showPromptPanel"
                   [class.fa-chevron-up]="showPromptPanel"></i>
              </div>

              <div *ngIf="showPromptPanel" class="mt-3">
                <textarea class="form-control form-control-sm mb-2"
                          rows="4"
                          [(ngModel)]="consultantPrompt"
                          [disabled]="regenerating"
                          placeholder="Ex : Cette entreprise migre vers Azure en 2026, priorisez les recommandations cloud et cybersécurité. L'axe Marketing est une priorité stratégique. Ignorer les recommandations RH pour l'instant."></textarea>
                <div class="d-flex align-items-center gap-2">
                  <button class="btn btn-sm px-3 rounded-pill"
                          style="background:#6366f1;color:#fff;"
                          (click)="regenerate()"
                          [disabled]="regenerating">
                    <span *ngIf="regenerating" class="spinner-border spinner-border-sm me-2" style="width:12px;height:12px;"></span>
                    <i *ngIf="!regenerating" class="fas fa-sync-alt me-1"></i>
                    {{ regenerating ? 'Génération en cours…' : 'Régénérer les recommandations' }}
                  </button>
                  <span *ngIf="regenerateError" class="text-danger small"><i class="fas fa-exclamation-circle me-1"></i>{{ regenerateError }}</span>
                  <span *ngIf="regenerateSuccess" class="text-success small"><i class="fas fa-check-circle me-1"></i>{{ regenerateSuccess }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="text-muted small">Modifiez, supprimez ou ajoutez des recommandations avant d'envoyer.</span>
            <button class="btn btn-outline-primary btn-sm" (click)="addRec()">
              <i class="fas fa-plus me-1"></i>Ajouter
            </button>
          </div>

          <div *ngIf="recommendations.length === 0" class="text-center text-muted py-5">
            <i class="fas fa-inbox fa-2x mb-3 d-block"></i>
            Aucune recommandation. L'IA n'a pas pu en générer ou elles ont été supprimées.
          </div>

          <div *ngFor="let r of recommendations; let i = index" class="card border-0 shadow-sm rounded-3 mb-3">
            <div class="card-body p-3">

              <!-- View mode -->
              <div *ngIf="!r.editing" class="d-flex gap-3 align-items-start">
                <div>
                  <span class="badge rounded-pill mb-1 d-block text-center" style="width:70px;font-size:11px;"
                        [style.background]="getPriorityColor(r.priority)+'20'" [style.color]="getPriorityColor(r.priority)">
                    {{ r.priority }}
                  </span>
                  <span class="badge rounded-pill" style="font-size:10px;width:70px;text-align:center;"
                        [style.background]="getAxisColor(r.axis)+'20'" [style.color]="getAxisColor(r.axis)">
                    {{ r.axis }}
                  </span>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold mb-1">{{ r.title }}</div>
                  <p class="text-muted small mb-1">{{ r.description }}</p>
                  <p class="text-muted small mb-0 fst-italic">{{ r.bestPractice }}</p>
                </div>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-secondary py-0 px-2" (click)="r.editing=true">
                    <i class="fas fa-pencil-alt" style="font-size:11px;"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger py-0 px-2" (click)="removeRec(i)">
                    <i class="fas fa-trash" style="font-size:11px;"></i>
                  </button>
                </div>
              </div>

              <!-- Edit mode -->
              <div *ngIf="r.editing">
                <div class="row g-2 mb-2">
                  <div class="col-4">
                    <select class="form-select form-select-sm" [(ngModel)]="r.axis">
                      <option value="METIER">Métier</option>
                      <option value="PROCESSUS">Processus</option>
                      <option value="SI">SI</option>
                      <option value="CANAUX_DISTRIBUTION">Canaux &amp; UX</option>
                      <option value="MARKETING_COMMUNICATION">Marketing &amp; Communication</option>
                      <option value="RH_CULTURE_DIGITALE">RH &amp; Culture Digitale</option>
                      <option value="OFFRES_DIGITALES">Offres Digitales</option>
                    </select>
                  </div>
                  <div class="col-4">
                    <select class="form-select form-select-sm" [(ngModel)]="r.priority">
                      <option value="HAUTE">HAUTE</option>
                      <option value="MOYENNE">MOYENNE</option>
                      <option value="BASSE">BASSE</option>
                    </select>
                  </div>
                  <div class="col-4 d-flex gap-1">
                    <button class="btn btn-success btn-sm flex-grow-1" (click)="r.editing=false"><i class="fas fa-check"></i></button>
                    <button class="btn btn-outline-danger btn-sm" (click)="removeRec(i)"><i class="fas fa-trash"></i></button>
                  </div>
                </div>
                <input class="form-control form-control-sm mb-2" [(ngModel)]="r.title" placeholder="Titre">
                <textarea class="form-control form-control-sm mb-2" rows="2" [(ngModel)]="r.description" placeholder="Description"></textarea>
                <input class="form-control form-control-sm" [(ngModel)]="r.bestPractice" placeholder="Référence / bonne pratique">
              </div>
            </div>
          </div>
        </div>

        <!-- ── TAB: BENCHMARKING ── -->
        <div *ngIf="tab==='bench'">

          <!-- Consultant Prompt Panel — Benchmarking -->
          <div class="card border-0 shadow-sm rounded-3 mb-4" style="border-left:4px solid #0891b2 !important;">
            <div class="card-body p-3">
              <div class="d-flex align-items-center gap-2 mb-0"
                   style="cursor:pointer;user-select:none;"
                   (click)="showBenchPromptPanel = !showBenchPromptPanel">
                <div class="rounded-2 d-flex align-items-center justify-content-center flex-shrink-0"
                     style="width:32px;height:32px;background:#e0f2fe;">
                  <i class="fas fa-magic" style="color:#0891b2;font-size:13px;"></i>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold small" style="color:#0369a1;">Régénérer le benchmarking avec directives IA</div>
                  <div class="text-muted" style="font-size:11px;">Orientez l'analyse comparative selon le contexte stratégique de l'entreprise</div>
                </div>
                <i class="fas text-muted"
                   [class.fa-chevron-down]="!showBenchPromptPanel"
                   [class.fa-chevron-up]="showBenchPromptPanel"></i>
              </div>

              <div *ngIf="showBenchPromptPanel" class="mt-3">
                <textarea class="form-control form-control-sm mb-2"
                          rows="4"
                          [(ngModel)]="benchConsultantPrompt"
                          [disabled]="benchRegenerating"
                          placeholder="Ex : Cette entreprise envisage une expansion en Europe en 2026. Comparez-la aux leaders européens du secteur et adaptez la feuille de route à ce contexte international."></textarea>
                <div class="d-flex align-items-center gap-2">
                  <button class="btn btn-sm px-3 rounded-pill"
                          style="background:#0891b2;color:#fff;"
                          (click)="regenerateBenchmark()"
                          [disabled]="benchRegenerating">
                    <span *ngIf="benchRegenerating" class="spinner-border spinner-border-sm me-2" style="width:12px;height:12px;"></span>
                    <i *ngIf="!benchRegenerating" class="fas fa-sync-alt me-1"></i>
                    {{ benchRegenerating ? 'Génération en cours…' : 'Régénérer le benchmarking' }}
                  </button>
                  <span *ngIf="benchRegenerateError" class="text-danger small"><i class="fas fa-exclamation-circle me-1"></i>{{ benchRegenerateError }}</span>
                  <span *ngIf="benchRegenerateSuccess" class="text-success small"><i class="fas fa-check-circle me-1"></i>{{ benchRegenerateSuccess }}</span>
                </div>
              </div>
            </div>
          </div>

          <div *ngIf="!benchmark" class="text-center text-muted py-5">
            <i class="fas fa-chart-line fa-2x mb-3 d-block"></i>
            Données de benchmarking non disponibles (service IA non accessible lors de la génération).
          </div>
          <div *ngIf="benchmark">
            <!-- Sector -->
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

            <!-- Axis comparison -->
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
                        <span [class]="ab.gapToAverage >= 0 ? 'text-success' : 'text-danger'">
                          {{ ab.gapToAverage >= 0 ? '+' : '' }}{{ ab.gapToAverage | number:'1.0-1' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Trends -->
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

        <!-- Footer: validate button -->
        <div *ngIf="!validated" class="mt-4 d-flex justify-content-end gap-2">
          <div *ngIf="validateError" class="alert alert-danger py-2 px-3 mb-0 me-auto small">{{ validateError }}</div>
          <button class="btn btn-primary px-4 rounded-pill" (click)="validate()" [disabled]="validating">
            <span *ngIf="validating" class="spinner-border spinner-border-sm me-2"></span>
            <i *ngIf="!validating" class="fas fa-paper-plane me-2"></i>
            Valider et envoyer par email
          </button>
        </div>
        <div *ngIf="validated" class="mt-4 alert alert-success text-center fw-semibold">
          <i class="fas fa-check-circle me-2"></i>Résultats envoyés à l'entreprise.
        </div>
        <div *ngIf="validateSuccess" class="mt-3 alert alert-success">
          <i class="fas fa-envelope-check me-2"></i>{{ validateSuccess }}
        </div>
      </div>
    </div>
  `
})
export class ConsultantReviewComponent implements OnInit {
  evaluationId!: number;
  tab = 'scores';
  loading = true;
  error = '';
  validateError = '';
  validateSuccess = '';
  validating = false;

  companyName = '';
  pendingReview = true;
  validated = false;
  globalScore = 0;
  maturityLevel = '';
  recommendations: Recommendation[] = [];
  subAxisScores: SubAxisScore[] = [];
  benchmark: any = null;
  aiPending = false;
  initialGenerating = false;
  initialGenerateError = '';

  showPromptPanel = false;
  consultantPrompt = '';
  regenerating = false;
  regenerateError = '';
  regenerateSuccess = '';

  showBenchPromptPanel = false;
  benchConsultantPrompt = '';
  benchRegenerating = false;
  benchRegenerateError = '';
  benchRegenerateSuccess = '';

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
    METIER: 'Métier', PROCESSUS: 'Processus', SI: 'SI',
    CANAUX_DISTRIBUTION: 'Canaux & UX',
    MARKETING_COMMUNICATION: 'Marketing',
    RH_CULTURE_DIGITALE: 'RH & Culture',
    OFFRES_DIGITALES: 'Offres Digitales'
  };
  private readonly priorityColors: Record<string, string> = {
    HAUTE: '#dc2626', MOYENNE: '#d97706', BASSE: '#16a34a'
  };

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    this.evaluationId = Number(this.route.snapshot.paramMap.get('id'));
    this.http.get<any>(`${environment.apiUrl}/evaluations/${this.evaluationId}/full-review`).subscribe({
      next: (data) => {
        const ev = data.evaluation;
        this.companyName = ev.companyName;
        this.pendingReview = data.pendingReview ?? true;
        this.validated = data.validated ?? false;
        this.globalScore = ev.globalScore;
        this.maturityLevel = ev.maturityLevel;
        this.subAxisScores = ev.scoresBySubAxis || [];
        const allAxes = [
          { key: 'METIER',                  label: 'Métier',                    color: '#0d6efd' },
          { key: 'PROCESSUS',               label: 'Processus',                 color: '#198754' },
          { key: 'SI',                      label: 'Système d\'Information',    color: '#6366f1' },
          { key: 'CANAUX_DISTRIBUTION',     label: 'Canaux & UX',               color: '#0891b2' },
          { key: 'MARKETING_COMMUNICATION', label: 'Marketing & Communication', color: '#d97706' },
          { key: 'RH_CULTURE_DIGITALE',     label: 'RH & Culture Digitale',     color: '#7c3aed' },
          { key: 'OFFRES_DIGITALES',        label: 'Offres Digitales',          color: '#059669' },
        ];
        this.axisBars = allAxes
          .map(a => ({
            label: a.label,
            score: (ev.scoresByAxis || []).find((s: AxisScore) => s.axis === a.key)?.score || 0,
            color: a.color
          }))
          ;
        this.recommendations = (data.recommendations || []).map((r: Recommendation) => ({ ...r, editing: false }));
        this.benchmark = data.benchmark && Object.keys(data.benchmark).length > 0 ? data.benchmark : null;
        this.aiPending = data.aiPending ?? false;
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.error?.message || 'Erreur lors du chargement des données.';
        this.loading = false;
      }
    });
  }

  generateInitial() {
    this.initialGenerateError = '';
    this.initialGenerating = true;
    const recsCall = this.http.post<any[]>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate`, { consultantPrompt: '' }
    );
    const benchCall = this.http.post<any>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate-benchmark`, { consultantPrompt: '' }
    );
    recsCall.subscribe({
      next: (recs) => {
        this.recommendations = recs.map((r: Recommendation) => ({ ...r, editing: false }));
      },
      error: (err) => { this.initialGenerateError = err?.error?.message || 'Erreur recommandations.'; }
    });
    benchCall.subscribe({
      next: (bench) => {
        this.benchmark = bench;
        this.initialGenerating = false;
        this.aiPending = false;
      },
      error: (err) => {
        this.initialGenerating = false;
        this.initialGenerateError = err?.error?.message || 'Erreur benchmarking.';
      }
    });
  }

  regenerateBenchmark() {
    this.benchRegenerateError = '';
    this.benchRegenerateSuccess = '';
    this.benchRegenerating = true;
    this.http.post<any>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate-benchmark`,
      { consultantPrompt: this.benchConsultantPrompt }
    ).subscribe({
      next: (bench) => {
        this.benchmark = bench;
        this.benchRegenerating = false;
        this.benchRegenerateSuccess = 'Benchmarking régénéré avec succès.';
      },
      error: (err) => {
        this.benchRegenerating = false;
        this.benchRegenerateError = err?.error?.message || 'Erreur lors de la régénération.';
      }
    });
  }

  regenerate() {
    this.regenerateError = '';
    this.regenerateSuccess = '';
    this.regenerating = true;
    this.http.post<any[]>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate`,
      { consultantPrompt: this.consultantPrompt }
    ).subscribe({
      next: (recs) => {
        this.recommendations = recs.map((r: Recommendation) => ({ ...r, editing: false }));
        this.regenerating = false;
        this.regenerateSuccess = `${recs.length} recommandations régénérées.`;
      },
      error: (err) => {
        this.regenerating = false;
        this.regenerateError = err?.error?.message || 'Erreur lors de la régénération.';
      }
    });
  }

  addRec() {
    this.recommendations.push({ axis: 'METIER', priority: 'MOYENNE', title: '', description: '', bestPractice: '', editing: true });
  }

  removeRec(i: number) { this.recommendations.splice(i, 1); }

  validate() {
    this.validateError = '';
    this.validateSuccess = '';
    const hasEditing = this.recommendations.some(r => r.editing);
    if (hasEditing) { this.validateError = 'Fermez d\'abord les recommandations en cours de modification.'; return; }
    this.validating = true;
    const payload = this.recommendations.map(({ editing: _, ...r }) => r);
    this.http.post<any>(`${environment.apiUrl}/evaluations/${this.evaluationId}/validate`, payload).subscribe({
      next: (res) => {
        this.validating = false;
        this.validateSuccess = res.message;
        this.validated = true;
        this.pendingReview = false;
      },
      error: (err) => {
        this.validating = false;
        this.validateError = err?.error?.message || 'Erreur lors de l\'envoi.';
      }
    });
  }

  getAxisColor(axis: string): string { return this.axisColors[axis] ?? '#6c757d'; }
  getAxisLabel(axis: string): string { return this.axisLabels[axis] ?? axis; }
  getPriorityColor(p: string): string { return this.priorityColors[p] ?? '#6c757d'; }
}
