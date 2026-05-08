export interface Evaluation {
  id: number;
  companyId: number;
  companyName?: string;
  date: Date;
  status: 'IN_PROGRESS' | 'COMPLETED';
}