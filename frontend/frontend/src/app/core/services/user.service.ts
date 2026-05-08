import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { User, UserStats } from '../models/user.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly apiUrl = `${environment.apiUrl}/users`;

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map(users => users.map(u => this.mapUser(u)))
    );
  }

  getUser(id: number): Observable<User> {
    return this.http.get<any>(`${this.apiUrl}/${id}`).pipe(
      map(u => this.mapUser(u))
    );
  }

  addUser(user: User): Observable<User> {
    return this.http.post<any>(this.apiUrl, {
      username: user.username,
      email: user.email,
      password: user.password,
      firstName: user.firstName,
      lastName: user.lastName,
      phone: user.phone,
      role: user.role,
      companyId: user.companyId,
      isActive: user.isActive ?? true
    }).pipe(map(u => this.mapUser(u)));
  }

  updateUser(id: number, userData: Partial<User>): Observable<User> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, {
      username: userData.username,
      email: userData.email,
      firstName: userData.firstName,
      lastName: userData.lastName,
      phone: userData.phone,
      role: userData.role,
      companyId: userData.companyId,
      isActive: userData.isActive
    }).pipe(map(u => this.mapUser(u)));
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  toggleUserStatus(id: number): Observable<User> {
    return this.http.put<any>(`${this.apiUrl}/${id}/status`, {}).pipe(
      map(u => this.mapUser(u))
    );
  }

  getUsersByRole(role: string): Observable<User[]> {
    return this.getUsers().pipe(map(users => users.filter(u => u.role === role)));
  }

  getActiveUsers(): Observable<User[]> {
    return this.getUsers().pipe(map(users => users.filter(u => u.isActive)));
  }

  getInactiveUsers(): Observable<User[]> {
    return this.getUsers().pipe(map(users => users.filter(u => !u.isActive)));
  }

  getUsersByCompany(companyId: number): Observable<User[]> {
    return this.getUsers().pipe(map(users => users.filter(u => u.companyId === companyId)));
  }

  getUserStats(): Observable<UserStats> {
    return this.getUsers().pipe(
      map(users => ({
        total: users.length,
        active: users.filter(u => u.isActive).length,
        inactive: users.filter(u => !u.isActive).length,
        byRole: {
          ADMIN: users.filter(u => u.role === 'ADMIN').length,
          CONSULTANT: users.filter(u => u.role === 'CONSULTANT').length,
          CLIENT: users.filter(u => u.role === 'CLIENT').length
        }
      }))
    );
  }

  searchUsers(query: string): Observable<User[]> {
    const lower = query.toLowerCase();
    return this.getUsers().pipe(
      map(users => users.filter(u =>
        u.firstName.toLowerCase().includes(lower) ||
        u.lastName.toLowerCase().includes(lower) ||
        u.email.toLowerCase().includes(lower) ||
        u.username.toLowerCase().includes(lower)
      ))
    );
  }

  private mapUser(u: any): User {
    return {
      id: u.id,
      username: u.username,
      email: u.email,
      firstName: u.firstName,
      lastName: u.lastName,
      role: u.role,
      companyId: u.companyId,
      companyName: u.companyName,
      phone: u.phone,
      isActive: u.isActive,
      lastLogin: u.lastLogin ? new Date(u.lastLogin) : undefined,
      createdAt: u.createdAt ? new Date(u.createdAt) : undefined,
      updatedAt: u.updatedAt ? new Date(u.updatedAt) : undefined
    };
  }
}
