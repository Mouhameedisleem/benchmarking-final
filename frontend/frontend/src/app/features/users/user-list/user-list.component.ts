import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../core/services/user.service';
import { CompanyService } from '../../../core/services/company.service';
import { User, USER_ROLES } from '../../../core/models/user.model';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
  users: User[] = [];
  filteredUsers: User[] = [];
  userStats: any = { total: 0, active: 0, inactive: 0, byRole: {} };
  
  // Filtres
  searchTerm = '';
  selectedRole = '';
  selectedStatus = '';
  selectedCompany = '';
  
  // Pagination
  currentPage = 1;
  itemsPerPage = 10;
  totalPages = 1;
  pages: number[] = [];
  Math = Math;
  
  // Données pour les filtres
  roles = USER_ROLES;
  companies: any[] = [];
  
  isLoading = false;
  errorMessage = '';

  constructor(
    private userService: UserService,
    private companyService: CompanyService
  ) {}

  ngOnInit() {
    this.loadUsers();
    this.loadCompanies();
    this.loadStats();
  }

  loadUsers() {
    this.isLoading = true;
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.applyFilters();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des utilisateurs';
        this.isLoading = false;
      }
    });
  }

  loadCompanies() {
    this.companyService.getCompanies().subscribe(data => {
      this.companies = data;
    });
  }

  loadStats() {
    this.userService.getUserStats().subscribe(data => {
      this.userStats = data;
    });
  }

  applyFilters() {
    this.filteredUsers = this.users.filter(user => {
      const matchesSearch = !this.searchTerm || 
        user.firstName.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        user.lastName.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(this.searchTerm.toLowerCase());
      
      const matchesRole = !this.selectedRole || user.role === this.selectedRole;
      const matchesStatus = !this.selectedStatus || 
        (this.selectedStatus === 'active' && user.isActive) ||
        (this.selectedStatus === 'inactive' && !user.isActive);
      const matchesCompany = !this.selectedCompany || user.companyId?.toString() === this.selectedCompany;

      return matchesSearch && matchesRole && matchesStatus && matchesCompany;
    });

    this.currentPage = 1;
    this.calculatePagination();
  }

  resetFilters() {
    this.searchTerm = '';
    this.selectedRole = '';
    this.selectedStatus = '';
    this.selectedCompany = '';
    this.applyFilters();
  }

  calculatePagination() {
    this.totalPages = Math.ceil(this.filteredUsers.length / this.itemsPerPage);
    this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
  }

  getPaginatedUsers(): User[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    return this.filteredUsers.slice(start, end);
  }

  changePage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  getRoleLabel(role: string): string {
    const roleObj = this.roles.find(r => r.value === role);
    return roleObj ? roleObj.label : role;
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

  toggleUserStatus(user: User) {
    this.userService.toggleUserStatus(user.id!).subscribe({
      next: (updatedUser) => {
        if (updatedUser) {
          this.loadUsers();
          this.loadStats();
        }
      },
      error: () => {
        alert('Erreur lors du changement de statut');
      }
    });
  }

  deleteUser(id: number) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
      this.userService.deleteUser(id).subscribe({
        next: () => {
          this.loadUsers();
          this.loadStats();
        },
        error: () => {
          alert('Erreur lors de la suppression');
        }
      });
    }
  }

  exportToCSV() {
    const headers = ['ID', 'Prénom', 'Nom', 'Email', 'Rôle', 'Entreprise', 'Statut', 'Dernière connexion'];
    const rows = this.filteredUsers.map(u => [
      u.id,
      u.firstName,
      u.lastName,
      u.email,
      this.getRoleLabel(u.role),
      this.getCompanyName(u.companyId),
      u.isActive ? 'Actif' : 'Inactif',
      u.lastLogin ? new Date(u.lastLogin).toLocaleDateString() : '-'
    ]);
    
    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'utilisateurs.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  }
}