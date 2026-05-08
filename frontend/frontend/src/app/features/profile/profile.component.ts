import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { UserService } from '../../core/services/user.service';
import { User } from '../../core/models/user.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container py-4" style="max-width: 700px;">
      <div class="d-flex align-items-center mb-4">
        <button class="btn btn-outline-secondary btn-sm me-3" (click)="goBack()">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </button>
        <h3 class="mb-0">Mon Profil</h3>
      </div>

      <div *ngIf="isLoading" class="text-center py-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <div *ngIf="!isLoading && user" class="card border-0 shadow-sm">
        <div class="card-body p-4">

          <!-- Avatar -->
          <div class="d-flex align-items-center mb-4 pb-3 border-bottom">
            <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3 flex-shrink-0"
                 style="width: 64px; height: 64px; font-size: 1.5rem; font-weight: bold;">
              {{ getInitials() }}
            </div>
            <div>
              <h5 class="mb-0">{{ form.firstName }} {{ form.lastName }}</h5>
              <small class="text-muted">{{ user.email }}</small><br>
              <span class="badge mt-1" [ngClass]="getRoleBadge()">{{ getRoleLabel() }}</span>
            </div>
          </div>

          <!-- Alerts -->
          <div *ngIf="successMsg" class="alert alert-success alert-dismissible">
            <i class="fas fa-check-circle me-2"></i>{{ successMsg }}
            <button type="button" class="btn-close" (click)="successMsg = ''"></button>
          </div>
          <div *ngIf="errorMsg" class="alert alert-danger alert-dismissible">
            <i class="fas fa-exclamation-circle me-2"></i>{{ errorMsg }}
            <button type="button" class="btn-close" (click)="errorMsg = ''"></button>
          </div>

          <!-- Form -->
          <form (ngSubmit)="saveProfile()" #profileForm="ngForm">
            <div class="row g-3">

              <div class="col-md-6">
                <label class="form-label fw-semibold">Prénom <span class="text-danger">*</span></label>
                <input type="text" class="form-control"
                       [(ngModel)]="form.firstName" name="firstName" required
                       placeholder="Votre prénom">
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Nom <span class="text-danger">*</span></label>
                <input type="text" class="form-control"
                       [(ngModel)]="form.lastName" name="lastName" required
                       placeholder="Votre nom">
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Nom d'utilisateur <span class="text-danger">*</span></label>
                <input type="text" class="form-control"
                       [(ngModel)]="form.username" name="username" required
                       placeholder="Nom d'utilisateur">
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Email</label>
                <input type="email" class="form-control bg-light" [value]="user.email || ''" readonly
                       title="L'email ne peut pas être modifié ici">
                <small class="text-muted">Contacter l'administrateur pour changer l'email</small>
              </div>

              <div class="col-md-6">
                <label class="form-label fw-semibold">Rôle</label>
                <input type="text" class="form-control bg-light" [value]="getRoleLabel()" readonly>
              </div>

              <div class="col-md-6" *ngIf="user.companyName">
                <label class="form-label fw-semibold">Entreprise</label>
                <input type="text" class="form-control bg-light" [value]="user.companyName" readonly>
              </div>

            </div>

            <div class="mt-4 pt-3 border-top d-flex gap-2 flex-wrap">
              <button type="submit" class="btn btn-primary"
                      [disabled]="isSaving || !profileForm.valid">
                <span *ngIf="isSaving" class="spinner-border spinner-border-sm me-2"></span>
                <i *ngIf="!isSaving" class="fas fa-save me-2"></i>
                {{ isSaving ? 'Enregistrement...' : 'Enregistrer les modifications' }}
              </button>
              <button type="button" class="btn btn-outline-secondary" (click)="resetForm()">
                <i class="fas fa-undo me-1"></i>Réinitialiser
              </button>
              <button type="button" class="btn btn-outline-secondary ms-auto" (click)="goToSettings()">
                <i class="fas fa-lock me-1"></i>Modifier le mot de passe
              </button>
            </div>
          </form>

        </div>
      </div>
    </div>
  `
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  isLoading = true;
  isSaving = false;
  successMsg = '';
  errorMsg = '';

  form = { firstName: '', lastName: '', username: '' };

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
    this.user = this.authService.getCurrentUser();
    this.fillForm();
    this.isLoading = false;
    // Refresh from backend to get latest data
    this.authService.refreshProfile().subscribe({
      next: () => {
        this.user = this.authService.getCurrentUser();
        this.fillForm();
      },
      error: () => {}
    });
  }

  private fillForm() {
    if (this.user) {
      this.form.firstName = this.user.firstName || '';
      this.form.lastName  = this.user.lastName  || '';
      this.form.username  = this.user.username  || '';
    }
  }

  resetForm() {
    this.fillForm();
    this.successMsg = '';
    this.errorMsg   = '';
  }

  saveProfile() {
    if (!this.user?.id) return;
    this.isSaving = true;
    this.errorMsg = '';
    this.successMsg = '';

    this.userService.updateUser(this.user.id, {
      ...this.user,
      firstName: this.form.firstName,
      lastName:  this.form.lastName,
      username:  this.form.username
    }).subscribe({
      next: (updated) => {
        // Sync user object and localStorage
        this.user = { ...this.user!, ...updated };
        const stored = localStorage.getItem('currentUser');
        if (stored) {
          const parsed = JSON.parse(stored);
          parsed.firstName = updated.firstName;
          parsed.lastName  = updated.lastName;
          parsed.username  = updated.username;
          localStorage.setItem('currentUser', JSON.stringify(parsed));
        }
        this.fillForm();
        this.isSaving   = false;
        this.successMsg = 'Profil mis à jour avec succès.';
      },
      error: (err) => {
        this.errorMsg = err?.error?.message || 'Erreur lors de la mise à jour.';
        this.isSaving = false;
      }
    });
  }

  getInitials(): string {
    const f = this.form.firstName?.charAt(0) || '';
    const l = this.form.lastName?.charAt(0)  || '';
    return (f + l).toUpperCase() || this.user?.username?.charAt(0).toUpperCase() || 'U';
  }

  getRoleLabel(): string {
    const labels: any = { ADMIN: 'Administrateur', CONSULTANT: 'Consultant', CLIENT: 'Client' };
    return labels[this.user?.role || ''] || this.user?.role || '';
  }

  getRoleBadge(): string {
    const classes: any = { ADMIN: 'bg-danger', CONSULTANT: 'bg-primary', CLIENT: 'bg-success' };
    return classes[this.user?.role || ''] || 'bg-secondary';
  }

  goBack()      { history.back(); }
  goToSettings(){ this.router.navigate(['/settings']); }
}
