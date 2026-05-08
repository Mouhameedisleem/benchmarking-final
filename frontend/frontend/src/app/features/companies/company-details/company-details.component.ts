import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CompanyService } from '../../../core/services/company.service';
import { AuthService } from '../../../core/services/auth.service';
import { Company } from '../../../core/models/company.model';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-company-details',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './company-details.component.html',
  styleUrls: ['./company-details.component.css']
})
export class CompanyDetailsComponent implements OnInit {
  company: Company | null = null;
  isLoading = true;
  errorMessage = '';

  sectors: any[] = [];
  countries: any[] = [];

  questionnaireId: number | null = null;
  regenerating = false;
  regenerateSuccess = '';
  regenerateError = '';

  get isConsultantOrAdmin(): boolean {
    const role = this.authService.getCurrentUser()?.role;
    return role === 'ADMIN' || role === 'CONSULTANT';
  }

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private companyService: CompanyService,
    private authService: AuthService,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.loadFilterData();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadCompany(+id);
    } else {
      this.errorMessage = 'ID entreprise manquant';
      this.isLoading = false;
    }
  }

  loadFilterData() {
    this.companyService.getSectors().subscribe(data => this.sectors = data);
    this.companyService.getCountries().subscribe(data => this.countries = data);
  }

  loadCompany(id: number) {
    this.companyService.getCompany(id).subscribe({
      next: (company) => {
        if (company) {
          this.company = company;
          this.loadActiveQuestionnaire(id);
        } else {
          this.errorMessage = 'Entreprise non trouvée';
        }
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement';
        this.isLoading = false;
      }
    });
  }

  private loadActiveQuestionnaire(companyId: number) {
    this.http.get<any[]>(`${environment.apiUrl}/questionnaires?companyId=${companyId}`).subscribe({
      next: (list) => {
        const active = list?.find(q => q.active) ?? list?.[0];
        this.questionnaireId = active?.id ?? null;
      },
      error: () => {}
    });
  }

  regenerateOptions() {
    if (!this.questionnaireId || this.regenerating) return;
    this.regenerating = true;
    this.regenerateSuccess = '';
    this.regenerateError = '';
    this.http.post<any>(`${environment.apiUrl}/questionnaires/${this.questionnaireId}/regenerate-options`, {})
      .subscribe({
        next: () => {
          this.regenerating = false;
          this.regenerateSuccess = 'Options contextualisées générées avec succès.';
        },
        error: (err) => {
          this.regenerating = false;
          this.regenerateError = err?.error?.message || 'Erreur lors de la génération des options.';
        }
      });
  }

  getSectorName(sectorId: string): string {
    const sector = this.sectors.find(s => s.id === sectorId);
    return sector ? `${sector.icon || ''} ${sector.name}` : sectorId;
  }

  getCountryFlag(countryCode: string): string {
    const country = this.countries.find(c => c.code === countryCode);
    return country ? country.flag || '🌍' : '🌍';
  }

  getCountryName(countryCode: string): string {
    const country = this.countries.find(c => c.code === countryCode);
    return country ? country.name : countryCode;
  }

  getSizeClass(size: string): string {
    const classes: any = {
      'TPE': 'bg-secondary',
      'PME': 'bg-primary',
      'ETI': 'bg-warning text-dark',
      'GE': 'bg-success'
    };
    return classes[size] || 'bg-secondary';
  }

  getSizeDescription(size: string): string {
    const option = this.companyService.getSizeOptions().find(opt => opt.value === size);
    return option ? option.description : '';
  }

  editCompany() {
    if (this.company?.id) {
      this.router.navigate(['/companies', this.company.id, 'edit']);
    }
  }

  deleteCompany() {
    if (this.company?.id && confirm('Êtes-vous sûr de vouloir supprimer cette entreprise ?')) {
      this.companyService.deleteCompany(this.company.id).subscribe({
        next: () => this.router.navigate(['/companies']),
        error: (err) => {
          this.errorMessage = err?.error?.message || 'Erreur lors de la suppression';
        }
      });
    }
  }

  goBack() {
    this.router.navigate(['/companies']);
  }

  startEvaluation() {
    if (this.company?.id) {
      this.router.navigate(['/evaluations/new'], {
        queryParams: { companyId: this.company.id }
      });
    }
  }
}
