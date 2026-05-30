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

          <!-- Row 1: Score global ring + Radar side by side -->
          <div class="row g-3 mb-3">
            <div class="col-md-4 col-lg-3">
              <div class="card border-0 shadow-sm rounded-4 p-4 h-100 d-flex flex-column align-items-center justify-content-center text-center">
                <svg viewBox="0 0 130 130" width="130" height="130">
                  <circle cx="65" cy="65" r="54" fill="none" stroke="#f3f4f6" stroke-width="11"/>
                  <circle cx="65" cy="65" r="54" fill="none"
                          [attr.stroke]="scoreColor(globalScore)" stroke-width="11"
                          [attr.stroke-dasharray]="ringDash(54, globalScore)"
                          stroke-linecap="round" transform="rotate(-90 65 65)"/>
                  <text x="65" y="60" text-anchor="middle" font-size="30" font-weight="900"
                        [attr.fill]="scoreColor(globalScore)">{{ globalScore | number:'1.0-0' }}</text>
                  <text x="65" y="79" text-anchor="middle" font-size="12" fill="#9ca3af">/100</text>
                </svg>
                <div class="text-muted small mt-2 mb-2">Score global</div>
                <span class="badge rounded-pill px-3 py-2"
                      [style.background]="maturityBg(maturityLevel)"
                      [style.color]="maturityColor(maturityLevel)"
                      style="font-size:13px;font-weight:700;">
                  {{ maturityLabel(maturityLevel) }}
                </span>
              </div>
            </div>
            <div class="col-md-8 col-lg-9">
              <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
                <div class="fw-semibold mb-1" style="font-size:13px;color:#374151;">
                  <i class="fas fa-chart-area me-2" style="color:#1768e5;"></i>Vue radar — maturité par axe
                </div>
                <svg viewBox="0 0 400 390" width="100%" style="max-width:500px;display:block;margin:0 auto;overflow:visible;">
                  <polygon *ngFor="let g of radarGrid; let gi=index"
                           [attr.points]="g" fill="none"
                           [attr.stroke]="gi===4 ? '#d1d5db' : '#e5e7eb'"
                           [attr.stroke-width]="gi===4 ? 1.5 : 1" stroke-dasharray="3 3"/>
                  <text x="204" y="170" fill="#d1d5db" font-size="8">20</text>
                  <text x="204" y="141" fill="#d1d5db" font-size="8">40</text>
                  <text x="204" y="113" fill="#d1d5db" font-size="8">60</text>
                  <text x="204" y="84"  fill="#d1d5db" font-size="8">80</text>
                  <line *ngFor="let s of radarSpokes"
                        x1="200" y1="195" [attr.x2]="s.x2" [attr.y2]="s.y2"
                        stroke="#e5e7eb" stroke-width="1"/>
                  <polygon [attr.points]="radarPolygon"
                           fill="#1768e5" fill-opacity="0.12"
                           stroke="#1768e5" stroke-width="2" stroke-linejoin="round"/>
                  <ng-container *ngFor="let p of radarItems">
                    <circle [attr.cx]="p.dx" [attr.cy]="p.dy" r="4"
                            [attr.fill]="p.color" stroke="#fff" stroke-width="1.5"/>
                    <text *ngIf="p.score > 0"
                          [attr.x]="p.dx" [attr.y]="p.dy - 7"
                          text-anchor="middle" fill="#374151" font-size="9" font-weight="700">
                      {{ p.score | number:'1.0-0' }}
                    </text>
                    <text [attr.x]="p.lx" [attr.y]="p.ly"
                          [attr.text-anchor]="p.anchor" [attr.fill]="p.color"
                          font-size="11" font-weight="600" dominant-baseline="middle">{{ p.label }}</text>
                  </ng-container>
                </svg>
              </div>
            </div>
          </div>

          <!-- Row 2: Axis ring cards (3-col grid) -->
          <div class="card border-0 shadow-sm rounded-4 p-4 mb-3">
            <div class="fw-semibold mb-3" style="font-size:13px;color:#374151;">
              <i class="fas fa-chart-bar me-2" style="color:#6366f1;"></i>Scores par axe
            </div>
            <div class="row g-3">
              <div *ngFor="let a of axisBars" class="col-6 col-md-4">
                <div class="rounded-4 p-3 h-100 d-flex align-items-center gap-3"
                     style="background:#f9fafb;border:1.5px solid #f1f5f9;border-left-width:3px;"
                     [style.border-left-color]="a.color">
                  <svg viewBox="0 0 68 68" width="56" height="56" style="flex-shrink:0;">
                    <circle cx="34" cy="34" r="26" fill="none" stroke="#e5e7eb" stroke-width="7"/>
                    <circle cx="34" cy="34" r="26" fill="none"
                            [attr.stroke]="a.score > 0 ? a.color : '#d1d5db'" stroke-width="7"
                            [attr.stroke-dasharray]="ringDash(26, a.score)"
                            stroke-linecap="round" transform="rotate(-90 34 34)"/>
                    <text x="34" y="39" text-anchor="middle" font-size="14" font-weight="900"
                          [attr.fill]="a.score > 0 ? a.color : '#9ca3af'">
                      {{ a.score > 0 ? (a.score | number:'1.0-0') : '–' }}
                    </text>
                  </svg>
                  <div style="min-width:0;flex:1;">
                    <div class="fw-semibold" style="font-size:12px;color:#1e293b;line-height:1.3;">{{ a.label }}</div>
                    <div *ngIf="a.score > 0" class="text-muted" style="font-size:11px;margin-top:2px;">{{ a.score | number:'1.0-1' }}/100</div>
                    <span *ngIf="a.score === 0" class="badge bg-light text-secondary mt-1" style="font-size:10px;">Non évalué</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sub-axes: 3-col redesigned cards -->
          <div *ngIf="subAxisScores.length > 0" class="card border-0 shadow-sm rounded-4 p-4">
            <div class="fw-semibold mb-3" style="font-size:13px;color:#374151;">
              <i class="fas fa-layer-group me-2" style="color:#7c3aed;"></i>Détail par sous-axe
            </div>
            <div class="row g-2">
              <div *ngFor="let s of subAxisScores" class="col-md-4">
                <div class="rounded-3 p-3 h-100" style="background:#fafafa;border:1px solid #f1f5f9;">
                  <div class="mb-2">
                    <span class="badge rounded-2"
                          style="font-size:9px;font-weight:700;padding:2px 7px;"
                          [style.background]="axisColor(s.axis)+'18'"
                          [style.color]="axisColor(s.axis)">
                      {{ axisLabel(s.axis) }}
                    </span>
                  </div>
                  <div class="fw-semibold mb-2" style="font-size:12px;color:#374151;line-height:1.3;">{{ s.subAxis }}</div>
                  <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-grow-1 rounded-pill" style="height:6px;"
                         [style.background]="axisColor(s.axis)+'20'">
                      <div class="progress-bar rounded-pill"
                           [style.width]="s.score+'%'"
                           [style.background]="axisColor(s.axis)">
                      </div>
                    </div>
                    <span class="fw-bold flex-shrink-0"
                          [style.color]="axisColor(s.axis)"
                          style="font-size:12px;min-width:24px;text-align:right;">
                      {{ s.score | number:'1.0-0' }}
                    </span>
                  </div>
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
                <p class="text-muted small mb-1 fst-italic">{{ r.bestPractice }}</p>
                <a *ngIf="r.sourceUrl" [href]="r.sourceUrl" target="_blank" rel="noopener noreferrer"
                   class="text-decoration-none d-inline-flex align-items-center gap-1"
                   style="font-size:11px;color:#6366f1;">
                  <i class="fas fa-external-link-alt" style="font-size:9px;"></i>
                  {{ r.source || 'Source' }}
                </a>
                <span *ngIf="!r.sourceUrl && r.source"
                      class="d-inline-flex align-items-center gap-1"
                      style="font-size:11px;color:#9ca3af;">
                  <i class="fas fa-book" style="font-size:9px;"></i>
                  {{ r.source }}
                </span>
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
                    <div class="text-muted mb-1" style="font-size:11px;">{{ t.horizon }} · Adoption : {{ t.adoptionRate }}</div>
                    <a *ngIf="t.sourceUrl" [href]="t.sourceUrl" target="_blank" rel="noopener noreferrer"
                       class="text-decoration-none d-inline-flex align-items-center gap-1"
                       style="font-size:11px;color:#0891b2;">
                      <i class="fas fa-external-link-alt" style="font-size:9px;"></i>
                      {{ t.source }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Bouton PDF -->
      <div class="mt-4 d-flex justify-content-end">
        <button class="btn btn-outline-secondary px-3 rounded-pill" (click)="downloadPdf()" [disabled]="pdfDownloading">
          <span *ngIf="pdfDownloading" class="spinner-border spinner-border-sm me-1" style="width:13px;height:13px;"></span>
          <i *ngIf="!pdfDownloading" class="fas fa-file-pdf me-2" style="color:#dc2626;"></i>
          Télécharger le rapport PDF
        </button>
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
  evaluationId = 0;
  pdfDownloading = false;
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
    OFFRES_DIGITALES: '#059669',
    MODELE_OPERATIONNEL_INNOVATION: '#f97316',
    IT_DATA: '#8b5cf6'
  };

  readonly axisLabels: Record<string, string> = {
    METIER: 'Métier',
    PROCESSUS: 'Processus',
    SI: 'Système d\'Information',
    CANAUX_DISTRIBUTION: 'Canaux & UX',
    MARKETING_COMMUNICATION: 'Marketing & Communication',
    RH_CULTURE_DIGITALE: 'RH & Culture Digitale',
    OFFRES_DIGITALES: 'Offres Digitales',
    MODELE_OPERATIONNEL_INNOVATION: 'Modèle Opérationnel & Innovation',
    IT_DATA: 'IT & Data'
  };

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('evaluationId'));
    this.evaluationId = id;
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
          { key: 'METIER',                         label: 'Métier',                            color: '#0d6efd'  },
          { key: 'PROCESSUS',                      label: 'Processus',                         color: '#198754'  },
          { key: 'SI',                             label: 'Système d\'Information',            color: '#6366f1'  },
          { key: 'CANAUX_DISTRIBUTION',            label: 'Canaux & UX',                       color: '#0891b2'  },
          { key: 'MARKETING_COMMUNICATION',        label: 'Marketing & Communication',         color: '#d97706'  },
          { key: 'RH_CULTURE_DIGITALE',            label: 'RH & Culture Digitale',            color: '#7c3aed'  },
          { key: 'OFFRES_DIGITALES',               label: 'Offres Digitales',                 color: '#059669'  },
          { key: 'MODELE_OPERATIONNEL_INNOVATION', label: 'Modèle Opérationnel & Innovation', color: '#e11d48'  },
          { key: 'IT_DATA',                        label: 'IT & Data',                        color: '#0284c7'  },
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

  ringDash(r: number, score: number): string {
    const c = 2 * Math.PI * r;
    return `${Math.max(0, Math.min(score, 100)) / 100 * c} ${c}`;
  }

  scoreColor(score: number): string {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#eab308';
    if (score >= 20) return '#f97316';
    return '#ef4444';
  }

  downloadPdf() {
    this.pdfDownloading = true;
    this.http.get(`${environment.apiUrl}/evaluations/${this.evaluationId}/report/pdf`,
      { responseType: 'blob' }
    ).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `rapport-${this.companyName}-${new Date().toISOString().slice(0, 10)}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
        this.pdfDownloading = false;
      },
      error: () => { this.pdfDownloading = false; }
    });
  }

  // ── Radar chart ───────────────────────────────────────────────────────────
  get radarPolygon(): string {
    const n = this.axisBars.length;
    if (!n) return '';
    return this.axisBars.map((a, i) => {
      const ang = (2 * Math.PI * i / n) - Math.PI / 2;
      const r = (Math.max(0, a.score) / 100) * 142;
      return `${200 + r * Math.cos(ang)},${195 + r * Math.sin(ang)}`;
    }).join(' ');
  }

  get radarGrid(): string[] {
    const n = this.axisBars.length;
    if (!n) return [];
    return [0.2, 0.4, 0.6, 0.8, 1.0].map(f =>
      Array.from({ length: n }, (_, i) => {
        const ang = (2 * Math.PI * i / n) - Math.PI / 2;
        const r = f * 142;
        return `${200 + r * Math.cos(ang)},${195 + r * Math.sin(ang)}`;
      }).join(' ')
    );
  }

  get radarSpokes(): { x2: number; y2: number }[] {
    const n = this.axisBars.length;
    return Array.from({ length: n }, (_, i) => {
      const ang = (2 * Math.PI * i / n) - Math.PI / 2;
      return { x2: 200 + 142 * Math.cos(ang), y2: 195 + 142 * Math.sin(ang) };
    });
  }

  get radarItems(): { dx: number; dy: number; lx: number; ly: number; label: string; score: number; color: string; anchor: string }[] {
    const n = this.axisBars.length;
    const sl = ['Métier', 'Processus', 'SI', 'Canaux', 'Marketing', 'RH', 'Offres', 'Mod. Op.', 'IT & Data'];
    return this.axisBars.map((a, i) => {
      const ang = (2 * Math.PI * i / n) - Math.PI / 2;
      const r   = (Math.max(0, a.score) / 100) * 142;
      const lx  = 200 + 173 * Math.cos(ang);
      const ly  = 195 + 173 * Math.sin(ang);
      return {
        dx: 200 + r * Math.cos(ang), dy: 195 + r * Math.sin(ang),
        lx, ly, label: sl[i] ?? a.label, score: a.score, color: a.color,
        anchor: lx < 185 ? 'end' : lx > 215 ? 'start' : 'middle'
      };
    });
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