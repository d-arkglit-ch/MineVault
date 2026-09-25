"""
Seeded Geological Dataset for CMPDI / Coal India Limited (SIH26023).
Focus Area: North Karanpura Coalfield, Block IV.
Includes historical exploration records (MECL 1998, CMPDI 2021, GSI 1985).
"""
import sys
from pathlib import Path

_backend_dir = str(Path(__file__).resolve().parent.parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from typing import List
from app.models.schemas import (
    BoreholeRecord,
    BoreholeCoordinates,
    ProximateAssay,
    LithologicalInterval,
    FactEvidenceCitation,
    BoundingBox,
    DiscrepancyItem
)

try:
    from app.core.crypto import generate_sha256
except ImportError:
    from backend.app.core.crypto import generate_sha256

# -------------------------------------------------------------------------
# Seeded Borehole Records
# -------------------------------------------------------------------------

SEED_BOREHOLES: List[BoreholeRecord] = [
    BoreholeRecord(
        boreholeId="BH-NK-094",
        coalfield="North Karanpura",
        sectorBlock="Block IV (Tandwa Sector)",
        coordinates=BoreholeCoordinates(
            latitude="23° 48' 12.4\" N",
            longitude="85° 08' 45.1\" E",
            collarElevationMsl=482.35,
            datum="WGS84 / UTM Zone 45N"
        ),
        totalDrilledDepthMeters=198.50,
        targetSeamThickness=8.42,
        coalGrade="G7",
        proximateAssay=ProximateAssay(
            ashPercent=23.4,
            moisturePercent=6.8,
            volatileMatterPercent=29.2,
            fixedCarbonPercent=40.6,
            grossCalorificValueKcal=5420.0
        ),
        statutoryClearance="FLAGGED_DISCREPANCY",
        discrepancyId="DISC-094",
        corePhotoUrl="/assets/core-box-run-114-122.jpg",
        intervals=[
            LithologicalInterval(
                fromDepthMeters=0.0,
                toDepthMeters=42.10,
                thicknessMeters=42.10,
                lithologyDescription="Alluvium, sub-rounded gravels and weathered ferruginous soil",
                coreRecoveryPercent=62.5,
                seamCode="ALLUVIUM",
                sourceBoundingBox=BoundingBox(x=120.0, y=340.0, width=420.0, height=18.0, pageNumber=12)
            ),
            LithologicalInterval(
                fromDepthMeters=42.10,
                toDepthMeters=114.28,
                thicknessMeters=72.18,
                lithologyDescription="Medium to coarse-grained Barakar sandstone with carbonaceous streaks",
                coreRecoveryPercent=88.4,
                seamCode="SANDSTONE",
                sourceBoundingBox=BoundingBox(x=120.0, y=362.0, width=420.0, height=18.0, pageNumber=12)
            ),
            LithologicalInterval(
                fromDepthMeters=114.28,
                toDepthMeters=122.70,
                thicknessMeters=8.42,
                lithologyDescription="Target Coal Seam IX: Dull to bright banded coal with vitrain bands",
                coreRecoveryPercent=96.8,
                seamCode="SEAM_IX",
                sourceBoundingBox=BoundingBox(x=120.0, y=384.0, width=420.0, height=22.0, pageNumber=12)
            ),
            LithologicalInterval(
                fromDepthMeters=122.70,
                toDepthMeters=154.10,
                thicknessMeters=31.40,
                lithologyDescription="Interburden: Hard siliceous shale and fine micaceous sandstone",
                coreRecoveryPercent=92.1,
                seamCode="INTERBURDEN",
                sourceBoundingBox=BoundingBox(x=120.0, y=410.0, width=420.0, height=18.0, pageNumber=12)
            ),
            LithologicalInterval(
                fromDepthMeters=154.10,
                toDepthMeters=160.35,
                thicknessMeters=6.25,
                lithologyDescription="Coal Seam X (Lower Horizon): Intercalated shaly coal",
                coreRecoveryPercent=94.0,
                seamCode="SEAM_X",
                sourceBoundingBox=BoundingBox(x=120.0, y=432.0, width=420.0, height=18.0, pageNumber=13)
            ),
        ],
        evidenceTrail=[
            FactEvidenceCitation(
                documentId="CMPDI-GR-2021-NK4",
                documentTitle="CMPDI Detailed Geological Assessment Report — Block IV North Karanpura",
                agency="CMPDI",
                year=2021,
                boundingBox=BoundingBox(x=140.0, y=382.0, width=320.0, height=28.0, pageNumber=12),
                sha256Hash="9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311",
                extractionConfidence=0.984,
                snippetText="Borehole BH-NK-094: Seam IX intercepted at 114.28m to 122.70m, verified clean thickness 8.42m via sonic wireline log."
            ),
            FactEvidenceCitation(
                documentId="MECL-EXP-1998-NK",
                documentTitle="MECL Regional Exploration Memoir — North Karanpura Coalfield (Vol II)",
                agency="MECL",
                year=1998,
                boundingBox=BoundingBox(x=115.0, y=510.0, width=310.0, height=24.0, pageNumber=84),
                sha256Hash="4e712a8910e1b38f8219c0258d4a9823e5a7b21908d2459a11ef932bca5012d9",
                extractionConfidence=0.912,
                snippetText="Borehole BH-NK-094 (Rotary Rig R-14): Seam IX logged at 6.80m thickness. Core recovery 68% due to mud washout."
            )
        ]
    ),
    BoreholeRecord(
        boreholeId="BH-NK-091",
        coalfield="North Karanpura",
        sectorBlock="Block IV (Tandwa Sector)",
        coordinates=BoreholeCoordinates(
            latitude="23° 48' 04.1\" N",
            longitude="85° 08' 22.8\" E",
            collarElevationMsl=478.10,
            datum="WGS84 / UTM Zone 45N"
        ),
        totalDrilledDepthMeters=182.00,
        targetSeamThickness=7.95,
        coalGrade="G7",
        proximateAssay=ProximateAssay(
            ashPercent=24.1,
            moisturePercent=6.5,
            volatileMatterPercent=28.9,
            fixedCarbonPercent=40.5,
            grossCalorificValueKcal=5380.0
        ),
        statutoryClearance="DGMS_CLEARED",
        intervals=[],
        evidenceTrail=[
            FactEvidenceCitation(
                documentId="CMPDI-GR-2021-NK4",
                documentTitle="CMPDI Detailed Geological Assessment Report — Block IV North Karanpura",
                agency="CMPDI",
                year=2021,
                boundingBox=BoundingBox(x=110.0, y=210.0, width=300.0, height=20.0, pageNumber=15),
                sha256Hash="3a98f121e7d2489c09214b7189a023814ef9012d89a712bc90214a781298d012",
                extractionConfidence=0.978,
                snippetText="BH-NK-091: Seam IX intercepted at 112.50m depth, thickness 7.95m."
            )
        ]
    ),
    BoreholeRecord(
        boreholeId="BH-NK-092",
        coalfield="North Karanpura",
        sectorBlock="Block IV (Tandwa Sector)",
        coordinates=BoreholeCoordinates(
            latitude="23° 48' 08.9\" N",
            longitude="85° 08' 31.4\" E",
            collarElevationMsl=479.80,
            datum="WGS84 / UTM Zone 45N"
        ),
        totalDrilledDepthMeters=190.50,
        targetSeamThickness=8.10,
        coalGrade="G7",
        proximateAssay=ProximateAssay(
            ashPercent=23.8,
            moisturePercent=6.9,
            volatileMatterPercent=29.0,
            fixedCarbonPercent=40.3,
            grossCalorificValueKcal=5410.0
        ),
        statutoryClearance="DGMS_CLEARED",
        intervals=[],
        evidenceTrail=[]
    ),
    BoreholeRecord(
        boreholeId="BH-NK-095",
        coalfield="North Karanpura",
        sectorBlock="Block IV (Tandwa Sector)",
        coordinates=BoreholeCoordinates(
            latitude="23° 48' 19.3\" N",
            longitude="85° 09' 02.1\" E",
            collarElevationMsl=485.60,
            datum="WGS84 / UTM Zone 45N"
        ),
        totalDrilledDepthMeters=205.00,
        targetSeamThickness=8.65,
        coalGrade="G7",
        proximateAssay=ProximateAssay(
            ashPercent=25.2,
            moisturePercent=7.1,
            volatileMatterPercent=28.0,
            fixedCarbonPercent=39.7,
            grossCalorificValueKcal=5240.0
        ),
        statutoryClearance="DGMS_CLEARED",
        intervals=[],
        evidenceTrail=[]
    ),
    BoreholeRecord(
        boreholeId="BH-NK-096",
        coalfield="North Karanpura",
        sectorBlock="Block IV (Tandwa Sector)",
        coordinates=BoreholeCoordinates(
            latitude="23° 48' 24.0\" N",
            longitude="85° 09' 18.5\" E",
            collarElevationMsl=488.10,
            datum="WGS84 / UTM Zone 45N"
        ),
        totalDrilledDepthMeters=212.00,
        targetSeamThickness=8.80,
        coalGrade="G7",
        proximateAssay=ProximateAssay(
            ashPercent=26.0,
            moisturePercent=7.0,
            volatileMatterPercent=27.5,
            fixedCarbonPercent=39.5,
            grossCalorificValueKcal=5220.0
        ),
        statutoryClearance="UNDER_JOINT_REVIEW",
        intervals=[],
        evidenceTrail=[]
    )
]

# -------------------------------------------------------------------------
# Seeded Discrepancy Queue Items (PRD Section 5.1 & Design Doc Section 6.3)
# -------------------------------------------------------------------------

_disc_094_notes = (
    "Historical MECL 1998 rotary survey under-reported thickness due to core loss and washout in brittle vitrain horizon. "
    "CMPDI 2021 sonic caliper & gamma-density logs confirm true thickness of 8.42m. "
    "Net reserve impact across 2.4 sq km influence polygon: +5.44 Million Tonnes (Proved UNFC 111)."
)
_disc_096_notes = "Fault boundary proximity dip angle correction required before inventory sign-off."

SEED_DISCREPANCIES: List[DiscrepancyItem] = [
    DiscrepancyItem(
        discrepancyId="DISC-094",
        boreholeId="BH-NK-094",
        coalfield="North Karanpura",
        block="Block IV (Tandwa)",
        seam="Seam IX",
        agencyA="MECL",
        surveyYearA=1998,
        reportedThicknessA=6.80,
        methodA="Rotary Core Drilling (68% recovery, mud-flush)",
        agencyB="CMPDI",
        surveyYearB=2021,
        reportedThicknessB=8.42,
        methodB="Digital Sonic Wireline Log & High-Recovery Core (96.8%)",
        thicknessDeltaMeters=1.62,
        status="UNDER_REVIEW",
        verifiedThicknessMeters=None,
        reconciliationNotes=_disc_094_notes,
        digitalSignatureHash=generate_sha256(f"DISC-094:{_disc_094_notes}"),
        auditDocketNo="CMPDI/RI-II/NK-IV/DISC-094/2026"
    ),
    DiscrepancyItem(
        discrepancyId="DISC-096",
        boreholeId="BH-NK-096",
        coalfield="North Karanpura",
        block="Block IV (Tandwa)",
        seam="Seam X",
        agencyA="GSI",
        surveyYearA=1985,
        reportedThicknessA=5.40,
        methodA="Direct Core Barrel",
        agencyB="CMPDI",
        surveyYearB=2021,
        reportedThicknessB=6.25,
        methodB="Wireline Resistivity/Sonic Log",
        thicknessDeltaMeters=0.85,
        status="UNDER_REVIEW",
        verifiedThicknessMeters=None,
        reconciliationNotes=_disc_096_notes,
        digitalSignatureHash=generate_sha256(f"DISC-096:{_disc_096_notes}"),
        auditDocketNo="CMPDI/RI-II/NK-IV/DISC-096/2026"
    )
]
