import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { CompanyService } from '../../../core/services/company.service';
import { UserService } from '../../../core/services/user.service';
import { EvaluationService, EvaluationSummary } from '../../../core/services/evaluation.service';
import { Company } from '../../../core/models/company.model';
import { User } from '../../../core/models/user.model';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container-fluid py-4" style="max-width:1200px;margin:auto;">

      <!-- ── Header ── -->
      <div class="mb-4">
        <h4 class="fw-bold mb-0">Dashboard Administrateur</h4>
        <p class="text-muted mb-0 small">Bienvenue, {{ currentUser?.firstName }} {{ currentUser?.lastName }}</p>
      </div>

      <!-- ── Stats ── -->
      <div class="row g-3 mb-4">
        <div class="col">
          <div class="card border-0 shadow-sm rounded-4 h-100">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width:48px;height:48px;background:#eff6ff;">
                <i class="fas fa-building" style="color:#1a56db;font-size:20px;"></i>
              </div>
              <div>
                <div class="fw-bold fs-4 mb-0" style="color:#0f172a;">{{ companies.length }}</div>
                <div class="text-muted small">Entreprises</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card border-0 shadow-sm rounded-4 h-100">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width:48px;height:48px;background:#f0fdf4;">
                <i class="fas fa-user-tie" style="color:#16a34a;font-size:20px;"></i>
              </div>
              <div>
                <div class="fw-bold fs-4 mb-0" style="color:#0f172a;">{{ consultantCount }}</div>
                <div class="text-muted small">Consultants</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card border-0 shadow-sm rounded-4 h-100">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width:48px;height:48px;background:#fefce8;">
                <i class="fas fa-chart-bar" style="color:#ca8a04;font-size:20px;"></i>
              </div>
              <div>
                <div class="fw-bold fs-4 mb-0" style="color:#0f172a;">{{ evaluatedCount }}</div>
                <div class="text-muted small">Évaluées</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card border-0 shadow-sm rounded-4 h-100">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width:48px;height:48px;background:#fef2f2;">
                <i class="fas fa-clock" style="color:#dc2626;font-size:20px;"></i>
              </div>
              <div>
                <div class="fw-bold fs-4 mb-0" style="color:#0f172a;">{{ pendingCount }}</div>
                <div class="text-muted small">En attente</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card border-0 shadow-sm rounded-4 h-100">
            <div class="card-body d-flex align-items-center gap-3 p-3">
              <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width:48px;height:48px;background:#f5f3ff;">
                <i class="fas fa-users" style="color:#7c3aed;font-size:20px;"></i>
              </div>
              <div>
                <div class="fw-bold fs-4 mb-0" style="color:#0f172a;">{{ totalUsers }}</div>
                <div class="text-muted small">Utilisateurs</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Quick-action cards ── -->
      <div class="row g-4">

        <!-- Entreprises -->
        <div class="col-md-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #0d6efd !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#e3f2fd;">
                  <i class="fas fa-building text-primary fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold">Gestion des entreprises</div>
                  <div class="text-muted small">Ajouter, modifier, supprimer</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>{{ companies.length }} entreprise(s) enregistrée(s)</li>
                <li><i class="fas fa-check text-success me-2"></i>Assigner des consultants</li>
                <li><i class="fas fa-check text-success me-2"></i>Configurer les questionnaires</li>
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

        <!-- Utilisateurs -->
        <div class="col-md-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #198754 !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#e8f5e9;">
                  <i class="fas fa-users text-success fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold">Gestion des utilisateurs</div>
                  <div class="text-muted small">Comptes & consultants</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>{{ consultantCount }} consultant(s) actif(s)</li>
                <li><i class="fas fa-check text-success me-2"></i>{{ totalUsers }} utilisateur(s) au total</li>
                <li><i class="fas fa-check text-success me-2"></i>Créer & gérer les accès</li>
              </ul>
              <div class="d-flex gap-2">
                <a routerLink="/users" class="btn btn-success btn-sm rounded-pill px-3">
                  <i class="fas fa-users me-1"></i>Utilisateurs
                </a>
                <a routerLink="/users/new" class="btn btn-outline-success btn-sm rounded-pill px-3">
                  <i class="fas fa-user-plus me-1"></i>Nouveau
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Résultats -->
        <div class="col-md-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #f59e0b !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#fefce8;">
                  <i class="fas fa-chart-bar fs-5" style="color:#ca8a04;"></i>
                </div>
                <div>
                  <div class="fw-bold">Résultats & Évaluations</div>
                  <div class="text-muted small">Scores et analyses</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>{{ evaluatedCount }} entreprise(s) évaluée(s)</li>
                <li><i class="fas fa-check text-success me-2"></i>{{ pendingCount }} en attente de validation</li>
                <li><i class="fas fa-check text-success me-2"></i>Niveaux de maturité & recommandations</li>
              </ul>
              <a routerLink="/companies" class="btn btn-sm rounded-pill px-3"
                 style="background:#f59e0b;color:#fff;">
                <i class="fas fa-chart-line me-1"></i>Voir les résultats
              </a>
            </div>
          </div>
        </div>

        <!-- Référentiels -->
        <div class="col-md-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="border-left:4px solid #6366f1 !important;">
            <div class="card-body p-4">
              <div class="d-flex align-items-center mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center me-3"
                     style="width:48px;height:48px;background:#ede9fe;">
                  <i class="fas fa-brain fs-5" style="color:#6366f1;"></i>
                </div>
                <div>
                  <div class="fw-bold">Référentiels & Questions</div>
                  <div class="text-muted small">Base de connaissance IA</div>
                </div>
              </div>
              <ul class="list-unstyled text-muted small mb-3">
                <li><i class="fas fa-check text-success me-2"></i>7 frameworks internationaux</li>
                <li><i class="fas fa-check text-success me-2"></i>Gartner, McKinsey, ISO, COBIT…</li>
                <li><i class="fas fa-check text-success me-2"></i>Base de questions administrable</li>
              </ul>
              <div class="d-flex gap-2">
                <a routerLink="/consultant/frameworks" class="btn btn-sm rounded-pill px-3"
                   style="background:#6366f1;color:#fff;">
                  <i class="fas fa-eye me-1"></i>Référentiels
                </a>
                <a routerLink="/questions" class="btn btn-outline-secondary btn-sm rounded-pill px-3">
                  <i class="fas fa-question-circle me-1"></i>Questions
                </a>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  `,
  styles: []
})
export class AdminDashboardComponent implements OnInit {
  currentUser: User | null = null;
  companies: Company[] = [];
  pendingReviews: EvaluationSummary[] = [];
  evaluationMap = new Map<number, EvaluationSummary>();

  consultantCount = 0;
  totalUsers = 0;

  constructor(
    private authService: AuthService,
    private companyService: CompanyService,
    private userService: UserService,
    private evaluationService: EvaluationService
  ) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    this.companyService.getCompanies().subscribe(data => this.companies = data);

    this.userService.getUsers().subscribe(users => {
      this.totalUsers = users.length;
      this.consultantCount = users.filter(u => u.role === 'CONSULTANT').length;
    });

    this.evaluationService.getAllEvaluations().subscribe(evals => {
      evals.forEach(ev => {
        const existing = this.evaluationMap.get(ev.companyId);
        if (!existing || new Date(ev.createdAt) > new Date(existing.createdAt)) {
          this.evaluationMap.set(ev.companyId, ev);
        }
      });
    });

    this.evaluationService.getPendingReviews().subscribe(data => this.pendingReviews = data);
  }

  get evaluatedCount(): number { return this.evaluationMap.size; }
  get pendingCount(): number { return this.pendingReviews.length; }

  getScore(companyId: number): EvaluationSummary | undefined {
    return this.evaluationMap.get(companyId);
  }

  deleteCompany(id: number) {
    if (confirm('Supprimer cette entreprise ?')) {
      this.companyService.deleteCompany(id).subscribe({
        next: () => { this.companies = this.companies.filter(c => c.id !== id); this.evaluationMap.delete(id); },
        error: () => alert('Erreur lors de la suppression')
      });
    }
  }

  scoreColor(score: number): string { return this.evaluationService.getScoreColor(score); }
  levelLabel(level: string): string { return this.evaluationService.getMaturityLabel(level); }
  maturityColor(level: string): string { return this.evaluationService.getMaturityColor(level); }

  maturityBg(level: string): string {
    const map: Record<string, string> = {
      INITIAL: '#fef2f2', BASIQUE: '#fff7ed',
      INTERMEDIAIRE: '#fefce8', AVANCE: '#eff6ff', OPTIMISE: '#f0fdf4'
    };
    return map[level] ?? '#f1f5f9';
  }
}
