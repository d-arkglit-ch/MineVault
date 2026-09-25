from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Core Data Contracts (Matching PRD Section 4 & Design Doc)
# ---------------------------------------------------------

class BoundingBox(BaseModel):
    x: float = Field(..., description="X coordinate in pts or percent")
    y: float = Field(..., description="Y coordinate in pts or percent")
    width: float = Field(..., description="Bounding box width")
    height: float = Field(..., description="Bounding box height")
    pageNumber: int = Field(..., description="1-indexed document page number")

class FactEvidenceCitation(BaseModel):
    documentId: str
    documentTitle: str
    agency: Literal['MECL', 'CMPDI', 'GSI', 'CIL']
    year: int
    boundingBox: Optional[BoundingBox] = None
    sha256Hash: str = Field(..., description="SHA-256 tamper-evident cryptographic hash")
    extractionConfidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    snippetText: Optional[str] = None

class LithologicalInterval(BaseModel):
    fromDepthMeters: float
    toDepthMeters: float
    thicknessMeters: float
    lithologyDescription: str
    coreRecoveryPercent: float
    seamCode: Optional[Literal['SEAM_IX', 'SEAM_X', 'INTERBURDEN', 'ALLUVIUM', 'SANDSTONE', 'SHALE']] = None
    sourceBoundingBox: Optional[BoundingBox] = None

class ProximateAssay(BaseModel):
    ashPercent: float
    moisturePercent: float
    volatileMatterPercent: Optional[float] = None
    fixedCarbonPercent: Optional[float] = None
    grossCalorificValueKcal: float

class BoreholeCoordinates(BaseModel):
    latitude: str
    longitude: str
    collarElevationMsl: float
    datum: str = "WGS84 / UTM Zone 45N"

class BoreholeRecord(BaseModel):
    boreholeId: str
    coalfield: str
    sectorBlock: str
    coordinates: BoreholeCoordinates
    totalDrilledDepthMeters: float
    targetSeamThickness: float
    coalGrade: Literal['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'Coking W-IV']
    proximateAssay: ProximateAssay
    statutoryClearance: Literal['DGMS_CLEARED', 'UNDER_JOINT_REVIEW', 'FLAGGED_DISCREPANCY']
    intervals: List[LithologicalInterval] = []
    evidenceTrail: List[FactEvidenceCitation] = []
    corePhotoUrl: Optional[str] = None
    discrepancyId: Optional[str] = None

# ---------------------------------------------------------
# Verification & Reconciliation Queue
# ---------------------------------------------------------

class DiscrepancyItem(BaseModel):
    discrepancyId: str
    boreholeId: str
    coalfield: str
    block: str
    seam: str
    agencyA: str
    surveyYearA: int
    reportedThicknessA: float
    methodA: str
    agencyB: str
    surveyYearB: int
    reportedThicknessB: float
    methodB: str
    thicknessDeltaMeters: float
    status: Literal['UNDER_REVIEW', 'RESOLVED', 'REJECTED']
    verifiedThicknessMeters: Optional[float] = None
    reconciliationNotes: str
    digitalSignatureHash: str
    auditDocketNo: str

# ---------------------------------------------------------
# Report Generation Schemas
# ---------------------------------------------------------

ReportModeType = Literal['EXECUTIVE_SUMMARY', 'HISTORICAL_TREND', 'STATUTORY_AUDIT', 'PQ_FAST_RESPONSE']

class ReportGenerationRequest(BaseModel):
    mode: ReportModeType
    coalfield: str
    block: str
    questionTitle: Optional[str] = None
    includeCitations: bool = True

class GeneratedReportResponse(BaseModel):
    reportId: str
    title: str
    mode: ReportModeType
    generatedAt: str
    executionTimeSeconds: float
    manualBaselineTimeMinutes: float = 220.0  # ~3 hours 40 mins
    efficiencyGainPercent: float = 98.2
    executiveSummary: str
    findingsTable: List[Dict[str, Any]] = []
    citations: List[FactEvidenceCitation] = []
    statutoryClearanceStatus: str
    dgmsDocketNo: str
    digitalSignatureHash: str

# ---------------------------------------------------------
# Ingestion Schemas
# ---------------------------------------------------------

class IngestionJobResponse(BaseModel):
    jobId: str
    filename: str
    pageCount: int
    status: Literal['PENDING', 'PROCESSING', 'EXTRACTED', 'VERIFIED', 'FAILED', 'NO_TEXT_DETECTED']
    confidenceScore: float
    extractedTables: int
    extractedBoreholes: List[str] = []
    boundingBoxes: List[BoundingBox] = []
    ocrEngine: Optional[str] = "Google Cloud Vision"
    extractedIntervals: Optional[List[Dict[str, Any]]] = None
    warnings: Optional[List[str]] = None

# ---------------------------------------------------------
# Conversational / AI Query Schemas
# ---------------------------------------------------------

class HybridQueryRequest(BaseModel):
    query: str
    sessionId: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

class HybridQueryResponse(BaseModel):
    query: str
    answer: str
    confidenceScore: float
    routingPath: str
    citations: List[FactEvidenceCitation] = []
    agentSteps: List[str] = []
    validated: bool
