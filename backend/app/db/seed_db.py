"""
Database Seeding Script for CMPDI Geological Intelligence Platform.
Migrates archival exploration datasets into the 8 normalized tables:
- Documents
- Document Chunks (RAG)
- Boreholes
- Lithological Intervals
- Fact Evidence Citations
- Discrepancies

Features Idempotent Seeding and Partial Recovery (safely populates missing tables without duplicating).
"""

import sys
import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session

backend_dir = str(Path(__file__).resolve().parent.parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.db.database import SessionLocal, init_db
from app.db.models import (
    DocumentModel,
    DocumentChunkModel,
    BoreholeModel,
    LithologicalIntervalModel,
    FactEvidenceCitationModel,
    DiscrepancyModel
)
from app.db.seed_data import SEED_BOREHOLES, SEED_DISCREPANCIES
from app.core.crypto import generate_sha256

logger = logging.getLogger("geomine.db")


# Archival parent exploration documents
SEED_DOCUMENTS = [
    {
        "document_id": "CMPDI-GR-2021-NK4",
        "title": "CMPDI Detailed Geological Assessment Report — Block IV North Karanpura",
        "agency": "CMPDI",
        "year": 2021,
        "filename": "CMPDI_Block_IV_North_Karanpura_GR_2021.pdf",
        "file_type": "PDF",
        "storage_path": "/uploads/CMPDI_Block_IV_North_Karanpura_GR_2021.pdf",
        "sha256_hash": "9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311",
        "page_count": 12
    },
    {
        "document_id": "MECL-1998-NK4",
        "title": "MECL Historical Regional Exploration Report — North Karanpura Block IV",
        "agency": "MECL",
        "year": 1998,
        "filename": "MECL_1998_North_Karanpura_Report.pdf",
        "file_type": "PDF",
        "storage_path": "/uploads/MECL_1998_North_Karanpura_Report.pdf",
        "sha256_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        "page_count": 45
    },
    {
        "document_id": "GSI-1985-NK",
        "title": "GSI Memoir on Gondwana Coalfields of Eastern India",
        "agency": "GSI",
        "year": 1985,
        "filename": "GSI_1985_Gondwana_Coalfields.pdf",
        "file_type": "PDF",
        "storage_path": "/uploads/GSI_1985_Gondwana_Coalfields.pdf",
        "sha256_hash": "b2c3d4e5f6a17890123456789abcdef0123456789abcdef0123456789abcdef0",
        "page_count": 120
    }
]

# Baseline document chunks for future RAG retrieval
SEED_CHUNKS = [
    {
        "chunk_id": "CHUNK-CMPDI-2021-NK4-P12-01",
        "document_id": "CMPDI-GR-2021-NK4",
        "page_number": 12,
        "text_content": (
            "CENTRAL MINE PLANNING & DESIGN INSTITUTE LIMITED (RI-II Ranchi)\n"
            "BOREHOLE NO: BH-NK-094 (Tandwa Sector, Block IV)\n"
            "Collar Elevation: 482.35m MSL. Total Drilled Depth: 198.50m.\n"
            "Target Coal Seam IX: Intercepted at 114.28m to 122.70m (Clean thickness: 8.42m).\n"
            "Core Recovery: 96.8%. Quality Grade: G7 Non-Coking Coal (GCV: 5,420 kcal/kg, Ash: 23.4%).\n"
            "Wireline Logging: Dual-detector sonic caliper confirms true seam thickness 8.42m without washouts."
        ),
        "bbox_json": json.dumps([120.0, 340.0, 420.0, 110.0]),
        "sha256_hash": "9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311",
        "extraction_confidence": 0.984,
        "metadata_json": json.dumps({"borehole": "BH-NK-094", "coalfield": "North Karanpura", "seam": "SEAM_IX"})
    },
    {
        "chunk_id": "CHUNK-MECL-1998-NK4-P24-02",
        "document_id": "MECL-1998-NK4",
        "page_number": 24,
        "text_content": (
            "MINERAL EXPLORATION CORPORATION LIMITED (MECL 1998 Survey)\n"
            "BOREHOLE NO: BH-NK-094 (Block IV, Tandwa Sector)\n"
            "Target Horizon: Seam IX intercepted at 114.28m to 121.08m.\n"
            "Reported Thickness: 6.80m (Rotary core barrel extraction, Core recovery: 78.2%).\n"
            "Notice: Core loss recorded due to friable roof shale washing during rotary drilling run."
        ),
        "bbox_json": json.dumps([100.0, 280.0, 450.0, 95.0]),
        "sha256_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        "extraction_confidence": 0.912,
        "metadata_json": json.dumps({"borehole": "BH-NK-094", "agency": "MECL", "historical_thickness": 6.80})
    }
]


def seed_database(db: Session):
    """
    Populates normalized database tables with initial exploration records.
    Implements granular table-by-table partial recovery.
    """
    seeded_summary = {}

    # 1. Documents
    doc_count = db.query(DocumentModel).count()
    if doc_count == 0:
        for doc_info in SEED_DOCUMENTS:
            db.add(DocumentModel(**doc_info))
        db.commit()
        seeded_summary["documents"] = len(SEED_DOCUMENTS)
    else:
        seeded_summary["documents"] = 0

    # 2. Document Chunks (RAG)
    chunk_count = db.query(DocumentChunkModel).count()
    if chunk_count == 0:
        for chunk_info in SEED_CHUNKS:
            db.add(DocumentChunkModel(**chunk_info))
        db.commit()
        seeded_summary["document_chunks"] = len(SEED_CHUNKS)
    else:
        seeded_summary["document_chunks"] = 0

    # 3. Boreholes & Normalized Intervals & Citations
    bh_count = db.query(BoreholeModel).count()
    intervals_count = db.query(LithologicalIntervalModel).count()
    citations_count = db.query(FactEvidenceCitationModel).count()

    bh_seeded = 0
    intervals_seeded = 0
    citations_seeded = 0

    if bh_count == 0:
        for bh in SEED_BOREHOLES:
            db.add(BoreholeModel.from_schema(bh))
            bh_seeded += 1
        db.commit()

        # Seed normalized intervals and citations for each borehole
        for bh in SEED_BOREHOLES:
            for idx, it in enumerate(bh.intervals):
                cit_id = f"CIT-{bh.boreholeId}-INT-{idx+1}"
                bbox_json = json.dumps([it.sourceBoundingBox.x, it.sourceBoundingBox.y, it.sourceBoundingBox.width, it.sourceBoundingBox.height]) if it.sourceBoundingBox else None

                # Create normalized interval
                interval_model = LithologicalIntervalModel(
                    interval_id=f"{bh.boreholeId}-INT-{idx+1}",
                    borehole_id=bh.boreholeId,
                    from_depth_meters=it.fromDepthMeters,
                    to_depth_meters=it.toDepthMeters,
                    thickness_meters=it.thicknessMeters,
                    lithology_description=it.lithologyDescription,
                    core_recovery_percent=it.coreRecoveryPercent,
                    seam_code=it.seamCode,
                    citation_id=cit_id if it.seamCode == "SEAM_IX" else None,
                    bbox_json=bbox_json
                )
                db.add(interval_model)
                intervals_seeded += 1

                # If coal seam, add normalized citation
                if it.seamCode == "SEAM_IX":
                    cit_model = FactEvidenceCitationModel(
                        citation_id=cit_id,
                        document_id="CMPDI-GR-2021-NK4",
                        document_title="CMPDI Detailed Geological Assessment Report — Block IV North Karanpura",
                        agency="CMPDI",
                        year=2021,
                        page_number=12,
                        bbox_json=bbox_json,
                        sha256_hash="9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311",
                        extraction_confidence=0.984,
                        fact_type="BOREHOLE_SEAM",
                        fact_reference_id=bh.boreholeId,
                        snippet_text=f"Borehole {bh.boreholeId}: Seam IX intercepted at {it.fromDepthMeters}m to {it.toDepthMeters}m ({it.thicknessMeters}m verified thickness)."
                    )
                    db.add(cit_model)
                    citations_seeded += 1

        db.commit()
    elif intervals_count == 0:
        # Partial recovery: boreholes exist, but intervals need backfilling
        existing_boreholes = db.query(BoreholeModel).all()
        for bh_model in existing_boreholes:
            raw_intervals = json.loads(bh_model.intervals_json) if bh_model.intervals_json else []
            for idx, it in enumerate(raw_intervals):
                cit_id = f"CIT-{bh_model.borehole_id}-INT-{idx+1}"
                bbox = it.get("sourceBoundingBox")
                bbox_json = json.dumps(bbox) if bbox else None

                interval_model = LithologicalIntervalModel(
                    interval_id=f"{bh_model.borehole_id}-INT-{idx+1}",
                    borehole_id=bh_model.borehole_id,
                    from_depth_meters=it.get("fromDepthMeters", 0.0),
                    to_depth_meters=it.get("toDepthMeters", 0.0),
                    thickness_meters=it.get("thicknessMeters", 0.0),
                    lithology_description=it.get("lithologyDescription", ""),
                    core_recovery_percent=it.get("coreRecoveryPercent", 90.0),
                    seam_code=it.get("seamCode"),
                    citation_id=cit_id if it.get("seamCode") == "SEAM_IX" else None,
                    bbox_json=bbox_json
                )
                db.add(interval_model)
                intervals_seeded += 1
        db.commit()

    seeded_summary["boreholes"] = bh_seeded
    seeded_summary["lithological_intervals"] = intervals_seeded
    seeded_summary["fact_evidence_citations"] = citations_seeded

    # 4. Discrepancies
    disc_count = db.query(DiscrepancyModel).count()
    if disc_count == 0:
        disc_seeded = 0
        for disc in SEED_DISCREPANCIES:
            db.add(DiscrepancyModel.from_schema(disc))
            disc_seeded += 1
        db.commit()
        seeded_summary["discrepancies"] = disc_seeded
    else:
        seeded_summary["discrepancies"] = 0

    total_seeded = sum(seeded_summary.values())
    if total_seeded > 0:
        logger.info(f"Database seeded successfully: {seeded_summary}")
        print(f"Seeded {seeded_summary['boreholes']} boreholes, {seeded_summary['discrepancies']} discrepancies, {seeded_summary['lithological_intervals']} intervals, {seeded_summary['documents']} documents.")
    else:
        logger.info("Database already populated across all tables. Skipping seed.")
        print(f"Seeded 0 boreholes, 0 discrepancies (database already populated with {bh_count} boreholes).")

    return seeded_summary


def run_seed():
    """CLI runner to initialize and seed database."""
    init_db()
    db = SessionLocal()
    try:
        return seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_seed()
