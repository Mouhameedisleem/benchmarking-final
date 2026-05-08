export interface Recommendation {
  id: number;
  evaluationId: number;
  type: 'METIER' | 'PROCESSUS' | 'SI';
  content: string;
  priority: 'HAUTE' | 'MOYENNE' | 'BASSE';
}