import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { User } from '../models/user.model';
import { CompanyRegistration } from '../models/company.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly apiUrl = `${environment.apiUrl}/auth`;

  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {
    this.loadStoredUser();
  }

  private loadStoredUser() {
    const token = localStorage.getItem('token');
    const stored = localStorage.getItem('currentUser');
    if (stored && token && !this.isTokenExpired(token)) {
      this.currentUserSubject.next(JSON.parse(stored));
    } else {
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
    }
  }

  isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, { email, password }).pipe(
      tap(res => this.storeSession(res))
    );
  }

  register(data: CompanyRegistration): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register-company`, data).pipe(
      tap(res => this.storeSession(res))
    );
  }

  registerConsultant(data: { firstName: string; lastName: string; email: string; password: string; phone?: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register-consultant`, data).pipe(
      tap(res => this.storeSession(res))
    );
  }

  logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    if (!token || this.isTokenExpired(token)) {
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
      this.currentUserSubject.next(null);
      return false;
    }
    return !!this.currentUserSubject.value;
  }

  hasRole(role: string | string[]): boolean {
    const user = this.currentUserSubject.value;
    if (!user) return false;
    return Array.isArray(role) ? role.includes(user.role) : user.role === role;
  }

  refreshProfile(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/me`).pipe(
      tap(res => this.storeSession(res))
    );
  }

  changePassword(currentPassword: string, newPassword: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/change-password`, { currentPassword, newPassword });
  }

  forgotPassword(email: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/forgot-password`, { email });
  }

  resetPassword(email: string, code: string, newPassword: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/reset-password`, { email, code, newPassword });
  }

  private storeSession(res: any) {
    const user: User = {
      id: res.id,
      username: res.username,
      email: res.email,
      firstName: res.firstName,
      lastName: res.lastName,
      role: res.role,
      companyId: res.companyId,
      companyName: res.companyName,
      isActive: true
    };
    if (res.token) {
      localStorage.setItem('token', res.token);
    }
    localStorage.setItem('currentUser', JSON.stringify(user));
    this.currentUserSubject.next(user);
  }
}
