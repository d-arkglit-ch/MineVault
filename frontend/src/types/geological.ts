export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  pageNumber: number;
}

export interface FactEvidenceCitation {
  documentId: string;
  documentTitle: string;
  agency: 'MECL' | 'CMPDI' | 'GSI' | 'CIL';
  year: number;
  boundingBox?: BoundingBox;
  sha256Hash: string;
  extractionConfidence?: number | null;
  snippetText?: string;
}

export interface LithologicalInterval {
  fromDepthMeters: number;
  toDepthMeters: number;
  thicknessMeters: number;
  lithologyDescription: string;
  coreRecoveryPercent: number;
  seamCode?: 'SEAM_IX' | 'SEAM_X' | 'INTERBURDEN' | 'ALLUVIUM' | 'SANDSTONE' | 'SHALE';
  sourceBoundingBox?: BoundingBox;
}

export interface ProximateAssay {
  ashPercent: number;
  moisturePercent: number;
  volatileMatterPercent?: number;
  fixedCarbonPercent?: number;
  grossCalorificValueKcal: number;
}

export interface BoreholeCoordinates {
  latitude: string;
  longitude: string;
  collarElevationMsl: number;
  datum: string;
}

export interface BoreholeRecord {
  boreholeId: string;
  coalfield: string;
  sectorBlock: string;
  coordinates: BoreholeCoordinates;
  totalDrilledDepthMeters: number;
  targetSeamThickness: number;
  coalGrade: 'G1' | 'G2' | 'G3' | 'G4' | 'G5' | 'G6' | 'G7' | 'Coking W-IV';
  proximateAssay: ProximateAssay;
  statutoryClearance: 'DGMS_CLEARED' | 'UNDER_JOINT_REVIEW' | 'FLAGGED_DISCREPANCY';
  intervals: LithologicalInterval[];
  evidenceTrail: FactEvidenceCitation[];
  corePhotoUrl?: string;
  discrepancyId?: string;
}

export interface DiscrepancyItem {
  discrepancyId: string;
  boreholeId: string;
  coalfield: string;
  block: string;
  seam: string;
  agencyA: string;
  surveyYearA: number;
  reportedThicknessA: number;
  methodA: string;
  agencyB: string;
  surveyYearB: number;
  reportedThicknessB: number;
  methodB: string;
  thicknessDeltaMeters: number;
  status: 'UNDER_REVIEW' | 'RESOLVED' | 'REJECTED';
  verifiedThicknessMeters?: number;
  reconciliationNotes: string;
  digitalSignatureHash: string;
  auditDocketNo: string;
}

export type ReportModeType = 'EXECUTIVE_SUMMARY' | 'HISTORICAL_TREND' | 'STATUTORY_AUDIT' | 'PQ_FAST_RESPONSE';

export interface GeneratedReportResponse {
  reportId: string;
  title: string;
  mode: ReportModeType;
  generatedAt: string;
  executionTimeSeconds: number;
  manualBaselineTimeMinutes: number;
  efficiencyGainPercent: number;
  executiveSummary: string;
  findingsTable: Array<Record<string, any>>;
  citations: FactEvidenceCitation[];
  statutoryClearanceStatus: string;
  dgmsDocketNo: string;
  digitalSignatureHash: string;
}
