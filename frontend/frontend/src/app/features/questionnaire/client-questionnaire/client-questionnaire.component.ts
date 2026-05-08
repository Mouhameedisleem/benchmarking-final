import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Subscription } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { QuestionnaireService } from '../../../core/services/questionnaire.service';
import { AuthService } from '../../../core/services/auth.service';
import { Question, QuestionResponse, QuestionSection } from '../../../core/models/question.model';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-client-questionnaire',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './client-questionnaire.component.html',
  styleUrls: ['./client-questionnaire.component.css']
})
export class ClientQuestionnaireComponent implements OnInit, OnDestroy {
  currentSection: QuestionSection | null = null;
  sections: QuestionSection[] = [];
  currentIndex = 0;
  globalProgress = { answered: 0, total: 0, percentage: 0 };
  companyName = '';
  isLoading = true;
  errorMessage = '';
  isSubmitting = false;
  submitted = false;

  private subscription: Subscription = new Subscription();

  constructor(
    private questionnaireService: QuestionnaireService,
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit() {
    const user = this.authService.getCurrentUser();
    if (!user?.companyId) {
      this.errorMessage = 'Aucune entreprise associée à votre compte';
      this.isLoading = false;
      return;
    }

    // Check if an evaluation already exists — if so redirect to score page
    this.http.get<any>(`${environment.apiUrl}/evaluations/latest?companyId=${user.companyId}`)
      .pipe(catchError(() => of(null)))
      .subscribe(evaluation => {
        if (evaluation?.evaluationId) {
          this.router.navigate(['/client/dashboard']);
          return;
        }
        this.loadQuestionnaire(user.companyId!);
      });
  }

  private loadQuestionnaire(companyId: number) {
    this.questionnaireService.initQuestionnaire(companyId).subscribe({
      next: (state) => {
        this.companyName = state.companyName;
        this.sections = state.sections;
        this.currentIndex = state.currentSection;
        this.currentSection = this.sections[this.currentIndex];
        this.globalProgress = this.questionnaireService.getGlobalProgress();
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = 'Erreur lors du chargement du questionnaire';
        this.isLoading = false;
        console.error(error);
      }
    });

    // S'abonner aux changements d'état
    this.subscription.add(
      this.questionnaireService.currentState$.subscribe(state => {
        if (state) {
          this.sections = state.sections;
          this.currentIndex = state.currentSection;
          this.currentSection = this.sections[this.currentIndex];
          this.globalProgress = this.questionnaireService.getGlobalProgress();
        }
      })
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  /**
   * Sauvegarde la réponse à une question
   */
  onAnswerChange(question: Question, event: any) {
    let value: any = event.target?.value;
    
    // Convertir en nombre si nécessaire
    if (question.responseType === 'SCALE_1_5' || question.responseType === 'PERCENTAGE') {
      value = parseInt(value, 10);
    } else if (question.responseType === 'BOOLEAN') {
      value = event.target?.checked;
    }

    const response: QuestionResponse = {
      questionId: question.id!,
      value: value
    };

    this.questionnaireService.saveResponse(question.id!, response);
  }

  /**
   * Sauvegarde un commentaire
   */
  onCommentChange(question: Question, event: any) {
    const existing = this.questionnaireService.currentState.value?.responses[question.id!];
    const response: QuestionResponse = existing ?? { questionId: question.id!, value: 0 };
    response.comment = event.target?.value;
    this.questionnaireService.saveResponse(question.id!, response);
  }

  /**
   * Passe à la section suivante
   */
  nextSection() {
    if (this.questionnaireService.nextSection()) {
      // Scroll en haut de la page
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  /**
   * Retourne à la section précédente
   */
  previousSection() {
    if (this.questionnaireService.previousSection()) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  /**
   * Soumet le questionnaire complet
   */
  submitQuestionnaire() {
    if (!this.questionnaireService.isCurrentSectionComplete()) {
      alert('Veuillez répondre à toutes les questions de cette section avant de continuer.');
      return;
    }

    if (confirm('Êtes-vous sûr de vouloir soumettre le questionnaire ? Vous ne pourrez plus modifier vos réponses.')) {
      this.isSubmitting = true;
      this.questionnaireService.calculateFinalScore().subscribe({
        next: () => {
          this.isSubmitting = false;
          this.submitted = true;
        },
        error: (error) => {
          this.isSubmitting = false;
          alert('Erreur lors du calcul du score');
          console.error(error);
        }
      });
    }
  }

  /**
   * Récupère la réponse à une question
   */
  getResponse(questionId: number): any {
    return this.questionnaireService.currentState.value?.responses[questionId]?.value;
  }

  /**
   * Récupère le commentaire d'une question
   */
  getComment(questionId: number): string {
    return this.questionnaireService.currentState.value?.responses[questionId]?.comment || '';
  }

  /**
   * Vérifie si une question a une réponse
   */
  hasResponse(questionId: number): boolean {
    return this.questionnaireService.currentState.value?.responses[questionId] !== undefined;
  }

  /**
   * Obtient la classe CSS pour le type de réponse
   */
  readonly FALLBACK_OPTIONS = [
    'Aucun dispositif ou outil en place',
    'Premiers essais isolés, sans processus établi',
    'Pratiques partiellement formalisées, adoption en cours',
    'Pratiques établies, mesurées et déployées à grande échelle',
    'Excellence opérationnelle, pilotage continu par la donnée',
  ];

  getMaturityOptions(question: Question): string[] {
    return question.options && question.options.length === 5 ? question.options : this.FALLBACK_OPTIONS;
  }

  isAnswered(questionId: number): boolean {
    return this.questionnaireService.currentState.value?.responses[questionId] !== undefined;
  }

  isCommentFilled(questionId: number): boolean {
    const c = this.questionnaireService.currentState.value?.responses[questionId]?.comment;
    return !!c && c.trim().length > 0;
  }

  getResponseTypeClass(question: Question): string {
    const response = this.getResponse(question.id!);
    if (response !== undefined && response !== null && response !== '') {
      return 'is-valid';
    }
    return '';
  }

  /**
   * Calcule le pourcentage de progression de la section
   */
  getSectionProgress(section: QuestionSection): number {
    return section.progress.percentage;
  }

  /**
   * Vérifie si la section courante est complète
   */
  get isCurrentSectionComplete(): boolean {
    return this.questionnaireService.isCurrentSectionComplete();
  }

  /**
   * Vérifie si c'est la dernière section
   */
  get isLastSection(): boolean {
    return this.currentIndex === this.sections.length - 1;
  }

  /**
   * Récupère l'icône de la catégorie
   */
  getCategoryIcon(categoryId: string): string {
    const icons: any = {
      'CANAUX': '📱',
      'SELFCARE': '🤳',
      'MARKETING': '📢',
      'OFFRES': '💳',
      'OPEN_BANKING': '🔓',
      'AUTOMATISATION': '⚙️',
      'GOUVERNANCE': '📊',
      'INNOVATION': '💡',
      'CULTURE': '🌱',
      'COLLABORATIF': '👥',
      'RH': '👔',
      'AGILITE': '🔄',
      'SOCLE_IT': '💻',
      'DATA': '📊',
      'POSTE_TRAVAIL': '🖥️'
    };
    return icons[categoryId] || '📋';
  }
}