import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { ActionPlanService, ActionPlanTask, ActionPlanRequest } from './action-plan.service';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-action-plan',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './action-plan.component.html',
  styleUrls: ['./action-plan.component.css']
})
export class ActionPlanComponent implements OnInit {
  evaluationId!: number;
  tasks: ActionPlanTask[] = [];
  view: 'kanban' | 'list' = 'kanban';
  loading = false;
  generating = false;
  companyName = '';

  editingTask: ActionPlanTask | null = null;
  editForm: ActionPlanRequest = {};

  readonly AXES = ['METIER', 'PROCESSUS', 'SI', 'CANAUX_DISTRIBUTION',
                   'MARKETING_COMMUNICATION', 'RH_CULTURE_DIGITALE', 'OFFRES_DIGITALES',
                   'MODELE_OPERATIONNEL_INNOVATION', 'IT_DATA'];
  readonly PRIORITIES = ['HAUTE', 'MOYENNE', 'BASSE'];
  readonly PHASES = ['Phase 1 - Court terme', 'Phase 2 - Moyen terme', 'Phase 3 - Long terme'];

  constructor(
    private route: ActivatedRoute,
    private actionPlanService: ActionPlanService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.evaluationId = Number(this.route.snapshot.paramMap.get('evaluationId'));
    this.load();
  }

  load(): void {
    this.loading = true;
    this.actionPlanService.getByEvaluation(this.evaluationId).subscribe({
      next: tasks => {
        this.tasks = tasks;
        if (tasks.length > 0) this.companyName = tasks[0].companyName;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  generate(): void {
    this.generating = true;
    this.http.get<any>(`${environment.apiUrl}/evaluations/${this.evaluationId}/recommendations`)
      .pipe(catchError(() => of([])))
      .subscribe(recs => {
        this.actionPlanService.generate(this.evaluationId, recs).subscribe({
          next: tasks => {
            this.tasks = tasks;
            if (tasks.length > 0) this.companyName = tasks[0].companyName;
            this.generating = false;
          },
          error: () => { this.generating = false; }
        });
      });
  }

  // ── Kanban getters ──────────────────────────────────────────────────────────

  get todoTasks(): ActionPlanTask[] { return this.tasks.filter(t => t.status === 'TODO'); }
  get inProgressTasks(): ActionPlanTask[] { return this.tasks.filter(t => t.status === 'IN_PROGRESS'); }
  get doneTasks(): ActionPlanTask[] { return this.tasks.filter(t => t.status === 'DONE'); }

  // ── Status transitions ──────────────────────────────────────────────────────

  moveForward(task: ActionPlanTask): void {
    const next = task.status === 'TODO' ? 'IN_PROGRESS' : 'DONE';
    this.patchStatus(task, next);
  }

  moveBack(task: ActionPlanTask): void {
    const prev = task.status === 'DONE' ? 'IN_PROGRESS' : 'TODO';
    this.patchStatus(task, prev);
  }

  private patchStatus(task: ActionPlanTask, status: ActionPlanTask['status']): void {
    this.actionPlanService.update(task.id, { status }).subscribe(updated => {
      Object.assign(task, updated);
    });
  }

  // ── Edit modal ──────────────────────────────────────────────────────────────

  openEdit(task: ActionPlanTask): void {
    this.editingTask = task;
    this.editForm = {
      title: task.title,
      description: task.description,
      axe: task.axe,
      priority: task.priority,
      phase: task.phase,
      responsible: task.responsible,
      deadline: task.deadline ? task.deadline.substring(0, 10) : '',
      status: task.status
    };
  }

  saveEdit(): void {
    if (!this.editingTask) return;
    this.actionPlanService.update(this.editingTask.id, this.editForm).subscribe(updated => {
      Object.assign(this.editingTask!, updated);
      this.editingTask = null;
    });
  }

  cancelEdit(): void { this.editingTask = null; }

  deleteTask(task: ActionPlanTask): void {
    if (!confirm('Supprimer cette tâche ?')) return;
    this.actionPlanService.delete(task.id).subscribe(() => {
      this.tasks = this.tasks.filter(t => t.id !== task.id);
    });
  }

  // ── Excel export ────────────────────────────────────────────────────────────

  exportExcel(): void {
    this.actionPlanService.exportExcel(this.evaluationId).subscribe(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `plan-action-${this.evaluationId}.xlsx`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // ── Helpers ─────────────────────────────────────────────────────────────────

  priorityClass(priority: string): string {
    return priority === 'HAUTE' ? 'bg-danger' : priority === 'MOYENNE' ? 'bg-warning text-dark' : 'bg-success';
  }

  statusLabel(status: string): string {
    return status === 'TODO' ? 'À faire' : status === 'IN_PROGRESS' ? 'En cours' : 'Terminé';
  }

  axeShort(axe: string): string {
    const map: Record<string, string> = {
      METIER: 'Métier', PROCESSUS: 'Processus', SI: 'SI',
      CANAUX_DISTRIBUTION: 'Canaux', MARKETING_COMMUNICATION: 'Marketing',
      RH_CULTURE_DIGITALE: 'RH', OFFRES_DIGITALES: 'Offres',
      MODELE_OPERATIONNEL_INNOVATION: 'Modèle Op.', IT_DATA: 'IT & Data'
    };
    return map[axe] ?? axe;
  }

  isOverdue(deadline: string): boolean {
    return !!deadline && new Date(deadline) < new Date();
  }

  get doneCount(): number { return this.doneTasks.length; }
  get progress(): number { return this.tasks.length ? Math.round((this.doneCount / this.tasks.length) * 100) : 0; }
}
