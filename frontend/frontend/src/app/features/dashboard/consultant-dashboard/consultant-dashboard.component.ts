import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/models/user.model';
import { environment } from '../../../../environments/environment';

interface PendingEvaluation {
  evaluationId: number;
  companyId: number;
  companyName: string;
  globalScore: number;
  maturityLevel: string;
  status: string;
  createdAt: string;
}

@Component({
  selector: 'app-consultant-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container-fluid py-4" style="max-width:1100px;margin:auto;">
      <div class="mb-4">
        <h4 class="fw-bold mb-0">Dashboard Consultant</h4>
        <p class="text-muted mb-0 small">Bienvenue, {{ currentUser?.firstName || currentUser?.username }}</p>
      </div>

      <!-- Pending evaluations alert -->
      <div *ngIf="pendingEvaluations.length > 0"
           class="alert border-0 rounded-4 mb-4 d-flex align-items-center gap-3"
           style="background:#fff7ed;border-left:4px solid #f97316 !important;">
        <i class="fas fa-clock-rotate-left fa-lg" style="color:#f97316;"></i>
        <div class="flex-grow-1">
          <span class="fw-semibold" style="color:#9a3412;">
            {{ pendingEvaluations.length }} évaluation(s) en attente de validation
          </span>
          <span class="text-muted small ms-2">— Consultez, modifiez les recommandations et envoyez les résultats par email.</span>
        </div>
      </div>

      <!-- Pending evaluations list -->
      <div *ngIf="pendingEvaluations.length > 0" class="card border-0 shadow-sm rounded-4 mb-4">
        <div class="card-header bg-white border-0 pt-4 px-4 pb-2">
          <h6 class="fw-bold mb-0">
            <i class="fas fa-inbox text-warning me-2"></i>Évaluations à valider
          </h6>
        </div>
        <div class="card-body px-4 pb-4">
          <div *ngFor="let ev of pendingEvaluations"
               class="d-flex align-items-center gap-3 p-3 rounded-3 mb-2"
               style="background:#fafafa;border:1px solid #f1f5f9;">
            <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0 fw-bold text-white"
                 style="width:40px;height:40px;background:#f97316;font-size:14px;">
              {{ ev.companyName.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-grow-1">
              <div class="fw-semibold">{{ ev.companyName }}</div>
              <div class="text-muted small">
                Score : <strong>{{ ev.globalScore | number:'1.0-1' }}/100</strong> ·
                Niveau : <strong>{{ ev.maturityLevel }}</strong> ·
                Soumis le {{ ev.createdAt | date:'dd/MM/yyyy' }}
              </div>
            </div>
            <a [routerLink]="['/consultant/evaluations', ev.evaluationId, 'review']"
               class="btn btn-warning btn-sm rounded-pill px-3">
              <i class="fas fa-magnifying-glass me-1"></i>Consulter &amp; valider
            </a>
          </div>
        </div>
      </div>

      <!-- Quick-action cards -->
      <div class="row g-4">

        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #198754 !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#e8f5e9;">
                  <i class="fas fa-chart-line text-success fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold">Résultats & Analyses</div>
                  <div class="text-muted small">Vue complète par entreprise</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>Scores et niveaux de maturité</li>
                <li><i class="fas fa-check text-success me-2"></i>Recommandations IA</li>
                <li><i class="fas fa-check text-success me-2"></i>Complétude des questionnaires</li>
              </ul>
              <a routerLink="/consultant/analysis" class="btn btn-success btn-sm rounded-pill px-3">
                <i class="fas fa-chart-bar me-1"></i>Voir l'analyse
              </a>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #0d6efd !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#e3f2fd;">
                  <i class="fas fa-building text-primary fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold">Gestion des entreprises</div>
                  <div class="text-muted small">Consulter et gérer</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>Liste des entreprises</li>
                <li><i class="fas fa-check text-success me-2"></i>Ajouter une entreprise</li>
                <li><i class="fas fa-check text-success me-2"></i>Configurer le questionnaire</li>
              </ul>
              <div class="d-flex gap-2">
                <a routerLink="/companies" class="btn btn-primary btn-sm rounded-pill px-3">
                  <i class="fas fa-list me-1"></i>Liste
                </a>
                <a routerLink="/companies/new" class="btn btn-outline-primary btn-sm rounded-pill px-3">
                  <i class="fas fa-plus me-1"></i>Nouvelle
                </a>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #6366f1 !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#ede9fe;">
                  <i class="fas fa-brain fs-5" style="color:#6366f1;"></i>
                </div>
                <div>
                  <div class="fw-bold">Référentiels IA</div>
                  <div class="text-muted small">Frameworks de la base de connaissance</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>7 frameworks internationaux</li>
                <li><i class="fas fa-check text-success me-2"></i>Gartner, McKinsey, ISO, COBIT…</li>
                <li><i class="fas fa-check text-success me-2"></i>Critères par secteur</li>
              </ul>
              <a routerLink="/consultant/frameworks" class="btn btn-sm rounded-pill px-3"
                 style="background:#6366f1;color:#fff;">
                <i class="fas fa-eye me-1"></i>Explorer
              </a>
            </div>
          </div>
        </div>

      </div>
    </div>
  `
})
export class ConsultantDashboardComponent implements OnInit {
  currentUser: User | null = null;
  pendingEvaluations: PendingEvaluation[] = [];

  constructor(private authService: AuthService, private http: HttpClient) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    this.loadPendingEvaluations();
  }

  private loadPendingEvaluations() {
    this.http.get<any[]>(`${environment.apiUrl}/evaluations/pending-review`).subscribe({
      next: (data) => { this.pendingEvaluations = data || []; },
      error: () => { this.pendingEvaluations = []; }
    });
  }
}
