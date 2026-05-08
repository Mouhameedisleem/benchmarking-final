import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, Router, NavigationEnd } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, distinctUntilChanged, of } from 'rxjs';
import { AuthService } from '../../services/auth.service';  // Correction du chemin
import { User } from '../../models/user.model';  // Correction du chemin
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  currentUser: User | null = null;
  currentDate = new Date();
  breadcrumbs: { label: string; url: string }[] = [];
  isMenuOpen = false;
  questionnaireCompleted = false;

  notifications: { title: string; subtitle: string; icon: string; iconBg: string }[] = [];

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) {
    // S'abonner aux changements d'utilisateur
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Générer le breadcrumb à chaque changement de route
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.generateBreadcrumbs();
      }
    });
  }

  ngOnInit(): void {
    this.generateBreadcrumbs();
    this.authService.currentUser$.pipe(
      distinctUntilChanged((a, b) => a?.id === b?.id && a?.role === b?.role)
    ).subscribe(user => {
      if (user && (user.role === 'ADMIN' || user.role === 'CONSULTANT')) {
        this.loadNotifications();
      } else {
        this.notifications = [];
      }
      if (user?.role === 'CLIENT' && user?.companyId) {
        this.http.get<any>(`${environment.apiUrl}/evaluations/latest?companyId=${user.companyId}`)
          .pipe(catchError(() => of(null)))
          .subscribe(ev => { this.questionnaireCompleted = !!ev?.evaluationId; });
      } else {
        this.questionnaireCompleted = false;
      }
    });
  }

  private loadNotifications(): void {
    this.notifications = [
      {
        title: 'Nouvel utilisateur inscrit',
        subtitle: 'En attente de validation',
        icon: 'fas fa-user-plus text-warning',
        iconBg: 'bg-warning bg-opacity-10'
      },
      {
        title: 'Évaluation soumise',
        subtitle: 'À traiter dès que possible',
        icon: 'fas fa-clipboard-check text-success',
        iconBg: 'bg-success bg-opacity-10'
      },
      {
        title: 'Rapport disponible',
        subtitle: 'Prêt à être téléchargé',
        icon: 'fas fa-file-pdf text-primary',
        iconBg: 'bg-primary bg-opacity-10'
      }
    ];
  }

  /**
   * Vérifie si l'utilisateur est authentifié
   */
  isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }

  /**
   * Vérifie si l'utilisateur a un rôle spécifique
   */
  hasRole(role: string | string[]): boolean {
    return this.authService.hasRole(role);
  }

  /**
   * Déconnexion
   */
  logout(event: Event): void {
    event.preventDefault();
    this.authService.logout();
  }

  /**
   * Obtient le libellé du rôle de l'utilisateur
   */
  getRoleLabel(): string {
    if (!this.currentUser) return '';
    
    const roles: { [key: string]: string } = {
      'ADMIN': 'Administrateur',
      'CONSULTANT': 'Consultant',
      'CLIENT': 'Client'
    };
    return roles[this.currentUser.role] || this.currentUser.role;
  }

  /**
   * Obtient la classe CSS pour le badge du rôle
   */
  getRoleBadgeClass(): string {
    if (!this.currentUser) return '';
    
    const classes: { [key: string]: string } = {
      'ADMIN': 'bg-danger',
      'CONSULTANT': 'bg-primary',
      'CLIENT': 'bg-success'
    };
    return classes[this.currentUser.role] || 'bg-secondary';
  }

  /**
   * Vérifie si l'utilisateur a une entreprise associée
   */
  hasCompany(): boolean {
    return !!(this.currentUser?.companyId);
  }

  /**
   * Obtient l'ID de l'entreprise de l'utilisateur
   */
  getCompanyId(): number | null {
    return this.currentUser?.companyId || null;
  }

  /**
   * Génère le fil d'Ariane (breadcrumb) basé sur l'URL actuelle
   */
  private generateBreadcrumbs(): void {
    const urlParts = this.router.url.split('/').filter(part => part && part !== '');
    this.breadcrumbs = [];
    
    // Toujours ajouter l'accueil
    this.breadcrumbs.push({
      label: 'Accueil',
      url: this.getHomeRoute()
    });

    let currentUrl = '';
    urlParts.forEach((part, index) => {
      currentUrl += `/${part}`;
      
      // Ignorer les IDs numériques (ex: /companies/1)
      if (part.match(/^\d+$/)) {
        return;
      }

      let label = this.formatBreadcrumbLabel(part);
      
      // Cas spéciaux
      if (part === 'admin' && index === 0) label = 'Administration';
      if (part === 'consultant' && index === 0) label = 'Consultant';
      if (part === 'client' && index === 0) label = 'Client';
      if (part === 'dashboard') label = 'Dashboard';
      if (part === 'companies') label = 'Entreprises';
      if (part === 'questions') label = 'Questions';
      if (part === 'users') label = 'Utilisateurs';
      if (part === 'reports') label = 'Rapports';
      if (part === 'powerbi') label = 'Power BI';
      if (part === 'new') label = 'Nouveau';
      if (part === 'edit') label = 'Modifier';

      this.breadcrumbs.push({
        label: label,
        url: currentUrl
      });
    });
  }

  /**
   * Formate un segment d'URL en libellé lisible
   */
  private formatBreadcrumbLabel(part: string): string {
    // Remplacer les tirets par des espaces et mettre la première lettre en majuscule
    return part
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  /**
   * Obtient la route d'accueil en fonction du rôle
   */
  private getHomeRoute(): string {
    if (!this.currentUser) return '/';
    
    switch (this.currentUser.role) {
      case 'ADMIN':
        return '/admin/dashboard';
      case 'CONSULTANT':
        return '/consultant/dashboard';
      case 'CLIENT':
        return '/client/dashboard';
      default:
        return '/';
    }
  }

  /**
   * Bascule le menu mobile
   */
  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  /**
   * Ferme le menu mobile
   */
  closeMenu(): void {
    this.isMenuOpen = false;
  }

  /**
   * Vérifie si un lien est actif
   */
  isLinkActive(url: string): boolean {
    return this.router.url.includes(url);
  }

  /**
   * Obtient les initiales de l'utilisateur pour l'avatar
   */
  getUserInitials(): string {
    if (!this.currentUser) return 'U';
    
    const first = this.currentUser.firstName?.charAt(0) || '';
    const last = this.currentUser.lastName?.charAt(0) || '';
    
    if (first && last) {
      return (first + last).toUpperCase();
    }
    return this.currentUser.username?.charAt(0).toUpperCase() || 'U';
  }

  /**
   * Obtient le nom complet de l'utilisateur
   */
  getFullName(): string {
    if (!this.currentUser) return 'Utilisateur';
    
    if (this.currentUser.firstName && this.currentUser.lastName) {
      return `${this.currentUser.firstName} ${this.currentUser.lastName}`;
    }
    return this.currentUser.username || 'Utilisateur';
  }
}