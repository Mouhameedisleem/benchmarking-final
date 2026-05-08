export interface Company {
  id?: number;
  name: string;
  sector: string;
  country: string;
  size: 'TPE' | 'PME' | 'ETI' | 'GE';
  activityDomain: string;
  website?: string;
  phone?: string;
  email?: string;
  address?: string;
  consultantId?: number;
  consultantName?: string;
  createdAt?: Date;
  updatedAt?: Date;
}

// AJOUT : Interface pour l'inscription
export interface CompanyRegistration {
  companyName: string;
  sector: string;
  country: string;
  size: 'TPE' | 'PME' | 'ETI' | 'GE';
  activityDomain: string;
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
}

export interface Sector {
  id: string;
  name: string;
  icon?: string;
}

export interface Country {
  code: string;
  name: string;
  flag?: string;
}