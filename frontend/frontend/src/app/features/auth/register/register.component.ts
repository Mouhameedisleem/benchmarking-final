import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light py-4">
      <div class="row w-100 justify-content-center">
        <div class="col-md-6 col-lg-5">

          <!-- Header -->
          <div class="text-center mb-4">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3 shadow"
                 style="width:72px;height:72px;">
              <i class="fas fa-user-tie fa-2x"></i>
            </div>
            <h2 class="fw-bold text-primary">IA Benchmark</h2>
            <p class="text-muted">Créez votre compte consultant</p>
          </div>

          <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-primary text-white py-3 text-center">
              <h5 class="mb-0"><i class="fas fa-user-plus me-2"></i>Inscription Consultant</h5>
            </div>

            <div class="card-body p-4">
              <!-- Error -->
              <div *ngIf="errorMessage" class="alert alert-danger rounded-3 py-2 small">
                <i class="fas fa-exclamation-circle me-1"></i>{{ errorMessage }}
              </div>

              <form (ngSubmit)="onSubmit()" #form="ngForm">

                <div class="row">
                  <div class="col-6 mb-3">
                    <label class="form-label fw-semibold small">Prénom *</label>
                    <input type="text" class="form-control"
                           [(ngModel)]="consultant.firstName" name="firstName"
                           required #fn="ngModel" placeholder="Jean"
                           [class.is-invalid]="fn.invalid && fn.touched">
                    <div class="invalid-feedback small">Prénom requis</div>
                  </div>
                  <div class="col-6 mb-3">
                    <label class="form-label fw-semibold small">Nom *</label>
                    <input type="text" class="form-control"
                           [(ngModel)]="consultant.lastName" name="lastName"
                           required #ln="ngModel" placeholder="Dupont"
                           [class.is-invalid]="ln.invalid && ln.touched">
                    <div class="invalid-feedback small">Nom requis</div>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold small">Email professionnel *</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-envelope text-primary"></i></span>
                    <input type="email" class="form-control"
                           [(ngModel)]="consultant.email" name="email"
                           required email #em="ngModel" placeholder="jean.dupont@cabinet.com"
                           [class.is-invalid]="em.invalid && em.touched">
                    <div class="invalid-feedback small">Email valide requis</div>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold small">Téléphone</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-phone text-primary"></i></span>
                    <input type="tel" class="form-control"
                           [(ngModel)]="consultant.phone" name="phone"
                           placeholder="+33 6 00 00 00 00">
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-semibold small">Mot de passe *</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-lock text-primary"></i></span>
                    <input [type]="showPwd ? 'text' : 'password'" class="form-control"
                           [(ngModel)]="consultant.password" name="password"
                           required minlength="6" #pwd="ngModel"
                           placeholder="Minimum 6 caractères"
                           [class.is-invalid]="pwd.invalid && pwd.touched">
                    <button type="button" class="btn btn-outline-secondary"
                            (click)="showPwd = !showPwd">
                      <i class="fas" [class.fa-eye]="!showPwd" [class.fa-eye-slash]="showPwd"></i>
                    </button>
                    <div class="invalid-feedback small">Mot de passe (6 car. min) requis</div>
                  </div>
                </div>

                <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold rounded-3 mt-2"
                        [disabled]="form.invalid || isLoading">
                  <span *ngIf="!isLoading"><i class="fas fa-check-circle me-2"></i>Créer mon compte consultant</span>
                  <span *ngIf="isLoading"><span class="spinner-border spinner-border-sm me-2"></span>Création…</span>
                </button>
              </form>
            </div>

            <div class="card-footer bg-light text-center py-3">
              <small class="text-muted">
                Déjà un compte ? <a routerLink="/login" class="text-primary fw-semibold">Se connecter</a>
              </small>
            </div>
          </div>

        </div>
      </div>
    </div>
  `
})
export class RegisterComponent {
  consultant = { firstName: '', lastName: '', email: '', password: '', phone: '' };
  isLoading = false;
  errorMessage = '';
  showPwd = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = '';

    this.authService.registerConsultant(this.consultant).subscribe({
      next: () => {
        this.isLoading = false;
        this.router.navigate(['/consultant/dashboard']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err?.error?.message || 'Erreur lors de l\'inscription. Vérifiez vos informations.';
      }
    });
  }
}
