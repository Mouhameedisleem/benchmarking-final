export interface Score {
  evaluationId: number;
  globalScore: number;
  scoresByAxis: {
    METIER: number;
    PROCESSUS: number;
    SI: number;
  };
  maturityLevel: 'INITIAL' | 'BASIQUE' | 'INTERMEDIAIRE' | 'AVANCE' | 'OPTIMISE';
}