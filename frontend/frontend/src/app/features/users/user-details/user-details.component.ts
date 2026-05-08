import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { UserService } from '../../../core/services/user.service';
import { CompanyService } from '../../../core/services/company.service';
import { User, USER_ROLES } from '../../../core/models/user.model';

@Component({
  selector: 'app-user-details',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.css']
})
export class UserDetailsComponent implements OnInit {
  user: User | null = null;
  isLoading = true;
  errorMessage = '';
  
  roles = USER_ROLES;
  companies: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService,
    private companyService: CompanyService
  ) {}

  ngOnInit() {
    this.loadCompanies();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadUser(+id);
    } else {
      this.errorMessage = 'ID utilisateur manquant';
      this.isLoading = false;
    }
  }

  loadCompanies() {
    this.companyService.getCompanies().subscribe({
      next: (data) => {
        this.companies = data;
      }
    });
  }

  loadUser(id: number) {
    this.userService.getUser(id).subscribe({
      next: (user) => {
        if (user) {
          this.user = user;
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

  getRoleLabel(role: string): string {
    const r = this.roles.find(r => r.value === role);
    return r ? r.label : role;
  }

  getRoleBadgeClass(role: string): string {
    const classes: any = {
      'ADMIN': 'bg-danger',
      'CONSULTANT': 'bg-primary',
      'CLIENT': 'bg-success'
    };
    return classes[role] || 'bg-secondary';
  }

  getCompanyName(companyId?: number): string {
    if (!companyId) return '-';
    const company = this.companies.find(c => c.id === companyId);
    return company ? company.name : '-';
  }

  getInitials(): string {
    if (!this.user) return 'U';
    const first = this.user.firstName?.charAt(0) || '';
    const last = this.user.lastName?.charAt(0) || '';
    return (first + last).toUpperCase() || 'U';
  }

  editUser() {
    if (this.user?.id) {
      this.router.navigate(['/users', this.user.id, 'edit']);
    }
  }

  deleteUser() {
    if (this.user?.id && confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
      this.userService.deleteUser(this.user.id).subscribe({
        next: () => {
          this.router.navigate(['/users']);
        },
        error: () => {
          alert('Erreur lors de la suppression');
        }
      });
    }
  }

  toggleStatus() {
    if (this.user?.id) {
      this.userService.toggleUserStatus(this.user.id).subscribe({
        next: (updatedUser) => {
          if (updatedUser) {
            this.user = updatedUser;
          }
        },
        error: () => {
          alert('Erreur lors du changement de statut');
        }
      });
    }
  }

  goBack() {
    this.router.navigate(['/users']);
  }
}