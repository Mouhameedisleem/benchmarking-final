import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="landing-page">

      <!-- ══════════ NAVBAR ══════════ -->
      <nav class="lp-nav">
        <div class="lp-nav-inner">
          <div class="d-flex align-items-center gap-2">
            <div class="nav-logo-icon"><i class="fas fa-robot"></i></div>
            <span class="nav-brand">IA Benchmark</span>
          </div>
          <div class="nav-actions">
            <a routerLink="/login" class="btn-nav-login">Se connecter</a>
            <a routerLink="/register" class="btn-nav-register">Commencer gratuitement</a>
          </div>
        </div>
      </nav>

      <!-- ══════════ HERO ══════════ -->
      <section class="hero-section">
        <div class="hero-bg-shapes">
          <div class="shape shape-1"></div>
          <div class="shape shape-2"></div>
          <div class="shape shape-3"></div>
        </div>
        <div class="hero-content">
          <div class="hero-badge">
            <span class="badge-dot"></span>Powered by Artificial Intelligence
          </div>
          <h1 class="hero-title">
            Évaluez la maturité digitale<br>
            <span class="gradient-text">de vos entreprises clientes</span>
          </h1>
          <p class="hero-sub">
            IA Benchmark génère automatiquement des questionnaires personnalisés, calcule un score de maturité précis et produit des recommandations stratégiques grâce à l'intelligence artificielle.
          </p>
          <div class="hero-cta">
            <a routerLink="/register" class="btn-hero-primary">
              <i class="fas fa-rocket me-2"></i>Démarrer l'évaluation
            </a>
            <a routerLink="/login" class="btn-hero-secondary">
              <i class="fas fa-sign-in-alt me-2"></i>Se connecter
            </a>
          </div>
          <!-- Badges de confiance -->
          <div class="trust-badges">
            <div class="trust-item"><i class="fas fa-shield-alt"></i><span>Données sécurisées</span></div>
            <div class="trust-sep">·</div>
            <div class="trust-item"><i class="fas fa-brain"></i><span>IA générative</span></div>
            <div class="trust-sep">·</div>
            <div class="trust-item"><i class="fas fa-globe"></i><span>Benchmarking international</span></div>
          </div>
        </div>

        <!-- Hero illustration -->
        <div class="hero-visual">
          <svg viewBox="0 0 480 440" xmlns="http://www.w3.org/2000/svg" class="hero-svg">
            <defs>
              <linearGradient id="gBlue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#1a56db"/>
                <stop offset="100%" stop-color="#7c3aed"/>
              </linearGradient>
              <linearGradient id="gPurple" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#7c3aed"/>
                <stop offset="100%" stop-color="#06b6d4"/>
              </linearGradient>
              <linearGradient id="gGreen" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#059669"/>
                <stop offset="100%" stop-color="#06b6d4"/>
              </linearGradient>
              <linearGradient id="gCard" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="100%" stop-color="#f0f4ff" stop-opacity="1"/>
              </linearGradient>
              <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#1a56db" flood-opacity="0.15"/>
              </filter>
              <filter id="shadowSm" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.1"/>
              </filter>
              <clipPath id="cardClip">
                <rect x="40" y="30" width="400" height="380" rx="24"/>
              </clipPath>
            </defs>

            <!-- Background card -->
            <rect x="40" y="30" width="400" height="380" rx="24" fill="url(#gCard)" filter="url(#shadow)"/>

            <!-- Top accent bar -->
            <rect x="40" y="30" width="400" height="5" rx="5" fill="url(#gBlue)"/>

            <!-- ── Header strip ── -->
            <rect x="40" y="35" width="400" height="48" fill="#f8fafc"/>
            <circle cx="70" cy="59" r="6" fill="#fca5a5"/>
            <circle cx="88" cy="59" r="6" fill="#fcd34d"/>
            <circle cx="106" cy="59" r="6" fill="#6ee7b7"/>
            <text x="130" y="63" font-size="11" fill="#94a3b8" font-family="Inter,sans-serif">Rapport de maturité digitale — IA Benchmark</text>

            <!-- ── Central AI brain illustration ── -->
            <!-- Brain outline (simplified circuit brain) -->
            <g transform="translate(240,155)">
              <!-- Outer glow ring -->
              <circle cx="0" cy="0" r="72" fill="none" stroke="url(#gBlue)" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.5">
                <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/>
              </circle>
              <!-- Middle ring -->
              <circle cx="0" cy="0" r="55" fill="none" stroke="#e0e7ff" stroke-width="1" opacity="0.8"/>
              <!-- Core circle -->
              <circle cx="0" cy="0" r="42" fill="url(#gBlue)" opacity="0.1"/>
              <circle cx="0" cy="0" r="36" fill="url(#gBlue)" opacity="0.15"/>
              <!-- Robot/AI icon -->
              <circle cx="0" cy="0" r="28" fill="url(#gBlue)"/>
              <!-- Robot face -->
              <rect x="-12" y="-16" width="24" height="20" rx="4" fill="white" opacity="0.9"/>
              <rect x="-8" y="-12" width="6" height="5" rx="1.5" fill="url(#gBlue)"/>
              <rect x="2" y="-12" width="6" height="5" rx="1.5" fill="url(#gBlue)"/>
              <rect x="-6" y="-3" width="12" height="3" rx="1.5" fill="url(#gBlue)" opacity="0.6"/>
              <rect x="-16" y="-5" width="4" height="8" rx="2" fill="white" opacity="0.7"/>
              <rect x="12" y="-5" width="4" height="8" rx="2" fill="white" opacity="0.7"/>
              <!-- Antenna -->
              <line x1="0" y1="-16" x2="0" y2="-25" stroke="white" stroke-width="2" opacity="0.9"/>
              <circle cx="0" cy="-27" r="3" fill="white"/>
              <!-- Legs -->
              <rect x="-10" y="12" width="8" height="10" rx="2" fill="white" opacity="0.7"/>
              <rect x="2" y="12" width="8" height="10" rx="2" fill="white" opacity="0.7"/>

              <!-- Radiating connection lines -->
              <line x1="55" y1="0" x2="90" y2="0" stroke="url(#gBlue)" stroke-width="1.5" opacity="0.4"/>
              <line x1="-55" y1="0" x2="-90" y2="0" stroke="url(#gBlue)" stroke-width="1.5" opacity="0.4"/>
              <line x1="39" y1="-39" x2="60" y2="-60" stroke="url(#gPurple)" stroke-width="1.5" opacity="0.4"/>
              <line x1="-39" y1="-39" x2="-60" y2="-60" stroke="url(#gPurple)" stroke-width="1.5" opacity="0.4"/>
              <line x1="39" y1="39" x2="60" y2="60" stroke="url(#gGreen)" stroke-width="1.5" opacity="0.4"/>
              <line x1="-39" y1="39" x2="-60" y2="60" stroke="url(#gGreen)" stroke-width="1.5" opacity="0.4"/>
              <line x1="0" y1="-55" x2="0" y2="-85" stroke="url(#gBlue)" stroke-width="1.5" opacity="0.4"/>
            </g>

            <!-- ── Satellite nodes ── -->
            <!-- Node: Métier (top) -->
            <g transform="translate(240,58)">
              <circle cx="0" cy="0" r="18" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
              <text x="0" y="-4" text-anchor="middle" font-size="9" font-weight="700" fill="#1a56db" font-family="Inter,sans-serif">Axe</text>
              <text x="0" y="6" text-anchor="middle" font-size="8" fill="#1a56db" font-family="Inter,sans-serif">Métier</text>
            </g>

            <!-- Node: Processus (top-right) -->
            <g transform="translate(308,87)">
              <circle cx="0" cy="0" r="18" fill="#f5f3ff" stroke="#c4b5fd" stroke-width="1.5"/>
              <text x="0" y="-4" text-anchor="middle" font-size="9" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">Axe</text>
              <text x="0" y="6" text-anchor="middle" font-size="7" fill="#7c3aed" font-family="Inter,sans-serif">Processus</text>
            </g>

            <!-- Node: SI (top-left) -->
            <g transform="translate(172,87)">
              <circle cx="0" cy="0" r="18" fill="#ecfeff" stroke="#a5f3fc" stroke-width="1.5"/>
              <text x="0" y="-4" text-anchor="middle" font-size="9" font-weight="700" fill="#0891b2" font-family="Inter,sans-serif">Axe</text>
              <text x="0" y="6" text-anchor="middle" font-size="8" fill="#0891b2" font-family="Inter,sans-serif">SI</text>
            </g>

            <!-- Node right: Score 78% -->
            <g transform="translate(342,155)">
              <rect x="-22" y="-14" width="44" height="28" rx="8" fill="#fff" stroke="#e0e7ff" stroke-width="1.5" filter="url(#shadowSm)"/>
              <text x="0" y="-2" text-anchor="middle" font-size="12" font-weight="800" fill="#1a56db" font-family="Inter,sans-serif">78%</text>
              <text x="0" y="9" text-anchor="middle" font-size="7" fill="#94a3b8" font-family="Inter,sans-serif">Métier</text>
            </g>

            <!-- Node left: Score 65% -->
            <g transform="translate(138,155)">
              <rect x="-22" y="-14" width="44" height="28" rx="8" fill="#fff" stroke="#ede9fe" stroke-width="1.5" filter="url(#shadowSm)"/>
              <text x="0" y="-2" text-anchor="middle" font-size="12" font-weight="800" fill="#7c3aed" font-family="Inter,sans-serif">65%</text>
              <text x="0" y="9" text-anchor="middle" font-size="7" fill="#94a3b8" font-family="Inter,sans-serif">Processus</text>
            </g>

            <!-- Node bottom-right: Score 72% -->
            <g transform="translate(308,225)">
              <rect x="-22" y="-14" width="44" height="28" rx="8" fill="#fff" stroke="#cffafe" stroke-width="1.5" filter="url(#shadowSm)"/>
              <text x="0" y="-2" text-anchor="middle" font-size="12" font-weight="800" fill="#0891b2" font-family="Inter,sans-serif">72%</text>
              <text x="0" y="9" text-anchor="middle" font-size="7" fill="#94a3b8" font-family="Inter,sans-serif">SI</text>
            </g>

            <!-- Node bottom-left: IA badge -->
            <g transform="translate(172,225)">
              <rect x="-22" y="-14" width="44" height="28" rx="8" fill="url(#gGreen)" filter="url(#shadowSm)"/>
              <text x="0" y="-2" text-anchor="middle" font-size="11" font-weight="800" fill="#fff" font-family="Inter,sans-serif">IA</text>
              <text x="0" y="9" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.8)" font-family="Inter,sans-serif">Générative</text>
            </g>

            <!-- ── Bottom score bar section ── -->
            <rect x="60" y="275" width="360" height="115" rx="16" fill="#f8fafc"/>

            <!-- Global score pill -->
            <rect x="80" y="291" width="100" height="30" rx="15" fill="url(#gBlue)"/>
            <text x="130" y="311" text-anchor="middle" font-size="12" font-weight="700" fill="white" font-family="Inter,sans-serif">Score global : 72</text>

            <!-- Level badge -->
            <rect x="196" y="291" width="70" height="30" rx="15" fill="#d1fae5"/>
            <text x="231" y="311" text-anchor="middle" font-size="11" font-weight="700" fill="#059669" font-family="Inter,sans-serif">✓ Avancé</text>

            <!-- Bar chart bars -->
            <text x="80" y="340" font-size="9" fill="#94a3b8" font-family="Inter,sans-serif">Métier</text>
            <rect x="80" y="344" width="260" height="7" rx="4" fill="#e0e7ff"/>
            <rect x="80" y="344" width="202" height="7" rx="4" fill="url(#gBlue)"/>
            <text x="348" y="352" font-size="9" font-weight="700" fill="#1a56db" font-family="Inter,sans-serif">78%</text>

            <text x="80" y="361" font-size="9" fill="#94a3b8" font-family="Inter,sans-serif">Processus</text>
            <rect x="80" y="365" width="260" height="7" rx="4" fill="#ede9fe"/>
            <rect x="80" y="365" width="169" height="7" rx="4" fill="url(#gPurple)"/>
            <text x="348" y="373" font-size="9" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">65%</text>

            <text x="80" y="382" font-size="9" fill="#94a3b8" font-family="Inter,sans-serif">SI</text>
            <rect x="80" y="386" width="260" height="7" rx="4" fill="#cffafe"/>
            <rect x="80" y="386" width="187" height="7" rx="4" fill="url(#gGreen)"/>
            <text x="348" y="394" font-size="9" font-weight="700" fill="#0891b2" font-family="Inter,sans-serif">72%</text>

            <!-- Floating sparkle dots -->
            <circle cx="430" cy="60" r="4" fill="#fcd34d" opacity="0.8"/>
            <circle cx="55"  cy="160" r="3" fill="#f9a8d4" opacity="0.7"/>
            <circle cx="450" cy="200" r="5" fill="#6ee7b7" opacity="0.6"/>
            <circle cx="60"  cy="320" r="3" fill="#93c5fd" opacity="0.7"/>
            <circle cx="420" cy="380" r="4" fill="#c4b5fd" opacity="0.6"/>
          </svg>
        </div>
      </section>

      <!-- ══════════ STATS ══════════ -->
      <section class="stats-section">
        <div class="stats-inner">
          <div class="stat-block" *ngFor="let s of stats">
            <div class="stat-number">{{ s.value }}</div>
            <div class="stat-desc">{{ s.label }}</div>
          </div>
        </div>
      </section>

      <!-- ══════════ FONCTIONNALITÉS ══════════ -->
      <section class="features-section">
        <div class="section-container">
          <div class="section-header">
            <div class="section-pill">Fonctionnalités</div>
            <h2 class="section-title">Tout ce dont vous avez besoin pour évaluer et progresser</h2>
            <p class="section-sub">Une plateforme complète pensée pour les consultants et leurs entreprises clientes.</p>
          </div>
          <div class="features-grid">
            <div class="feature-card" *ngFor="let f of features">
              <div class="feature-icon-wrap" [style.background]="f.bg">
                <i class="fas" [class]="f.icon" [style.color]="f.color"></i>
              </div>
              <h3 class="feature-title">{{ f.title }}</h3>
              <p class="feature-desc">{{ f.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ══════════ COMMENT ÇA MARCHE ══════════ -->
      <section class="how-section">
        <div class="section-container">
          <div class="section-header">
            <div class="section-pill">Processus</div>
            <h2 class="section-title">Comment ça marche ?</h2>
            <p class="section-sub">Un processus simple et structuré en 4 étapes.</p>
          </div>
          <div class="steps-row">
            <div class="step-card" *ngFor="let step of steps; let i = index">
              <div class="step-num">{{ i + 1 }}</div>
              <div class="step-icon"><i class="fas" [class]="step.icon"></i></div>
              <h4 class="step-title">{{ step.title }}</h4>
              <p class="step-desc">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ══════════ CTA FINAL ══════════ -->
      <section class="cta-section">
        <div class="cta-card">
          <div class="cta-glow"></div>
          <h2 class="cta-title">Prêt à évaluer votre premier client ?</h2>
          <p class="cta-sub">Inscrivez-vous en tant que consultant et commencez dès aujourd'hui. L'IA fait le reste.</p>
          <div class="cta-actions">
            <a routerLink="/register" class="btn-cta-primary">
              <i class="fas fa-user-plus me-2"></i>Créer mon compte consultant
            </a>
            <a routerLink="/login" class="btn-cta-ghost">
              J'ai déjà un compte <i class="fas fa-arrow-right ms-2"></i>
            </a>
          </div>
        </div>
      </section>

      <!-- ══════════ FOOTER ══════════ -->
      <footer class="lp-footer">
        <div class="footer-inner">
          <div class="d-flex align-items-center gap-2">
            <div class="nav-logo-icon nav-logo-icon-sm"><i class="fas fa-robot"></i></div>
            <span class="footer-brand">IA Benchmark</span>
          </div>
          <p class="footer-copy">© 2026 IA Benchmark — Plateforme d'évaluation de maturité digitale</p>
        </div>
      </footer>

    </div>
  `,
  styles: [`
    /* ── Reset & base ── */
    .landing-page { font-family: 'Inter', 'Segoe UI', sans-serif; background: #fff; color: #0f172a; }

    /* ── Navbar ── */
    .lp-nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(255,255,255,.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid #f1f5f9;
    }
    .lp-nav-inner {
      max-width: 1200px; margin: 0 auto; padding: 16px 32px;
      display: flex; justify-content: space-between; align-items: center;
    }
    .nav-logo-icon {
      width: 36px; height: 36px;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 16px; color: #fff;
    }
    .nav-logo-icon-sm { width: 28px; height: 28px; font-size: 12px; border-radius: 8px; }
    .nav-brand { font-size: 18px; font-weight: 800; color: #0f172a; }
    .nav-actions { display: flex; gap: 12px; align-items: center; }
    .btn-nav-login {
      padding: 8px 18px; border-radius: 8px; font-size: 14px; font-weight: 600;
      color: #374151; text-decoration: none; transition: color .2s;
    }
    .btn-nav-login:hover { color: #1a56db; }
    .btn-nav-register {
      padding: 9px 20px; border-radius: 9px; font-size: 14px; font-weight: 600;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      color: #fff; text-decoration: none; transition: opacity .2s, transform .1s;
    }
    .btn-nav-register:hover { opacity: .9; transform: translateY(-1px); color: #fff; }

    /* ── Hero ── */
    .hero-section {
      min-height: calc(100vh - 69px);
      display: flex; align-items: center; gap: 60px;
      padding: 80px 80px 80px 80px;
      max-width: 1300px; margin: 0 auto;
      position: relative;
    }
    .hero-bg-shapes { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
    .shape {
      position: absolute; border-radius: 50%;
      filter: blur(80px); opacity: .12;
    }
    .shape-1 { width: 600px; height: 600px; background: #1a56db; top: -200px; right: -100px; }
    .shape-2 { width: 400px; height: 400px; background: #7c3aed; bottom: -100px; left: -100px; }
    .shape-3 { width: 300px; height: 300px; background: #06b6d4; top: 40%; left: 35%; }

    .hero-content { flex: 1; position: relative; z-index: 1; }
    .hero-badge {
      display: inline-flex; align-items: center; gap: 8px;
      background: #eff6ff; border: 1px solid #bfdbfe;
      color: #1d4ed8; padding: 6px 16px; border-radius: 999px;
      font-size: 13px; font-weight: 600; margin-bottom: 28px;
    }
    .badge-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: #1a56db;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%,100% { opacity: 1; transform: scale(1); }
      50% { opacity: .5; transform: scale(1.4); }
    }
    .hero-title {
      font-size: 3.2rem; font-weight: 900; line-height: 1.15;
      letter-spacing: -.8px; margin-bottom: 24px;
    }
    .gradient-text {
      background: linear-gradient(135deg,#1a56db,#7c3aed,#06b6d4);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { font-size: 17px; color: #64748b; line-height: 1.75; max-width: 520px; margin-bottom: 36px; }
    .hero-cta { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 36px; }
    .btn-hero-primary {
      padding: 15px 28px; border-radius: 12px; font-size: 15px; font-weight: 700;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      color: #fff; text-decoration: none; transition: transform .15s, box-shadow .15s;
      box-shadow: 0 4px 20px rgba(26,86,219,.35);
    }
    .btn-hero-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(26,86,219,.45); color:#fff; }
    .btn-hero-secondary {
      padding: 15px 28px; border-radius: 12px; font-size: 15px; font-weight: 600;
      background: #fff; border: 1.5px solid #e2e8f0; color: #374151;
      text-decoration: none; transition: border-color .2s, box-shadow .2s;
    }
    .btn-hero-secondary:hover { border-color: #1a56db; color: #1a56db; box-shadow: 0 0 0 3px rgba(26,86,219,.08); }

    .trust-badges { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
    .trust-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #94a3b8; }
    .trust-item i { color: #1a56db; }
    .trust-sep { color: #e2e8f0; }

    /* ── Mockup ── */
    .hero-visual { flex: 0 0 460px; position: relative; z-index: 1; }
    .mockup-card {
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 24px 80px rgba(15,23,42,.15), 0 0 0 1px #f1f5f9;
      overflow: hidden;
    }
    .mockup-header {
      background: #f8fafc; border-bottom: 1px solid #f1f5f9;
      padding: 14px 18px; display: flex; align-items: center; gap: 12px;
    }
    .mockup-dots { display: flex; gap: 5px; }
    .mockup-dots span { width: 10px; height: 10px; border-radius: 50%; background: #e2e8f0; }
    .mockup-dots span:first-child { background: #fca5a5; }
    .mockup-dots span:nth-child(2) { background: #fcd34d; }
    .mockup-dots span:nth-child(3) { background: #6ee7b7; }
    .mockup-title { font-size: 12px; color: #94a3b8; font-weight: 500; }
    .mockup-body { padding: 24px; }

    .score-ring-wrap { text-align: center; margin-bottom: 20px; }
    .score-ring {
      width: 90px; height: 90px; border-radius: 50%;
      background: conic-gradient(#1a56db 0deg 259deg, #f1f5f9 259deg);
      display: flex; align-items: center; justify-content: center;
      margin: 0 auto 8px;
    }
    .score-inner {
      width: 70px; height: 70px; border-radius: 50%; background: #fff;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .score-val { font-size: 22px; font-weight: 800; color: #1a56db; line-height: 1; }
    .score-unit { font-size: 10px; color: #94a3b8; }
    .score-label { font-size: 12px; color: #1a56db; font-weight: 600; }

    .axes-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 18px; }
    .axis-header { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px; }
    .axis-name { color: #374151; font-weight: 500; }
    .axis-score { font-weight: 700; }
    .axis-bar { height: 6px; background: #f1f5f9; border-radius: 999px; overflow: hidden; }
    .axis-fill { height: 100%; border-radius: 999px; transition: width .6s ease; }

    .reco-preview {
      background: #eff6ff; border-radius: 10px; padding: 12px 14px;
      border-left: 3px solid #1a56db;
    }
    .reco-label { font-size: 11px; font-weight: 700; color: #1a56db; margin-bottom: 5px; }
    .reco-label i { margin-right: 5px; }
    .reco-text { font-size: 12px; color: #475569; line-height: 1.5; }

    /* ── Stats ── */
    .stats-section { background: #0f172a; padding: 60px 32px; }
    .stats-inner {
      max-width: 900px; margin: 0 auto;
      display: grid; grid-template-columns: repeat(4,1fr); gap: 24px;
      text-align: center;
    }
    .stat-block {}
    .stat-number { font-size: 2.4rem; font-weight: 900; color: #fff; letter-spacing: -1px; }
    .stat-desc { font-size: 13px; color: #94a3b8; margin-top: 4px; }

    /* ── Features ── */
    .features-section { padding: 100px 32px; background: #f8fafc; }
    .section-container { max-width: 1100px; margin: 0 auto; }
    .section-header { text-align: center; max-width: 640px; margin: 0 auto 60px; }
    .section-pill {
      display: inline-block; padding: 5px 14px; border-radius: 999px;
      background: #eff6ff; color: #1d4ed8; font-size: 12px; font-weight: 700;
      letter-spacing: .5px; text-transform: uppercase; margin-bottom: 14px;
    }
    .section-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 14px; letter-spacing: -.4px; }
    .section-sub { color: #64748b; font-size: 16px; line-height: 1.7; }

    .features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
    .feature-card {
      background: #fff; border-radius: 16px; padding: 28px 24px;
      border: 1px solid #f1f5f9;
      box-shadow: 0 2px 12px rgba(15,23,42,.04);
      transition: transform .2s, box-shadow .2s;
    }
    .feature-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(15,23,42,.1); }
    .feature-icon-wrap {
      width: 48px; height: 48px; border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; margin-bottom: 18px;
    }
    .feature-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 10px; }
    .feature-desc { font-size: 14px; color: #64748b; line-height: 1.65; margin: 0; }

    /* ── How it works ── */
    .how-section { padding: 100px 32px; background: #fff; }
    .steps-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }
    .step-card {
      text-align: center; padding: 32px 20px;
      position: relative;
    }
    .step-card:not(:last-child)::after {
      content: '→';
      position: absolute; right: -10px; top: 40px;
      font-size: 20px; color: #e2e8f0;
    }
    .step-num {
      width: 32px; height: 32px; border-radius: 50%;
      background: linear-gradient(135deg,#1a56db,#7c3aed);
      color: #fff; font-size: 14px; font-weight: 800;
      display: flex; align-items: center; justify-content: center;
      margin: 0 auto 16px;
    }
    .step-icon {
      font-size: 28px; color: #1a56db; margin-bottom: 16px;
    }
    .step-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
    .step-desc { font-size: 13px; color: #64748b; line-height: 1.6; }

    /* ── CTA ── */
    .cta-section { padding: 80px 32px; }
    .cta-card {
      max-width: 780px; margin: 0 auto;
      background: linear-gradient(145deg,#0f172a,#1e3a5f,#1a56db);
      border-radius: 28px; padding: 64px 48px; text-align: center;
      position: relative; overflow: hidden;
    }
    .cta-glow {
      position: absolute; width: 400px; height: 400px; border-radius: 50%;
      background: rgba(124,58,237,.3); filter: blur(80px);
      top: -100px; right: -100px; pointer-events: none;
    }
    .cta-title { font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px; position: relative; }
    .cta-sub { color: #94a3b8; font-size: 16px; margin-bottom: 36px; position: relative; }
    .cta-actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; position: relative; }
    .btn-cta-primary {
      padding: 14px 28px; border-radius: 12px; font-size: 15px; font-weight: 700;
      background: #fff; color: #1a56db; text-decoration: none;
      transition: transform .15s, box-shadow .15s;
    }
    .btn-cta-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2); color: #1a56db; }
    .btn-cta-ghost {
      padding: 14px 28px; border-radius: 12px; font-size: 15px; font-weight: 600;
      border: 1.5px solid rgba(255,255,255,.25); color: #fff; text-decoration: none;
      transition: background .2s, border-color .2s;
    }
    .btn-cta-ghost:hover { background: rgba(255,255,255,.1); border-color: rgba(255,255,255,.4); color: #fff; }

    /* ── Footer ── */
    .lp-footer { background: #f8fafc; border-top: 1px solid #f1f5f9; padding: 28px 32px; }
    .footer-inner {
      max-width: 1100px; margin: 0 auto;
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
    }
    .footer-brand { font-size: 15px; font-weight: 700; color: #0f172a; }
    .footer-copy { font-size: 12px; color: #94a3b8; margin: 0; }

    /* ── Responsive ── */
    @media (max-width: 1024px) {
      .hero-section { flex-direction: column; padding: 60px 32px; }
      .hero-visual { flex: none; width: 100%; max-width: 480px; }
      .hero-title { font-size: 2.4rem; }
      .features-grid { grid-template-columns: repeat(2,1fr); }
      .steps-row { grid-template-columns: repeat(2,1fr); }
      .stats-inner { grid-template-columns: repeat(2,1fr); }
    }
    @media (max-width: 640px) {
      .features-grid, .steps-row { grid-template-columns: 1fr; }
      .hero-title { font-size: 1.9rem; }
      .cta-card { padding: 40px 24px; }
      .cta-title { font-size: 1.6rem; }
      .lp-nav-inner { padding: 14px 20px; }
      .btn-nav-login { display: none; }
    }
  `]
})
export class LandingComponent {
  axes = [
    { name: 'Axe Métier', score: 78, color: '#1a56db' },
    { name: 'Axe Processus', score: 65, color: '#7c3aed' },
    { name: 'Axe SI', score: 72, color: '#06b6d4' },
    { name: 'Axe Canaux & UX', score: 58, color: '#059669' },
    { name: 'Axe Marketing', score: 81, color: '#d97706' },
    { name: 'Axe RH & Culture', score: 63, color: '#7c3aed' },
    { name: 'Axe Offres Digitales', score: 70, color: '#10b981' }
  ];

  stats = [
    { value: '7 axes', label: 'Métier · Processus · SI · Canaux · Marketing · RH · Offres' },
    { value: '20+', label: 'Questions par évaluation' },
    { value: 'IA', label: 'Recommandations personnalisées' },
    { value: '360°', label: 'Benchmarking sectoriel' }
  ];

  features = [
    {
      icon: 'fa-robot',
      title: 'Génération IA de questionnaires',
      desc: "L'IA génère automatiquement un questionnaire sur mesure adapté au secteur, à la taille et au pays de l'entreprise évaluée.",
      color: '#1a56db', bg: '#eff6ff'
    },
    {
      icon: 'fa-chart-bar',
      title: 'Score de maturité digitale',
      desc: 'Un score global et par axe (Métier, Processus, SI) calculé automatiquement à partir des réponses de l\'entreprise.',
      color: '#7c3aed', bg: '#f5f3ff'
    },
    {
      icon: 'fa-globe',
      title: 'Benchmarking sectoriel',
      desc: 'Positionnez chaque entreprise par rapport aux standards régionaux et internationaux de son secteur d\'activité.',
      color: '#0891b2', bg: '#ecfeff'
    },
    {
      icon: 'fa-lightbulb',
      title: 'Recommandations personnalisées',
      desc: "Des recommandations stratégiques générées par l'IA et validées par le consultant avant envoi à l'entreprise.",
      color: '#d97706', bg: '#fffbeb'
    },
    {
      icon: 'fa-user-tie',
      title: 'Espace consultant dédié',
      desc: 'Gérez toutes vos entreprises clientes, suivez les évaluations en attente et validez les résultats avant envoi.',
      color: '#059669', bg: '#ecfdf5'
    },
    {
      icon: 'fa-envelope-open-text',
      title: 'Rapport envoyé par email',
      desc: "Après validation, l'entreprise reçoit automatiquement son score, ses recommandations et son benchmarking par email.",
      color: '#dc2626', bg: '#fef2f2'
    }
  ];

  steps = [
    {
      icon: 'fa-building',
      title: 'Ajout de l\'entreprise',
      desc: 'Le consultant crée le profil de l\'entreprise cliente (secteur, pays, taille).'
    },
    {
      icon: 'fa-robot',
      title: 'Génération du questionnaire',
      desc: 'L\'IA génère automatiquement un questionnaire personnalisé que le consultant valide.'
    },
    {
      icon: 'fa-clipboard-list',
      title: 'Réponse de l\'entreprise',
      desc: 'L\'entreprise reçoit ses accès et répond au questionnaire en ligne à son rythme.'
    },
    {
      icon: 'fa-paper-plane',
      title: 'Résultats & recommandations',
      desc: 'Le consultant valide les résultats IA et l\'entreprise reçoit son rapport complet par email.'
    }
  ];
}
