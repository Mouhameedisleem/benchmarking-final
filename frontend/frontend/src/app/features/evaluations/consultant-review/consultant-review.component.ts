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
  source?: string;
  sourceUrl?: string;
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
interface Trend { title: string; description: string; impactLevel: string; horizon: string; adoptionRate: string; source: string; sourceUrl?: string; }
interface SubAxisBenchmark {
  axis: string; subAxis: string; companyScore: number;
  tendances: any[]; analyseStatique: string; maturiteMaximale: string;
  cadreJuridique: any[]; maLeveesFonds: any[];
  leadersNationaux: any[]; leadersRegionaux: any[]; leadersInternationaux: any[];
  analysePersonnalisee: string;
  zoomCaseStudy?: any;
  comparatifOrganisations?: any;
  risques?: any[];
  opportunites?: any[];
}

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
          <li class="nav-item">
            <button class="nav-link" [class.active]="tab==='sous-axes'" (click)="tab='sous-axes'">
              <i class="fas fa-layer-group me-1"></i>Sous-Axes
              <span *ngIf="subAxisBenchmarks.length" class="badge bg-primary ms-1">{{ subAxisBenchmarks.length }}</span>
            </button>
          </li>
        </ul>

        <!-- ── TAB: SCORES ── -->
        <div *ngIf="tab==='scores'">

          <!-- Row 1: Score global ring + Radar -->
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
                  {{ getMaturityLevelLabel(maturityLevel) }}
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

          <!-- Target maturity card -->
          <div class="card border-0 shadow-sm rounded-4 mt-3 p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div class="fw-semibold">Maturité cible</div>
              <button *ngIf="!editingTargetMaturity" class="btn btn-sm btn-outline-secondary" (click)="startEditTargetMaturity()">
                <i class="fas fa-pencil-alt me-1" style="font-size:11px;"></i>Modifier
              </button>
            </div>
            <div class="d-flex gap-2 mb-3">
              <div *ngFor="let lv of maturityLevels"
                   class="flex-fill text-center py-2 px-1 rounded-3 small fw-semibold"
                   [style.background]="getMaturityLevelBg(lv)"
                   [style.color]="getMaturityLevelColor(lv)">
                {{ getMaturityLevelLabel(lv) }}
              </div>
            </div>
            <div class="d-flex gap-3 align-items-center flex-wrap">
              <div>
                <div class="text-muted small mb-1">Niveau actuel</div>
                <span class="badge px-3 py-2 rounded-pill" style="background:#e8f0fe;color:#1768e5;">{{ maturityLevel }}</span>
              </div>
              <i class="fas fa-arrow-right text-muted"></i>
              <div>
                <div class="text-muted small mb-1">Maturité cible</div>
                <div *ngIf="!editingTargetMaturity">
                  <span class="badge px-3 py-2 rounded-pill"
                        [style.background]="targetMaturityLevel ? '#dcfce7' : '#f3f4f6'"
                        [style.color]="targetMaturityLevel ? '#166534' : '#9ca3af'">
                    {{ targetMaturityLevel ? getMaturityLevelLabel(targetMaturityLevel) : 'Non définie' }}
                  </span>
                </div>
                <div *ngIf="editingTargetMaturity" class="d-flex gap-2 align-items-center">
                  <select class="form-select form-select-sm" style="width:auto;" [(ngModel)]="editTargetLevel">
                    <option *ngFor="let lv of maturityLevels" [value]="lv">{{ getMaturityLevelLabel(lv) }}</option>
                  </select>
                  <button class="btn btn-sm btn-success" (click)="saveTargetMaturity()" [disabled]="targetMaturitySaving">
                    <span *ngIf="targetMaturitySaving" class="spinner-border spinner-border-sm" style="width:12px;height:12px;"></span>
                    <i *ngIf="!targetMaturitySaving" class="fas fa-check"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-secondary" (click)="editingTargetMaturity=false">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </div>
            </div>
            <div *ngIf="targetMaturitySuccess" class="alert alert-success py-1 px-2 mt-2 small mb-0">{{ targetMaturitySuccess }}</div>
            <div *ngIf="targetMaturityError" class="alert alert-danger py-1 px-2 mt-2 small mb-0">{{ targetMaturityError }}</div>
          </div>

          <!-- Sub-axes: 3-col redesigned cards -->
          <div *ngIf="subAxisScores.length > 0" class="card border-0 shadow-sm rounded-4 mt-3 p-4">
            <div class="fw-semibold mb-3" style="font-size:13px;color:#374151;">
              <i class="fas fa-layer-group me-2" style="color:#7c3aed;"></i>Détail par sous-axe
            </div>
            <div class="row g-2">
              <div *ngFor="let s of subAxisScores" class="col-md-4">
                <div class="rounded-3 p-3 h-100" style="background:#fafafa;border:1px solid #f1f5f9;">
                  <div class="mb-2">
                    <span class="badge rounded-2"
                          style="font-size:9px;font-weight:700;padding:2px 7px;"
                          [style.background]="getAxisColor(s.axis)+'18'"
                          [style.color]="getAxisColor(s.axis)">
                      {{ getAxisLabel(s.axis) }}
                    </span>
                  </div>
                  <div class="fw-semibold mb-2" style="font-size:12px;color:#374151;line-height:1.3;">{{ s.subAxis }}</div>
                  <div class="d-flex align-items-center gap-2">
                    <div class="progress flex-grow-1 rounded-pill" style="height:6px;"
                         [style.background]="getAxisColor(s.axis)+'20'">
                      <div class="progress-bar rounded-pill"
                           [style.width]="s.score+'%'"
                           [style.background]="getAxisColor(s.axis)">
                      </div>
                    </div>
                    <span class="fw-bold flex-shrink-0"
                          [style.color]="getAxisColor(s.axis)"
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

          <div *ngIf="recommendations.length === 0" class="text-center py-5">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle mb-3"
                 style="width:72px;height:72px;background:#f1f5f9;">
              <i class="fas fa-robot fa-2x" style="color:#94a3b8;"></i>
            </div>
            <p class="fw-semibold mb-1" style="color:#374151;">Aucune recommandation disponible</p>
            <p class="text-muted small mb-4">
              L'IA n'a pas pu en générer ou elles ont été supprimées.<br>
              Cliquez ci-dessous pour lancer une nouvelle génération.
            </p>
            <button class="btn btn-primary rounded-pill px-4"
                    (click)="generateRecs()"
                    [disabled]="initialGenerating || regenerating">
              <span *ngIf="initialGenerating || regenerating"
                    class="spinner-border spinner-border-sm me-2" style="width:14px;height:14px;"></span>
              <i *ngIf="!initialGenerating && !regenerating" class="fas fa-magic me-2"></i>
              {{ (initialGenerating || regenerating) ? 'Génération en cours…' : 'Générer les recommandations IA' }}
            </button>
            <p *ngIf="initialGenerateError" class="text-danger small mt-3">
              <i class="fas fa-exclamation-circle me-1"></i>{{ initialGenerateError }}
            </p>
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
                      <option value="MODELE_OPERATIONNEL_INNOVATION">Modèle Opérationnel &amp; Innovation</option>
                      <option value="IT_DATA">IT &amp; Data</option>
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

          <div *ngIf="benchRegenerating" class="text-center py-5">
            <div class="spinner-border text-info mb-3"></div>
            <p class="text-muted">Génération du benchmarking en cours (1-3 min)…</p>
          </div>
          <div *ngIf="!benchmark && !benchRegenerating" class="text-center text-muted py-5">
            <i class="fas fa-chart-line fa-2x mb-3 d-block"></i>
            <span *ngIf="!benchRegenerateError">Données de benchmarking non disponibles (service IA non accessible lors de la génération).</span>
            <span *ngIf="benchRegenerateError" class="text-danger">{{ benchRegenerateError }}</span>
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
            <div class="card border-0 shadow-sm rounded-4 p-4"
                 *ngIf="benchmark.trends?.length || showTrendForm">
              <div class="d-flex align-items-center justify-content-between mb-3">
                <div class="fw-semibold" style="font-size:13px;color:#374151;">
                  <i class="fas fa-chart-line me-2" style="color:#0891b2;"></i>Tendances sectorielles
                </div>
                <button *ngIf="!showTrendForm"
                        class="btn btn-sm btn-outline-primary rounded-pill px-3"
                        style="font-size:11px;"
                        (click)="openAddTrend()">
                  <i class="fas fa-plus me-1"></i>Ajouter
                </button>
              </div>

              <!-- Inline add/edit form -->
              <div *ngIf="showTrendForm"
                   class="rounded-3 mb-4 p-3"
                   style="background:#f8faff;border:1.5px solid #c7d2fe;">
                <div class="fw-semibold small mb-3" style="color:#4f46e5;">
                  <i class="fas fa-{{ editingTrendIdx !== null ? 'pencil-alt' : 'plus-circle' }} me-1"></i>
                  {{ editingTrendIdx !== null ? 'Modifier la tendance' : 'Nouvelle tendance' }}
                </div>
                <div class="row g-2 mb-3">
                  <div class="col-12">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Titre *</label>
                    <input type="text" class="form-control form-control-sm" [(ngModel)]="trendDraft.title"
                           placeholder="Ex : Adoption de l'IA générative dans le secteur">
                  </div>
                  <div class="col-12">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Description *</label>
                    <textarea class="form-control form-control-sm" rows="3"
                              [(ngModel)]="trendDraft.description"
                              placeholder="Décrivez la tendance et son impact sur le secteur…"></textarea>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Niveau d'impact</label>
                    <select class="form-select form-select-sm" [(ngModel)]="trendDraft.impactLevel">
                      <option value="ELEVE">Élevé</option>
                      <option value="MOYEN">Moyen</option>
                      <option value="FAIBLE">Faible</option>
                    </select>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Horizon</label>
                    <select class="form-select form-select-sm" [(ngModel)]="trendDraft.horizon">
                      <option value="Court terme">Court terme</option>
                      <option value="Moyen terme">Moyen terme</option>
                      <option value="Long terme">Long terme</option>
                    </select>
                  </div>
                  <div class="col-md-4">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Taux d'adoption</label>
                    <input type="text" class="form-control form-control-sm"
                           [(ngModel)]="trendDraft.adoptionRate"
                           placeholder="Ex : 35%">
                  </div>
                  <div class="col-12">
                    <label class="form-label mb-1" style="font-size:11px;font-weight:600;">Source</label>
                    <input type="text" class="form-control form-control-sm"
                           [(ngModel)]="trendDraft.source"
                           placeholder="Ex : Gartner 2024, McKinsey Digital 2025">
                  </div>
                </div>
                <div class="d-flex gap-2 justify-content-end">
                  <button class="btn btn-sm btn-outline-secondary rounded-pill px-3"
                          (click)="cancelTrend()">Annuler</button>
                  <button class="btn btn-sm btn-primary rounded-pill px-3"
                          (click)="saveTrend()"
                          [disabled]="!trendDraft.title.trim()">
                    <i class="fas fa-check me-1"></i>
                    {{ editingTrendIdx !== null ? 'Enregistrer' : 'Ajouter' }}
                  </button>
                </div>
              </div>

              <!-- Empty state when no trends yet -->
              <div *ngIf="!benchmark.trends?.length && !showTrendForm"
                   class="text-center text-muted py-3 small">
                Aucune tendance. Cliquez sur "Ajouter" pour en créer une.
              </div>

              <!-- Trend cards grid -->
              <div class="row g-2">
                <div *ngFor="let t of benchmark.trends; let ti=index" class="col-md-6">
                  <div class="p-3 rounded-3 border h-100"
                       [style.border-color]="editingTrendIdx === ti ? '#818cf8' : '#e5e7eb'"
                       [style.background]="editingTrendIdx === ti ? '#f5f3ff' : '#fff'">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <span class="fw-semibold small flex-grow-1 me-2">{{ t.title }}</span>
                      <div class="d-flex align-items-center gap-1 flex-shrink-0">
                        <span class="badge" style="font-size:10px;"
                              [style.background]="t.impactLevel==='ÉLEVÉ'||t.impactLevel==='ELEVE'||t.impactLevel==='HIGH' ? '#fef9c3' : t.impactLevel==='FAIBLE' ? '#f0fdf4' : '#fffbeb'"
                              [style.color]="t.impactLevel==='ÉLEVÉ'||t.impactLevel==='ELEVE'||t.impactLevel==='HIGH' ? '#854d0e' : t.impactLevel==='FAIBLE' ? '#166534' : '#92400e'">
                          {{ t.impactLevel }}
                        </span>
                        <button class="btn btn-link btn-sm p-0 ms-1"
                                style="color:#6366f1;" title="Modifier"
                                (click)="openEditTrend(ti)">
                          <i class="fas fa-pencil-alt" style="font-size:11px;"></i>
                        </button>
                        <button class="btn btn-link btn-sm p-0"
                                style="color:#ef4444;" title="Supprimer"
                                (click)="deleteTrend(ti)">
                          <i class="fas fa-trash" style="font-size:11px;"></i>
                        </button>
                      </div>
                    </div>
                    <p class="text-muted small mb-1">{{ t.description }}</p>
                    <div class="text-muted mb-1" style="font-size:11px;">
                      {{ t.horizon }} · Adoption : {{ t.adoptionRate }}
                    </div>
                    <a *ngIf="t.sourceUrl" [href]="t.sourceUrl" target="_blank" rel="noopener noreferrer"
                       class="text-decoration-none d-inline-flex align-items-center gap-1"
                       style="font-size:11px;color:#0891b2;">
                      <i class="fas fa-external-link-alt" style="font-size:9px;"></i>
                      {{ t.source }}
                    </a>
                    <span *ngIf="!t.sourceUrl && t.source"
                          class="d-inline-flex align-items-center gap-1"
                          style="font-size:11px;color:#9ca3af;">
                      <i class="fas fa-book" style="font-size:9px;"></i>
                      {{ t.source }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty trends state (when benchmark exists but no trends yet) -->
            <div *ngIf="benchmark && !benchmark.trends?.length && !showTrendForm"
                 class="card border-0 shadow-sm rounded-4 p-4">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="fw-semibold" style="font-size:13px;color:#374151;">
                  <i class="fas fa-chart-line me-2" style="color:#0891b2;"></i>Tendances sectorielles
                </div>
                <button class="btn btn-sm btn-outline-primary rounded-pill px-3"
                        style="font-size:11px;" (click)="openAddTrend()">
                  <i class="fas fa-plus me-1"></i>Ajouter
                </button>
              </div>
              <div class="text-center text-muted py-3 small">
                Aucune tendance disponible. Cliquez sur "Ajouter" pour en créer une manuellement.
              </div>
            </div>
          </div>
        </div>

        <!-- ── TAB: SOUS-AXES ── -->
        <div *ngIf="tab==='sous-axes'">
          <div *ngIf="benchRegenerating && !subAxisBenchmarks.length" class="text-center py-5">
            <div class="spinner-border text-info mb-3"></div>
            <p class="text-muted">Génération des analyses sous-axes en cours (1-3 min)…</p>
          </div>
          <div *ngIf="!benchRegenerating && !subAxisBenchmarks.length" class="text-center text-muted py-5">
            <i class="fas fa-layer-group fa-2x mb-3 d-block" style="color:#d1d5db;"></i>
            <p class="fw-semibold mb-1" style="color:#374151;">Analyses sous-axes non disponibles</p>
            <p class="small">Régénérez le benchmarking pour inclure l'analyse détaillée par sous-axe.</p>
          </div>

          <ng-container *ngFor="let group of groupedSubAxisBenchmarks">
            <!-- Axis group header -->
            <div class="d-flex align-items-center gap-2 mb-2 mt-4">
              <span class="badge px-3 py-2 rounded-pill fw-semibold"
                    [style.background]="getAxisColor(group.axis)+'18'"
                    [style.color]="getAxisColor(group.axis)"
                    style="font-size:12px;">
                <i class="fas fa-layer-group me-1" style="font-size:10px;"></i>{{ getAxisLabel(group.axis) }}
              </span>
              <div class="flex-grow-1" style="height:1px;background:#e5e7eb;"></div>
            </div>

            <!-- Sub-axis accordion (Angular-driven, no BS JS needed) -->
            <div *ngFor="let sab of group.items; let i=index" class="card border-0 shadow-sm rounded-3 mb-2 overflow-hidden">

              <!-- Header (clickable) -->
              <div class="d-flex align-items-center gap-3 px-4 py-3"
                   style="cursor:pointer;background:#f8fafc;"
                   (click)="toggleSubAxis(group.axis+'-'+i)">
                <span class="fw-semibold flex-grow-1" style="font-size:14px;">{{ sab.subAxis }}</span>
                <div class="progress rounded-pill flex-shrink-0" style="width:80px;height:7px;">
                  <div class="progress-bar rounded-pill"
                       [style.width]="sab.companyScore+'%'"
                       [style.background]="getAxisColor(group.axis)"></div>
                </div>
                <span class="fw-bold small flex-shrink-0" [style.color]="getAxisColor(group.axis)" style="min-width:46px;text-align:right;">
                  {{ sab.companyScore | number:'1.0-0' }}/100
                </span>
                <i class="fas fa-chevron-down text-muted flex-shrink-0"
                   style="font-size:11px;transition:transform .2s;"
                   [style.transform]="isSubAxisOpen(group.axis+'-'+i) ? 'rotate(180deg)' : 'none'"></i>
              </div>

              <!-- Body (collapsible) -->
              <div *ngIf="isSubAxisOpen(group.axis+'-'+i)" class="px-4 pb-4 pt-2">

                <!-- Analyse personnalisée -->
                <div *ngIf="sab.analysePersonnalisee" class="rounded-3 p-3 mb-3"
                     style="background:#eff6ff;border-left:3px solid #3b82f6;">
                  <i class="fas fa-robot me-2" style="color:#3b82f6;font-size:11px;"></i>
                  <span class="small" style="color:#1e40af;">{{ sab.analysePersonnalisee }}</span>
                </div>

                <!-- ── ZOOM CASE STUDY ── -->
                <div *ngIf="sab.zoomCaseStudy?.entreprise" class="rounded-3 p-3 mb-3"
                     style="background:linear-gradient(135deg,#1e40af08,#7c3aed08);border:1px solid #c7d2fe;">
                  <div class="d-flex align-items-center gap-2 mb-2">
                    <span class="badge rounded-pill px-2 py-1" style="background:#1e40af;font-size:10px;">
                      <i class="fas fa-search-plus me-1"></i>ZOOM — Cas d'excellence mondial
                    </span>
                    <span class="fw-bold small" style="color:#1e40af;">{{ sab.zoomCaseStudy.entreprise }}</span>
                    <span class="text-muted small">· {{ sab.zoomCaseStudy.pays }}</span>
                    <span *ngIf="sab.zoomCaseStudy.annee" class="ms-auto badge rounded-pill"
                          style="font-size:9px;background:#e0e7ff;color:#3730a3;">{{ sab.zoomCaseStudy.annee }}</span>
                  </div>
                  <div class="small fw-semibold mb-1" style="color:#3730a3;">
                    <i class="fas fa-microchip me-1"></i>{{ sab.zoomCaseStudy.technologie }}
                  </div>
                  <p class="small mb-2" style="color:#374151;line-height:1.5;">{{ sab.zoomCaseStudy.description }}</p>
                  <div class="rounded-2 px-3 py-2" style="background:#1e40af12;">
                    <span class="small fw-semibold" style="color:#1e40af;">
                      <i class="fas fa-chart-bar me-1"></i>Résultats : </span>
                    <span class="small" style="color:#1e40af;">{{ sab.zoomCaseStudy.resultats }}</span>
                  </div>
                  <div class="mt-1 text-end" style="font-size:10px;color:#9ca3af;">{{ sab.zoomCaseStudy.source }}</div>
                </div>

                <!-- Tendances + Leaders -->
                <div class="row g-3 mb-3">
                  <div class="col-md-6" *ngIf="sab.tendances?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#fafafa;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-chart-line me-1" style="color:#6366f1;"></i>Tendances digitales
                      </div>
                      <div *ngFor="let t of sab.tendances.slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="small fw-semibold mb-0">{{ t.titre }}</div>
                        <div class="text-muted" style="font-size:11px;line-height:1.4;">{{ t.description | slice:0:130 }}…</div>
                        <div style="font-size:10px;color:#9ca3af;" class="mt-1">{{ t.source }}</div>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6" *ngIf="sab.leadersNationaux?.length || sab.leadersInternationaux?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#fafafa;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-trophy me-1" style="color:#f59e0b;"></i>Leaders de référence
                      </div>
                      <div *ngFor="let l of allLeaders(sab).slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="d-flex align-items-center gap-2 mb-0">
                          <span class="badge rounded-pill" style="font-size:9px;background:#e8f0fe;color:#1768e5;">{{ l.pays }}</span>
                          <span class="small fw-semibold">{{ l.entreprise }}</span>
                        </div>
                        <div class="text-muted" style="font-size:11px;line-height:1.4;">{{ l.pratique | slice:0:120 }}…</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ── COMPARATIF ORGANISATIONS ── -->
                <div *ngIf="sab.comparatifOrganisations?.colonnes?.length" class="mb-3">
                  <div class="fw-semibold small mb-2" style="color:#374151;">
                    <i class="fas fa-table me-1" style="color:#0891b2;"></i>{{ sab.comparatifOrganisations.titre || 'Comparatif organisations' }}
                  </div>
                  <div class="rounded-3 overflow-hidden" style="border:1px solid #e5e7eb;">
                    <div class="table-responsive" style="max-height:320px;overflow-y:auto;">
                      <table class="table table-sm mb-0" style="font-size:11px;">
                        <thead style="position:sticky;top:0;z-index:1;background:#f1f5f9;">
                          <tr>
                            <th *ngFor="let col of sab.comparatifOrganisations.colonnes; let ci=index"
                                class="fw-semibold py-2 px-2"
                                [style.text-align]="ci===0?'left':'center'"
                                style="white-space:nowrap;color:#374151;border-bottom:2px solid #e2e8f0;">
                              {{ col }}
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr *ngFor="let ligne of sab.comparatifOrganisations.lignes; let ri=index"
                              [style.background]="ri%2===0?'#fff':'#f9fafb'">
                            <td class="fw-semibold py-2 px-2" style="white-space:nowrap;color:#1e293b;">{{ ligne.organisation }}</td>
                            <td *ngFor="let val of ligne.valeurs" class="py-2 px-2 text-center">
                              <span *ngIf="val==='✓'" style="color:#16a34a;font-size:13px;">✓</span>
                              <span *ngIf="val==='✗'" style="color:#dc2626;font-size:13px;">✗</span>
                              <span *ngIf="val==='Partiel'" class="badge rounded-pill px-2" style="background:#fef9c3;color:#854d0e;font-size:9px;">Partiel</span>
                              <span *ngIf="val!=='✓' && val!=='✗' && val!=='Partiel'" class="text-muted" style="font-size:10px;">{{ val }}</span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="px-3 py-1 text-end" style="font-size:9px;color:#9ca3af;background:#f8fafc;border-top:1px solid #e5e7eb;">
                      Contenu figé — Sources : rapports annuels et enquêtes terrain 2023-2024
                    </div>
                  </div>
                </div>

                <!-- Cadre juridique + M&A -->
                <div class="row g-3 mb-3">
                  <div class="col-md-6" *ngIf="sab.cadreJuridique?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#fafafa;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-balance-scale me-1" style="color:#0891b2;"></i>Cadre juridique
                      </div>
                      <div *ngFor="let c of sab.cadreJuridique.slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="d-flex align-items-start gap-2">
                          <span class="badge rounded-pill flex-shrink-0 mt-1"
                                style="font-size:9px;"
                                [style.background]="c.impact==='Obligation'?'#fef2f2':c.impact==='Opportunité'?'#f0fdf4':'#f0f9ff'"
                                [style.color]="c.impact==='Obligation'?'#dc2626':c.impact==='Opportunité'?'#166534':'#0369a1'">
                            {{ c.impact }}
                          </span>
                          <div>
                            <div class="small fw-semibold">{{ c.texte }}</div>
                            <div class="text-muted" style="font-size:11px;">{{ c.description }}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6" *ngIf="sab.maLeveesFonds?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#fafafa;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-coins me-1" style="color:#10b981;"></i>M&amp;A &amp; Levées de fonds
                      </div>
                      <div *ngFor="let m of sab.maLeveesFonds.slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="d-flex align-items-center gap-2 mb-1">
                          <span class="badge rounded-pill" style="font-size:9px;background:#dcfce7;color:#166534;">{{ m.annee }}</span>
                          <span *ngIf="m.montant && m.montant!=='Non divulgué' && m.montant!=='N/A'"
                                class="small fw-semibold" style="color:#059669;">{{ m.montant }}</span>
                          <span class="badge rounded-pill" style="font-size:9px;background:#e0f2fe;color:#0369a1;">{{ m.operation }}</span>
                        </div>
                        <div class="text-muted" style="font-size:11px;line-height:1.4;">{{ m.detail | slice:0:130 }}…</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Risques + Opportunités -->
                <div class="row g-3 mb-3" *ngIf="sab.risques?.length || sab.opportunites?.length">
                  <div class="col-md-6" *ngIf="sab.risques?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#fff5f5;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-exclamation-triangle me-1" style="color:#dc2626;"></i>Risques sectoriels
                      </div>
                      <div *ngFor="let r of (sab.risques || []).slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="d-flex align-items-start gap-2 mb-1">
                          <span class="badge rounded-pill flex-shrink-0 mt-1"
                                style="font-size:9px;background:#fee2e2;color:#b91c1c;">{{ r.severity }}</span>
                          <div class="small fw-semibold" style="color:#7f1d1d;">{{ r.title }}</div>
                        </div>
                        <div class="text-muted" style="font-size:11px;line-height:1.4;">{{ r.description | slice:0:120 }}…</div>
                        <div *ngIf="r.mitigation" class="mt-1 rounded-2 px-2 py-1" style="background:#fef2f2;font-size:10px;color:#9f1239;">
                          <i class="fas fa-shield-alt me-1"></i>{{ r.mitigation | slice:0:100 }}…
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6" *ngIf="sab.opportunites?.length">
                    <div class="rounded-3 p-3 h-100" style="background:#f0fdf4;">
                      <div class="fw-semibold small mb-2" style="color:#374151;">
                        <i class="fas fa-lightbulb me-1" style="color:#16a34a;"></i>Opportunités sectorielles
                      </div>
                      <div *ngFor="let o of (sab.opportunites || []).slice(0,3)" class="mb-2 pb-2 border-bottom border-light">
                        <div class="d-flex align-items-start gap-2 mb-1">
                          <span class="badge rounded-pill flex-shrink-0 mt-1"
                                style="font-size:9px;background:#dcfce7;color:#15803d;">{{ o.impact_level }}</span>
                          <div class="small fw-semibold" style="color:#14532d;">{{ o.title }}</div>
                        </div>
                        <div class="text-muted" style="font-size:11px;line-height:1.4;">{{ o.description | slice:0:120 }}…</div>
                        <div *ngIf="o.time_to_value || o.prerequisite_maturity" class="mt-1 d-flex gap-2 flex-wrap">
                          <span *ngIf="o.time_to_value" class="badge rounded-pill"
                                style="font-size:9px;background:#bbf7d0;color:#166534;">
                            <i class="fas fa-clock me-1"></i>{{ o.time_to_value }}
                          </span>
                          <span *ngIf="o.prerequisite_maturity" class="badge rounded-pill"
                                style="font-size:9px;background:#e0f2fe;color:#075985;">
                            <i class="fas fa-layer-group me-1"></i>{{ o.prerequisite_maturity }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Maturité maximale -->
                <div *ngIf="sab.maturiteMaximale" class="rounded-3 p-3"
                     style="background:#f0fdf4;border-left:3px solid #10b981;">
                  <div class="fw-semibold small mb-1" style="color:#065f46;">
                    <i class="fas fa-star me-1" style="color:#10b981;"></i>Maturité maximale — référence d'excellence
                  </div>
                  <p class="small mb-0" style="color:#047857;">{{ sab.maturiteMaximale }}</p>
                </div>

              </div><!-- /body -->
            </div><!-- /card -->
          </ng-container>
        </div>

        <!-- Footer: boutons action -->
        <div class="mt-4 d-flex justify-content-end gap-2 align-items-center flex-wrap">
          <div *ngIf="validateError" class="alert alert-danger py-2 px-3 mb-0 me-auto small">{{ validateError }}</div>

          <!-- Télécharger PDF -->
          <button class="btn btn-outline-secondary px-3 rounded-pill" (click)="downloadPdf()" [disabled]="pdfDownloading">
            <span *ngIf="pdfDownloading" class="spinner-border spinner-border-sm me-1" style="width:13px;height:13px;"></span>
            <i *ngIf="!pdfDownloading" class="fas fa-file-pdf me-2" style="color:#dc2626;"></i>
            Télécharger PDF
          </button>

          <!-- Télécharger PPT -->
          <button class="btn btn-outline-secondary px-3 rounded-pill" (click)="downloadPpt()" [disabled]="pptDownloading">
            <span *ngIf="pptDownloading" class="spinner-border spinner-border-sm me-1" style="width:13px;height:13px;"></span>
            <i *ngIf="!pptDownloading" class="fas fa-file-powerpoint me-2" style="color:#d04423;"></i>
            Télécharger PPT
          </button>

          <button *ngIf="!validated" class="btn btn-primary px-4 rounded-pill" (click)="validate()" [disabled]="validating">
            <span *ngIf="validating" class="spinner-border spinner-border-sm me-2"></span>
            <i *ngIf="!validating" class="fas fa-paper-plane me-2"></i>
            Valider et envoyer par email
          </button>
        </div>
        <div *ngIf="validated" class="mt-4 alert alert-success">
          <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
            <span class="fw-semibold">
              <i class="fas fa-check-circle me-2"></i>Résultats envoyés à l'entreprise.
            </span>
            <a [routerLink]="['/consultant/action-plan', evaluationId]"
               class="btn btn-sm btn-success rounded-pill px-3">
              <i class="fas fa-tasks me-1"></i>Voir le plan d'action
            </a>
          </div>
        </div>
        <div *ngIf="validateSuccess" class="mt-3 alert alert-info">
          <i class="fas fa-envelope me-2"></i>{{ validateSuccess }}
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

  targetMaturityLevel = '';
  editTargetLevel = '';
  editingTargetMaturity = false;
  targetMaturitySaving = false;
  targetMaturitySuccess = '';
  targetMaturityError = '';

  readonly maturityLevels = ['INITIAL', 'BASIQUE', 'INTERMEDIAIRE', 'AVANCE', 'OPTIMISE'];

  showBenchPromptPanel = false;
  benchConsultantPrompt = '';
  benchRegenerating = false;
  benchRegenerateError = '';
  benchRegenerateSuccess = '';

  pdfDownloading = false;
  pptDownloading = false;

  showTrendForm = false;
  editingTrendIdx: number | null = null;
  trendDraft: { title: string; description: string; impactLevel: string; horizon: string; adoptionRate: string; source: string } =
    { title: '', description: '', impactLevel: 'MOYEN', horizon: 'Moyen terme', adoptionRate: '', source: '' };

  axisBars: { label: string; score: number; color: string }[] = [];
  subAxisBenchmarks: SubAxisBenchmark[] = [];
  openSubAxes = new Set<string>();

  private readonly axisColors: Record<string, string> = {
    METIER: '#0d6efd',              BUSINESS: '#0d6efd',
    PROCESSUS: '#198754',           PROCESS: '#198754',
    SI: '#6366f1',                  INFORMATION_SYSTEM: '#6366f1',
    CANAUX_DISTRIBUTION: '#0891b2',
    MARKETING_COMMUNICATION: '#d97706',
    RH_CULTURE_DIGITALE: '#7c3aed',
    OFFRES_DIGITALES: '#059669',
    MODELE_OPERATIONNEL_INNOVATION: '#e11d48',
    IT_DATA: '#0284c7',
  };

  readonly axisLabels: Record<string, string> = {
    METIER: 'Métier',       BUSINESS: 'Métier',
    PROCESSUS: 'Processus', PROCESS: 'Processus',
    SI: 'SI',               INFORMATION_SYSTEM: 'Système d\'Information',
    CANAUX_DISTRIBUTION: 'Canaux & UX',
    MARKETING_COMMUNICATION: 'Marketing',
    RH_CULTURE_DIGITALE: 'RH & Culture',
    OFFRES_DIGITALES: 'Offres Digitales',
    MODELE_OPERATIONNEL_INNOVATION: 'Modèle Opérationnel & Innovation',
    IT_DATA: 'IT & Data',
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
          { key: 'METIER',                         label: 'Métier',                             color: '#0d6efd' },
          { key: 'PROCESSUS',                      label: 'Processus',                          color: '#198754' },
          { key: 'SI',                             label: 'Système d\'Information',             color: '#6366f1' },
          { key: 'CANAUX_DISTRIBUTION',            label: 'Canaux & UX',                        color: '#0891b2' },
          { key: 'MARKETING_COMMUNICATION',        label: 'Marketing & Communication',          color: '#d97706' },
          { key: 'RH_CULTURE_DIGITALE',            label: 'RH & Culture Digitale',             color: '#7c3aed' },
          { key: 'OFFRES_DIGITALES',               label: 'Offres Digitales',                  color: '#059669' },
          { key: 'MODELE_OPERATIONNEL_INNOVATION', label: 'Modèle Opérationnel & Innovation',  color: '#e11d48' },
          { key: 'IT_DATA',                        label: 'IT & Data',                         color: '#0284c7' },
        ];
        this.axisBars = allAxes
          .map(a => ({
            label: a.label,
            score: (ev.scoresByAxis || []).find((s: AxisScore) => s.axis === a.key)?.score || 0,
            color: a.color
          }))
          ;
        this.targetMaturityLevel = ev.targetMaturityLevel || '';
        this.editTargetLevel = this.targetMaturityLevel || this.suggestNextMaturity(this.maturityLevel);
        this.recommendations = (data.recommendations || []).map((r: Recommendation) => ({ ...r, editing: false }));
        this.benchmark = data.benchmark && Object.keys(data.benchmark).length > 0 ? data.benchmark : null;
        this.subAxisBenchmarks = this.benchmark?.subAxisBenchmarks || [];
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

    // Step 1 — Recommendations (critical path)
    this.http.post<any[]>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate`, { consultantPrompt: '' }
    ).subscribe({
      next: (recs) => {
        this.recommendations = recs.map((r: Recommendation) => ({ ...r, editing: false }));
        this.initialGenerating = false;
        this.aiPending = recs.length === 0;
        // Step 2 — Benchmark runs AFTER recommendations to avoid Groq rate limits
        this._generateBenchmarkBackground();
      },
      error: (err) => {
        this.initialGenerateError = this.parseAiError(err);
        this.initialGenerating = false;
        this._generateBenchmarkBackground();
      }
    });
  }

  private _generateBenchmarkBackground() {
    this.benchRegenerating = true;
    this.benchRegenerateError = '';
    this.http.post<any>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/regenerate-benchmark`, { consultantPrompt: '' }
    ).subscribe({
      next: (bench) => {
        this.benchmark = bench && Object.keys(bench).length > 0 ? bench : null;
        this.subAxisBenchmarks = bench?.subAxisBenchmarks || [];
        this.openSubAxes.clear();
        this.benchRegenerating = false;
      },
      error: (err) => {
        this.benchRegenerating = false;
        this.benchRegenerateError = this.parseAiError(err);
      }
    });
  }

  generateRecs() {
    this.consultantPrompt = '';
    this.regenerate();
  }

  private parseAiError(err: any): string {
    const raw: string = err?.error?.message || err?.error?.detail || err?.message || '';
    if (raw.includes('429') || raw.includes('RATE_LIMIT') || raw.toLowerCase().includes('quota')) {
      const waitMatch = raw.match(/Attendez (\d+)/);
      const wait = waitMatch ? waitMatch[1] : '60';
      return `⏱ Quota Groq atteint — le service IA a reçu trop de requêtes. Attendez ${wait} secondes puis réessayez.`;
    }
    if (raw.includes('503') || raw.includes('unavailable') || raw.includes('inaccessible') || raw.includes('unreachable')) {
      return '⚠️ Service IA indisponible. Vérifiez que le service Python est démarré (uvicorn main:app) puis réessayez.';
    }
    if (raw.includes('timeout') || raw.includes('TimeoutException')) {
      return '⏳ Le service IA a mis trop de temps à répondre. Réessayez dans quelques instants.';
    }
    if (raw) return raw;
    return '❌ Erreur lors de la génération. Réessayez dans quelques instants.';
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
        this.subAxisBenchmarks = bench?.subAxisBenchmarks || [];
        this.openSubAxes.clear();
        this.benchRegenerating = false;
        this.benchRegenerateSuccess = 'Benchmarking régénéré avec succès.';
      },
      error: (err) => {
        this.benchRegenerating = false;
        this.benchRegenerateError = this.parseAiError(err);
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
        this.regenerateError = this.parseAiError(err);
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

  getMaturityLevelLabel(level: string): string {
    const labels: Record<string, string> = {
      INITIAL: 'Initial', BASIQUE: 'Basique', INTERMEDIAIRE: 'Intermédiaire',
      AVANCE: 'Avancé', OPTIMISE: 'Optimisé'
    };
    return labels[level] ?? level;
  }

  getMaturityLevelBg(level: string): string {
    if (level === this.targetMaturityLevel) return '#166534';
    if (level === this.maturityLevel) return '#dbeafe';
    const ci = this.maturityLevels.indexOf(this.maturityLevel);
    const li = this.maturityLevels.indexOf(level);
    if (ci >= 0 && li < ci) return '#f0fdf4';
    return '#f9fafb';
  }

  getMaturityLevelColor(level: string): string {
    if (level === this.targetMaturityLevel) return '#ffffff';
    if (level === this.maturityLevel) return '#1768e5';
    const ci = this.maturityLevels.indexOf(this.maturityLevel);
    const li = this.maturityLevels.indexOf(level);
    if (ci >= 0 && li < ci) return '#16a34a';
    return '#9ca3af';
  }

  startEditTargetMaturity() {
    this.targetMaturitySuccess = '';
    this.targetMaturityError = '';
    this.editTargetLevel = this.targetMaturityLevel || this.suggestNextMaturity(this.maturityLevel);
    this.editingTargetMaturity = true;
  }

  saveTargetMaturity() {
    this.targetMaturitySuccess = '';
    this.targetMaturityError = '';
    this.targetMaturitySaving = true;
    this.http.put<void>(
      `${environment.apiUrl}/evaluations/${this.evaluationId}/target-maturity`,
      { targetMaturityLevel: this.editTargetLevel }
    ).subscribe({
      next: () => {
        this.targetMaturityLevel = this.editTargetLevel;
        this.targetMaturitySaving = false;
        this.editingTargetMaturity = false;
        this.targetMaturitySuccess = 'Maturité cible mise à jour.';
      },
      error: (err) => {
        this.targetMaturitySaving = false;
        this.targetMaturityError = err?.error?.message || 'Erreur lors de la mise à jour.';
      }
    });
  }

  private suggestNextMaturity(current: string): string {
    const idx = this.maturityLevels.indexOf(current);
    return idx >= 0 && idx < this.maturityLevels.length - 1 ? this.maturityLevels[idx + 1] : current;
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

  async downloadPpt(): Promise<void> {
    this.pptDownloading = true;
    try {
      const PptxGenJS = (await import('pptxgenjs')).default;
      const pptx = new (PptxGenJS as any)();
      pptx.layout = 'LAYOUT_WIDE'; // 13.33" × 7.5"

      const BLU = '1768e5', DRK = '1e293b', GRY = '64748b', WHT = 'FFFFFF';
      const LIT = 'f8fafc', BDR = 'e2e8f0', BLU2 = 'b0c8f0';

      const addHeader = (slide: any, title: string) => {
        slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 0.75, fill: { color: BLU } });
        slide.addText('IA Benchmark', { x: 0.3, y: 0.13, w: 3.5, h: 0.5, color: WHT, fontSize: 13, bold: true, fontFace: 'Arial' });
        slide.addText(title, { x: 3.8, y: 0.13, w: 9.3, h: 0.5, color: WHT, fontSize: 12, align: 'right', fontFace: 'Arial' });
      };

      // ── SLIDE 1 : COVER ─────────────────────────────────────────────
      const s1 = pptx.addSlide();
      s1.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: '100%', fill: { color: BLU } });
      s1.addText('Rapport de Maturité Digitale', {
        x: 0.5, y: 0.9, w: 12.3, h: 1.1, color: WHT, fontSize: 34, bold: true, align: 'center', fontFace: 'Arial'
      });
      s1.addShape(pptx.ShapeType.rect, { x: 2.5, y: 2.25, w: 8.3, h: 0.04, fill: { color: BLU2 } });
      s1.addText(this.companyName, {
        x: 0.5, y: 2.45, w: 12.3, h: 0.8, color: WHT, fontSize: 26, align: 'center', fontFace: 'Arial'
      });
      s1.addShape(pptx.ShapeType.ellipse, { x: 5.6, y: 3.65, w: 2.1, h: 2.1, fill: { color: '1050bb' }, line: { color: WHT, width: 2.5 } });
      s1.addText(String(Math.round(this.globalScore)), {
        x: 5.6, y: 3.85, w: 2.1, h: 1.0, color: WHT, fontSize: 38, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial'
      });
      s1.addText('/100', { x: 5.6, y: 4.8, w: 2.1, h: 0.4, color: BLU2, fontSize: 12, align: 'center', fontFace: 'Arial' });
      s1.addShape(pptx.ShapeType.rect, { x: 4.9, y: 6.05, w: 3.5, h: 0.6, fill: { color: WHT } });
      s1.addText(`Niveau : ${this.getMaturityLevelLabel(this.maturityLevel)}`, {
        x: 4.9, y: 6.05, w: 3.5, h: 0.6, color: BLU, fontSize: 12, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial'
      });
      s1.addText(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, {
        x: 0.5, y: 6.95, w: 12.3, h: 0.35, color: BLU2, fontSize: 10, align: 'center', fontFace: 'Arial'
      });

      // ── SLIDE 2 : SCORES PAR AXE ────────────────────────────────────
      const s2 = pptx.addSlide();
      addHeader(s2, 'Résultats de maturité digitale');
      s2.addText('Scores par axe', { x: 0.4, y: 0.92, w: 12.5, h: 0.6, color: DRK, fontSize: 20, bold: true, fontFace: 'Arial' });

      s2.addShape(pptx.ShapeType.rect, { x: 0.4, y: 1.68, w: 3.0, h: 1.85, fill: { color: BLU } });
      s2.addText('Score global', { x: 0.4, y: 1.73, w: 3.0, h: 0.4, color: BLU2, fontSize: 10, align: 'center', fontFace: 'Arial' });
      s2.addText(String(Math.round(this.globalScore)), {
        x: 0.4, y: 2.1, w: 3.0, h: 0.9, color: WHT, fontSize: 42, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial'
      });
      s2.addText('/100', { x: 0.4, y: 3.0, w: 3.0, h: 0.3, color: BLU2, fontSize: 11, align: 'center', fontFace: 'Arial' });
      s2.addShape(pptx.ShapeType.rect, { x: 0.4, y: 3.63, w: 3.0, h: 0.65, fill: { color: LIT }, line: { color: BDR, width: 1 } });
      s2.addText(`Niveau : ${this.getMaturityLevelLabel(this.maturityLevel)}`, {
        x: 0.4, y: 3.63, w: 3.0, h: 0.65, color: DRK, fontSize: 10, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial'
      });

      const barsToShow = this.axisBars.filter(a => a.score > 0);
      const barAreaX = 7.0, maxBarW = 5.5, barH = 0.33, rowH = 0.47;
      barsToShow.forEach((a, i) => {
        const rowY = 1.68 + i * rowH;
        const axHex = a.color.replace('#', '');
        s2.addText(a.label, { x: 3.8, y: rowY + 0.07, w: 3.1, h: barH, color: DRK, fontSize: 9.5, align: 'right', valign: 'middle', fontFace: 'Arial' });
        s2.addShape(pptx.ShapeType.rect, { x: barAreaX, y: rowY + 0.1, w: maxBarW, h: barH - 0.1, fill: { color: 'f1f5f9' }, line: { color: 'f1f5f9' } });
        s2.addShape(pptx.ShapeType.rect, { x: barAreaX, y: rowY + 0.1, w: Math.max(0.1, (a.score / 100) * maxBarW), h: barH - 0.1, fill: { color: axHex }, line: { color: axHex } });
        s2.addText(String(Math.round(a.score)), { x: barAreaX + maxBarW + 0.1, y: rowY + 0.06, w: 0.55, h: barH, color: axHex, fontSize: 10, bold: true, valign: 'middle', fontFace: 'Arial' });
      });

      // ── SLIDES 3+ : RECOMMANDATIONS ─────────────────────────────────
      const pColors: Record<string, string> = { HAUTE: 'dc2626', MOYENNE: 'd97706', BASSE: '16a34a' };
      const pLabels: Record<string, string> = { HAUTE: 'Priorité HAUTE', MOYENNE: 'Priorité MOYENNE', BASSE: 'Priorité BASSE' };
      for (const prio of ['HAUTE', 'MOYENNE', 'BASSE']) {
        const recs = this.recommendations.filter(r => r.priority === prio);
        if (!recs.length) continue;
        const pCol = pColors[prio];
        for (let gi = 0; gi < recs.length; gi += 4) {
          const chunk = recs.slice(gi, gi + 4);
          const sr = pptx.addSlide();
          addHeader(sr, 'Recommandations');
          sr.addShape(pptx.ShapeType.rect, { x: 0.4, y: 0.88, w: 2.5, h: 0.42, fill: { color: pCol } });
          sr.addText(pLabels[prio], { x: 0.4, y: 0.88, w: 2.5, h: 0.42, color: WHT, fontSize: 10, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial' });
          sr.addText(`${this.companyName}  ·  ${new Date().toLocaleDateString('fr-FR')}`, { x: 3.1, y: 0.93, w: 10, h: 0.3, color: GRY, fontSize: 9.5, fontFace: 'Arial' });
          chunk.forEach((rec, ri) => {
            const cardY = 1.45 + ri * 1.48;
            const axHex = this.getAxisColor(rec.axis).replace('#', '');
            sr.addShape(pptx.ShapeType.rect, { x: 0.4, y: cardY, w: 12.5, h: 1.35, fill: { color: LIT }, line: { color: BDR, width: 0.75 } });
            sr.addShape(pptx.ShapeType.rect, { x: 0.4, y: cardY, w: 0.12, h: 1.35, fill: { color: axHex } });
            sr.addText(this.getAxisLabel(rec.axis), { x: 0.6, y: cardY + 0.06, w: 2.0, h: 0.28, fill: { color: LIT }, color: axHex, fontSize: 9, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial' });
            sr.addText(rec.title || '', { x: 0.6, y: cardY + 0.38, w: 12.1, h: 0.32, color: DRK, fontSize: 10.5, bold: true, fontFace: 'Arial' });
            const desc = (rec.description || '').length > 200 ? rec.description!.slice(0, 200) + '…' : (rec.description || '');
            sr.addText(desc, { x: 0.6, y: cardY + 0.72, w: 12.1, h: 0.35, color: GRY, fontSize: 9, fontFace: 'Arial' });
            if (rec.source) {
              sr.addText(rec.source, { x: 0.6, y: cardY + 1.1, w: 12.1, h: 0.2, color: '9ca3af', fontSize: 8, italic: true, fontFace: 'Arial' });
            }
          });
        }
      }

      // ── SLIDE : BENCHMARKING ────────────────────────────────────────
      if (this.benchmark?.sectorBenchmark) {
        const sb = pptx.addSlide();
        addHeader(sb, 'Benchmarking sectoriel');
        sb.addText('Positionnement sectoriel', { x: 0.4, y: 0.92, w: 12.5, h: 0.6, color: DRK, fontSize: 20, bold: true, fontFace: 'Arial' });
        const bm = this.benchmark.sectorBenchmark;
        const kpis = [
          { label: 'Score entreprise',   val: String(Math.round(this.globalScore)),              color: BLU },
          { label: 'Moy. nationale',     val: (bm.nationalAverage || 0).toFixed(1),              color: '0891b2' },
          { label: 'Moy. internationale',val: (bm.internationalAverage || 0).toFixed(1),         color: '059669' },
          { label: 'Top quartile',       val: (bm.topQuartileScore || 0).toFixed(1),             color: '7c3aed' },
        ];
        kpis.forEach((k, ki) => {
          const kx = 0.4 + ki * 3.2;
          sb.addShape(pptx.ShapeType.rect, { x: kx, y: 1.68, w: 2.9, h: 1.85, fill: { color: LIT }, line: { color: BDR, width: 1 } });
          sb.addText(k.val, { x: kx, y: 1.75, w: 2.9, h: 1.0, color: k.color, fontSize: 36, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial' });
          sb.addText('/100', { x: kx, y: 2.7, w: 2.9, h: 0.3, color: GRY, fontSize: 10, align: 'center', fontFace: 'Arial' });
          sb.addText(k.label, { x: kx, y: 3.1, w: 2.9, h: 0.35, color: DRK, fontSize: 10, bold: true, align: 'center', fontFace: 'Arial' });
        });
        if (bm.positioningLabel) {
          sb.addShape(pptx.ShapeType.rect, { x: 0.4, y: 3.65, w: 12.5, h: 0.5, fill: { color: 'dbeafe' }, line: { color: 'bfdbfe', width: 1 } });
          sb.addText(`Positionnement : ${bm.positioningLabel}  ·  Percentile ${bm.companyPercentile}e`, {
            x: 0.4, y: 3.65, w: 12.5, h: 0.5, color: BLU, fontSize: 12, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial'
          });
        }
        if (this.benchmark.axisBenchmarks?.length) {
          const hdr = { bold: true, fill: { color: BLU }, color: WHT, fontSize: 9, fontFace: 'Arial' };
          const rows: any[][] = [[
            { text: 'Axe', options: { ...hdr, align: 'left' } },
            { text: 'Score', options: { ...hdr, align: 'center' } },
            { text: 'Moy. sect.', options: { ...hdr, align: 'center' } },
            { text: 'Top Q.', options: { ...hdr, align: 'center' } },
            { text: 'Écart', options: { ...hdr, align: 'center' } },
          ]];
          this.benchmark.axisBenchmarks.forEach((ab: any, idx: number) => {
            const bg = idx % 2 === 0 ? LIT : WHT;
            const gc = (ab.gapToAverage ?? 0) >= 0 ? '16a34a' : 'dc2626';
            rows.push([
              { text: ab.axisLabel || ab.axis, options: { fill: { color: bg }, color: DRK, fontSize: 9, bold: true, fontFace: 'Arial' } },
              { text: `${(ab.companyScore || 0).toFixed(1)}`, options: { fill: { color: bg }, color: BLU, fontSize: 9, bold: true, align: 'center', fontFace: 'Arial' } },
              { text: `${(ab.sectorAverage || 0).toFixed(1)}`, options: { fill: { color: bg }, color: DRK, fontSize: 9, align: 'center', fontFace: 'Arial' } },
              { text: `${(ab.topQuartile || 0).toFixed(1)}`, options: { fill: { color: bg }, color: DRK, fontSize: 9, align: 'center', fontFace: 'Arial' } },
              { text: `${(ab.gapToAverage ?? 0) >= 0 ? '+' : ''}${(ab.gapToAverage || 0).toFixed(1)}`, options: { fill: { color: bg }, color: gc, fontSize: 9, bold: true, align: 'center', fontFace: 'Arial' } },
            ]);
          });
          sb.addTable(rows, { x: 0.4, y: 4.3, w: 12.5, rowH: 0.32, border: { type: 'solid', color: BDR, pt: 0.5 } });
        }
      }

      // ── SLIDE : TENDANCES SECTORIELLES ──────────────────────────────
      if ((this.benchmark?.trends as Trend[] | undefined)?.length) {
        const st = pptx.addSlide();
        addHeader(st, 'Tendances sectorielles');
        st.addText('Tendances sectorielles', { x: 0.4, y: 0.92, w: 12.5, h: 0.6, color: DRK, fontSize: 20, bold: true, fontFace: 'Arial' });
        (this.benchmark.trends as Trend[]).slice(0, 6).forEach((t, ti) => {
          const col = ti % 2, row = Math.floor(ti / 2);
          const tx = 0.4 + col * 6.5, ty = 1.65 + row * 1.85;
          const ic = (t.impactLevel === 'ELEVE' || t.impactLevel === 'ÉLEVÉ' || t.impactLevel === 'HIGH') ? 'ef4444'
                   : t.impactLevel === 'FAIBLE' ? '16a34a' : 'd97706';
          st.addShape(pptx.ShapeType.rect, { x: tx, y: ty, w: 6.2, h: 1.7, fill: { color: LIT }, line: { color: BDR, width: 0.75 } });
          st.addShape(pptx.ShapeType.rect, { x: tx, y: ty, w: 0.1, h: 1.7, fill: { color: '0891b2' } });
          st.addText(t.title || '', { x: tx + 0.2, y: ty + 0.1, w: 4.8, h: 0.3, color: DRK, fontSize: 10, bold: true, fontFace: 'Arial' });
          st.addText(t.impactLevel || '', { x: tx + 5.2, y: ty + 0.1, w: 1.0, h: 0.28, fill: { color: 'f3f4f6' }, color: ic, fontSize: 8.5, bold: true, align: 'center', valign: 'middle', fontFace: 'Arial' });
          const desc = (t.description || '').length > 160 ? t.description.slice(0, 160) + '…' : (t.description || '');
          st.addText(desc, { x: tx + 0.2, y: ty + 0.45, w: 6.0, h: 0.8, color: GRY, fontSize: 8.5, fontFace: 'Arial' });
          st.addText(`${t.horizon}  ·  ${t.adoptionRate}  ·  ${t.source}`, { x: tx + 0.2, y: ty + 1.35, w: 6.0, h: 0.28, color: '9ca3af', fontSize: 8, italic: true, fontFace: 'Arial' });
        });
      }

      // ── SLIDE FINALE ────────────────────────────────────────────────
      const sf = pptx.addSlide();
      sf.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: '100%', fill: { color: BLU } });
      sf.addText('Merci', { x: 0.5, y: 2.2, w: 12.3, h: 1.3, color: WHT, fontSize: 48, bold: true, align: 'center', fontFace: 'Arial' });
      sf.addText(this.companyName, { x: 0.5, y: 3.7, w: 12.3, h: 0.7, color: BLU2, fontSize: 22, align: 'center', fontFace: 'Arial' });
      sf.addText('Ce rapport a été généré par IA Benchmark — Confidentiel', {
        x: 0.5, y: 7.0, w: 12.3, h: 0.35, color: '7ca8e0', fontSize: 9.5, align: 'center', fontFace: 'Arial'
      });

      const fileName = `rapport-${this.companyName.replace(/[^a-zA-Z0-9]/g, '-')}-${new Date().toISOString().slice(0, 10)}.pptx`;
      await pptx.writeFile({ fileName });

    } catch (err) {
      console.error('PPT generation error:', err);
    } finally {
      this.pptDownloading = false;
    }
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

  getAxisColor(axis: string): string { return this.axisColors[axis] ?? '#6c757d'; }
  getAxisLabel(axis: string): string { return this.axisLabels[axis] ?? axis; }
  getPriorityColor(p: string): string { return this.priorityColors[p] ?? '#6c757d'; }

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

  maturityBg(level: string): string {
    return ({ INITIAL: '#fef2f2', BASIQUE: '#fff7ed', INTERMEDIAIRE: '#fefce8', AVANCE: '#eff6ff', OPTIMISE: '#f0fdf4' } as Record<string,string>)[level] ?? '#f1f5f9';
  }

  maturityColor(level: string): string {
    return ({ INITIAL: '#ef4444', BASIQUE: '#f97316', INTERMEDIAIRE: '#ca8a04', AVANCE: '#3b82f6', OPTIMISE: '#16a34a' } as Record<string,string>)[level] ?? '#6c757d';
  }

  // ── Sub-axis accordion ────────────────────────────────────────────────────
  get groupedSubAxisBenchmarks(): { axis: string; items: SubAxisBenchmark[] }[] {
    const groups: Record<string, SubAxisBenchmark[]> = {};
    for (const sab of this.subAxisBenchmarks) {
      if (!groups[sab.axis]) groups[sab.axis] = [];
      groups[sab.axis].push(sab);
    }
    return Object.entries(groups).map(([axis, items]) => ({ axis, items }));
  }

  toggleSubAxis(key: string): void {
    this.openSubAxes.has(key) ? this.openSubAxes.delete(key) : this.openSubAxes.add(key);
  }

  isSubAxisOpen(key: string): boolean { return this.openSubAxes.has(key); }

  allLeaders(sab: SubAxisBenchmark): any[] {
    return [...(sab.leadersNationaux || []), ...(sab.leadersRegionaux || []), ...(sab.leadersInternationaux || [])];
  }

  // ── Tendances sectorielles CRUD ───────────────────────────────────────────
  openAddTrend(): void {
    this.editingTrendIdx = null;
    this.trendDraft = { title: '', description: '', impactLevel: 'MOYEN', horizon: 'Moyen terme', adoptionRate: '', source: '' };
    this.showTrendForm = true;
  }

  openEditTrend(i: number): void {
    const t = this.benchmark.trends[i] as Trend;
    this.editingTrendIdx = i;
    this.trendDraft = {
      title: t.title || '',
      description: t.description || '',
      impactLevel: t.impactLevel || 'MOYEN',
      horizon: t.horizon || 'Moyen terme',
      adoptionRate: t.adoptionRate || '',
      source: t.source || ''
    };
    this.showTrendForm = true;
  }

  saveTrend(): void {
    if (!this.trendDraft.title.trim()) return;
    const trend: Trend = { ...this.trendDraft, sourceUrl: '' };
    if (!this.benchmark.trends) this.benchmark.trends = [];
    if (this.editingTrendIdx !== null) {
      this.benchmark.trends[this.editingTrendIdx] = trend;
    } else {
      this.benchmark.trends.push(trend);
    }
    this.showTrendForm = false;
    this.editingTrendIdx = null;
  }

  deleteTrend(i: number): void {
    this.benchmark.trends.splice(i, 1);
  }

  cancelTrend(): void {
    this.showTrendForm = false;
    this.editingTrendIdx = null;
  }
}
