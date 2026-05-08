import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-help',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container py-4" style="max-width: 800px;">
      <div class="d-flex align-items-center mb-4">
        <button class="btn btn-outline-secondary btn-sm me-3" onclick="history.back()">
          <i class="fas fa-arrow-left me-1"></i>Retour
        </button>
        <h3 class="mb-0">Centre d'aide</h3>
      </div>

      <!-- Quick links -->
      <div class="row g-3 mb-4">
        <div class="col-md-4" *ngIf="isAdmin()">
          <div class="card border-0 shadow-sm text-center p-3 h-100">
            <i class="fas fa-building fa-2x text-primary mb-2"></i>
            <h6>Gérer les entreprises</h6>
            <small class="text-muted">Ajouter, modifier, supprimer des entreprises</small>
            <a routerLink="/companies" class="btn btn-outline-primary btn-sm mt-2">Accéder</a>
          </div>
        </div>
        <div class="col-md-4" *ngIf="isAdmin()">
          <div class="card border-0 shadow-sm text-center p-3 h-100">
            <i class="fas fa-users fa-2x text-success mb-2"></i>
            <h6>Gérer les utilisateurs</h6>
            <small class="text-muted">Créer et gérer les comptes utilisateurs</small>
            <a routerLink="/users" class="btn btn-outline-success btn-sm mt-2">Accéder</a>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm text-center p-3 h-100">
            <i class="fas fa-user-cog fa-2x text-secondary mb-2"></i>
            <h6>Mon compte</h6>
            <small class="text-muted">Profil et paramètres personnels</small>
            <a routerLink="/profile" class="btn btn-outline-secondary btn-sm mt-2">Accéder</a>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white fw-semibold py-3">
          <i class="fas fa-question-circle me-2 text-info"></i>Questions fréquentes
        </div>
        <div class="card-body p-0">
          <div class="accordion accordion-flush" id="faqAccordion">

            <div class="accordion-item" *ngIf="isAdmin()">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed fw-semibold" type="button"
                        data-bs-toggle="collapse" data-bs-target="#faq1">
                  Comment créer un nouvel utilisateur ?
                </button>
              </h2>
              <div id="faq1" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body text-muted">
                  Allez dans <strong>Utilisateurs → Nouvel utilisateur</strong> via la barre de navigation ou le dashboard.
                  Remplissez les champs requis (nom, email, mot de passe, rôle) puis cliquez sur <em>Créer</em>.
                </div>
              </div>
            </div>

            <div class="accordion-item" *ngIf="isAdmin()">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed fw-semibold" type="button"
                        data-bs-toggle="collapse" data-bs-target="#faq2">
                  Comment associer un utilisateur à une entreprise ?
                </button>
              </h2>
              <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body text-muted">
                  Lors de la création ou de la modification d'un utilisateur, sélectionnez l'entreprise souhaitée
                  dans le champ <em>Entreprise associée</em>.
                </div>
              </div>
            </div>

            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed fw-semibold" type="button"
                        data-bs-toggle="collapse" data-bs-target="#faq3">
                  Comment modifier mon mot de passe ?
                </button>
              </h2>
              <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body text-muted">
                  Allez dans <strong>Paramètres</strong> via le menu en haut à droite (votre nom).
                  Saisissez votre mot de passe actuel, le nouveau mot de passe, et confirmez-le.
                </div>
              </div>
            </div>

            <div class="accordion-item">
              <h2 class="accordion-header">
                <button class="accordion-button collapsed fw-semibold" type="button"
                        data-bs-toggle="collapse" data-bs-target="#faq4">
                  Comment contacter le support ?
                </button>
              </h2>
              <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body text-muted">
                  Pour toute assistance, envoyez un email à
                  <a href="mailto:support&#64;iabenchmark.com">support&#64;iabenchmark.com</a>.
                  Précisez votre rôle et décrivez le problème rencontré.
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  `
})
export class HelpComponent {
  constructor(private authService: AuthService) {}

  isAdmin(): boolean {
    return this.authService.hasRole('ADMIN');
  }
}
