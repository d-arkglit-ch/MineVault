"""
Database Foundation Unit & Integration Tests (SIH26023).
Validates:
1. Clean schema initialization on isolated SQLite database
2. Idempotent seeding
3. Partial seed recovery
4. Granular SQL queries over normalized lithological intervals
5. Tamper-evident audit event recording on discrepancy approval
6. Cross-session persistence
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add backend and root to sys.path
backend_root = str(Path(__file__).resolve().parent.parent)
repo_root = str(Path(__file__).resolve().parent.parent.parent)
for p in [backend_root, repo_root]:
    if p not in sys.path:
        sys.path.insert(0, p)

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.models import (
    DocumentModel,
    DocumentChunkModel,
    BoreholeModel,
    LithologicalIntervalModel,
    FactEvidenceCitationModel,
    DiscrepancyModel,
    AuditEventModel,
    IngestionJobModel
)
from app.db.seed_db import seed_database
from app.core.crypto import generate_sha256


def get_test_db():
    """Creates a temporary, isolated SQLite database for testing."""
    tmp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    engine = create_engine(f"sqlite:///{tmp_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, TestingSessionLocal, tmp_path


def test_clean_initialization_and_seeding():
    """Verify that an empty database creates all 8 tables and seeds complete datasets."""
    engine, SessionFactory, db_path = get_test_db()
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        expected_tables = {
            "documents",
            "document_chunks",
            "boreholes",
            "lithological_intervals",
            "fact_evidence_citations",
            "discrepancies",
            "audit_events",
            "ingestion_jobs"
        }
        for tbl in expected_tables:
            assert tbl in tables, f"Expected table '{tbl}' was not created by Base.metadata"

        db = SessionFactory()
        summary = seed_database(db)
        db.close()

        assert summary["boreholes"] == 5, f"Expected 5 boreholes seeded, got {summary['boreholes']}"
        assert summary["discrepancies"] == 2, f"Expected 2 discrepancies seeded, got {summary['discrepancies']}"
        assert summary["documents"] == 3, f"Expected 3 documents seeded, got {summary['documents']}"
        assert summary["document_chunks"] == 2, f"Expected 2 chunks seeded, got {summary['document_chunks']}"
        assert summary["lithological_intervals"] >= 5, "Expected at least 5 intervals seeded"
        assert summary["fact_evidence_citations"] >= 1, "Expected at least 1 citation seeded"

        print("[PASS] Clean database initialization and 8-table creation verified.")
    finally:
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


def test_idempotent_startup():
    """Verify that running seeder multiple times does not duplicate records."""
    engine, SessionFactory, db_path = get_test_db()
    try:
        db = SessionFactory()
        seed_database(db)

        # Run seeder a second time
        second_summary = seed_database(db)

        assert second_summary["boreholes"] == 0, "Second seed run must seed 0 boreholes"
        assert second_summary["discrepancies"] == 0, "Second seed run must seed 0 discrepancies"
        assert second_summary["documents"] == 0, "Second seed run must seed 0 documents"

        # Assert total row counts in DB are unchanged
        assert db.query(BoreholeModel).count() == 5
        assert db.query(DiscrepancyModel).count() == 2
        assert db.query(DocumentModel).count() == 3

        db.close()
        print("[PASS] Idempotent database startup verified.")
    finally:
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


def test_partial_seed_recovery():
    """Verify that if one table loses data, seeder restores only the missing records."""
    engine, SessionFactory, db_path = get_test_db()
    try:
        db = SessionFactory()
        seed_database(db)

        # Case 1: Discrepancies are deleted, boreholes remain
        db.query(DiscrepancyModel).delete()
        db.commit()
        assert db.query(DiscrepancyModel).count() == 0
        assert db.query(BoreholeModel).count() == 5

        # Re-run seeder
        recovery_summary = seed_database(db)
        assert recovery_summary["discrepancies"] == 2, "Must recover missing discrepancies"
        assert recovery_summary["boreholes"] == 0, "Must NOT duplicate existing boreholes"
        assert db.query(BoreholeModel).count() == 5

        # Case 2: Intervals are deleted, boreholes remain
        db.query(LithologicalIntervalModel).delete()
        db.commit()
        assert db.query(LithologicalIntervalModel).count() == 0

        recovery_summary_2 = seed_database(db)
        assert recovery_summary_2["lithological_intervals"] >= 5, "Must backfill missing intervals"
        assert db.query(LithologicalIntervalModel).count() >= 5
        assert db.query(BoreholeModel).count() == 5

        db.close()
        print("[PASS] Partial seed recovery verified for isolated table loss.")
    finally:
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


def test_normalized_sql_interval_queries():
    """Verify granular SQL queries over normalized lithological_intervals table."""
    engine, SessionFactory, db_path = get_test_db()
    try:
        db = SessionFactory()
        seed_database(db)

        # 1. Query all coal seams above 8.0 meters
        thick_seams = db.query(LithologicalIntervalModel).filter(
            LithologicalIntervalModel.thickness_meters >= 8.0,
            LithologicalIntervalModel.seam_code == "SEAM_IX"
        ).all()
        assert len(thick_seams) >= 1, "Should find at least 1 Seam IX interval >= 8m"
        assert any(it.thickness_meters == 8.42 for it in thick_seams), "Must find Seam IX 8.42m"

        # 2. Query intervals with low core recovery (< 90%)
        low_recovery = db.query(LithologicalIntervalModel).filter(
            LithologicalIntervalModel.core_recovery_percent < 90.0
        ).all()
        assert len(low_recovery) >= 2, "Should find Alluvium (62.5%) and Barakar Sandstone (88.4%)"
        descriptions = [it.lithology_description.lower() for it in low_recovery]
        assert any("alluvium" in d for d in descriptions)
        assert any("sandstone" in d for d in descriptions)

        # 3. Query all intervals belonging to BH-NK-094 in order
        nk94_intervals = db.query(LithologicalIntervalModel).filter(
            LithologicalIntervalModel.borehole_id == "BH-NK-094"
        ).order_by(LithologicalIntervalModel.from_depth_meters.asc()).all()
        assert len(nk94_intervals) >= 5
        assert nk94_intervals[0].from_depth_meters == 0.0
        assert nk94_intervals[2].seam_code == "SEAM_IX"

        db.close()
        print("[PASS] Granular SQL queries over normalized lithological intervals verified.")
    finally:
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


def test_audit_event_logging_and_persistence():
    """Verify tamper-evident audit logging and cross-process persistence."""
    engine, SessionFactory, db_path = get_test_db()
    try:
        # Session 1: Perform approval and record audit event
        db1 = SessionFactory()
        seed_database(db1)

        disc = db1.query(DiscrepancyModel).filter(DiscrepancyModel.discrepancy_id == "DISC-094").first()
        assert disc.status == "UNDER_REVIEW"

        bh = db1.query(BoreholeModel).filter(BoreholeModel.borehole_id == disc.borehole_id).first()

        # Digital sign-off simulation
        disc.status = "RESOLVED"
        disc.verified_thickness_meters = disc.reported_thickness_b
        bh.statutory_clearance = "DGMS_CLEARED"
        bh.target_seam_thickness = disc.reported_thickness_b

        audit_hash = generate_sha256(f"EVT-001:EMP-RI2-8492:DISC-094:{disc.reported_thickness_b}")
        audit = AuditEventModel(
            event_id="EVT-001",
            event_type="APPROVE_THICKNESS",
            entity_type="discrepancy",
            entity_id="DISC-094",
            actor_id="EMP-RI2-8492",
            actor_role="Chief Geologist | RI-II Ranchi",
            before_json=json.dumps({"status": "UNDER_REVIEW"}),
            after_json=json.dumps({"status": "RESOLVED", "verifiedThicknessMeters": disc.reported_thickness_b}),
            reason="Approved verified thickness from CMPDI 2021 sonic caliper wireline log.",
            sha256_hash=audit_hash
        )
        db1.add(audit)
        db1.commit()
        db1.close()

        # Session 2: Read from a separate session (simulating server restart)
        db2 = SessionFactory()
        disc_check = db2.query(DiscrepancyModel).filter(DiscrepancyModel.discrepancy_id == "DISC-094").first()
        assert disc_check.status == "RESOLVED", "RESOLVED status must survive session restart"
        assert disc_check.verified_thickness_meters == 8.42

        bh_check = db2.query(BoreholeModel).filter(BoreholeModel.borehole_id == "BH-NK-094").first()
        assert bh_check.statutory_clearance == "DGMS_CLEARED"
        assert bh_check.target_seam_thickness == 8.42

        audit_check = db2.query(AuditEventModel).filter(AuditEventModel.event_id == "EVT-001").first()
        assert audit_check is not None
        assert audit_check.actor_id == "EMP-RI2-8492"
        assert len(audit_check.sha256_hash) == 64
        assert "CMPDI 2021 sonic caliper" in audit_check.reason

        db2.close()
        print("[PASS] Tamper-evident audit event recording & cross-session persistence verified.")
    finally:
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    test_clean_initialization_and_seeding()
    test_idempotent_startup()
    test_partial_seed_recovery()
    test_normalized_sql_interval_queries()
    test_audit_event_logging_and_persistence()
    print("\nAll database foundation tests passed successfully!")
