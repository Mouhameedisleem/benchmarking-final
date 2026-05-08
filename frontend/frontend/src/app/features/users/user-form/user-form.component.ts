import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { UserService } from '../../../core/services/user.service';
import { CompanyService } from '../../../core/services/company.service';
import { User, USER_ROLES } from '../../../core/models/user.model';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.css']
})
export class UserFormComponent implements OnInit {
  user: User = {
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    role: 'CLIENT',
    isActive: true,
    password: ''
  };

  isEditMode = false;
  userId: number | null = null;
  isLoading = false;
  errorMessage = '';

  // Données pour les selects
  roles = USER_ROLES;
  companies: any[] = [];
  showPassword = false;

  constructor(
    private userService: UserService,
    private companyService: CompanyService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadCompanies();
    this.checkEditMode();
  }

  loadCompanies() {
    this.companyService.getCompanies().subscribe({
      next: (data) => {
        this.companies = data;
      },
      error: (error) => {
        console.error('Erreur chargement entreprises:', error);
      }
    });
  }

  checkEditMode() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.userId = +id;
      this.loadUser(this.userId);
    }
  }

  loadUser(id: number) {
    this.isLoading = true;
    this.userService.getUser(id).subscribe({
      next: (user) => {
        if (user) {
          this.user = user;
          // Ne pas afficher le mot de passe en mode édition
          this.user.password = undefined;
        } else {
          this.errorMessage = 'Utilisateur non trouvé';
        }
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = '';

    if (this.isEditMode && this.userId) {
      // Mise à jour (sans mot de passe)
      const { password, ...userData } = this.user;
      this.userService.updateUser(this.userId, userData).subscribe({
        next: () => {
          this.router.navigate(['/users']);
        },
        error: () => {
          this.errorMessage = 'Erreur lors de la mise à jour';
          this.isLoading = false;
        }
      });
    } else {
      // Création
      this.userService.addUser(this.user).subscribe({
        next: () => {
          this.router.navigate(['/users']);
        },
        error: () => {
          this.errorMessage = "Erreur lors de l'ajout";
          this.isLoading = false;
        }
      });
    }
  }

  cancel() {
    this.router.navigate(['/users']);
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  // Vérifier si le rôle nécessite une entreprise
  get requiresCompany(): boolean {
    return this.user.role === 'CLIENT';
  }
}