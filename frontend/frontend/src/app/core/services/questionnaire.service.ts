import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, forkJoin, map, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {
  Question, QuestionSection, QuestionnaireState, QuestionResponse, CATEGORIES
} from '../models/question.model';
import { environment } from '../../../environments/environment';

interface ExtendedState extends QuestionnaireState {
  _questionnaireId?: number;
}

@Injectable({ providedIn: 'root' })
export class QuestionnaireService {
  private readonly questionnairesUrl = `${environment.apiUrl}/questionnaires`;
  private readonly companiesUrl = `${environment.apiUrl}/companies`;
  private readonly evaluationsUrl = `${environment.apiUrl}/evaluations`;

  currentState = new BehaviorSubject<ExtendedState | null>(null);
  currentState$ = this.currentState.asObservable();

  private readonly axisMap: Record<string, Question['axis']> = {
    BUSINESS:               'METIER',
    PROCESS:                'PROCESSUS',
    INFORMATION_SYSTEM:     'SI',
    METIER:                 'METIER',
    PROCESSUS:              'PROCESSUS',
    SI:                     'SI',
    CANAUX_DISTRIBUTION:             'CANAUX_DISTRIBUTION',
    MARKETING_COMMUNICATION:         'MARKETING_COMMUNICATION',
    RH_CULTURE_DIGITALE:             'RH_CULTURE_DIGITALE',
    OFFRES_DIGITALES:                'OFFRES_DIGITALES',
    MODELE_OPERATIONNEL_INNOVATION:  'MODELE_OPERATIONNEL_INNOVATION',
    IT_DATA:                         'IT_DATA',
  };

  constructor(private http: HttpClient) {}

  private draftKey(companyId: number, questionnaireId: number): string {
    return `questionnaire_draft_${companyId}_${questionnaireId}`;
  }

  private saveDraft(state: ExtendedState): void {
    if (!state._questionnaireId) return;
    try {
      localStorage.setItem(this.draftKey(state.companyId, state._questionnaireId), JSON.stringify({
        responses: state.responses,
        currentSection: state.currentSection
      }));
    } catch { /* storage quota exceeded — ignore */ }
  }

  private loadDraft(companyId: number, questionnaireId: number): { responses: { [key: number]: QuestionResponse }; currentSection: number } | null {
    try {
      const raw = localStorage.getItem(this.draftKey(companyId, questionnaireId));
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }

  clearDraft(companyId: number, questionnaireId: number): void {
    try { localStorage.removeItem(this.draftKey(companyId, questionnaireId)); } catch { /* ignore */ }
  }

  initQuestionnaire(companyId: number): Observable<ExtendedState> {
    return forkJoin({
      company: this.http.get<any>(`${this.companiesUrl}/${companyId}`),
      questionnaires: this.http.get<any[]>(`${this.questionnairesUrl}?companyId=${companyId}`).pipe(catchError(() => of([])))
    }).pipe(
      map(({ company, questionnaires }) => {
        const active = (questionnaires as any[]).find((q: any) => q.active) || questionnaires[0];
        const rawQuestions: any[] = active?.questions || [];
        const questions = rawQuestions.map((q: any, i: number) => this.mapQuestion(q, i));
        const sections = this.buildSections(questions);

        const draft = active?.id ? this.loadDraft(companyId, active.id) : null;

        const state: ExtendedState = {
          companyId,
          companyName: company.name,
          companySector: company.sector,
          companyCountry: company.country,
          currentSection: draft?.currentSection ?? 0,
          sections,
          responses: draft?.responses ?? {},
          completed: false,
          startedAt: new Date(),
          _questionnaireId: active?.id
        };

        if (draft) {
          this.updateSectionProgress(state);
        }

        this.currentState.next(state);
        return state;
      })
    );
  }

  saveResponse(questionId: number, response: QuestionResponse) {
    const state = this.currentState.value;
    if (!state) return;
    const updated: ExtendedState = {
      ...state,
      responses: { ...state.responses, [questionId]: response }
    };
    this.updateSectionProgress(updated);
    this.currentState.next(updated);
    this.saveDraft(updated);
  }

  nextSection(): boolean {
    const state = this.currentState.value;
    if (!state || state.currentSection >= state.sections.length - 1) return false;
    const updated = { ...state, currentSection: state.currentSection + 1 };
    this.currentState.next(updated);
    this.saveDraft(updated);
    return true;
  }

  previousSection(): boolean {
    const state = this.currentState.value;
    if (!state || state.currentSection <= 0) return false;
    const updated = { ...state, currentSection: state.currentSection - 1 };
    this.currentState.next(updated);
    this.saveDraft(updated);
    return true;
  }

  isCurrentSectionComplete(): boolean {
    const state = this.currentState.value;
    if (!state) return false;
    const section = state.sections[state.currentSection];
    return section.questions
      .filter(q => q.required)
      .every(q => state.responses[q.id!] !== undefined);
  }

  getGlobalProgress(): { answered: number; total: number; percentage: number } {
    const state = this.currentState.value;
    if (!state) return { answered: 0, total: 0, percentage: 0 };
    const allQuestions = state.sections.flatMap(s => s.questions);
    const answered = allQuestions.filter(q => state.responses[q.id!] !== undefined).length;
    const total = allQuestions.length;
    return { answered, total, percentage: total ? Math.round((answered / total) * 100) : 0 };
  }

  calculateFinalScore(): Observable<{ evaluationId: number }> {
    const state = this.currentState.value!;
    const answers = Object.entries(state.responses).map(([qId, res]) => ({
      questionId: Number(qId),
      value: typeof res.value === 'boolean' ? (res.value ? 5 : 1) : Number(res.value),
      comment: res.comment
    }));

    return this.http.post<any>(this.evaluationsUrl, {
      companyId: state.companyId,
      questionnaireId: state._questionnaireId,
      answers
    }).pipe(map(r => {
      if (state._questionnaireId) {
        this.clearDraft(state.companyId, state._questionnaireId);
      }
      return { evaluationId: r.evaluationId };
    }));
  }

  private mapQuestion(q: any, index: number): Question {
    const axis = this.axisMap[q.axis] || 'METIER';
    return {
      id: q.id,
      content: q.text,
      axis,
      subAxis: q.subAxis || '',
      category: this.inferCategory(axis),
      order: q.displayOrder || index + 1,
      weight: q.weight || 1,
      isActive: true,
      required: true,
      responseType: 'SCALE_1_5',
      options: q.options || []
    };
  }

  private inferCategory(axis: Question['axis']): string {
    const defaults: Record<string, string> = {
      METIER:                  'CANAUX',
      PROCESSUS:               'AUTOMATISATION',
      SI:                      'SOCLE_IT',
      CANAUX_DISTRIBUTION:            'CANAUX',
      MARKETING_COMMUNICATION:        'MARKETING',
      RH_CULTURE_DIGITALE:            'RH',
      OFFRES_DIGITALES:               'OFFRES',
      MODELE_OPERATIONNEL_INNOVATION: 'MODELE_OPERATIONNEL',
      IT_DATA:                        'IT_DATA',
    };
    return defaults[axis] || 'CANAUX';
  }

  private buildSections(questions: Question[]): QuestionSection[] {
    const grouped = new Map<string, Question[]>();
    for (const q of questions) {
      const key = `${q.axis}::${q.category}`;
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key)!.push(q);
    }

    const sections: QuestionSection[] = [];
    let order = 0;
    for (const [key, qs] of grouped.entries()) {
      const [axis, category] = key.split('::');
      const cat = CATEGORIES.find(c => c.id === category);
      sections.push({
        category,
        categoryLabel: cat?.name || category,
        axis,
        icon: cat?.icon,
        questions: qs,
        progress: {
          answered: 0,
          total: qs.length,
          percentage: 0,
          mandatoryAnswered: 0,
          mandatoryTotal: qs.filter(q => q.required).length
        },
        order: order++,
        isActive: true
      });
    }
    return sections.sort((a, b) => a.order - b.order);
  }

  private updateSectionProgress(state: ExtendedState) {
    for (const section of state.sections) {
      const answered = section.questions.filter(q => state.responses[q.id!] !== undefined).length;
      const mandatoryAnswered = section.questions
        .filter(q => q.required && state.responses[q.id!] !== undefined).length;
      section.progress = {
        answered,
        total: section.questions.length,
        percentage: section.questions.length
          ? Math.round((answered / section.questions.length) * 100)
          : 0,
        mandatoryAnswered,
        mandatoryTotal: section.questions.filter(q => q.required).length
      };
    }
  }
}
