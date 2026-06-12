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
    <div class="auth-shell">

      <!-- ═══ LEFT PANEL ═══ -->
      <div class="panel-left">
        <!-- Animated orbs -->
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>

        <!-- Grid overlay -->
        <div class="grid-overlay"></div>

        <div class="panel-left-inner">
          <!-- Logo -->
          <div class="logo-row">
            <div class="logo-mark">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="logo-text">IA Benchmark</span>
          </div>

          <!-- Hero content -->
          <div class="hero-content">
            <div class="hero-badge">
              <span class="badge-dot"></span>
              Plateforme active · 2026
            </div>

            <h1 class="hero-title">
              Mesurez la maturité digitale.<br>
              <span class="hero-title-accent">Transformez la performance.</span>
            </h1>

            <p class="hero-sub">
              Évaluez vos entreprises clientes sur 9 axes stratégiques, benchmarkez leur position sectorielle et générez des recommandations IA personnalisées.
            </p>

            <!-- Metrics -->
            <div class="metrics-row">
              <div class="metric">
                <div class="metric-value">9</div>
                <div class="metric-label">Axes évalués</div>
              </div>
              <div class="metric-divider"></div>
              <div class="metric">
                <div class="metric-value">27</div>
                <div class="metric-label">Sous-axes</div>
              </div>
              <div class="metric-divider"></div>
              <div class="metric">
                <div class="metric-value">IA</div>
                <div class="metric-label">Générée</div>
              </div>
            </div>

            <!-- Feature chips -->
            <div class="chips">
              <div class="chip">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Questionnaire adaptatif par secteur
              </div>
              <div class="chip">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Benchmarking sectoriel automatisé
              </div>
              <div class="chip">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Export PPT & rapport PDF complet
              </div>
            </div>
          </div>

          <p class="panel-footer">© 2026 IA Benchmark — Confidentiel</p>
        </div>
      </div>

      <!-- ═══ RIGHT PANEL ═══ -->
      <div class="panel-right">
        <!-- Mobile logo -->
        <div class="mobile-logo">
          <div class="logo-mark logo-mark-dark">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <span class="logo-text-dark">IA Benchmark</span>
        </div>

        <div class="form-container">
          <!-- Header -->
          <div class="form-header">
            <h2 class="form-title">Bon retour 👋</h2>
            <p class="form-sub">Connectez-vous à votre espace consultant</p>
          </div>

          <form (ngSubmit)="onSubmit()" #loginForm="ngForm" class="form-body">

            <!-- Email -->
            <div class="field-group">
              <label class="field-label">Adresse email</label>
              <div class="field-wrap" [class.is-error]="email.invalid && email.touched" [class.is-focus]="emailFocused">
                <svg class="field-ico" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="1.8"/>
                  <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="1.8"/>
                </svg>
                <input
                  type="email"
                  class="field-input"
                  [(ngModel)]="credentials.email"
                  name="email"
                  required
                  #email="ngModel"
                  (focus)="emailFocused=true"
                  (blur)="emailFocused=false"
                  placeholder="vous@cabinet.com">
              </div>
              <span class="field-error" *ngIf="email.invalid && email.touched">Email requis</span>
            </div>

            <!-- Password -->
            <div class="field-group">
              <div class="field-label-row">
                <label class="field-label">Mot de passe</label>
                <a routerLink="/forgot-password" class="forgot-link">Oublié ?</a>
              </div>
              <div class="field-wrap" [class.is-error]="password.invalid && password.touched" [class.is-focus]="pwdFocused">
                <svg class="field-ico" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="1.8"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="1.8"/>
                </svg>
                <input
                  [type]="showPassword ? 'text' : 'password'"
                  class="field-input"
                  [(ngModel)]="credentials.password"
                  name="password"
                  required
                  #password="ngModel"
                  (focus)="pwdFocused=true"
                  (blur)="pwdFocused=false"
                  placeholder="••••••••">
                <button type="button" class="eye-btn" (click)="showPassword=!showPassword" tabindex="-1">
                  <svg *ngIf="!showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8"/></svg>
                  <svg *ngIf="showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" stroke="currentColor" stroke-width="1.8"/><line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="1.8"/></svg>
                </button>
              </div>
              <span class="field-error" *ngIf="password.invalid && password.touched">Mot de passe requis</span>
            </div>

            <!-- Remember me -->
            <label class="remember-row">
              <div class="checkbox-wrap">
                <input type="checkbox" [(ngModel)]="rememberMe" name="remember">
                <div class="checkbox-ui"></div>
              </div>
              <span>Se souvenir de moi</span>
            </label>

            <!-- Error banner -->
            <div class="error-banner" *ngIf="errorMessage">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#dc2626" stroke-width="1.8"/><line x1="12" y1="8" x2="12" y2="12" stroke="#dc2626" stroke-width="1.8"/><line x1="12" y1="16" x2="12.01" y2="16" stroke="#dc2626" stroke-width="2.5"/></svg>
              {{ errorMessage }}
            </div>

            <!-- Submit -->
            <button type="submit" class="btn-primary" [disabled]="loginForm.invalid || isLoading">
              <span *ngIf="!isLoading">
                Se connecter
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2"/><polyline points="12 5 19 12 12 19" stroke="currentColor" stroke-width="2"/></svg>
              </span>
              <span *ngIf="isLoading" class="loading-row">
                <span class="spinner"></span>Connexion en cours…
              </span>
            </button>

          </form>

          <!-- Divider -->
          <div class="divider"><span>ou</span></div>

          <!-- Register CTA -->
          <a routerLink="/register" class="btn-secondary">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="1.8"/><line x1="19" y1="8" x2="19" y2="14" stroke="currentColor" stroke-width="1.8"/><line x1="22" y1="11" x2="16" y2="11" stroke="currentColor" stroke-width="1.8"/></svg>
            Créer un compte consultant
          </a>

          <p class="hint-note">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/><line x1="12" y1="16" x2="12" y2="12" stroke="currentColor" stroke-width="1.8"/><line x1="12" y1="8" x2="12.01" y2="8" stroke="currentColor" stroke-width="2.5"/></svg>
            Les accès entreprise sont créés par votre consultant.
          </p>
        </div>
      </div>

    </div>
  `,
  styles: [`
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .auth-shell {
      display: flex;
      min-height: 100vh;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ══ LEFT PANEL ══ */
    .panel-left {
      width: 52%;
      background: #0a0f1e;
      position: relative;
      overflow: hidden;
      display: none;
    }
    @media (min-width: 1024px) { .panel-left { display: flex; } }

    .orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      animation: float 8s ease-in-out infinite;
    }
    .orb-1 {
      width: 500px; height: 500px;
      background: radial-gradient(circle, rgba(37,99,235,.35) 0%, transparent 70%);
      top: -150px; right: -100px;
      animation-delay: 0s;
    }
    .orb-2 {
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(124,58,237,.25) 0%, transparent 70%);
      bottom: -100px; left: -80px;
      animation-delay: -3s;
    }
    .orb-3 {
      width: 300px; height: 300px;
      background: radial-gradient(circle, rgba(16,185,129,.15) 0%, transparent 70%);
      top: 45%; left: 30%;
      animation-delay: -6s;
    }
    @keyframes float {
      0%, 100% { transform: translateY(0) scale(1); }
      50% { transform: translateY(-30px) scale(1.05); }
    }

    .grid-overlay {
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
      background-size: 48px 48px;
    }

    .panel-left-inner {
      position: relative;
      z-index: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 40px 48px;
      width: 100%;
    }

    .logo-row {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-mark {
      width: 40px; height: 40px;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }
    .logo-mark-dark {
      background: linear-gradient(135deg, #2563eb, #7c3aed);
    }
    .logo-text {
      font-size: 18px; font-weight: 700;
      color: #fff; letter-spacing: -.3px;
    }

    .hero-content { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 40px 0; }

    .hero-badge {
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(37,99,235,.15);
      border: 1px solid rgba(37,99,235,.3);
      color: #93c5fd;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px; font-weight: 500;
      letter-spacing: .3px;
      width: fit-content;
      margin-bottom: 28px;
    }
    .badge-dot {
      width: 7px; height: 7px;
      background: #34d399;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: .6; transform: scale(.85); }
    }

    .hero-title {
      font-size: 2.6rem; font-weight: 800;
      color: #f1f5f9;
      line-height: 1.15;
      letter-spacing: -.6px;
      margin-bottom: 20px;
    }
    .hero-title-accent {
      background: linear-gradient(90deg, #60a5fa, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .hero-sub {
      color: #64748b;
      font-size: 15px; line-height: 1.75;
      max-width: 400px;
      margin-bottom: 40px;
    }

    .metrics-row {
      display: flex; align-items: center; gap: 0;
      background: rgba(255,255,255,.04);
      border: 1px solid rgba(255,255,255,.08);
      border-radius: 16px;
      padding: 20px 28px;
      margin-bottom: 28px;
      width: fit-content;
      gap: 0;
    }
    .metric { text-align: center; padding: 0 24px; }
    .metric:first-child { padding-left: 0; }
    .metric:last-child { padding-right: 0; }
    .metric-value {
      font-size: 2rem; font-weight: 800;
      background: linear-gradient(135deg, #60a5fa, #a78bfa);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1;
    }
    .metric-label { font-size: 11px; color: #475569; margin-top: 4px; white-space: nowrap; }
    .metric-divider { width: 1px; height: 36px; background: rgba(255,255,255,.08); }

    .chips { display: flex; flex-direction: column; gap: 10px; }
    .chip {
      display: flex; align-items: center; gap: 10px;
      color: #cbd5e1; font-size: 13.5px;
    }

    .panel-footer { color: #1e293b; font-size: 12px; }

    /* ══ RIGHT PANEL ══ */
    .panel-right {
      flex: 1;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 24px;
      position: relative;
    }
    .panel-right::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, #2563eb, #7c3aed, #06b6d4);
    }

    .mobile-logo {
      display: flex; align-items: center; gap: 10px;
      margin-bottom: 36px;
    }
    @media (min-width: 1024px) { .mobile-logo { display: none; } }
    .logo-text-dark { font-size: 18px; font-weight: 700; color: #0f172a; }

    .form-container { width: 100%; max-width: 400px; }

    .form-header { margin-bottom: 32px; }
    .form-title { font-size: 2rem; font-weight: 800; color: #0f172a; letter-spacing: -.5px; margin-bottom: 6px; }
    .form-sub { font-size: 14px; color: #64748b; }

    .form-body { display: flex; flex-direction: column; gap: 20px; }

    .field-group { display: flex; flex-direction: column; gap: 6px; }
    .field-label { font-size: 13px; font-weight: 600; color: #374151; }
    .field-label-row { display: flex; justify-content: space-between; align-items: center; }
    .forgot-link { font-size: 13px; color: #2563eb; text-decoration: none; font-weight: 500; }
    .forgot-link:hover { text-decoration: underline; }

    .field-wrap {
      display: flex; align-items: center;
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      border-radius: 10px;
      padding: 0 14px;
      transition: border-color .15s, box-shadow .15s, background .15s;
    }
    .field-wrap.is-focus {
      border-color: #2563eb;
      background: #fff;
      box-shadow: 0 0 0 3px rgba(37,99,235,.1);
    }
    .field-wrap.is-error { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239,68,68,.1); }
    .field-ico { color: #94a3b8; flex-shrink: 0; margin-right: 10px; }
    .field-input {
      flex: 1; border: none; outline: none; background: transparent;
      padding: 13px 0; font-size: 14.5px; color: #0f172a;
      font-family: inherit;
    }
    .field-input::placeholder { color: #cbd5e1; }
    .eye-btn {
      background: none; border: none; cursor: pointer;
      color: #94a3b8; padding: 0; margin-left: 8px;
      display: flex; align-items: center;
      transition: color .15s;
    }
    .eye-btn:hover { color: #2563eb; }
    .field-error { font-size: 12px; color: #ef4444; }

    .remember-row {
      display: flex; align-items: center; gap: 9px;
      font-size: 13px; color: #4b5563; cursor: pointer;
      user-select: none;
    }
    .checkbox-wrap { position: relative; flex-shrink: 0; }
    .checkbox-wrap input { opacity: 0; position: absolute; width: 16px; height: 16px; cursor: pointer; }
    .checkbox-ui {
      width: 16px; height: 16px;
      border: 1.5px solid #d1d5db;
      border-radius: 4px;
      background: #fff;
      transition: all .15s;
    }
    .checkbox-wrap input:checked ~ .checkbox-ui {
      background: #2563eb;
      border-color: #2563eb;
    }

    .error-banner {
      display: flex; align-items: center; gap: 8px;
      background: #fef2f2; border: 1px solid #fecaca;
      color: #dc2626; border-radius: 8px;
      padding: 11px 14px; font-size: 13.5px;
    }

    .btn-primary {
      width: 100%;
      background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
      color: #fff; border: none; border-radius: 10px;
      padding: 14px; font-size: 15px; font-weight: 600;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: opacity .2s, transform .15s, box-shadow .2s;
      letter-spacing: .1px;
      font-family: inherit;
      box-shadow: 0 4px 15px rgba(37,99,235,.3);
    }
    .btn-primary:hover:not(:disabled) {
      opacity: .93;
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(37,99,235,.35);
    }
    .btn-primary:active:not(:disabled) { transform: translateY(0); }
    .btn-primary:disabled { opacity: .55; cursor: not-allowed; box-shadow: none; }

    .loading-row { display: flex; align-items: center; gap: 10px; }
    .spinner {
      width: 16px; height: 16px;
      border: 2px solid rgba(255,255,255,.3);
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin .7s linear infinite;
      flex-shrink: 0;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .divider {
      display: flex; align-items: center; gap: 12px;
      color: #cbd5e1; font-size: 12px;
      margin: 20px 0;
    }
    .divider::before, .divider::after {
      content: ''; flex: 1; height: 1px; background: #f1f5f9;
    }

    .btn-secondary {
      width: 100%;
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      color: #374151; border-radius: 10px;
      padding: 13px;
      font-size: 14px; font-weight: 600;
      text-decoration: none;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: border-color .15s, color .15s, background .15s;
      font-family: inherit;
    }
    .btn-secondary:hover {
      border-color: #2563eb; color: #2563eb;
      background: #eff6ff;
    }

    .hint-note {
      display: flex; align-items: center; justify-content: center; gap: 6px;
      font-size: 12px; color: #94a3b8;
      text-align: center; margin-top: 20px;
    }
  `]
})
export class LoginComponent {
  credentials = { email: '', password: '' };
  rememberMe = false;
  isLoading = false;
  errorMessage = '';
  showPassword = false;
  emailFocused = false;
  pwdFocused = false;

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
