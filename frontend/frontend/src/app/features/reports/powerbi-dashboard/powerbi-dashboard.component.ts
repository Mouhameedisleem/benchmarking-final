import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-powerbi-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container py-4">
      <h2>Dashboard Power BI</h2>
      <div class="alert alert-info">
        <i class="fas fa-info-circle me-2"></i>
        Intégration Power BI à venir
      </div>
    </div>
  `
})
export class PowerbiDashboardComponent {}