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
    // ── Afrique du Nord ──────────────────────────────────────────────────────
    { code: 'DZ', name: 'Algérie',       flag: '🇩🇿' },
    { code: 'EG', name: 'Égypte',        flag: '🇪🇬' },
    { code: 'LY', name: 'Libye',         flag: '🇱🇾' },
    { code: 'MA', name: 'Maroc',         flag: '🇲🇦' },
    { code: 'MR', name: 'Mauritanie',    flag: '🇲🇷' },
    { code: 'SD', name: 'Soudan',        flag: '🇸🇩' },
    { code: 'TN', name: 'Tunisie',       flag: '🇹🇳' },
    // ── Afrique subsaharienne ────────────────────────────────────────────────
    { code: 'AO', name: 'Angola',        flag: '🇦🇴' },
    { code: 'BJ', name: 'Bénin',         flag: '🇧🇯' },
    { code: 'BF', name: 'Burkina Faso',  flag: '🇧🇫' },
    { code: 'BI', name: 'Burundi',       flag: '🇧🇮' },
    { code: 'CM', name: 'Cameroun',      flag: '🇨🇲' },
    { code: 'CV', name: 'Cap-Vert',      flag: '🇨🇻' },
    { code: 'CF', name: 'Centrafrique',  flag: '🇨🇫' },
    { code: 'KM', name: 'Comores',       flag: '🇰🇲' },
    { code: 'CG', name: 'Congo',         flag: '🇨🇬' },
    { code: 'CD', name: 'RD Congo',      flag: '🇨🇩' },
    { code: 'CI', name: "Côte d'Ivoire", flag: '🇨🇮' },
    { code: 'DJ', name: 'Djibouti',      flag: '🇩🇯' },
    { code: 'ER', name: 'Érythrée',      flag: '🇪🇷' },
    { code: 'ET', name: 'Éthiopie',      flag: '🇪🇹' },
    { code: 'GA', name: 'Gabon',         flag: '🇬🇦' },
    { code: 'GM', name: 'Gambie',        flag: '🇬🇲' },
    { code: 'GH', name: 'Ghana',         flag: '🇬🇭' },
    { code: 'GN', name: 'Guinée',        flag: '🇬🇳' },
    { code: 'GW', name: 'Guinée-Bissau', flag: '🇬🇼' },
    { code: 'GQ', name: 'Guinée équatoriale', flag: '🇬🇶' },
    { code: 'KE', name: 'Kenya',         flag: '🇰🇪' },
    { code: 'LS', name: 'Lesotho',       flag: '🇱🇸' },
    { code: 'LR', name: 'Liberia',       flag: '🇱🇷' },
    { code: 'MG', name: 'Madagascar',    flag: '🇲🇬' },
    { code: 'MW', name: 'Malawi',        flag: '🇲🇼' },
    { code: 'ML', name: 'Mali',          flag: '🇲🇱' },
    { code: 'MZ', name: 'Mozambique',    flag: '🇲🇿' },
    { code: 'NA', name: 'Namibie',       flag: '🇳🇦' },
    { code: 'NE', name: 'Niger',         flag: '🇳🇪' },
    { code: 'NG', name: 'Nigeria',       flag: '🇳🇬' },
    { code: 'UG', name: 'Ouganda',       flag: '🇺🇬' },
    { code: 'RW', name: 'Rwanda',        flag: '🇷🇼' },
    { code: 'SN', name: 'Sénégal',       flag: '🇸🇳' },
    { code: 'SC', name: 'Seychelles',    flag: '🇸🇨' },
    { code: 'SL', name: 'Sierra Leone',  flag: '🇸🇱' },
    { code: 'SO', name: 'Somalie',       flag: '🇸🇴' },
    { code: 'SS', name: 'Soudan du Sud', flag: '🇸🇸' },
    { code: 'ZA', name: 'Afrique du Sud',flag: '🇿🇦' },
    { code: 'TZ', name: 'Tanzanie',      flag: '🇹🇿' },
    { code: 'TD', name: 'Tchad',         flag: '🇹🇩' },
    { code: 'TG', name: 'Togo',          flag: '🇹🇬' },
    { code: 'ZM', name: 'Zambie',        flag: '🇿🇲' },
    { code: 'ZW', name: 'Zimbabwe',      flag: '🇿🇼' },
    // ── Moyen-Orient ────────────────────────────────────────────────────────
    { code: 'SA', name: 'Arabie saoudite', flag: '🇸🇦' },
    { code: 'BH', name: 'Bahreïn',        flag: '🇧🇭' },
    { code: 'AE', name: 'Émirats arabes unis', flag: '🇦🇪' },
    { code: 'IQ', name: 'Irak',           flag: '🇮🇶' },
    { code: 'IR', name: 'Iran',           flag: '🇮🇷' },
    { code: 'IL', name: 'Israël',         flag: '🇮🇱' },
    { code: 'JO', name: 'Jordanie',       flag: '🇯🇴' },
    { code: 'KW', name: 'Koweït',         flag: '🇰🇼' },
    { code: 'LB', name: 'Liban',          flag: '🇱🇧' },
    { code: 'OM', name: 'Oman',           flag: '🇴🇲' },
    { code: 'QA', name: 'Qatar',          flag: '🇶🇦' },
    { code: 'SY', name: 'Syrie',          flag: '🇸🇾' },
    { code: 'TR', name: 'Turquie',        flag: '🇹🇷' },
    { code: 'YE', name: 'Yémen',          flag: '🇾🇪' },
    // ── Europe occidentale ───────────────────────────────────────────────────
    { code: 'DE', name: 'Allemagne',      flag: '🇩🇪' },
    { code: 'AD', name: 'Andorre',        flag: '🇦🇩' },
    { code: 'AT', name: 'Autriche',       flag: '🇦🇹' },
    { code: 'BE', name: 'Belgique',       flag: '🇧🇪' },
    { code: 'CY', name: 'Chypre',         flag: '🇨🇾' },
    { code: 'DK', name: 'Danemark',       flag: '🇩🇰' },
    { code: 'ES', name: 'Espagne',        flag: '🇪🇸' },
    { code: 'FI', name: 'Finlande',       flag: '🇫🇮' },
    { code: 'FR', name: 'France',         flag: '🇫🇷' },
    { code: 'GR', name: 'Grèce',          flag: '🇬🇷' },
    { code: 'IE', name: 'Irlande',        flag: '🇮🇪' },
    { code: 'IS', name: 'Islande',        flag: '🇮🇸' },
    { code: 'IT', name: 'Italie',         flag: '🇮🇹' },
    { code: 'LI', name: 'Liechtenstein',  flag: '🇱🇮' },
    { code: 'LU', name: 'Luxembourg',     flag: '🇱🇺' },
    { code: 'MT', name: 'Malte',          flag: '🇲🇹' },
    { code: 'MC', name: 'Monaco',         flag: '🇲🇨' },
    { code: 'NO', name: 'Norvège',        flag: '🇳🇴' },
    { code: 'NL', name: 'Pays-Bas',       flag: '🇳🇱' },
    { code: 'PT', name: 'Portugal',       flag: '🇵🇹' },
    { code: 'GB', name: 'Royaume-Uni',    flag: '🇬🇧' },
    { code: 'SE', name: 'Suède',          flag: '🇸🇪' },
    { code: 'CH', name: 'Suisse',         flag: '🇨🇭' },
    // ── Europe centrale & orientale ─────────────────────────────────────────
    { code: 'AL', name: 'Albanie',        flag: '🇦🇱' },
    { code: 'BY', name: 'Biélorussie',    flag: '🇧🇾' },
    { code: 'BA', name: 'Bosnie-Herzégovine', flag: '🇧🇦' },
    { code: 'BG', name: 'Bulgarie',       flag: '🇧🇬' },
    { code: 'HR', name: 'Croatie',        flag: '🇭🇷' },
    { code: 'EE', name: 'Estonie',        flag: '🇪🇪' },
    { code: 'HU', name: 'Hongrie',        flag: '🇭🇺' },
    { code: 'LV', name: 'Lettonie',       flag: '🇱🇻' },
    { code: 'LT', name: 'Lituanie',       flag: '🇱🇹' },
    { code: 'MK', name: 'Macédoine du Nord', flag: '🇲🇰' },
    { code: 'MD', name: 'Moldavie',       flag: '🇲🇩' },
    { code: 'ME', name: 'Monténégro',     flag: '🇲🇪' },
    { code: 'PL', name: 'Pologne',        flag: '🇵🇱' },
    { code: 'CZ', name: 'République tchèque', flag: '🇨🇿' },
    { code: 'RO', name: 'Roumanie',       flag: '🇷🇴' },
    { code: 'RU', name: 'Russie',         flag: '🇷🇺' },
    { code: 'RS', name: 'Serbie',         flag: '🇷🇸' },
    { code: 'SK', name: 'Slovaquie',      flag: '🇸🇰' },
    { code: 'SI', name: 'Slovénie',       flag: '🇸🇮' },
    { code: 'UA', name: 'Ukraine',        flag: '🇺🇦' },
    // ── Amériques ────────────────────────────────────────────────────────────
    { code: 'AR', name: 'Argentine',      flag: '🇦🇷' },
    { code: 'BO', name: 'Bolivie',        flag: '🇧🇴' },
    { code: 'BR', name: 'Brésil',         flag: '🇧🇷' },
    { code: 'CA', name: 'Canada',         flag: '🇨🇦' },
    { code: 'CL', name: 'Chili',          flag: '🇨🇱' },
    { code: 'CO', name: 'Colombie',       flag: '🇨🇴' },
    { code: 'CR', name: 'Costa Rica',     flag: '🇨🇷' },
    { code: 'CU', name: 'Cuba',           flag: '🇨🇺' },
    { code: 'EC', name: 'Équateur',       flag: '🇪🇨' },
    { code: 'US', name: 'États-Unis',     flag: '🇺🇸' },
    { code: 'MX', name: 'Mexique',        flag: '🇲🇽' },
    { code: 'PA', name: 'Panama',         flag: '🇵🇦' },
    { code: 'PY', name: 'Paraguay',       flag: '🇵🇾' },
    { code: 'PE', name: 'Pérou',          flag: '🇵🇪' },
    { code: 'DO', name: 'République dominicaine', flag: '🇩🇴' },
    { code: 'UY', name: 'Uruguay',        flag: '🇺🇾' },
    { code: 'VE', name: 'Venezuela',      flag: '🇻🇪' },
    // ── Asie ─────────────────────────────────────────────────────────────────
    { code: 'CN', name: 'Chine',          flag: '🇨🇳' },
    { code: 'KR', name: 'Corée du Sud',   flag: '🇰🇷' },
    { code: 'IN', name: 'Inde',           flag: '🇮🇳' },
    { code: 'ID', name: 'Indonésie',      flag: '🇮🇩' },
    { code: 'JP', name: 'Japon',          flag: '🇯🇵' },
    { code: 'KZ', name: 'Kazakhstan',     flag: '🇰🇿' },
    { code: 'MY', name: 'Malaisie',       flag: '🇲🇾' },
    { code: 'MN', name: 'Mongolie',       flag: '🇲🇳' },
    { code: 'NP', name: 'Népal',          flag: '🇳🇵' },
    { code: 'PK', name: 'Pakistan',       flag: '🇵🇰' },
    { code: 'PH', name: 'Philippines',    flag: '🇵🇭' },
    { code: 'SG', name: 'Singapour',      flag: '🇸🇬' },
    { code: 'LK', name: 'Sri Lanka',      flag: '🇱🇰' },
    { code: 'TH', name: 'Thaïlande',      flag: '🇹🇭' },
    { code: 'VN', name: 'Viêt Nam',       flag: '🇻🇳' },
    // ── Océanie ──────────────────────────────────────────────────────────────
    { code: 'AU', name: 'Australie',      flag: '🇦🇺' },
    { code: 'NZ', name: 'Nouvelle-Zélande', flag: '🇳🇿' },
  ].sort((a, b) => a.name.localeCompare(b.name, 'fr', { sensitivity: 'base' }));

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
