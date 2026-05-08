import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width: 600px;">
      <div class="d-flex align-items-center mb-4">
        <button class="btn btn-outline-secondary btn-sm me-3" (click)="goBack()">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </button>
        <h3 class="mb-0">Paramètres</h3>
      </div>

      <!-- Change password -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-header bg-white border-bottom fw-semibold py-3">
          <i class="fas fa-lock me-2 text-primary"></i>Modifier le mot de passe
        </div>
        <div class="card-body p-4">
          <div *ngIf="successMsg" class="alert alert-success alert-dismissible">
            <i class="fas fa-check-circle me-2"></i>{{ successMsg }}
            <button type="button" class="btn-close" (click)="successMsg = ''"></button>
          </div>
          <div *ngIf="errorMsg" class="alert alert-danger alert-dismissible">
            <i class="fas fa-exclamation-circle me-2"></i>{{ errorMsg }}
            <button type="button" class="btn-close" (click)="errorMsg = ''"></button>
          </div>

          <form (ngSubmit)="changePassword()" #pwdForm="ngForm">
            <div class="mb-3">
              <label class="form-label fw-semibold">Mot de passe actuel</label>
              <div class="input-group">
                <input [type]="showCurrent ? 'text' : 'password'" class="form-control"
                       [(ngModel)]="currentPassword" name="currentPassword" required
                       placeholder="Votre mot de passe actuel">
                <button class="btn btn-outline-secondary" type="button" (click)="showCurrent = !showCurrent">
                  <i [class]="showCurrent ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Nouveau mot de passe</label>
              <div class="input-group">
                <input [type]="showNew ? 'text' : 'password'" class="form-control"
                       [(ngModel)]="newPassword" name="newPassword" required minlength="6"
                       placeholder="Au moins 6 caractères">
                <button class="btn btn-outline-secondary" type="button" (click)="showNew = !showNew">
                  <i [class]="showNew ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold">Confirmer le nouveau mot de passe</label>
              <div class="input-group">
                <input [type]="showConfirm ? 'text' : 'password'" class="form-control"
                       [(ngModel)]="confirmPassword" name="confirmPassword" required
                       placeholder="Répétez le nouveau mot de passe">
                <button class="btn btn-outline-secondary" type="button" (click)="showConfirm = !showConfirm">
                  <i [class]="showConfirm ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
              <div *ngIf="newPassword && confirmPassword && newPassword !== confirmPassword"
                   class="text-danger small mt-1">
                <i class="fas fa-exclamation-triangle me-1"></i>Les mots de passe ne correspondent pas.
              </div>
            </div>

            <button type="submit" class="btn btn-primary w-100"
                    [disabled]="isSaving || !pwdForm.valid || newPassword !== confirmPassword">
              <span *ngIf="isSaving" class="spinner-border spinner-border-sm me-2"></span>
              <i *ngIf="!isSaving" class="fas fa-save me-2"></i>
              {{ isSaving ? 'Enregistrement...' : 'Modifier le mot de passe' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Account info (read-only) -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom fw-semibold py-3">
          <i class="fas fa-info-circle me-2 text-secondary"></i>Informations du compte
        </div>
        <div class="card-body p-4">
          <p class="text-muted small mb-2">
            <i class="fas fa-envelope me-2"></i>{{ currentUser?.email }}
          </p>
          <p class="text-muted small mb-0">
            <i class="fas fa-shield-alt me-2"></i>{{ getRoleLabel() }}
          </p>
          <hr>
          <a class="btn btn-outline-primary btn-sm" routerLink="/profile">
            <i class="fas fa-user me-1"></i>Voir mon profil complet
          </a>
        </div>
      </div>
    </div>
  `
})
export class SettingsComponent {
  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
  showCurrent = false;
  showNew = false;
  showConfirm = false;
  isSaving = false;
  successMsg = '';
  errorMsg = '';

  get currentUser() {
    return this.authService.getCurrentUser();
  }

  constructor(private authService: AuthService, private router: Router) {}

  changePassword() {
    if (this.newPassword !== this.confirmPassword) {
      this.errorMsg = 'Les mots de passe ne correspondent pas.';
      return;
    }
    this.isSaving = true;
    this.errorMsg = '';
    this.successMsg = '';

    this.authService.changePassword(this.currentPassword, this.newPassword).subscribe({
      next: () => {
        this.successMsg = 'Mot de passe modifié avec succès.';
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.isSaving = false;
      },
      error: (err) => {
        this.errorMsg = err?.error?.message || 'Erreur lors de la modification du mot de passe.';
        this.isSaving = false;
      }
    });
  }

  getRoleLabel(): string {
    const labels: any = { ADMIN: 'Administrateur', CONSULTANT: 'Consultant', CLIENT: 'Client' };
    return labels[this.currentUser?.role || ''] || this.currentUser?.role || '';
  }

  goBack() {
    history.back();
  }
}
