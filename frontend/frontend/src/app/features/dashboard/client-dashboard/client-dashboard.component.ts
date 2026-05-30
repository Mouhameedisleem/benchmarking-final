import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { AuthService } from '../../../core/services/auth.service';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-client-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container-fluid py-4 px-4" style="max-width:1000px;margin:auto;">

      <!-- Welcome banner -->
      <div class="rounded-4 p-4 mb-4 text-white" style="background:linear-gradient(135deg,#1768e5,#0d4fa8);">
        <div class="d-flex align-items-center gap-3">
          <div class="rounded-circle d-flex align-items-center justify-content-center text-white fw-bold flex-shrink-0"
               style="width:54px;height:54px;font-size:1.3rem;background:rgba(255,255,255,.2);">
            {{ (user?.companyName || user?.firstName || 'E').charAt(0).toUpperCase() }}
          </div>
          <div class="flex-grow-1">
            <h4 class="fw-bold mb-0 text-white">Bienvenue, {{ user?.companyName || user?.firstName || 'Entreprise' }}</h4>
            <small style="color:rgba(255,255,255,.8);">
              Plateforme d'évaluation de maturité digitale — fondée sur Gartner, McKinsey, ISO &amp; CMMI
            </small>
          </div>
          <!-- Completion badge -->
          <div *ngIf="evaluationStatus !== 'none'" class="text-end flex-shrink-0">
            <span *ngIf="evaluationStatus === 'validated'"
                  class="badge fs-6 px-3 py-2" style="background:rgba(255,255,255,.2);">
              <i class="fas fa-check-circle me-1"></i>Résultats validés
            </span>
            <span *ngIf="evaluationStatus === 'pending'"
                  class="badge fs-6 px-3 py-2" style="background:rgba(255,255,255,.2);">
              <i class="fas fa-clock me-1"></i>En attente de validation
            </span>
            <span *ngIf="evaluationStatus === 'submitted'"
                  class="badge fs-6 px-3 py-2" style="background:rgba(255,255,255,.2);">
              <i class="fas fa-paper-plane me-1"></i>Questionnaire soumis
            </span>
          </div>
        </div>
      </div>

      <!-- Cards -->
      <div class="row g-4">

        <!-- Questionnaire -->
        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="transition:transform .15s;"
               onmouseenter="this.style.transform='translateY(-3px)'"
               onmouseleave="this.style.transform='translateY(0)'">
            <div class="card-body p-4 d-flex flex-column">
              <div class="d-flex align-items-center gap-3 mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                     style="width:48px;height:48px;" [style.background]="evaluationStatus === 'none' ? '#e3f2fd' : '#e8f5e9'">
                  <i class="fas fs-5" [class]="evaluationStatus === 'none' ? 'fa-clipboard-list text-primary' : 'fa-check-circle text-success'"></i>
                </div>
                <div>
                  <div class="fw-bold">Questionnaire</div>
                  <div class="text-muted small">Évaluation de maturité</div>
                </div>
              </div>

              <!-- Not yet submitted -->
              <ng-container *ngIf="evaluationStatus === 'none'">
                <ul class="list-unstyled small text-muted mb-4">
                  <li class="mb-1"><i class="fas fa-check text-success me-1"></i>Questions personnalisées</li>
                  <li class="mb-1"><i class="fas fa-check text-success me-1"></i>Analyse par 9 axes stratégiques</li>
                  <li class="mb-1"><i class="fas fa-check text-success me-1"></i>Score instantané à la soumission</li>
                </ul>
                <a routerLink="/client/questionnaire" class="btn btn-primary w-100 rounded-pill mt-auto">
                  <i class="fas fa-play me-1"></i>Remplir le questionnaire
                </a>
              </ng-container>

              <!-- Already submitted -->
              <ng-container *ngIf="evaluationStatus !== 'none'">
                <div class="mb-3">
                  <div class="d-flex justify-content-between small text-muted mb-1">
                    <span>Complétude</span><span class="fw-bold text-success">100%</span>
                  </div>
                  <div class="progress rounded-pill" style="height:8px;">
                    <div class="progress-bar bg-success" style="width:100%;"></div>
                  </div>
                </div>
                <div class="alert alert-success border-0 rounded-3 p-3 mb-3 small">
                  <i class="fas fa-check-circle me-2"></i>
                  <strong>Questionnaire complété</strong>
                </div>
                <button class="btn btn-outline-secondary w-100 rounded-pill mt-auto" disabled>
                  <i class="fas fa-lock me-1"></i>Déjà soumis
                </button>
              </ng-container>
            </div>
          </div>
        </div>

        <!-- Next steps info -->
        <div class="col-md-8">
          <div class="card border-0 shadow-sm h-100 rounded-4" style="background:#f8faff;">
            <div class="card-body p-4 d-flex flex-column justify-content-center">
              <div class="d-flex align-items-center gap-3 mb-3">
                <div class="rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                     style="width:48px;height:48px;background:#e3f2fd;">
                  <i class="fas fa-info-circle text-primary fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold">Prochaines étapes</div>
                  <div class="text-muted small">Votre évaluation est en cours de traitement</div>
                </div>
              </div>
              <ol class="ps-3 mb-0 text-muted small" style="line-height:2;">
                <li *ngIf="evaluationStatus === 'none'">
                  <strong>Complétez</strong> le questionnaire d'évaluation (ci-contre).
                </li>
                <li [class.fw-bold]="evaluationStatus === 'submitted' || evaluationStatus === 'pending'"
                    [class.text-dark]="evaluationStatus === 'submitted' || evaluationStatus === 'pending'">
                  <i *ngIf="evaluationStatus === 'pending'" class="fas fa-clock text-warning me-1"></i>
                  Votre consultant <strong>analyse et valide</strong> vos résultats.
                </li>
                <li>Vous recevrez votre <strong>score, recommandations et rapport</strong> par <strong>email</strong> dès validation.</li>
              </ol>
              <div *ngIf="evaluationStatus === 'pending'"
                   class="alert alert-warning border-0 rounded-3 p-3 mt-3 mb-0 small">
                <i class="fas fa-envelope me-2"></i>
                Votre évaluation est <strong>en attente de validation</strong> par votre consultant. Vous serez notifié par email.
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  `
})
export class ClientDashboardComponent implements OnInit {
  user: any = null;
  evaluation: any = null;
  evaluationStatus: 'none' | 'submitted' | 'pending' | 'validated' = 'none';

  constructor(private authService: AuthService, private http: HttpClient) {}

  ngOnInit() {
    this.user = this.authService.getCurrentUser();
    if (this.user?.companyId) {
      this.http.get<any>(`${environment.apiUrl}/evaluations/latest?companyId=${this.user.companyId}`)
        .pipe(catchError(() => of(null)))
        .subscribe(ev => {
          if (ev?.evaluationId) {
            this.evaluation = ev;
            if (ev.validated) this.evaluationStatus = 'validated';
            else if (ev.pendingReview) this.evaluationStatus = 'pending';
            else this.evaluationStatus = 'submitted';
          }
        });
    }
  }

  maturityLabel(level: string): string {
    const labels: Record<string, string> = {
      INITIAL: 'Initial', BASIQUE: 'Basique', INTERMEDIAIRE: 'Intermédiaire',
      AVANCE: 'Avancé', OPTIMISE: 'Optimisé'
    };
    return labels[level] || level || '';
  }
}
