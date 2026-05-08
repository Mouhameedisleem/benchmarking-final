import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CompanyService } from '../../../core/services/company.service';
import { EvaluationService, EvaluationSummary } from '../../../core/services/evaluation.service';
import { AuthService } from '../../../core/services/auth.service';
import { Company } from '../../../core/models/company.model';

@Component({
  selector: 'app-company-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './company-list.component.html',
  styleUrls: ['./company-list.component.css']
})
export class CompanyListComponent implements OnInit {
  companies: Company[] = [];
  filteredCompanies: Company[] = [];
  evaluationsByCompany = new Map<number, EvaluationSummary>();

  searchTerm = '';
  selectedSector = '';
  selectedCountry = '';
  selectedSize = '';
  Math = Math;

  currentPage = 1;
  itemsPerPage = 10;
  totalPages = 1;
  pages: number[] = [];

  sectors: any[] = [];
  countries: any[] = [];
  sizeOptions = this.companyService.getSizeOptions();

  isLoading = false;
  errorMessage = '';
  isAdmin = false;

  constructor(
    private companyService: CompanyService,
    private evaluationService: EvaluationService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.isAdmin = this.authService.getCurrentUser()?.role === 'ADMIN';
    this.loadCompanies();
    this.loadFilterData();
    if (this.isAdmin) {
      this.loadEvaluations();
    }
  }

  loadCompanies() {
    this.isLoading = true;
    this.companyService.getCompanies().subscribe({
      next: (data) => {
        this.companies = data;
        this.filteredCompanies = [...data];
        this.calculatePagination();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des entreprises';
        this.isLoading = false;
      }
    });
  }

  loadFilterData() {
    this.companyService.getSectors().subscribe(data => this.sectors = data);
    this.companyService.getCountries().subscribe(data => this.countries = data);
  }

  loadEvaluations() {
    this.evaluationService.getAllEvaluations().subscribe({
      next: (evals) => {
        // Keep only the most recent evaluation per company
        evals.forEach(ev => {
          const existing = this.evaluationsByCompany.get(ev.companyId);
          if (!existing || new Date(ev.createdAt) > new Date(existing.createdAt)) {
            this.evaluationsByCompany.set(ev.companyId, ev);
          }
        });
      },
      error: () => { /* silent — score column stays empty */ }
    });
  }

  getLatestScore(companyId: number): EvaluationSummary | undefined {
    return this.evaluationsByCompany.get(companyId);
  }

  getScoreColor(score: number): string {
    return this.evaluationService.getScoreColor(score);
  }

  getMaturityLabel(level: string): string {
    return this.evaluationService.getMaturityLabel(level);
  }

  applyFilters() {
    this.filteredCompanies = this.companies.filter(company => {
      const matchesSearch = !this.searchTerm ||
        company.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        company.activityDomain.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        (company.consultantName ?? '').toLowerCase().includes(this.searchTerm.toLowerCase());

      const matchesSector = !this.selectedSector || company.sector === this.selectedSector;
      const matchesCountry = !this.selectedCountry || company.country === this.selectedCountry;
      const matchesSize = !this.selectedSize || company.size === this.selectedSize;

      return matchesSearch && matchesSector && matchesCountry && matchesSize;
    });

    this.currentPage = 1;
    this.calculatePagination();
  }

  resetFilters() {
    this.searchTerm = '';
    this.selectedSector = '';
    this.selectedCountry = '';
    this.selectedSize = '';
    this.filteredCompanies = [...this.companies];
    this.calculatePagination();
  }

  calculatePagination() {
    this.totalPages = Math.ceil(this.filteredCompanies.length / this.itemsPerPage);
    this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
  }

  getPaginatedCompanies(): Company[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    return this.filteredCompanies.slice(start, end);
  }

  changePage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  deleteCompany(id: number, event: Event) {
    event.stopPropagation();
    if (confirm('Êtes-vous sûr de vouloir supprimer cette entreprise ?')) {
      this.companyService.deleteCompany(id).subscribe({
        next: () => this.loadCompanies(),
        error: () => alert('Erreur lors de la suppression')
      });
    }
  }

  getSectorName(sectorId: string): string {
    const sector = this.sectors.find(s => s.id === sectorId);
    return sector ? `${sector.icon || ''} ${sector.name}` : sectorId;
  }

  getCountryFlag(countryCode: string): string {
    const country = this.countries.find(c => c.code === countryCode);
    return country ? country.flag || '🌍' : '🌍';
  }

  getSizeBadgeClass(size: string): string {
    const classes: Record<string, string> = {
      TPE: 'bg-secondary', PME: 'bg-primary',
      ETI: 'bg-warning text-dark', GE: 'bg-success'
    };
    return classes[size] || 'bg-secondary';
  }

  exportToCSV() {
    const headers = ['Nom', 'Secteur', 'Pays', 'Taille', 'Consultant', 'Score', 'Email', 'Téléphone'];
    const rows = this.filteredCompanies.map(c => {
      const score = this.getLatestScore(c.id!);
      return [
        c.name,
        this.getSectorName(c.sector),
        c.country,
        c.size,
        c.consultantName || '',
        score ? score.globalScore.toFixed(0) : '',
        c.email || '',
        c.phone || ''
      ];
    });

    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'entreprises.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
