import { Routes } from '@angular/router';
import { LandingComponent } from './features/landing/landing.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent }from './features/auth/register/register.component';
import { ProfileComponent } from './features/profile/profile.component';
import { SettingsComponent } from './features/settings/settings.component';
import { HelpComponent } from './features/help/help.component';

// Dashboards
import { AdminDashboardComponent } from './features/dashboard/admin-dashboard/admin-dashboard.component';
import { ConsultantDashboardComponent } from './features/dashboard/consultant-dashboard/consultant-dashboard.component';
import { ConsultantAnalysisComponent } from './features/dashboard/consultant-analysis/consultant-analysis.component';
import { ConsultantFrameworksComponent } from './features/dashboard/consultant-frameworks/consultant-frameworks.component';
import { ClientDashboardComponent } from './features/dashboard/client-dashboard/client-dashboard.component';

// Companies
import { CompanyListComponent } from './features/companies/company-list/company-list.component';
import { CompanyFormComponent } from './features/companies/company-form/company-form.component';
import { CompanyDetailsComponent } from './features/companies/company-details/company-details.component';
import { CompanySetupComponent } from './features/companies/company-setup/company-setup.component';
import { CompanyQuestionnaireComponent } from './features/companies/company-questionnaire/company-questionnaire.component';

// Questions
import { QuestionListComponent } from './features/questionnaire/question-list/question-list.component';
import { QuestionFormComponent } from './features/questionnaire/question-form/question-form.component';
import { ClientQuestionnaireComponent } from './features/questionnaire/client-questionnaire/client-questionnaire.component';

// Users
import { UserListComponent } from './features/users/user-list/user-list.component';
import { UserFormComponent } from './features/users/user-form/user-form.component';
import { UserDetailsComponent } from './features/users/user-details/user-details.component';

// Results & Reports
import { ScoreResultComponent } from './features/results/score-result/score-result.component';
import { ReportGeneratorComponent } from './features/reports/report-generator/report-generator.component';
import { ConsultantReviewComponent } from './features/evaluations/consultant-review/consultant-review.component';

// Guards
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  // Public routes
  { path: 'home', component: LandingComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  
  // Admin routes
  { 
    path: 'admin/dashboard', 
    component: AdminDashboardComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN'] }
  },
  
  // Consultant routes
  {
    path: 'consultant/dashboard',
    component: ConsultantDashboardComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CONSULTANT'] }
  },
  {
    path: 'consultant/evaluations/:id/review',
    component: ConsultantReviewComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  {
    path: 'consultant/analysis',
    component: ConsultantAnalysisComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CONSULTANT', 'ADMIN'] }
  },
  {
    path: 'consultant/frameworks',
    component: ConsultantFrameworksComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CONSULTANT', 'ADMIN'] }
  },
  
  // Client routes
  {
    path: 'client/dashboard',
    component: ClientDashboardComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CLIENT'] }
  },
  {
    path: 'client/questionnaire',
    component: ClientQuestionnaireComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CLIENT'] }
  },
  
  // Company routes (Admin & Consultant)
  { 
    path: 'companies', 
    component: CompanyListComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  { 
    path: 'companies/new', 
    component: CompanyFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  { 
    path: 'companies/:id', 
    component: CompanyDetailsComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT', 'CLIENT'] }
  },
  {
    path: 'companies/:id/edit',
    component: CompanyFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  {
    path: 'companies/:id/setup',
    component: CompanySetupComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  {
    path: 'companies/:id/questionnaire',
    component: CompanyQuestionnaireComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  
  // Question routes (Admin & Consultant)
  { 
    path: 'questions', 
    component: QuestionListComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  { 
    path: 'questions/new', 
    component: QuestionFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  { 
    path: 'questions/:id/edit', 
    component: QuestionFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  
  // User routes (Admin only)
  { 
    path: 'users', 
    component: UserListComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN'] }
  },
  { 
    path: 'users/new', 
    component: UserFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN'] }
  },
  { 
    path: 'users/:id', 
    component: UserDetailsComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN'] }
  },
  { 
    path: 'users/:id/edit', 
    component: UserFormComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN'] }
  },
  
  // Results routes (accessible by all authenticated users)
  { 
    path: 'results/:evaluationId', 
    component: ScoreResultComponent,
    canActivate: [AuthGuard],
    data: { roles: ['ADMIN', 'CONSULTANT', 'CLIENT'] }
  },
  
  // Reports routes (Admin & Consultant)
  { 
    path: 'reports', 
    component: ReportGeneratorComponent,
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  
  // Client specific routes (avec lazy loading)
  { 
    path: 'client/score', 
    loadComponent: () => import('./features/reports/score-view/score-view.component')
      .then(m => m.ScoreViewComponent),
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CLIENT'] }
  },
  { 
    path: 'client/report', 
    loadComponent: () => import('./features/reports/report-download/report-download.component')
      .then(m => m.ReportDownloadComponent),
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['CLIENT'] }
  },
  
  // Power BI Dashboard (Admin & Consultant)
  { 
    path: 'powerbi', 
    loadComponent: () => import('./features/reports/powerbi-dashboard/powerbi-dashboard.component')
      .then(m => m.PowerbiDashboardComponent),
    canActivate: [AuthGuard, RoleGuard],
    data: { roles: ['ADMIN', 'CONSULTANT'] }
  },
  
  // Profile, Settings, Help (all authenticated users)
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: 'help', component: HelpComponent, canActivate: [AuthGuard] },

  // Redirects
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: '**', redirectTo: '/home' }
];