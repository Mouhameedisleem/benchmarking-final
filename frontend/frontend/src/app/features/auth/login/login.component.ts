import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="login-wrapper">

      <!-- ── Panneau gauche : branding ── -->
      <div class="login-left d-none d-lg-flex flex-column justify-content-between p-5">
        <!-- Logo -->
        <div class="d-flex align-items-center gap-3">
          <div class="brand-icon">
            <i class="fas fa-robot"></i>
          </div>
          <span class="brand-name">IA Benchmark</span>
        </div>

        <!-- Tagline central -->
        <div class="left-content">
          <div class="left-badge mb-4">
            <i class="fas fa-chart-line me-2"></i>Plateforme de maturité digitale
          </div>
          <h1 class="left-title">Évaluez, comparez, progressez.</h1>
          <p class="left-sub">
            Mesurez le niveau de maturité digitale de vos entreprises clientes, obtenez des recommandations personnalisées et benchmarkez leur position dans leur secteur.
          </p>

          <!-- Statistiques -->
          <div class="stats-grid mt-5">
            <div class="stat-card">
              <div class="stat-number">7</div>
              <div class="stat-label">Axes d'évaluation</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">IA</div>
              <div class="stat-label">Questions générées</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">360°</div>
              <div class="stat-label">Analyse complète</div>
            </div>
          </div>

          <!-- Features -->
          <div class="features-list mt-5">
            <div class="feature-item">
              <i class="fas fa-check-circle feature-icon"></i>
              <span>Questionnaire adapté au secteur d'activité</span>
            </div>
            <div class="feature-item">
              <i class="fas fa-check-circle feature-icon"></i>
              <span>Score de maturité et benchmarking sectoriel</span>
            </div>
            <div class="feature-item">
              <i class="fas fa-check-circle feature-icon"></i>
              <span>Recommandations personnalisées par l'IA</span>
            </div>
          </div>
        </div>

        <!-- Footer gauche -->
        <div class="left-footer">
          <p class="mb-0">© 2026 IA Benchmark — Tous droits réservés</p>
        </div>
      </div>

      <!-- ── Panneau droit : formulaire ── -->
      <div class="login-right d-flex flex-column justify-content-center align-items-center p-4 p-lg-5">

        <!-- Mobile logo -->
        <div class="d-flex d-lg-none align-items-center gap-2 mb-5">
          <div class="brand-icon brand-icon-sm"><i class="fas fa-robot"></i></div>
          <span class="brand-name-dark">IA Benchmark</span>
        </div>

        <div class="login-form-box w-100">
          <div class="mb-5">
            <h2 class="form-title">Bienvenue</h2>
            <p class="form-subtitle">Connectez-vous à votre espace de travail</p>
          </div>

          <form (ngSubmit)="onSubmit()" #loginForm="ngForm">

            <!-- Email -->
            <div class="mb-4">
              <label class="field-label">Adresse email</label>
              <div class="field-wrapper" [class.field-error]="email.invalid && email.touched">
                <i class="fas fa-envelope field-icon"></i>
                <input
                  type="email"
                  class="field-input"
                  [(ngModel)]="credentials.email"
                  name="email"
                  required
                  #email="ngModel"
                  placeholder="vous@exemple.com">
              </div>
              <span class="error-msg" *ngIf="email.invalid && email.touched">
                <i class="fas fa-exclamation-circle me-1"></i>Email requis
              </span>
            </div>

            <!-- Mot de passe -->
            <div class="mb-3">
              <label class="field-label">Mot de passe</label>
              <div class="field-wrapper" [class.field-error]="password.invalid && password.touched">
                <i class="fas fa-lock field-icon"></i>
                <input
                  [type]="showPassword ? 'text' : 'password'"
                  class="field-input"
                  [(ngModel)]="credentials.password"
                  name="password"
                  required
                  #password="ngModel"
                  placeholder="••••••••••">
                <i class="fas field-toggle"
                   [class.fa-eye]="!showPassword"
                   [class.fa-eye-slash]="showPassword"
                   (click)="showPassword = !showPassword"></i>
              </div>
              <span class="error-msg" *ngIf="password.invalid && password.touched">
                <i class="fas fa-exclamation-circle me-1"></i>Mot de passe requis
              </span>
            </div>

            <!-- Remember / Forgot -->
            <div class="d-flex justify-content-between align-items-center mb-4">
              <label class="remember-label">
                <input type="checkbox" [(ngModel)]="rememberMe" name="remember">
                <span>Se souvenir de moi</span>
              </label>
              <a routerLink="/forgot-password" class="forgot-link">Mot de passe oublié ?</a>
            </div>

            <!-- Erreur -->
            <div class="error-banner mb-4" *ngIf="errorMessage">
              <i class="fas fa-exclamation-triangle me-2"></i>{{ errorMessage }}
            </div>

            <!-- Submit -->
            <button type="submit" class="btn-login w-100 mb-4" [disabled]="loginForm.invalid || isLoading">
              <span *ngIf="!isLoading">
                Se connecter <i class="fas fa-arrow-right ms-2"></i>
              </span>
              <span *ngIf="isLoading">
                <span class="spinner-border spinner-border-sm me-2"></span>Connexion…
              </span>
            </button>
          </form>

          <!-- Séparateur -->
          <div class="separator mb-4">
            <span>ou</span>
          </div>

          <!-- Inscription -->
          <a routerLink="/register" class="btn-register w-100 d-flex align-items-center justify-content-center gap-2">
            <i class="fas fa-user-plus"></i>Créer un compte consultant
          </a>

          <p class="hint-text mt-4">
            <i class="fas fa-info-circle me-1"></i>
            Les accès entreprise sont fournis par votre consultant après configuration.
          </p>
        </div>
      </div>

    </div>
  `,
  styles: [`
    /* ── Layout ── */
    .login-wrapper {
      display: flex;
      min-height: 100vh;
    }

    /* ── Left panel ── */
    .login-left {
      width: 52%;
      background: linear-gradient(145deg, #0f172a 0%, #1e3a5f 40%, #1a56db 100%);
      position: relative;
      overflow: hidden;
      color: #fff;
    }
    .login-left::before {
      content: '';
      position: absolute;
      width: 500px; height: 500px;
      border-radius: 50%;
      background: rgba(255,255,255,.04);
      top: -120px; right: -120px;
    }
    .login-left::after {
      content: '';
      position: absolute;
      width: 350px; height: 350px;
      border-radius: 50%;
      background: rgba(255,255,255,.04);
      bottom: -80px; left: -80px;
    }

    .brand-icon {
      width: 44px; height: 44px;
      background: rgba(255,255,255,.15);
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px;
      backdrop-filter: blur(4px);
    }
    .brand-icon-sm {
      width: 36px; height: 36px;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 16px; color:#fff;
    }
    .brand-name { font-size: 20px; font-weight: 700; letter-spacing: -.3px; color: #fff; }
    .brand-name-dark { font-size: 20px; font-weight: 700; color: #1e293b; }

    .left-badge {
      display: inline-flex; align-items: center;
      background: rgba(255,255,255,.12);
      border: 1px solid rgba(255,255,255,.2);
      color: #93c5fd;
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 13px; font-weight: 500;
      backdrop-filter: blur(4px);
    }
    .left-title {
      font-size: 2.4rem; font-weight: 800;
      line-height: 1.2; margin-bottom: 1rem;
      letter-spacing: -.5px;
    }
    .left-sub { color: #94a3b8; font-size: 15px; line-height: 1.7; max-width: 420px; }

    .stats-grid {
      display: grid; grid-template-columns: repeat(3,1fr); gap: 12px;
    }
    .stat-card {
      background: rgba(255,255,255,.07);
      border: 1px solid rgba(255,255,255,.1);
      border-radius: 14px;
      padding: 18px 12px;
      text-align: center;
      backdrop-filter: blur(4px);
    }
    .stat-number { font-size: 1.8rem; font-weight: 800; color: #60a5fa; }
    .stat-label { font-size: 11px; color: #94a3b8; margin-top: 4px; }

    .features-list { display: flex; flex-direction: column; gap: 12px; }
    .feature-item { display: flex; align-items: center; gap: 12px; font-size: 14px; color: #cbd5e1; }
    .feature-icon { color: #34d399; font-size: 16px; flex-shrink: 0; }

    .left-footer { color: #475569; font-size: 12px; }

    /* ── Right panel ── */
    .login-right {
      flex: 1;
      background: #f8fafc;
    }
    .login-form-box { max-width: 420px; }

    .form-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; letter-spacing: -.5px; }
    .form-subtitle { color: #64748b; font-size: 15px; }

    /* Fields */
    .field-label { display: block; font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 8px; }
    .field-wrapper {
      display: flex; align-items: center;
      background: #fff;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 0 14px;
      transition: border-color .2s, box-shadow .2s;
    }
    .field-wrapper:focus-within {
      border-color: #1a56db;
      box-shadow: 0 0 0 3px rgba(26,86,219,.1);
    }
    .field-wrapper.field-error { border-color: #ef4444; }
    .field-icon { color: #94a3b8; font-size: 15px; margin-right: 10px; flex-shrink: 0; }
    .field-input {
      flex: 1; border: none; outline: none; background: transparent;
      padding: 14px 0; font-size: 15px; color: #0f172a;
    }
    .field-input::placeholder { color: #cbd5e1; }
    .field-toggle { color: #94a3b8; font-size: 15px; cursor: pointer; margin-left: 8px; flex-shrink: 0; }
    .field-toggle:hover { color: #1a56db; }
    .error-msg { font-size: 12px; color: #ef4444; margin-top: 5px; display: block; }

    /* Remember / Forgot */
    .remember-label { display: flex; align-items: center; gap: 7px; font-size: 13px; color: #4b5563; cursor: pointer; }
    .remember-label input { accent-color: #1a56db; }
    .forgot-link { font-size: 13px; color: #1a56db; text-decoration: none; font-weight: 500; }
    .forgot-link:hover { text-decoration: underline; }

    /* Error banner */
    .error-banner {
      background: #fef2f2; border: 1px solid #fecaca;
      color: #dc2626; border-radius: 10px;
      padding: 12px 16px; font-size: 14px;
    }

    /* Submit button */
    .btn-login {
      background: linear-gradient(135deg, #1a56db, #7c3aed);
      color: #fff; border: none; border-radius: 12px;
      padding: 14px; font-size: 15px; font-weight: 600;
      cursor: pointer; transition: opacity .2s, transform .1s;
      letter-spacing: .2px;
    }
    .btn-login:hover:not(:disabled) { opacity: .92; transform: translateY(-1px); }
    .btn-login:disabled { opacity: .6; cursor: not-allowed; }

    /* Separator */
    .separator {
      display: flex; align-items: center; gap: 12px; color: #cbd5e1; font-size: 13px;
    }
    .separator::before, .separator::after {
      content: ''; flex: 1; height: 1px; background: #e2e8f0;
    }

    /* Register button */
    .btn-register {
      background: #fff; border: 1.5px solid #e2e8f0;
      color: #374151; border-radius: 12px;
      padding: 13px; font-size: 14px; font-weight: 600;
      text-decoration: none; transition: border-color .2s, box-shadow .2s;
    }
    .btn-register:hover {
      border-color: #1a56db; color: #1a56db;
      box-shadow: 0 0 0 3px rgba(26,86,219,.08);
    }

    .hint-text { font-size: 12.5px; color: #94a3b8; text-align: center; }
  `]
})
export class LoginComponent {
  credentials = { email: '', password: '' };
  rememberMe = false;
  isLoading = false;
  errorMessage = '';
  showPassword = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = '';
    this.authService.login(this.credentials.email, this.credentials.password).subscribe({
      next: () => {
        this.isLoading = false;
        const user = this.authService.getCurrentUser();
        if (user?.role === 'ADMIN') this.router.navigate(['/admin/dashboard']);
        else if (user?.role === 'CONSULTANT') this.router.navigate(['/consultant/dashboard']);
        else this.router.navigate(['/client/dashboard']);
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Email ou mot de passe incorrect. Vérifiez vos identifiants.';
      }
    });
  }
}