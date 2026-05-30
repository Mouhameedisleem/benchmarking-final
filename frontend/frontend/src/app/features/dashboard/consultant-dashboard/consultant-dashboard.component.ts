import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { forkJoin } from 'rxjs';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/models/user.model';
import { environment } from '../../../../environments/environment';

interface EvalSummary {
  evaluationId: number; companyId: number; companyName: string;
  sector: string; country: string; companySize: string;
  globalScore: number; maturityLevel: string; status: string; createdAt: string;
}
interface PendingEval {
  evaluationId: number; companyId: number; companyName: string;
  globalScore: number; maturityLevel: string; status: string; createdAt: string;
}
interface DonutSegment {
  level: string; label: string; count: number; pct: number;
  dash: number; gap: number; rotDeg: number; color: string;
}

@Component({
  selector: 'app-consultant-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  styles: [`
    .kpi-icon { width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0; }
    .kpi-value { font-size:1.8rem;font-weight:900;line-height:1; }
    .section-label { font-size:11px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;color:#94a3b8; }
    .pending-row { transition:background .15s; }
    .pending-row:hover { filter:brightness(.97); }
    .quick-link { display:flex;align-items:center;gap:12px;padding:14px 20px;text-decoration:none;color:inherit;border-top:1px solid #f1f5f9;transition:background .15s; }
    .quick-link:first-child { border-top:none; }
    .quick-link:hover { background:#f8faff; }
  `],
  template: `
    <div class="container-fluid py-4" style="max-width:1280px;margin:auto;">

      <!-- ── Page Header ── -->
      <div class="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h4 class="fw-bold mb-1" style="color:#0f172a;">
            <i class="fas fa-gauge-high me-2 text-primary"></i>Tableau de Bord
          </h4>
          <p class="text-muted mb-0 small">
            Bienvenue, <strong>{{ currentUser?.firstName || currentUser?.username }}</strong>
          </p>
        </div>
        <button class="btn btn-sm btn-outline-secondary rounded-pill px-3" (click)="reload()">
          <i class="fas fa-rotate-right me-1"></i>Actualiser
        </button>
      </div>

      <!-- Loading -->
      <div *ngIf="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Chargement…</p>
      </div>

      <ng-container *ngIf="!loading">

        <!-- ════ KPI Cards ════ -->
        <div class="row g-3 mb-4">

          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="d-flex align-items-center gap-3">
                <div class="kpi-icon" style="background:#e8f0fe;">
                  <i class="fas fa-building text-primary"></i>
                </div>
                <div>
                  <div class="kpi-value" style="color:#0f2242;">{{ totalCompanies }}</div>
                  <div class="text-muted small">Entreprises</div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="d-flex align-items-center gap-3">
                <div class="kpi-icon" style="background:#e8f5e9;">
                  <i class="fas fa-chart-simple text-success"></i>
                </div>
                <div>
                  <div class="kpi-value" style="color:#0f2242;">{{ avgScore | number:'1.0-1' }}</div>
                  <div class="text-muted small">Score moyen</div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="d-flex align-items-center gap-3">
                <div class="kpi-icon" style="background:#dcfce7;">
                  <i class="fas fa-circle-check" style="color:#16a34a;"></i>
                </div>
                <div>
                  <div class="kpi-value" style="color:#0f2242;">{{ validatedCount }}</div>
                  <div class="text-muted small">Validées</div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6 col-md-3">
            <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
              <div class="d-flex align-items-center gap-3">
                <div class="kpi-icon" style="background:#fff7ed;">
                  <i class="fas fa-hourglass-half" style="color:#f97316;"></i>
                </div>
                <div>
                  <div class="kpi-value" style="color:#0f2242;">{{ pendingEvals.length }}</div>
                  <div class="text-muted small">En attente</div>
                </div>
              </div>
            </div>
          </div>

        </div>
        <!-- /KPIs -->

        <!-- ════ Two-column layout ════ -->
        <div class="row g-4 align-items-start">

          <!-- ═══ LEFT: Filters + Analytics (col-lg-7) ═══ -->
          <div class="col-lg-7">

            <!-- Overdue alert -->
            <div *ngIf="overdueAlerts.length > 0"
                 class="alert border-0 rounded-4 mb-3 d-flex align-items-start gap-3"
                 style="background:#fef2f2;border-left:4px solid #ef4444 !important;padding:14px 16px;">
              <i class="fas fa-triangle-exclamation fa-lg mt-1 flex-shrink-0" style="color:#ef4444;"></i>
              <div class="flex-grow-1">
                <div class="fw-semibold mb-2" style="color:#991b1b;font-size:14px;">
                  {{ overdueAlerts.length }} évaluation(s) en retard — plus de 7 jours sans validation
                </div>
                <div class="d-flex flex-wrap gap-2">
                  <span *ngFor="let al of overdueAlerts"
                        class="badge rounded-pill d-inline-flex align-items-center gap-2 px-3 py-2"
                        style="background:#fee2e2;color:#991b1b;font-size:11px;font-weight:500;">
                    <i class="fas fa-building" style="font-size:9px;"></i>
                    {{ al.companyName }}
                    <span class="opacity-75">({{ daysPending(al.createdAt) }}j)</span>
                    <a [routerLink]="['/consultant/evaluations', al.evaluationId, 'review']"
                       class="text-decoration-none ms-1" style="color:#991b1b;">
                      <i class="fas fa-arrow-right" style="font-size:9px;"></i>
                    </a>
                  </span>
                </div>
              </div>
            </div>

            <!-- Filters -->
            <div class="card border-0 shadow-sm rounded-4 mb-3 p-3">
              <div class="d-flex align-items-center gap-2 flex-wrap">
                <i class="fas fa-filter text-muted flex-shrink-0"></i>
                <select class="form-select form-select-sm rounded-pill" style="width:auto;min-width:140px;"
                        [(ngModel)]="filterSector">
                  <option value="">Tous les secteurs</option>
                  <option *ngFor="let s of sectors" [value]="s">{{ s }}</option>
                </select>
                <select class="form-select form-select-sm rounded-pill" style="width:auto;min-width:130px;"
                        [(ngModel)]="filterCountry">
                  <option value="">Tous les pays</option>
                  <option *ngFor="let c of countries" [value]="c">{{ c }}</option>
                </select>
                <select class="form-select form-select-sm rounded-pill" style="width:auto;min-width:150px;"
                        [(ngModel)]="filterSize">
                  <option value="">Toutes les tailles</option>
                  <option *ngFor="let sz of sizes" [value]="sz">{{ sz }}</option>
                </select>
                <button *ngIf="filterSector || filterCountry || filterSize"
                        class="btn btn-sm btn-outline-secondary rounded-pill"
                        (click)="resetFilters()">
                  <i class="fas fa-xmark me-1"></i>Réinitialiser
                </button>
                <span class="text-muted small ms-auto">
                  {{ filteredEvals.length }} entreprise(s)
                </span>
              </div>
            </div>

            <!-- Charts row: Donut + Ranking -->
            <div class="row g-3">

              <!-- Donut -->
              <div class="col-md-5">
                <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
                  <div class="fw-semibold mb-3" style="font-size:13px;">
                    <i class="fas fa-chart-pie me-2" style="color:#6366f1;"></i>Niveaux de maturité
                  </div>
                  <div *ngIf="filteredEvals.length === 0" class="text-center text-muted py-4">
                    <i class="fas fa-chart-pie fa-2x mb-2 d-block opacity-25"></i>Aucune donnée
                  </div>
                  <div *ngIf="filteredEvals.length > 0">
                    <div class="d-flex justify-content-center mb-3">
                      <svg viewBox="0 0 160 160" width="140" height="140">
                        <circle cx="80" cy="80" r="54" fill="none" stroke="#f3f4f6" stroke-width="22"/>
                        <circle *ngFor="let s of maturityDonut"
                                cx="80" cy="80" r="54" fill="none"
                                [attr.stroke]="s.color" stroke-width="22"
                                [attr.stroke-dasharray]="s.dash + ' ' + s.gap"
                                [attr.transform]="'rotate(' + s.rotDeg + ', 80, 80)'"/>
                        <text x="80" y="74" text-anchor="middle" font-size="24" font-weight="800" fill="#0f2242">
                          {{ filteredEvals.length }}
                        </text>
                        <text x="80" y="92" text-anchor="middle" font-size="9" fill="#6b7280">entreprises</text>
                      </svg>
                    </div>
                    <div class="d-flex flex-column gap-2">
                      <div *ngFor="let s of maturityDonut" class="d-flex align-items-center gap-2">
                        <span class="rounded-circle flex-shrink-0"
                              [style.background]="s.color"
                              style="width:9px;height:9px;display:inline-block;"></span>
                        <span class="small flex-grow-1">{{ s.label }}</span>
                        <span class="fw-semibold small">{{ s.count }}</span>
                        <span class="text-muted small">({{ s.pct * 100 | number:'1.0-0' }}%)</span>
                      </div>
                      <ng-container *ngFor="let lv of emptyLevels">
                        <div class="d-flex align-items-center gap-2" style="opacity:.4;">
                          <span class="rounded-circle flex-shrink-0"
                                [style.background]="lv.color"
                                style="width:9px;height:9px;display:inline-block;opacity:.3;"></span>
                          <span class="small flex-grow-1 text-muted">{{ lv.label }}</span>
                          <span class="text-muted small">0</span>
                        </div>
                      </ng-container>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Ranking -->
              <div class="col-md-7">
                <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="fw-semibold" style="font-size:13px;">
                      <i class="fas fa-ranking-star me-2" style="color:#f59e0b;"></i>Classement par score
                    </div>
                    <span class="badge bg-light text-secondary" style="font-size:11px;">Top {{ ranking.length }}</span>
                  </div>
                  <div *ngIf="ranking.length === 0" class="text-center text-muted py-4">
                    <i class="fas fa-trophy fa-2x mb-2 d-block opacity-25"></i>Aucune évaluation
                  </div>
                  <div *ngFor="let ev of ranking; let i=index" class="mb-2">
                    <div class="d-flex align-items-center gap-2 mb-1">
                      <span class="fw-bold text-muted flex-shrink-0"
                            style="width:18px;text-align:right;font-size:11px;">{{ i + 1 }}</span>
                      <span class="small fw-semibold flex-grow-1 text-truncate" style="max-width:150px;">
                        {{ ev.companyName }}
                      </span>
                      <span class="badge rounded-pill flex-shrink-0"
                            style="font-size:10px;"
                            [style.background]="maturityBg(ev.maturityLevel)"
                            [style.color]="maturityColor(ev.maturityLevel)">
                        {{ maturityLabel(ev.maturityLevel) }}
                      </span>
                      <span class="fw-bold flex-shrink-0"
                            style="width:30px;text-align:right;font-size:13px;"
                            [style.color]="scoreColor(ev.globalScore)">
                        {{ ev.globalScore | number:'1.0-0' }}
                      </span>
                      <a [routerLink]="['/consultant/evaluations', ev.evaluationId, 'review']"
                         class="btn btn-link btn-sm p-0 flex-shrink-0 text-muted">
                        <i class="fas fa-arrow-right" style="font-size:10px;"></i>
                      </a>
                    </div>
                    <div class="ms-4">
                      <div class="progress rounded-pill" style="height:4px;">
                        <div class="progress-bar rounded-pill"
                             [style.width]="ev.globalScore + '%'"
                             [style.background]="scoreColor(ev.globalScore)">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            <!-- /charts row -->

          </div>
          <!-- /LEFT -->

          <!-- ═══ RIGHT: Work queue + Quick nav (col-lg-5) ═══ -->
          <div class="col-lg-5">

            <!-- Pending evaluations card -->
            <div class="card border-0 shadow-sm rounded-4 mb-3">
              <div class="card-header bg-white border-0 pt-3 px-4 pb-2 d-flex align-items-center justify-content-between rounded-top-4">
                <h6 class="fw-bold mb-0" style="font-size:13px;">
                  <i class="fas fa-inbox text-warning me-2"></i>Évaluations à valider
                </h6>
                <span class="badge rounded-pill"
                      [class.text-bg-warning]="pendingEvals.length > 0"
                      [class.bg-light]="pendingEvals.length === 0"
                      [class.text-muted]="pendingEvals.length === 0">
                  {{ pendingEvals.length }}
                </span>
              </div>

              <div class="card-body px-3 pb-3 pt-1">

                <!-- Empty state -->
                <div *ngIf="pendingEvals.length === 0" class="text-center py-4">
                  <i class="fas fa-check-circle fa-2x mb-2 d-block" style="color:#22c55e;opacity:.5;"></i>
                  <p class="text-muted small mb-0">Toutes les évaluations sont traitées</p>
                </div>

                <!-- List -->
                <div *ngFor="let ev of pendingEvals"
                     class="pending-row d-flex align-items-center gap-3 p-2 rounded-3 mb-2"
                     [style.background]="isOverdue(ev.createdAt) ? '#fef2f2' : '#fafafa'"
                     [style.border]="isOverdue(ev.createdAt) ? '1px solid #fecaca' : '1px solid #f1f5f9'">
                  <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 fw-bold text-white"
                       style="width:38px;height:38px;font-size:13px;"
                       [style.background]="isOverdue(ev.createdAt) ? '#ef4444' : '#f97316'">
                    {{ ev.companyName.charAt(0).toUpperCase() }}
                  </div>
                  <div class="flex-grow-1" style="min-width:0;">
                    <div class="fw-semibold small text-truncate">
                      {{ ev.companyName }}
                      <span *ngIf="isOverdue(ev.createdAt)"
                            class="badge ms-1" style="background:#fee2e2;color:#991b1b;font-size:10px;">
                        <i class="fas fa-clock me-1"></i>{{ daysPending(ev.createdAt) }}j
                      </span>
                    </div>
                    <div class="text-muted" style="font-size:11px;">
                      <strong>{{ ev.globalScore | number:'1.0-1' }}/100</strong> ·
                      {{ maturityLabel(ev.maturityLevel) }} ·
                      {{ ev.createdAt | date:'dd/MM/yy' }}
                    </div>
                  </div>
                  <a [routerLink]="['/consultant/evaluations', ev.evaluationId, 'review']"
                     class="btn btn-sm rounded-pill px-2 flex-shrink-0"
                     style="font-size:11px;white-space:nowrap;"
                     [class.btn-danger]="isOverdue(ev.createdAt)"
                     [class.btn-warning]="!isOverdue(ev.createdAt)">
                    <i class="fas fa-magnifying-glass me-1"></i>Valider
                  </a>
                </div>

              </div>
            </div>
            <!-- /pending card -->

            <!-- Quick navigation card -->
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
              <div class="px-4 pt-3 pb-2">
                <span class="section-label">Accès rapide</span>
              </div>

              <a routerLink="/consultant/analysis" class="quick-link">
                <div class="rounded-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                     style="width:40px;height:40px;background:#e8f5e9;">
                  <i class="fas fa-chart-line text-success"></i>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold small">Résultats & Analyses</div>
                  <div class="text-muted" style="font-size:11px;">Vue complète par entreprise</div>
                </div>
                <i class="fas fa-chevron-right text-muted flex-shrink-0" style="font-size:11px;"></i>
              </a>

              <div class="quick-link">
                <div class="rounded-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                     style="width:40px;height:40px;background:#e3f2fd;">
                  <i class="fas fa-building text-primary"></i>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold small mb-1">Gestion des entreprises</div>
                  <div class="d-flex gap-2">
                    <a routerLink="/companies" class="btn btn-primary btn-sm rounded-pill px-2" style="font-size:11px;">
                      <i class="fas fa-list me-1"></i>Liste
                    </a>
                    <a routerLink="/companies/new" class="btn btn-outline-primary btn-sm rounded-pill px-2" style="font-size:11px;">
                      <i class="fas fa-plus me-1"></i>Nouvelle
                    </a>
                  </div>
                </div>
              </div>

              <a routerLink="/consultant/frameworks" class="quick-link">
                <div class="rounded-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                     style="width:40px;height:40px;background:#ede9fe;">
                  <i class="fas fa-brain" style="color:#6366f1;"></i>
                </div>
                <div class="flex-grow-1">
                  <div class="fw-semibold small">Référentiels IA</div>
                  <div class="text-muted" style="font-size:11px;">Frameworks de la base de connaissance</div>
                </div>
                <i class="fas fa-chevron-right text-muted flex-shrink-0" style="font-size:11px;"></i>
              </a>

            </div>
            <!-- /quick nav -->

          </div>
          <!-- /RIGHT -->

        </div>
        <!-- /two-column layout -->

      </ng-container>
    </div>
  `
})
export class ConsultantDashboardComponent implements OnInit {
  currentUser: User | null = null;
  allEvals: EvalSummary[] = [];
  pendingEvals: PendingEval[] = [];
  companiesCount = 0;
  loading = true;

  filterSector  = '';
  filterCountry = '';
  filterSize    = '';

  private readonly LEVELS = [
    { level: 'INITIAL',       label: 'Initial',       color: '#ef4444' },
    { level: 'BASIQUE',       label: 'Basique',        color: '#f97316' },
    { level: 'INTERMEDIAIRE', label: 'Intermédiaire',  color: '#eab308' },
    { level: 'AVANCE',        label: 'Avancé',         color: '#3b82f6' },
    { level: 'OPTIMISE',      label: 'Optimisé',       color: '#22c55e' },
  ];

  constructor(private authService: AuthService, private http: HttpClient) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    this.load();
  }

  reload() { this.loading = true; this.load(); }

  private load() {
    forkJoin({
      dashboard:  this.http.get<EvalSummary[]>(`${environment.apiUrl}/evaluations/dashboard`),
      pending:    this.http.get<PendingEval[]>(`${environment.apiUrl}/evaluations/pending-review`),
      companies:  this.http.get<any[]>(`${environment.apiUrl}/companies`)
    }).subscribe({
      next: ({ dashboard, pending, companies }) => {
        this.allEvals      = dashboard  || [];
        this.pendingEvals  = pending    || [];
        this.companiesCount = (companies || []).length;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  resetFilters() { this.filterSector = ''; this.filterCountry = ''; this.filterSize = ''; }

  // ── Derived: deduplicated latest evaluation per company ─────────────────────
  get latestByCompany(): EvalSummary[] {
    const seen = new Set<number>();
    return this.allEvals.filter(e => {
      if (seen.has(e.companyId)) return false;
      seen.add(e.companyId);
      return true;
    });
  }

  get filteredEvals(): EvalSummary[] {
    return this.latestByCompany.filter(e =>
      (!this.filterSector  || e.sector      === this.filterSector)  &&
      (!this.filterCountry || e.country     === this.filterCountry) &&
      (!this.filterSize    || e.companySize === this.filterSize)
    );
  }

  // ── Filter option lists ──────────────────────────────────────────────────────
  get sectors():   string[] { return [...new Set(this.latestByCompany.map(e => e.sector).filter(Boolean))].sort(); }
  get sizes():     string[] { return [...new Set(this.latestByCompany.map(e => e.companySize).filter(Boolean))].sort(); }

  private readonly COUNTRY_LIST = [
    // Afrique du Nord
    'Algérie', 'Égypte', 'Libye', 'Maroc', 'Mauritanie', 'Soudan', 'Tunisie',
    // Afrique subsaharienne
    'Afrique du Sud', 'Angola', "Bénin", 'Botswana', 'Burkina Faso', 'Burundi',
    'Cameroun', 'Cap-Vert', 'Comores', 'Congo', 'Côte d\'Ivoire', 'Djibouti',
    'Érythrée', 'Éthiopie', 'Gabon', 'Gambie', 'Ghana', 'Guinée',
    'Guinée-Bissau', 'Guinée équatoriale', 'Kenya', 'Lesotho', 'Liberia',
    'Madagascar', 'Malawi', 'Mali', 'Mozambique', 'Namibie', 'Niger',
    'Nigeria', 'Ouganda', 'RD Congo', 'Rwanda', 'São Tomé-et-Príncipe',
    'Sénégal', 'Seychelles', 'Sierra Leone', 'Somalie', 'Soudan du Sud',
    'Swaziland', 'Tanzanie', 'Tchad', 'Togo', 'Zambie', 'Zimbabwe',
    // Moyen-Orient
    'Arabie saoudite', 'Bahreïn', 'Émirats arabes unis', 'Irak', 'Iran',
    'Israël', 'Jordanie', 'Koweït', 'Liban', 'Oman', 'Palestine',
    'Qatar', 'Syrie', 'Turquie', 'Yémen',
    // Europe occidentale
    'Allemagne', 'Andorre', 'Autriche', 'Belgique', 'Chypre', 'Danemark',
    'Espagne', 'Finlande', 'France', 'Grèce', 'Irlande', 'Islande',
    'Italie', 'Liechtenstein', 'Luxembourg', 'Malte', 'Monaco',
    'Norvège', 'Pays-Bas', 'Portugal', 'Royaume-Uni', 'Suède', 'Suisse',
    // Europe centrale & orientale
    'Albanie', 'Biélorussie', 'Bosnie-Herzégovine', 'Bulgarie', 'Croatie',
    'Estonie', 'Hongrie', 'Kosovo', 'Lettonie', 'Lituanie', 'Macédoine du Nord',
    'Moldavie', 'Monténégro', 'Pologne', 'République tchèque', 'Roumanie',
    'Russie', 'Serbie', 'Slovaquie', 'Slovénie', 'Ukraine',
    // Amériques
    'Argentine', 'Bolivie', 'Brésil', 'Canada', 'Chili', 'Colombie',
    'Costa Rica', 'Cuba', 'Équateur', 'États-Unis', 'Guatemala', 'Haïti',
    'Honduras', 'Jamaïque', 'Mexique', 'Nicaragua', 'Panama', 'Paraguay',
    'Pérou', 'République dominicaine', 'Salvador', 'Uruguay', 'Venezuela',
    // Asie
    'Afghanistan', 'Azerbaïdjan', 'Bangladesh', 'Cambodge', 'Chine',
    'Corée du Sud', 'Géorgie', 'Inde', 'Indonésie', 'Japon', 'Kazakhstan',
    'Kirghizistan', 'Laos', 'Malaisie', 'Maldives', 'Mongolie', 'Myanmar',
    'Népal', 'Ouzbékistan', 'Pakistan', 'Philippines', 'Singapour',
    'Sri Lanka', 'Tadjikistan', 'Thaïlande', 'Turkménistan', 'Viêt Nam',
    // Océanie
    'Australie', 'Nouvelle-Zélande', 'Papouasie-Nouvelle-Guinée'
  ];

  get countries(): string[] {
    const fromData = this.latestByCompany.map(e => e.country).filter(Boolean) as string[];
    return [...new Set([...this.COUNTRY_LIST, ...fromData])].sort((a, b) =>
      a.localeCompare(b, 'fr', { sensitivity: 'base' })
    );
  }

  // ── KPI ─────────────────────────────────────────────────────────────────────
  get totalCompanies(): number { return this.companiesCount; }

  get avgScore(): number {
    const evals = this.filteredEvals.filter(e => e.globalScore > 0);
    if (!evals.length) return 0;
    return evals.reduce((s, e) => s + e.globalScore, 0) / evals.length;
  }

  get validatedCount(): number {
    return this.latestByCompany.filter(e => e.status === 'VALIDATED').length;
  }

  // ── Overdue alerts (pending > 7 days) ────────────────────────────────────────
  get overdueAlerts(): PendingEval[] {
    return this.pendingEvals.filter(e => this.daysPending(e.createdAt) > 7);
  }

  isOverdue(createdAt: string): boolean { return this.daysPending(createdAt) > 7; }

  daysPending(createdAt: string): number {
    return Math.floor((Date.now() - new Date(createdAt).getTime()) / 86_400_000);
  }

  // ── Company ranking ──────────────────────────────────────────────────────────
  get ranking(): EvalSummary[] {
    return [...this.filteredEvals]
      .filter(e => e.globalScore > 0)
      .sort((a, b) => b.globalScore - a.globalScore)
      .slice(0, 10);
  }

  // ── Donut chart ──────────────────────────────────────────────────────────────
  get maturityDonut(): DonutSegment[] {
    const total = this.filteredEvals.length;
    if (!total) return [];
    const C = 2 * Math.PI * 54;
    let cumDeg = -90;
    return this.LEVELS
      .map(lv => {
        const count = this.filteredEvals.filter(e => e.maturityLevel === lv.level).length;
        const pct   = count / total;
        const rotDeg = cumDeg;
        cumDeg += pct * 360;
        return { ...lv, count, pct, dash: pct * C, gap: (1 - pct) * C, rotDeg };
      })
      .filter(s => s.count > 0);
  }

  get emptyLevels() {
    const present = new Set(this.maturityDonut.map(s => s.level));
    return this.LEVELS.filter(lv => !present.has(lv.level));
  }

  // ── Color helpers ────────────────────────────────────────────────────────────
  scoreColor(score: number): string {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#eab308';
    if (score >= 20) return '#f97316';
    return '#ef4444';
  }

  maturityLabel(level: string): string {
    return { INITIAL: 'Initial', BASIQUE: 'Basique', INTERMEDIAIRE: 'Intermédiaire',
             AVANCE: 'Avancé', OPTIMISE: 'Optimisé' }[level] ?? level;
  }

  maturityColor(level: string): string {
    return { INITIAL: '#ef4444', BASIQUE: '#f97316', INTERMEDIAIRE: '#ca8a04',
             AVANCE: '#3b82f6', OPTIMISE: '#16a34a' }[level] ?? '#6c757d';
  }

  maturityBg(level: string): string {
    return { INITIAL: '#fef2f2', BASIQUE: '#fff7ed', INTERMEDIAIRE: '#fefce8',
             AVANCE: '#eff6ff', OPTIMISE: '#f0fdf4' }[level] ?? '#f1f5f9';
  }
}
