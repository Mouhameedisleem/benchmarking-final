import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { QuestionService } from '../../../core/services/question.service';
import { CompanyService } from '../../../core/services/company.service';
import { Question, SubAxis } from '../../../core/models/question.model';

@Component({
  selector: 'app-question-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './question-form.component.html',
  styleUrls: ['./question-form.component.css']
})
export class QuestionFormComponent implements OnInit {
question: Question = {
  content: '',
  axis: 'METIER',
  category: '',
  subAxis: '',
  order: 1,
  isActive: true,
  required: true,  // AJOUT
  responseType: 'BOOLEAN',
  sector: '',
  country: ''
};

  isEditMode = false;
  questionId: number | null = null;
  isLoading = false;
  errorMessage = '';

  // Données pour les selects
  axisOptions = this.questionService.getAxisOptions();
  categories: any[] = [];
  subAxes: SubAxis[] = [];
  filteredSubAxes: SubAxis[] = [];
  sectors: any[] = [];
  countries: any[] = [];

  constructor(
    private questionService: QuestionService,
    private companyService: CompanyService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadFilterData();
    this.checkEditMode();
  }

  loadFilterData() {
    // Charger les catégories - CORRECTION : ajouter subscribe
    this.questionService.getCategories().subscribe((data: any[]) => {
      this.categories = data;
    });

    // Charger tous les sous-axes - CORRECTION : ajouter subscribe
    this.questionService.getSubAxes().subscribe((data: SubAxis[]) => {
      this.subAxes = data;
    });

    // Charger les secteurs - CORRECTION : ajouter subscribe
    this.companyService.getSectors().subscribe((data: any[]) => {
      this.sectors = data;
    });

    // Charger les pays - CORRECTION : ajouter subscribe
    this.companyService.getCountries().subscribe((data: any[]) => {
      this.countries = data;
    });
  }

  checkEditMode() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.questionId = +id;
      this.loadQuestion(this.questionId);
    }
  }

  loadQuestion(id: number) {
    this.isLoading = true;
    this.questionService.getQuestion(id).subscribe({
      next: (question) => {
        if (question) {
          this.question = question;
          this.onAxisChange(); // Mettre à jour les sous-axes disponibles
          this.onCategoryChange(); // Mettre à jour les sous-axes filtrés
        } else {
          this.errorMessage = 'Question non trouvée';
        }
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement';
        this.isLoading = false;
      }
    });
  }

  onAxisChange() {
    // CORRECTION : getCategories retourne un Observable, donc subscribe
    this.questionService.getCategories().subscribe((allCategories: any[]) => {
      this.categories = allCategories.filter((c: any) => c.axis === this.question.axis);
    });
    
    // Réinitialiser la catégorie si elle n'est pas dans le nouvel axe
    if (this.question.category && !this.categories.find(c => c.id === this.question.category)) {
      this.question.category = '';
      this.question.subAxis = '';
    }
    
    this.onCategoryChange();
  }

  onCategoryChange() {
    if (this.question.category) {
      // Filtrer les sous-axes par catégorie
      this.filteredSubAxes = this.subAxes.filter(s => s.category === this.question.category);
    } else {
      this.filteredSubAxes = [];
    }
    this.question.subAxis = '';
  }

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = '';

    if (this.isEditMode && this.questionId) {
      // Mise à jour
      this.questionService.updateQuestion(this.questionId, this.question).subscribe({
        next: () => {
          this.router.navigate(['/questions']);
        },
        error: () => {
          this.errorMessage = 'Erreur lors de la mise à jour';
          this.isLoading = false;
        }
      });
    } else {
      // Création
      this.questionService.addQuestion(this.question).subscribe({
        next: () => {
          this.router.navigate(['/questions']);
        },
        error: () => {
          this.errorMessage = "Erreur lors de l'ajout";
          this.isLoading = false;
        }
      });
    }
  }

  cancel() {
    this.router.navigate(['/questions']);
  }
}