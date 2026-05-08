import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

type QuestionAxis = 'BUSINESS' | 'PROCESS' | 'INFORMATION_SYSTEM' | 'CANAUX_DISTRIBUTION' | 'MARKETING_COMMUNICATION' | 'RH_CULTURE_DIGITALE' | 'OFFRES_DIGITALES';

interface AiQuestion {
  text: string;
  axis: QuestionAxis;
  sub_axis: string;
  weight: number;
  display_order: number;
  source_framework?: string;
  options?: string[];
  editing?: boolean;
  reused?: boolean;
}

interface SectorQuestion {
  id: number;
  text: string;
  axis: QuestionAxis;
  subAxis: string;
  weight: number;
  displayOrder: number;
  options?: string[];
  selected?: boolean;
}

@Component({
  selector: 'app-company-setup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width:900px;">

      <!-- Header -->
      <div class="d-flex align-items-center mb-4">
        <a routerLink="/companies" class="btn btn-sm btn-outline-secondary me-3">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </a>
        <div>
          <h3 class="mb-0 fw-bold">Configuration du questionnaire</h3>
          <small class="text-muted">Génération et validation par l'IA</small>
        </div>
      </div>

      <!-- Stepper -->
      <div class="d-flex align-items-center mb-4">
        <div class="d-flex align-items-center" *ngFor="let s of steps; let i = index">
          <div class="d-flex align-items-center">
            <div class="rounded-circle d-flex align-items-center justify-content-center fw-bold"
                 style="width:36px;height:36px;font-size:14px;"
                 [style.background]="step > i ? '#198754' : step === i ? '#0d6efd' : '#e9ecef'"
                 [style.color]="step >= i ? '#fff' : '#6c757d'">
              <i *ngIf="step > i" class="fas fa-check" style="font-size:12px;"></i>
              <span *ngIf="step <= i">{{ i + 1 }}</span>
            </div>
            <span class="ms-2 small fw-semibold"
                  [class.text-primary]="step === i"
                  [class.text-success]="step > i"
                  [class.text-muted]="step < i">{{ s }}</span>
          </div>
          <div *ngIf="i < steps.length - 1"
               class="flex-grow-1 mx-3"
               style="height:2px;"
               [style.background]="step > i ? '#198754' : '#e9ecef'"></div>
        </div>
      </div>

      <!-- Step 0: Generating -->
      <div *ngIf="step === 0" class="card border-0 shadow-sm rounded-4">
        <div class="card-body p-5 text-center">
          <div class="mb-4">
            <div class="spinner-border text-primary mb-3" style="width:3rem;height:3rem;"></div>
            <h4 class="fw-bold">Génération en cours…</h4>
            <p class="text-muted">L'IA analyse le secteur et génère un questionnaire adapté.</p>
          </div>
          <div *ngIf="generateError" class="alert alert-danger">
            <i class="fas fa-exclamation-circle me-2"></i>{{ generateError }}
            <div class="mt-2">
              <button class="btn btn-danger btn-sm" (click)="loadAiQuestions()">Réessayer</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 1: Review questions -->
      <div *ngIf="step === 1">
        <div class="card border-0 shadow-sm rounded-4 mb-3">
          <div class="card-header bg-white border-0 pt-4 px-4 pb-2 d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-robot text-primary me-2"></i>Questions générées par l'IA
              </h5>
              <small class="text-muted">{{ questions.length }} questions — modifiez, supprimez ou ajoutez</small>
            </div>
            <button class="btn btn-outline-primary btn-sm" (click)="addQuestion()">
              <i class="fas fa-plus me-1"></i>Ajouter
            </button>
          </div>

          <div class="card-body px-4 pb-4">
            <!-- Sector reuse panel -->
            <div *ngIf="sectorQuestions.length > 0" class="mb-4 border rounded-3 overflow-hidden">
              <div class="d-flex align-items-center justify-content-between px-3 py-2"
                   style="background:#fefce8;cursor:pointer;border-bottom:1px solid #fef08a;"
                   (click)="showSectorPanel = !showSectorPanel">
                <span class="fw-semibold" style="color:#854d0e;">
                  ♻️ {{ sectorQuestions.length }} question(s) déjà utilisée(s) dans ce secteur
                  <span class="badge ms-2" style="background:#fef08a;color:#854d0e;font-size:11px;">
                    {{ countAvailableSectorQuestions() }} disponible(s)
                  </span>
                </span>
                <div class="d-flex align-items-center gap-2">
                  <button class="btn btn-sm btn-outline-warning py-0"
                          style="font-size:12px;"
                          (click)="$event.stopPropagation(); addAllSectorQuestions()">
                    Tout ajouter
                  </button>
                  <i class="fas" [class.fa-chevron-down]="!showSectorPanel" [class.fa-chevron-up]="showSectorPanel" style="color:#854d0e;"></i>
                </div>
              </div>
              <div *ngIf="showSectorPanel" class="p-3" style="background:#fffbeb;">
                <div *ngFor="let sq of sectorQuestions"
                     class="d-flex align-items-start gap-2 p-2 rounded mb-2"
                     [style.opacity]="sq.selected ? '0.5' : '1'"
                     style="background:#fff;border:1px solid #fef08a;">
                  <span class="badge mt-1 flex-shrink-0"
                        [style.background]="getAxisColor(sq.axis) + '20'"
                        [style.color]="getAxisColor(sq.axis)"
                        style="font-size:11px;">{{ getAxisLabel(sq.axis) }}</span>
                  <div class="flex-grow-1 small">
                    <div class="fw-semibold">{{ sq.text }}</div>
                    <div class="text-muted" style="font-size:11px;">{{ sq.subAxis }}</div>
                  </div>
                  <button class="btn btn-sm flex-shrink-0"
                          style="font-size:11px;padding:2px 8px;"
                          [class.btn-outline-warning]="!sq.selected"
                          [class.btn-success]="sq.selected"
                          [disabled]="sq.selected"
                          (click)="addSectorQuestion(sq)">
                    {{ sq.selected ? '✓ Ajouté' : '+ Ajouter' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Legend -->
            <div class="d-flex gap-3 mb-3 flex-wrap">
              <span *ngFor="let a of axisLabels" class="badge rounded-pill" [style.background]="a.color + '20'" [style.color]="a.color" style="font-size:12px;padding:6px 12px;">
                {{ a.label }} ({{ countAxis(a.key) }})
              </span>
            </div>

            <!-- Question list -->
            <div class="list-group list-group-flush">
              <div *ngFor="let q of questions; let i = index"
                   class="list-group-item border rounded-3 mb-2 p-3"
                   [style.border-left]="'4px solid ' + getAxisColor(q.axis) + ' !important'">

                <!-- View mode -->
                <div *ngIf="!q.editing" class="d-flex align-items-start gap-3">
                  <span class="badge mt-1 flex-shrink-0" [style.background]="getAxisColor(q.axis) + '20'" [style.color]="getAxisColor(q.axis)">
                    {{ getAxisLabel(q.axis) }}
                  </span>
                  <div class="flex-grow-1">
                    <p class="mb-1 small fw-semibold">
                      {{ q.text }}
                      <span *ngIf="q.reused" class="badge ms-1" style="background:#fef9c3;color:#854d0e;font-size:10px;">♻️ Réutilisé</span>
                    </p>
                    <small class="text-muted">{{ q.sub_axis }}<span *ngIf="q.source_framework"> · {{ q.source_framework }}</span></small>
                  </div>
                  <div class="d-flex gap-1 flex-shrink-0">
                    <button class="btn btn-sm btn-outline-secondary py-0 px-2" (click)="q.editing = true" title="Modifier">
                      <i class="fas fa-pencil-alt" style="font-size:11px;"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger py-0 px-2" (click)="removeQuestion(i)" title="Supprimer">
                      <i class="fas fa-trash" style="font-size:11px;"></i>
                    </button>
                  </div>
                </div>

                <!-- Edit mode -->
                <div *ngIf="q.editing">
                  <textarea class="form-control form-control-sm mb-2" rows="2" [(ngModel)]="q.text" placeholder="Texte de la question"></textarea>
                  <div class="row g-2">
                    <div class="col-4">
                      <select class="form-select form-select-sm" [(ngModel)]="q.axis">
                        <option value="BUSINESS">Métier</option>
                        <option value="PROCESS">Processus</option>
                        <option value="INFORMATION_SYSTEM">SI</option>
                        <option value="CANAUX_DISTRIBUTION">Canaux</option>
                        <option value="MARKETING_COMMUNICATION">Marketing</option>
                        <option value="RH_CULTURE_DIGITALE">RH & Culture</option>
                        <option value="OFFRES_DIGITALES">Offres digitales</option>
                      </select>
                    </div>
                    <div class="col-5">
                      <input class="form-control form-control-sm" [(ngModel)]="q.sub_axis" placeholder="Sous-axe">
                    </div>
                    <div class="col-3 d-flex gap-1">
                      <button class="btn btn-success btn-sm flex-grow-1" (click)="q.editing = false">
                        <i class="fas fa-check"></i>
                      </button>
                      <button class="btn btn-outline-danger btn-sm" (click)="removeQuestion(i)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-between">
          <button class="btn btn-outline-secondary" (click)="step = 0; loadAiQuestions()">
            <i class="fas fa-sync me-1"></i>Régénérer
          </button>
          <button class="btn btn-primary px-4" (click)="validateAndFinalize()" [disabled]="questions.length === 0">
            <i class="fas fa-paper-plane me-2"></i>Valider et envoyer les accès
          </button>
        </div>
      </div>

      <!-- Step 2: Finalizing -->
      <div *ngIf="step === 2" class="card border-0 shadow-sm rounded-4">
        <div class="card-body p-5 text-center">
          <div class="spinner-border text-success mb-3" style="width:3rem;height:3rem;"></div>
          <h4 class="fw-bold">Finalisation en cours…</h4>
          <p class="text-muted">Enregistrement du questionnaire et envoi des accès par email.</p>
        </div>
      </div>

      <!-- Step 3: Done -->
      <div *ngIf="step === 3" class="card border-0 shadow-sm rounded-4">
        <div class="card-body p-5 text-center">
          <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-4"
               style="width:80px;height:80px;">
            <i class="fas fa-check-circle text-success fa-3x"></i>
          </div>
          <h4 class="fw-bold text-success mb-2">Configuration terminée !</h4>

          <!-- Email sent OK -->
          <p *ngIf="!emailFailed" class="text-muted mb-4">
            <i class="fas fa-envelope text-success me-1"></i>{{ finalMessage }}
          </p>

          <!-- Email failed — show credentials inline -->
          <div *ngIf="emailFailed" class="alert alert-warning text-start mb-4">
            <p class="fw-semibold mb-2"><i class="fas fa-exclamation-triangle me-1"></i>Email non envoyé — partagez ces identifiants manuellement :</p>
            <div class="bg-white rounded p-3 font-monospace small border">
              <div *ngFor="let line of credentialLines" class="mb-1">{{ line }}</div>
            </div>
          </div>

          <p class="text-muted small mb-4">Le questionnaire est enregistré. L'entreprise peut se connecter et répondre.</p>
          <div class="d-flex justify-content-center gap-3">
            <a routerLink="/companies" class="btn btn-outline-secondary">
              <i class="fas fa-list me-1"></i>Mes entreprises
            </a>
            <a [routerLink]="['/companies', companyId]" class="btn btn-primary">
              <i class="fas fa-building me-1"></i>Voir l'entreprise
            </a>
          </div>
        </div>
      </div>

      <!-- Error on finalize -->
      <div *ngIf="finalizeError && step === 1" class="alert alert-danger mt-3">
        <i class="fas fa-exclamation-circle me-2"></i>{{ finalizeError }}
      </div>

    </div>
  `
})
export class CompanySetupComponent implements OnInit {
  companyId!: number;
  step = 0;
  questions: AiQuestion[] = [];
  generateError = '';
  finalizeError = '';
  finalMessage = '';
  emailFailed = false;
  credentialLines: string[] = [];

  sectorQuestions: SectorQuestion[] = [];
  showSectorPanel = false;

  steps = ['Génération IA', 'Révision', 'Envoi'];

  axisLabels = [
    { key: 'BUSINESS',               label: 'Métier',          color: '#0d6efd' },
    { key: 'PROCESS',                label: 'Processus',       color: '#198754' },
    { key: 'INFORMATION_SYSTEM',     label: 'SI',              color: '#6366f1' },
    { key: 'CANAUX_DISTRIBUTION',    label: 'Canaux',          color: '#f59e0b' },
    { key: 'MARKETING_COMMUNICATION',label: 'Marketing',       color: '#ec4899' },
    { key: 'RH_CULTURE_DIGITALE',    label: 'RH & Culture',    color: '#06b6d4' },
    { key: 'OFFRES_DIGITALES',       label: 'Offres digitales',color: '#84cc16' },
  ];

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.companyId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadAiQuestions();
  }

  loadAiQuestions() {
    this.step = 0;
    this.generateError = '';
    this.sectorQuestions = [];
    this.showSectorPanel = false;

    this.http.get<any>(`${environment.apiUrl}/companies/${this.companyId}/ai-questions`).subscribe({
      next: (res) => {
        this.questions = (res.questions as AiQuestion[]).map((q, i) => ({
          ...q,
          display_order: q.display_order ?? i + 1,
          editing: false,
          reused: false
        }));
        this.step = 1;
        this.loadSectorQuestions();
      },
      error: (err) => {
        this.generateError = err?.error?.message || 'Erreur lors de la génération. Vérifiez que le service IA est démarré.';
      }
    });
  }

  private loadSectorQuestions() {
    this.http.get<SectorQuestion[]>(`${environment.apiUrl}/companies/${this.companyId}/sector-questions`).subscribe({
      next: (qs) => {
        this.sectorQuestions = qs.map(q => ({ ...q, selected: false }));
      },
      error: () => { /* sector questions are optional, ignore errors */ }
    });
  }

  addSectorQuestion(sq: SectorQuestion) {
    if (sq.selected) return;
    sq.selected = true;
    this.questions.push({
      text: sq.text,
      axis: sq.axis,
      sub_axis: sq.subAxis,
      weight: sq.weight ?? 3,
      display_order: this.questions.length + 1,
      options: sq.options ?? [],
      editing: false,
      reused: true
    });
    this.questions.forEach((q, i) => q.display_order = i + 1);
  }

  addAllSectorQuestions() {
    this.sectorQuestions
      .filter(sq => !sq.selected)
      .forEach(sq => this.addSectorQuestion(sq));
  }

  addQuestion() {
    this.questions.push({
      text: '',
      axis: 'BUSINESS',
      sub_axis: '',
      weight: 3,
      display_order: this.questions.length + 1,
      editing: true
    });
  }

  removeQuestion(index: number) {
    this.questions.splice(index, 1);
    this.questions.forEach((q, i) => q.display_order = i + 1);
  }

  validateAndFinalize() {
    this.finalizeError = '';
    this.step = 2;

    const payload = {
      questions: this.questions.map((q, i) => ({
        text: q.text,
        axis: q.axis,
        subAxis: q.sub_axis || 'Général',
        weight: q.weight || 3,
        displayOrder: i + 1,
        options: q.options || []
      }))
    };

    this.http.post<any>(`${environment.apiUrl}/companies/${this.companyId}/finalize`, payload).subscribe({
      next: (res) => {
        const msg: string = res.message || '';
        this.emailFailed = msg.includes('email non envoyé') || msg.includes('erreur SMTP');
        if (this.emailFailed) {
          this.credentialLines = msg.split('|').map((s: string) => s.trim());
        } else {
          this.finalMessage = msg;
        }
        this.step = 3;
      },
      error: (err) => {
        this.finalizeError = err?.error?.message || 'Erreur lors de la finalisation.';
        this.step = 1;
      }
    });
  }

  getAxisColor(axis: string): string {
    return this.axisLabels.find(a => a.key === axis)?.color ?? '#6c757d';
  }

  getAxisLabel(axis: string): string {
    return this.axisLabels.find(a => a.key === axis)?.label ?? axis;
  }

  countAxis(key: string): number {
    return this.questions.filter(q => q.axis === key).length;
  }

  countAvailableSectorQuestions(): number {
    return this.sectorQuestions.filter(q => !q.selected).length;
  }
}
