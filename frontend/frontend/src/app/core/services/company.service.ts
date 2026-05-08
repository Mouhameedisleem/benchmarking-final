import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Company, Sector, Country } from '../models/company.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class CompanyService {
  private readonly apiUrl = `${environment.apiUrl}/companies`;

  private sectors: Sector[] = [
    { id: 'banking', name: 'Banque', icon: '🏦' },
    { id: 'insurance', name: 'Assurance', icon: '🛡️' },
    { id: 'industry', name: 'Industrie', icon: '🏭' },
    { id: 'retail', name: 'Commerce', icon: '🛒' },
    { id: 'healthcare', name: 'Santé', icon: '🏥' },
    { id: 'education', name: 'Éducation', icon: '📚' },
    { id: 'tech', name: 'Technologies', icon: '💻' },
    { id: 'transport', name: 'Transport', icon: '🚚' },
    { id: 'energy', name: 'Énergie', icon: '⚡' },
    { id: 'construction', name: 'Construction', icon: '🏗️' }
  ];

  private countries: Country[] = [
    { code: 'FR', name: 'France', flag: '🇫🇷' },
    { code: 'BE', name: 'Belgique', flag: '🇧🇪' },
    { code: 'CH', name: 'Suisse', flag: '🇨🇭' },
    { code: 'LU', name: 'Luxembourg', flag: '🇱🇺' },
    { code: 'MC', name: 'Monaco', flag: '🇲🇨' },
    { code: 'CA', name: 'Canada', flag: '🇨🇦' },
    { code: 'MA', name: 'Maroc', flag: '🇲🇦' },
    { code: 'TN', name: 'Tunisie', flag: '🇹🇳' },
    { code: 'DZ', name: 'Algérie', flag: '🇩🇿' },
    { code: 'SN', name: 'Sénégal', flag: '🇸🇳' }
  ];

  private sizeOptions = [
    { value: 'TPE', label: 'TPE', description: '< 10 salariés' },
    { value: 'PME', label: 'PME', description: '10-250 salariés' },
    { value: 'ETI', label: 'ETI', description: '250-5000 salariés' },
    { value: 'GE', label: 'GE', description: '> 5000 salariés' }
  ];

  constructor(private http: HttpClient) {}

  getCompanies(): Observable<Company[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map(list => list.map(c => this.mapCompany(c)))
    );
  }

  getCompany(id: number): Observable<Company> {
    return this.http.get<any>(`${this.apiUrl}/${id}`).pipe(
      map(c => this.mapCompany(c))
    );
  }

  addCompany(company: Company): Observable<Company> {
    return this.http.post<any>(this.apiUrl, this.mapToRequest(company)).pipe(
      map(c => this.mapCompany(c))
    );
  }

  updateCompany(id: number, data: Partial<Company>): Observable<Company> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, this.mapToRequest(data as Company)).pipe(
      map(c => this.mapCompany(c))
    );
  }

  deleteCompany(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  getSectors(): Observable<Sector[]> {
    return of(this.sectors);
  }

  getCountries(): Observable<Country[]> {
    return of(this.countries);
  }

  getSizeOptions(): { value: string; label: string; description: string }[] {
    return this.sizeOptions;
  }

  private mapCompany(c: any): Company {
    return {
      id: c.id,
      name: c.name,
      sector: c.sector,
      country: c.country,
      size: c.size,
      activityDomain: c.businessDomain,
      website: c.website,
      phone: c.phone,
      email: c.email,
      address: c.address,
      consultantId: c.consultantId,
      consultantName: c.consultantName,
      createdAt: c.createdAt ? new Date(c.createdAt) : undefined,
      updatedAt: c.updatedAt ? new Date(c.updatedAt) : undefined
    };
  }

  private mapToRequest(c: Company) {
    return {
      name: c.name,
      sector: c.sector,
      country: c.country,
      size: c.size,
      businessDomain: c.activityDomain,
      website: c.website,
      phone: c.phone,
      email: c.email,
      address: c.address,
      consultantId: c.consultantId ?? null
    };
  }
}
