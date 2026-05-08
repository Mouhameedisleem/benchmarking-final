import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { QuestionService } from '../../../core/services/question.service';
import { CompanyService } from '../../../core/services/company.service';
import { Question, SubAxis } from '../../../core/models/question.model';  // SubAxis est maintenant exporté

@Component({
  selector: 'app-question-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './question-list.component.html',
  styleUrls: ['./question-list.component.css']
})
export class QuestionListComponent implements OnInit {
  questions: Question[] = [];
  filteredQuestions: Question[] = [];
  
  searchTerm = '';
  selectedAxis = '';
  selectedSubAxis = '';
  selectedSector = '';
  showInactive = false;
  
  currentPage = 1;
  itemsPerPage = 10;
  totalPages = 1;
  pages: number[] = [];
  Math = Math;
  
  axisOptions = this.questionService.getAxisOptions();
  subAxes: SubAxis[] = [];  // Type correct
  sectors: any[] = [];
  
  isLoading = false;
  errorMessage = '';

  constructor(
    private questionService: QuestionService,
    private companyService: CompanyService
  ) {}

  ngOnInit() {
    this.loadQuestions();
    this.loadFilterData();
  }

  loadQuestions() {
    this.isLoading = true;
    this.questionService.getQuestions().subscribe({
      next: (data: Question[]) => {
        this.questions = data;
        this.applyFilters();
        this.isLoading = false;
      },
      error: (error: any) => {
        this.errorMessage = 'Erreur lors du chargement des questions';
        this.isLoading = false;
        console.error(error);
      }
    });
  }

  loadFilterData() {
    this.companyService.getSectors().subscribe((data: any[]) => {
      this.sectors = data;
    });
    
    this.questionService.getSubAxes().subscribe((data: SubAxis[]) => {  // Type correct
      this.subAxes = data;
    });
  }

  onAxisChange() {
    if (this.selectedAxis) {
      this.questionService.getSubAxesByAxis(this.selectedAxis).subscribe((data: SubAxis[]) => {
        this.subAxes = data;
      });
    } else {
      this.questionService.getSubAxes().subscribe((data: SubAxis[]) => {
        this.subAxes = data;
      });
    }
    this.selectedSubAxis = '';
    this.applyFilters();
  }

  applyFilters() {
    this.filteredQuestions = this.questions.filter((q: Question) => {  // Type ajouté
      if (!this.showInactive && !q.isActive) return false;
      
      const matchesSearch = !this.searchTerm || 
        q.content.toLowerCase().includes(this.searchTerm.toLowerCase());
      
      const matchesAxis = !this.selectedAxis || q.axis === this.selectedAxis;
      const matchesSubAxis = !this.selectedSubAxis || q.subAxis === this.selectedSubAxis;
      const matchesSector = !this.selectedSector || q.sector === this.selectedSector;

      return matchesSearch && matchesAxis && matchesSubAxis && matchesSector;
    });

    this.currentPage = 1;
    this.calculatePagination();
  }

  resetFilters() {
    this.searchTerm = '';
    this.selectedAxis = '';
    this.selectedSubAxis = '';
    this.selectedSector = '';
    this.showInactive = false;
    this.onAxisChange();
  }

  calculatePagination() {
    this.totalPages = Math.ceil(this.filteredQuestions.length / this.itemsPerPage);
    this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
  }

  getPaginatedItems(): Question[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    return this.filteredQuestions.slice(start, end);
  }

  changePage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  getAxisLabel(axis: string): string {
    const option = this.axisOptions.find((o: { value: string; label: string }) => o.value === axis);  // Type ajouté
    return option ? option.label : axis;
  }

  getSubAxisName(subAxisId: string): string {
    const subAxis = this.subAxes.find((s: SubAxis) => s.id === subAxisId);  // Type ajouté
    return subAxis ? subAxis.name : subAxisId;
  }

  getSectorName(sectorId: string): string {
    const sector = this.sectors.find((s: any) => s.id === sectorId);
    return sector ? `${sector.icon || ''} ${sector.name}` : 'Tous secteurs';
  }

  deleteQuestion(id: number) {
    if (confirm('Êtes-vous sûr de vouloir désactiver cette question ?')) {
      this.questionService.deleteQuestion(id).subscribe({
        next: () => {
          this.loadQuestions();
        },
        error: (error: any) => {  // Type ajouté
          alert('Erreur lors de la désactivation');
          console.error(error);
        }
      });
    }
  }

  toggleQuestionStatus(question: Question) {  // Type ajouté
    this.questionService.updateQuestion(question.id!, { isActive: !question.isActive }).subscribe({
      next: () => {
        this.loadQuestions();
      },
      error: (error: any) => {  // Type ajouté
        alert('Erreur lors du changement de statut');
        console.error(error);
      }
    });
  }
}