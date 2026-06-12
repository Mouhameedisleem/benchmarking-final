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
    <div class="auth-shell">

      <!-- ═══ LEFT PANEL ═══ -->
      <div class="panel-left">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="grid-overlay"></div>

        <div class="panel-left-inner">
          <div class="logo-row">
            <div class="logo-mark">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="logo-text">IA Benchmark</span>
          </div>

          <div class="hero-content">
            <div class="hero-badge">
              <span class="badge-dot"></span>
              Espace consultant · Accès illimité
            </div>

            <h1 class="hero-title">
              Rejoignez la plateforme<br>
              <span class="hero-title-accent">de référence en Afrique.</span>
            </h1>

            <p class="hero-sub">
              Accompagnez vos clients dans leur transformation digitale avec des outils d'évaluation sectoriels, des benchmarks IA et des recommandations actionnables.
            </p>

            <!-- Steps -->
            <div class="steps">
              <div class="step">
                <div class="step-num">1</div>
                <div class="step-body">
                  <div class="step-title">Créez votre profil consultant</div>
                  <div class="step-sub">Accès instantané à tous les outils</div>
                </div>
              </div>
              <div class="step-connector"></div>
              <div class="step">
                <div class="step-num">2</div>
                <div class="step-body">
                  <div class="step-title">Ajoutez vos entreprises clientes</div>
                  <div class="step-sub">Gestion multi-clients centralisée</div>
                </div>
              </div>
              <div class="step-connector"></div>
              <div class="step">
                <div class="step-num">3</div>
                <div class="step-body">
                  <div class="step-title">Générez vos rapports & benchmarks</div>
                  <div class="step-sub">Export PPT, PDF et tableaux de bord BI</div>
                </div>
              </div>
            </div>
          </div>

          <div class="trust-row">
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#34d399" stroke-width="2"/></svg>
              Données chiffrées
            </div>
            <div class="trust-dot"></div>
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#34d399" stroke-width="2"/></svg>
              Modèle IA sécurisé
            </div>
            <div class="trust-dot"></div>
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#34d399" stroke-width="2"/></svg>
              Support dédié
            </div>
          </div>

          <p class="panel-footer">© 2026 IA Benchmark — Confidentiel</p>
        </div>
      </div>

      <!-- ═══ RIGHT PANEL ═══ -->
      <div class="panel-right">
        <div class="mobile-logo">
          <div class="logo-mark logo-mark-gradient">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <span class="logo-text-dark">IA Benchmark</span>
        </div>

        <div class="form-container">
          <div class="form-header">
            <h2 class="form-title">Créer un compte</h2>
            <p class="form-sub">Renseignez vos informations pour accéder à la plateforme</p>
          </div>

          <form (ngSubmit)="onSubmit()" #regForm="ngForm" class="form-body">

            <!-- Name row -->
            <div class="field-row">
              <div class="field-group">
                <label class="field-label">Prénom <span class="req">*</span></label>
                <div class="field-wrap" [class.is-error]="fn.invalid && fn.touched" [class.is-focus]="fnFocused">
                  <input type="text" class="field-input"
                    [(ngModel)]="consultant.firstName" name="firstName"
                    required #fn="ngModel"
                    (focus)="fnFocused=true" (blur)="fnFocused=false"
                    placeholder="Jean">
                </div>
                <span class="field-error" *ngIf="fn.invalid && fn.touched">Requis</span>
              </div>

              <div class="field-group">
                <label class="field-label">Nom <span class="req">*</span></label>
                <div class="field-wrap" [class.is-error]="ln.invalid && ln.touched" [class.is-focus]="lnFocused">
                  <input type="text" class="field-input"
                    [(ngModel)]="consultant.lastName" name="lastName"
                    required #ln="ngModel"
                    (focus)="lnFocused=true" (blur)="lnFocused=false"
                    placeholder="Dupont">
                </div>
                <span class="field-error" *ngIf="ln.invalid && ln.touched">Requis</span>
              </div>
            </div>

            <!-- Email -->
            <div class="field-group">
              <label class="field-label">Email professionnel <span class="req">*</span></label>
              <div class="field-wrap" [class.is-error]="em.invalid && em.touched" [class.is-focus]="emFocused">
                <svg class="field-ico" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="1.8"/>
                  <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="1.8"/>
                </svg>
                <input type="email" class="field-input"
                  [(ngModel)]="consultant.email" name="email"
                  required email #em="ngModel"
                  (focus)="emFocused=true" (blur)="emFocused=false"
                  placeholder="jean.dupont@cabinet.com">
              </div>
              <span class="field-error" *ngIf="em.invalid && em.touched">Email valide requis</span>
            </div>

            <!-- Phone -->
            <div class="field-group">
              <label class="field-label">Téléphone <span class="optional">(optionnel)</span></label>
              <div class="field-wrap" [class.is-focus]="phFocused">
                <svg class="field-ico" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.57a16 16 0 0 0 6.29 6.29l.94-.94a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" stroke="currentColor" stroke-width="1.8"/>
                </svg>
                <input type="tel" class="field-input"
                  [(ngModel)]="consultant.phone" name="phone"
                  (focus)="phFocused=true" (blur)="phFocused=false"
                  placeholder="+213 6 00 00 00 00">
              </div>
            </div>

            <!-- Password -->
            <div class="field-group">
              <label class="field-label">Mot de passe <span class="req">*</span></label>
              <div class="field-wrap" [class.is-error]="pwd.invalid && pwd.touched" [class.is-focus]="pwdFocused">
                <svg class="field-ico" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="1.8"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="1.8"/>
                </svg>
                <input [type]="showPwd ? 'text' : 'password'" class="field-input"
                  [(ngModel)]="consultant.password" name="password"
                  required minlength="6" #pwd="ngModel"
                  (focus)="pwdFocused=true" (blur)="pwdFocused=false"
                  (ngModelChange)="updateStrength($event)"
                  placeholder="Minimum 6 caractères">
                <button type="button" class="eye-btn" (click)="showPwd=!showPwd" tabindex="-1">
                  <svg *ngIf="!showPwd" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8"/></svg>
                  <svg *ngIf="showPwd" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" stroke="currentColor" stroke-width="1.8"/><line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="1.8"/></svg>
                </button>
              </div>
              <!-- Strength bar -->
              <div class="strength-bar" *ngIf="consultant.password">
                <div class="strength-track">
                  <div class="strength-fill" [style.width.%]="pwdStrength * 33.3" [class]="'s'+pwdStrength"></div>
                </div>
                <span class="strength-label" [class]="'s'+pwdStrength">{{ pwdStrengthLabel }}</span>
              </div>
              <span class="field-error" *ngIf="pwd.invalid && pwd.touched">Mot de passe (6 car. min) requis</span>
            </div>

            <!-- Error banner -->
            <div class="error-banner" *ngIf="errorMessage">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#dc2626" stroke-width="1.8"/><line x1="12" y1="8" x2="12" y2="12" stroke="#dc2626" stroke-width="1.8"/><line x1="12" y1="16" x2="12.01" y2="16" stroke="#dc2626" stroke-width="2.5"/></svg>
              {{ errorMessage }}
            </div>

            <!-- Submit -->
            <button type="submit" class="btn-primary" [disabled]="regForm.invalid || isLoading">
              <span *ngIf="!isLoading">
                Créer mon compte
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2"/><polyline points="12 5 19 12 12 19" stroke="currentColor" stroke-width="2"/></svg>
              </span>
              <span *ngIf="isLoading" class="loading-row">
                <span class="spinner"></span>Création du compte…
              </span>
            </button>

          </form>

          <div class="divider"><span>déjà inscrit ?</span></div>

          <a routerLink="/login" class="btn-secondary">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" stroke="currentColor" stroke-width="1.8"/><polyline points="10 17 15 12 10 7" stroke="currentColor" stroke-width="1.8"/><line x1="15" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="1.8"/></svg>
            Se connecter à mon compte
          </a>

          <p class="terms-note">
            En créant un compte, vous acceptez nos
            <a href="#" class="terms-link">Conditions d'utilisation</a>
            et notre
            <a href="#" class="terms-link">Politique de confidentialité</a>.
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
      width: 50%;
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
      width: 450px; height: 450px;
      background: radial-gradient(circle, rgba(124,58,237,.35) 0%, transparent 70%);
      top: -100px; left: -80px;
      animation-delay: 0s;
    }
    .orb-2 {
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(37,99,235,.25) 0%, transparent 70%);
      bottom: -80px; right: -60px;
      animation-delay: -3s;
    }
    .orb-3 {
      width: 280px; height: 280px;
      background: radial-gradient(circle, rgba(16,185,129,.15) 0%, transparent 70%);
      top: 50%; left: 45%;
      animation-delay: -6s;
    }
    @keyframes float {
      0%, 100% { transform: translateY(0) scale(1); }
      50% { transform: translateY(-25px) scale(1.04); }
    }

    .grid-overlay {
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
      background-size: 48px 48px;
    }

    .panel-left-inner {
      position: relative; z-index: 1;
      display: flex; flex-direction: column; justify-content: space-between;
      padding: 40px 48px;
      width: 100%;
    }

    .logo-row { display: flex; align-items: center; gap: 12px; }
    .logo-mark {
      width: 40px; height: 40px;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }
    .logo-mark-gradient { background: linear-gradient(135deg, #2563eb, #7c3aed); }
    .logo-text { font-size: 18px; font-weight: 700; color: #fff; letter-spacing: -.3px; }

    .hero-content { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 40px 0; }

    .hero-badge {
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(124,58,237,.15);
      border: 1px solid rgba(124,58,237,.3);
      color: #c4b5fd;
      padding: 6px 14px; border-radius: 999px;
      font-size: 12px; font-weight: 500; letter-spacing: .3px;
      width: fit-content; margin-bottom: 28px;
    }
    .badge-dot {
      width: 7px; height: 7px;
      background: #a78bfa; border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: .6; transform: scale(.85); }
    }

    .hero-title {
      font-size: 2.4rem; font-weight: 800;
      color: #f1f5f9; line-height: 1.15;
      letter-spacing: -.6px; margin-bottom: 18px;
    }
    .hero-title-accent {
      background: linear-gradient(90deg, #a78bfa, #60a5fa);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .hero-sub {
      color: #64748b; font-size: 14.5px; line-height: 1.75;
      max-width: 380px; margin-bottom: 36px;
    }

    .steps { display: flex; flex-direction: column; }
    .step { display: flex; align-items: flex-start; gap: 14px; }
    .step-num {
      width: 32px; height: 32px; flex-shrink: 0;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 13px; font-weight: 700; color: #fff;
    }
    .step-body { padding-top: 4px; }
    .step-title { font-size: 14px; font-weight: 600; color: #e2e8f0; }
    .step-sub { font-size: 12px; color: #475569; margin-top: 2px; }
    .step-connector {
      width: 1px; height: 22px;
      background: rgba(255,255,255,.08);
      margin-left: 15px;
    }

    .trust-row {
      display: flex; align-items: center; gap: 12px;
      margin-bottom: 0;
    }
    .trust-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #475569; }
    .trust-dot { width: 3px; height: 3px; background: #1e293b; border-radius: 50%; }
    .panel-footer { color: #1e293b; font-size: 12px; margin-top: 16px; }

    /* ══ RIGHT PANEL ══ */
    .panel-right {
      flex: 1;
      background: #fff;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      padding: 40px 24px;
      position: relative;
      overflow-y: auto;
    }
    .panel-right::before {
      content: ''; position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg, #7c3aed, #2563eb, #06b6d4);
    }

    .mobile-logo {
      display: flex; align-items: center; gap: 10px;
      margin-bottom: 32px;
    }
    @media (min-width: 1024px) { .mobile-logo { display: none; } }
    .logo-text-dark { font-size: 18px; font-weight: 700; color: #0f172a; }

    .form-container { width: 100%; max-width: 420px; }

    .form-header { margin-bottom: 28px; }
    .form-title { font-size: 1.9rem; font-weight: 800; color: #0f172a; letter-spacing: -.5px; margin-bottom: 6px; }
    .form-sub { font-size: 14px; color: #64748b; }

    .form-body { display: flex; flex-direction: column; gap: 18px; }

    .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

    .field-group { display: flex; flex-direction: column; gap: 5px; }
    .field-label { font-size: 13px; font-weight: 600; color: #374151; }
    .req { color: #ef4444; }
    .optional { color: #94a3b8; font-weight: 400; font-size: 12px; }

    .field-wrap {
      display: flex; align-items: center;
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      border-radius: 10px;
      padding: 0 14px;
      transition: border-color .15s, box-shadow .15s, background .15s;
    }
    .field-wrap.is-focus {
      border-color: #7c3aed;
      background: #fff;
      box-shadow: 0 0 0 3px rgba(124,58,237,.1);
    }
    .field-wrap.is-error { border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239,68,68,.1); }
    .field-ico { color: #94a3b8; flex-shrink: 0; margin-right: 10px; }
    .field-input {
      flex: 1; border: none; outline: none; background: transparent;
      padding: 12px 0; font-size: 14px; color: #0f172a;
      font-family: inherit;
    }
    .field-input::placeholder { color: #cbd5e1; }
    .eye-btn {
      background: none; border: none; cursor: pointer;
      color: #94a3b8; padding: 0; margin-left: 8px;
      display: flex; align-items: center;
      transition: color .15s;
    }
    .eye-btn:hover { color: #7c3aed; }

    .strength-bar { display: flex; align-items: center; gap: 10px; margin-top: 4px; }
    .strength-track { flex: 1; height: 4px; background: #f1f5f9; border-radius: 2px; overflow: hidden; }
    .strength-fill { height: 100%; border-radius: 2px; transition: width .3s, background .3s; }
    .strength-fill.s1 { background: #ef4444; }
    .strength-fill.s2 { background: #f59e0b; }
    .strength-fill.s3 { background: #10b981; }
    .strength-label { font-size: 11px; font-weight: 600; white-space: nowrap; }
    .strength-label.s1 { color: #ef4444; }
    .strength-label.s2 { color: #f59e0b; }
    .strength-label.s3 { color: #10b981; }

    .field-error { font-size: 12px; color: #ef4444; }

    .error-banner {
      display: flex; align-items: center; gap: 8px;
      background: #fef2f2; border: 1px solid #fecaca;
      color: #dc2626; border-radius: 8px;
      padding: 11px 14px; font-size: 13.5px;
    }

    .btn-primary {
      width: 100%;
      background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
      color: #fff; border: none; border-radius: 10px;
      padding: 14px; font-size: 15px; font-weight: 600;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: opacity .2s, transform .15s, box-shadow .2s;
      letter-spacing: .1px; font-family: inherit;
      box-shadow: 0 4px 15px rgba(124,58,237,.3);
    }
    .btn-primary:hover:not(:disabled) {
      opacity: .93; transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(124,58,237,.35);
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
      margin: 18px 0;
    }
    .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #f1f5f9; }

    .btn-secondary {
      width: 100%;
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      color: #374151; border-radius: 10px;
      padding: 13px; font-size: 14px; font-weight: 600;
      text-decoration: none;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: border-color .15s, color .15s, background .15s;
      font-family: inherit;
    }
    .btn-secondary:hover {
      border-color: #7c3aed; color: #7c3aed; background: #faf5ff;
    }

    .terms-note {
      font-size: 12px; color: #94a3b8;
      text-align: center; margin-top: 18px; line-height: 1.6;
    }
    .terms-link { color: #7c3aed; text-decoration: none; font-weight: 500; }
    .terms-link:hover { text-decoration: underline; }
  `]
})
export class RegisterComponent {
  consultant = { firstName: '', lastName: '', email: '', password: '', phone: '' };
  isLoading = false;
  errorMessage = '';
  showPwd = false;
  pwdStrength = 0;
  pwdStrengthLabel = '';

  fnFocused = false; lnFocused = false;
  emFocused = false; phFocused = false; pwdFocused = false;

  constructor(private authService: AuthService, private router: Router) {}

  updateStrength(value: string) {
    if (!value) { this.pwdStrength = 0; return; }
    let s = 0;
    if (value.length >= 6) s++;
    if (value.length >= 10) s++;
    if (/[A-Z]/.test(value) && /[0-9!@#$%^&*]/.test(value)) s++;
    this.pwdStrength = Math.max(1, s);
    this.pwdStrengthLabel = ['', 'Faible', 'Moyen', 'Fort'][this.pwdStrength];
  }

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
