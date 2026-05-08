import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CompanyService } from '../../../core/services/company.service';
import { UserService } from '../../../core/services/user.service';
import { AuthService } from '../../../core/services/auth.service';
import { Company } from '../../../core/models/company.model';

@Component({
  selector: 'app-company-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './company-form.component.html',
  styleUrls: ['./company-form.component.css']
})
export class CompanyFormComponent implements OnInit {
  company: Company = {
    name: '',
    sector: '',
    country: '',
    size: 'PME',
    activityDomain: '',
    website: '',
    phone: '',
    email: '',
    address: '',
    consultantId: undefined
  };

  isEditMode = false;
  companyId: number | null = null;
  isLoading = false;
  errorMessage = '';
  isAdmin = false;

  sectors: any[] = [];
  countries: any[] = [];
  consultants: any[] = [];
  sizeOptions = this.companyService.getSizeOptions();

  constructor(
    private companyService: CompanyService,
    private userService: UserService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.isAdmin = this.authService.getCurrentUser()?.role === 'ADMIN';
    this.loadFilterData();
    this.checkEditMode();
  }

  loadFilterData() {
    this.companyService.getSectors().subscribe(data => this.sectors = data);
    this.companyService.getCountries().subscribe(data => this.countries = data);
    if (this.isAdmin) {
      this.userService.getUsersByRole('CONSULTANT').subscribe(data => this.consultants = data);
    }
  }

  checkEditMode() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.companyId = +id;
      this.loadCompany(this.companyId);
    }
  }

  loadCompany(id: number) {
    this.isLoading = true;
    this.companyService.getCompany(id).subscribe({
      next: (company) => {
        if (company) {
          this.company = company;
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

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = '';

    if (this.isEditMode && this.companyId) {
      // Mise à jour
      this.companyService.updateCompany(this.companyId, this.company).subscribe({
        next: () => {
          this.router.navigate(['/companies', this.companyId]);
        },
        error: () => {
          this.errorMessage = 'Erreur lors de la mise à jour';
          this.isLoading = false;
        }
      });
    } else {
      // Création
      this.companyService.addCompany(this.company).subscribe({
        next: (newCompany) => {
          this.router.navigate(['/companies', newCompany.id, 'setup']);
        },
        error: () => {
          this.errorMessage = "Erreur lors de l'ajout";
          this.isLoading = false;
        }
      });
    }
  }

  cancel() {
    if (this.companyId) {
      this.router.navigate(['/companies', this.companyId]);
    } else {
      this.router.navigate(['/companies']);
    }
  }
}