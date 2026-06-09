import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="fp-wrapper">

      <!-- Panneau gauche branding -->
      <div class="fp-left d-none d-lg-flex flex-column justify-content-between p-5">
        <div class="d-flex align-items-center gap-3">
          <div class="brand-icon"><i class="fas fa-robot"></i></div>
          <span class="brand-name">IA Benchmark</span>
        </div>
        <div class="left-content">
          <div class="left-badge mb-4">
            <i class="fas fa-lock me-2"></i>Sécurité de votre compte
          </div>
          <h1 class="left-title">Récupérez l'accès à votre espace.</h1>
          <p class="left-sub">
            Un code de vérification à 6 chiffres sera envoyé à votre adresse email.
            Il est valable 15 minutes.
          </p>
          <div class="steps-list mt-5">
            <div class="step-item" [class.active]="step === 1">
              <div class="step-number">1</div>
              <span>Entrez votre adresse email</span>
            </div>
            <div class="step-item" [class.active]="step === 2">
              <div class="step-number">2</div>
              <span>Saisissez le code reçu par email</span>
            </div>
            <div class="step-item" [class.active]="step === 3">
              <div class="step-number">3</div>
              <span>Définissez votre nouveau mot de passe</span>
            </div>
          </div>
        </div>
        <div class="left-footer">
          <p class="mb-0">© 2026 IA Benchmark — Tous droits réservés</p>
        </div>
      </div>

      <!-- Panneau droit : formulaire -->
      <div class="fp-right d-flex flex-column justify-content-center align-items-center p-4 p-lg-5">

        <!-- Mobile logo -->
        <div class="d-flex d-lg-none align-items-center gap-2 mb-5">
          <div class="brand-icon brand-icon-sm"><i class="fas fa-robot"></i></div>
          <span class="brand-name-dark">IA Benchmark</span>
        </div>

        <div class="fp-form-box w-100">

          <!-- ── Étape 1 : saisie email ── -->
          <ng-container *ngIf="step === 1">
            <div class="mb-5">
              <a routerLink="/login" class="back-link mb-4 d-inline-flex align-items-center gap-2">
                <i class="fas fa-arrow-left"></i> Retour à la connexion
              </a>
              <h2 class="form-title">Mot de passe oublié ?</h2>
              <p class="form-subtitle">
                Entrez votre email et nous vous enverrons un code de vérification.
              </p>
            </div>

            <form (ngSubmit)="requestCode()" #emailForm="ngForm">
              <div class="mb-4">
                <label class="field-label">Adresse email</label>
                <div class="field-wrapper" [class.field-error]="emailField.invalid && emailField.touched">
                  <i class="fas fa-envelope field-icon"></i>
                  <input
                    type="email"
                    class="field-input"
                    [(ngModel)]="email"
                    name="email"
                    required
                    email
                    #emailField="ngModel"
                    placeholder="vous@exemple.com">
                </div>
                <span class="error-msg" *ngIf="emailField.invalid && emailField.touched">
                  <i class="fas fa-exclamation-circle me-1"></i>Email invalide
                </span>
              </div>

              <div class="error-banner mb-4" *ngIf="errorMsg">
                <i class="fas fa-exclamation-triangle me-2"></i>{{ errorMsg }}
              </div>

              <button type="submit" class="btn-primary w-100" [disabled]="emailForm.invalid || isLoading">
                <span *ngIf="!isLoading">
                  Envoyer le code <i class="fas fa-paper-plane ms-2"></i>
                </span>
                <span *ngIf="isLoading">
                  <span class="spinner-border spinner-border-sm me-2"></span>Envoi en cours…
                </span>
              </button>
            </form>
          </ng-container>

          <!-- ── Étape 2 : saisie code + nouveau mot de passe ── -->
          <ng-container *ngIf="step === 2">
            <div class="mb-5">
              <button type="button" class="back-link mb-4 d-inline-flex align-items-center gap-2" (click)="step = 1; errorMsg = ''">
                <i class="fas fa-arrow-left"></i> Modifier l'email
              </button>
              <h2 class="form-title">Vérification</h2>
              <p class="form-subtitle">
                Un code a été envoyé à <strong>{{ email }}</strong>.<br>
                Saisissez-le ci-dessous avec votre nouveau mot de passe.
              </p>
            </div>

            <form (ngSubmit)="resetPassword()" #resetForm="ngForm">

              <!-- Code -->
              <div class="mb-4">
                <label class="field-label">Code de vérification</label>
                <div class="field-wrapper" [class.field-error]="codeField.invalid && codeField.touched">
                  <i class="fas fa-key field-icon"></i>
                  <input
                    type="text"
                    class="field-input code-input"
                    [(ngModel)]="code"
                    name="code"
                    required
                    minlength="6"
                    maxlength="6"
                    pattern="[0-9]{6}"
                    #codeField="ngModel"
                    placeholder="_ _ _ _ _ _"
                    autocomplete="one-time-code">
                </div>
                <span class="error-msg" *ngIf="codeField.invalid && codeField.touched">
                  <i class="fas fa-exclamation-circle me-1"></i>Le code doit contenir 6 chiffres
                </span>
              </div>

              <!-- Nouveau mot de passe -->
              <div class="mb-3">
                <label class="field-label">Nouveau mot de passe</label>
                <div class="field-wrapper" [class.field-error]="pwField.invalid && pwField.touched">
                  <i class="fas fa-lock field-icon"></i>
                  <input
                    [type]="showPassword ? 'text' : 'password'"
                    class="field-input"
                    [(ngModel)]="newPassword"
                    name="newPassword"
                    required
                    minlength="6"
                    #pwField="ngModel"
                    placeholder="Au moins 6 caractères">
                  <i class="fas field-toggle"
                     [class.fa-eye]="!showPassword"
                     [class.fa-eye-slash]="showPassword"
                     (click)="showPassword = !showPassword"></i>
                </div>
                <span class="error-msg" *ngIf="pwField.invalid && pwField.touched">
                  <i class="fas fa-exclamation-circle me-1"></i>Minimum 6 caractères
                </span>
              </div>

              <!-- Confirmation -->
              <div class="mb-4">
                <label class="field-label">Confirmer le mot de passe</label>
                <div class="field-wrapper" [class.field-error]="confirmField.touched && newPassword !== confirmPassword">
                  <i class="fas fa-lock field-icon"></i>
                  <input
                    [type]="showPassword ? 'text' : 'password'"
                    class="field-input"
                    [(ngModel)]="confirmPassword"
                    name="confirmPassword"
                    required
                    #confirmField="ngModel"
                    placeholder="Répétez le mot de passe">
                </div>
                <span class="error-msg" *ngIf="confirmField.touched && newPassword !== confirmPassword">
                  <i class="fas fa-exclamation-circle me-1"></i>Les mots de passe ne correspondent pas
                </span>
              </div>

              <div class="error-banner mb-4" *ngIf="errorMsg">
                <i class="fas fa-exclamation-triangle me-2"></i>{{ errorMsg }}
              </div>

              <button type="submit"
                class="btn-primary w-100"
                [disabled]="resetForm.invalid || newPassword !== confirmPassword || isLoading">
                <span *ngIf="!isLoading">
                  Réinitialiser le mot de passe <i class="fas fa-check ms-2"></i>
                </span>
                <span *ngIf="isLoading">
                  <span class="spinner-border spinner-border-sm me-2"></span>Mise à jour…
                </span>
              </button>

              <div class="resend-link mt-3 text-center">
                <span class="text-muted" style="font-size:13px;">Vous n'avez pas reçu le code ? </span>
                <button type="button" class="btn-link" (click)="requestCode()" [disabled]="isLoading">
                  Renvoyer
                </button>
              </div>
            </form>
          </ng-container>

          <!-- ── Étape 3 : succès ── -->
          <ng-container *ngIf="step === 3">
            <div class="success-box text-center">
              <div class="success-icon mb-4">
                <i class="fas fa-check-circle"></i>
              </div>
              <h2 class="form-title">Mot de passe mis à jour !</h2>
              <p class="form-subtitle mb-5">
                Votre mot de passe a été réinitialisé avec succès.
                Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.
              </p>
              <a routerLink="/login" class="btn-primary d-inline-flex align-items-center gap-2">
                <i class="fas fa-sign-in-alt"></i> Se connecter
              </a>
            </div>
          </ng-container>

        </div>
      </div>
    </div>
  `,
  styles: [`
    .fp-wrapper { display: flex; min-height: 100vh; }

    /* Left panel */
    .fp-left {
      width: 52%;
      background: linear-gradient(145deg, #0f172a 0%, #1e3a5f 40%, #1a56db 100%);
      position: relative; overflow: hidden; color: #fff;
    }
    .fp-left::before {
      content: ''; position: absolute;
      width: 500px; height: 500px; border-radius: 50%;
      background: rgba(255,255,255,.04); top: -120px; right: -120px;
    }
    .fp-left::after {
      content: ''; position: absolute;
      width: 350px; height: 350px; border-radius: 50%;
      background: rgba(255,255,255,.04); bottom: -80px; left: -80px;
    }
    .brand-icon {
      width: 44px; height: 44px;
      background: rgba(255,255,255,.15); border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; backdrop-filter: blur(4px);
    }
    .brand-icon-sm {
      width: 36px; height: 36px;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 16px; color: #fff;
    }
    .brand-name { font-size: 20px; font-weight: 700; color: #fff; }
    .brand-name-dark { font-size: 20px; font-weight: 700; color: #1e293b; }
    .left-badge {
      display: inline-flex; align-items: center;
      background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
      color: #93c5fd; padding: 6px 16px; border-radius: 999px;
      font-size: 13px; font-weight: 500;
    }
    .left-title { font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 1rem; }
    .left-sub { color: #94a3b8; font-size: 15px; line-height: 1.7; max-width: 420px; }
    .left-footer { color: #475569; font-size: 12px; }

    .steps-list { display: flex; flex-direction: column; gap: 16px; }
    .step-item {
      display: flex; align-items: center; gap: 14px;
      font-size: 14px; color: #64748b; transition: color .2s;
    }
    .step-item.active { color: #e2e8f0; }
    .step-number {
      width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 14px;
      background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.15);
      color: #64748b; transition: background .2s, color .2s;
    }
    .step-item.active .step-number {
      background: #1a56db; border-color: #1a56db; color: #fff;
    }

    /* Right panel */
    .fp-right { flex: 1; background: #f8fafc; }
    .fp-form-box { max-width: 420px; }

    .form-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
    .form-subtitle { color: #64748b; font-size: 15px; line-height: 1.6; }

    .back-link {
      font-size: 13px; color: #64748b; text-decoration: none;
      background: none; border: none; padding: 0; cursor: pointer;
      transition: color .2s;
    }
    .back-link:hover { color: #1a56db; }

    /* Fields */
    .field-label { display: block; font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 8px; }
    .field-wrapper {
      display: flex; align-items: center;
      background: #fff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 0 14px;
      transition: border-color .2s, box-shadow .2s;
    }
    .field-wrapper:focus-within { border-color: #1a56db; box-shadow: 0 0 0 3px rgba(26,86,219,.1); }
    .field-wrapper.field-error { border-color: #ef4444; }
    .field-icon { color: #94a3b8; font-size: 15px; margin-right: 10px; flex-shrink: 0; }
    .field-input {
      flex: 1; border: none; outline: none; background: transparent;
      padding: 14px 0; font-size: 15px; color: #0f172a;
    }
    .field-input::placeholder { color: #cbd5e1; }
    .code-input { letter-spacing: 6px; font-size: 20px; font-weight: 700; text-align: center; }
    .field-toggle { color: #94a3b8; font-size: 15px; cursor: pointer; margin-left: 8px; flex-shrink: 0; }
    .field-toggle:hover { color: #1a56db; }
    .error-msg { font-size: 12px; color: #ef4444; margin-top: 5px; display: block; }

    .error-banner {
      background: #fef2f2; border: 1px solid #fecaca;
      color: #dc2626; border-radius: 10px; padding: 12px 16px; font-size: 14px;
    }

    .btn-primary {
      display: inline-block;
      background: linear-gradient(135deg, #1a56db, #7c3aed);
      color: #fff; border: none; border-radius: 12px;
      padding: 14px 28px; font-size: 15px; font-weight: 600;
      cursor: pointer; transition: opacity .2s, transform .1s;
      text-decoration: none; text-align: center;
    }
    .btn-primary:hover:not(:disabled) { opacity: .92; transform: translateY(-1px); }
    .btn-primary:disabled { opacity: .6; cursor: not-allowed; }

    .btn-link {
      background: none; border: none; padding: 0;
      font-size: 13px; color: #1a56db; font-weight: 600; cursor: pointer;
    }
    .btn-link:hover { text-decoration: underline; }
    .btn-link:disabled { opacity: .5; cursor: not-allowed; }

    /* Success */
    .success-box { padding: 20px 0; }
    .success-icon {
      width: 80px; height: 80px; border-radius: 50%;
      background: linear-gradient(135deg, #d1fae5, #a7f3d0);
      display: inline-flex; align-items: center; justify-content: center;
      font-size: 36px; color: #059669;
    }
  `]
})
export class ForgotPasswordComponent {
  step = 1;
  email = '';
  code = '';
  newPassword = '';
  confirmPassword = '';
  showPassword = false;
  isLoading = false;
  errorMsg = '';

  constructor(private authService: AuthService, private router: Router) {}

  requestCode() {
    this.isLoading = true;
    this.errorMsg = '';
    this.authService.forgotPassword(this.email).subscribe({
      next: () => {
        this.isLoading = false;
        this.step = 2;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err?.error?.message || 'Aucun compte trouvé avec cet email.';
      }
    });
  }

  resetPassword() {
    if (this.newPassword !== this.confirmPassword) return;
    this.isLoading = true;
    this.errorMsg = '';
    this.authService.resetPassword(this.email, this.code, this.newPassword).subscribe({
      next: () => {
        this.isLoading = false;
        this.step = 3;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err?.error?.message || 'Code incorrect ou expiré. Vérifiez votre email.';
      }
    });
  }
}
