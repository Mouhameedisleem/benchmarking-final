export interface User {
  id?: number;
  username: string;
  email: string;
  password?: string;
  firstName: string;
  lastName: string;
  role: 'ADMIN' | 'CONSULTANT' | 'CLIENT';
  companyId?: number;
  companyName?: string;
  phone?: string;
  isActive: boolean;
  lastLogin?: Date;
  createdAt?: Date;
  updatedAt?: Date;
  createdBy?: number;
}

export interface UserFilters {
  role?: string;
  isActive?: boolean;
  companyId?: number;
  search?: string;
}

export interface UserStats {
  total: number;
  active: number;
  inactive: number;
  byRole: {
    ADMIN: number;
    CONSULTANT: number;
    CLIENT: number;
  };
}

export const USER_ROLES = [
  { value: 'ADMIN', label: 'Administrateur', description: 'Accès complet au système' },
  { value: 'CONSULTANT', label: 'Consultant', description: 'Peut gérer évaluations et entreprises' },
  { value: 'CLIENT', label: 'Client (Entreprise)', description: 'Accès limité à son entreprise' }
];