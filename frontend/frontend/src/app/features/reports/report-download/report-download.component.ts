import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-report-download',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container py-4">
      <h2>Télécharger le rapport</h2>
      <button class="btn btn-primary" (click)="downloadReport()">
        <i class="fas fa-download me-2"></i>Télécharger PDF
      </button>
    </div>
  `
})
export class ReportDownloadComponent {
  downloadReport() {
    alert('Téléchargement du rapport...');
  }
}