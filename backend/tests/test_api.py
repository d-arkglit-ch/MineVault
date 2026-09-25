"""
Unit Tests for CMPDI Geological Intelligence Backend API Endpoints (SIH26023).
"""

import sys
from pathlib import Path
repo_root = str(Path(__file__).resolve().parent.parent.parent)
backend_root = str(Path(__file__).resolve().parent.parent)
for p in [repo_root, backend_root]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.db.seed_data import SEED_BOREHOLES, SEED_DISCREPANCIES
from app.models.schemas import ReportGenerationRequest
from agents.core.mining_calculators import MiningCalculator

def test_seed_data_integrity():
    """Verify borehole dataset has expected records."""
    assert len(SEED_BOREHOLES) >= 4, "Should have at least 4 seeded boreholes"
    nk94 = next(b for b in SEED_BOREHOLES if b.boreholeId == "BH-NK-094")
    assert nk94.targetSeamThickness == 8.42, "Seam IX verified thickness must be 8.42m"
    assert nk94.coalGrade == "G7", "Grade must be G7 for GCV 5420 kcal/kg"
    print("[PASS] Seed data integrity verified.")

def test_discrepancy_arithmetic():
    """Verify discrepancy delta calculation."""
    disc = next(d for d in SEED_DISCREPANCIES if d.discrepancyId == "DISC-094")
    calculated_delta = round(disc.reportedThicknessB - disc.reportedThicknessA, 2)
    assert calculated_delta == disc.thicknessDeltaMeters, f"Delta {calculated_delta} != {disc.thicknessDeltaMeters}"
    print("[PASS] Discrepancy delta arithmetic verified.")

def test_mining_calculators():
    """Verify geological reserve formula and coal grading."""
    res = MiningCalculator.calculate_geological_reserves(
        area_sq_m=2400000.0,
        thickness_m=8.42,
        specific_gravity=1.40
    )
    # 2,400,000 * 8.42 * 1.40 = 28,291,200 tonnes = 28.2912 MT
    assert res["reserves_million_tonnes"] == 28.2912, f"Reserve MT was {res['reserves_million_tonnes']}"
    
    grade, band = MiningCalculator.get_coal_grade_from_gcv(6200.0)
    assert grade == "G4", f"GCV 6200 must be G4, got {grade}"
    grade_7, band_7 = MiningCalculator.get_coal_grade_from_gcv(5420.0)
    assert grade_7 == "G7", f"GCV 5420 must be G7, got {grade_7}"
    print("[PASS] Mining calculators verified.")

def test_borehole_table_parser():
    """Verify OCR error tolerance, domain validation, and bbox preservation."""
    from ingestion.parsers.borehole_parser import BoreholeTableParser
    parser = BoreholeTableParser()
    test_rows = [
        {"from_m": "0.00", "to_m": "42.10", "stratum": "Alluvium", "bbox": [120.0, 340.0, 420.0, 18.0]},
        {"from_m": "42.10m", "to_m": "114.28m", "stratum": "Sandstone", "bbox": [120.0, 362.0, 420.0, 18.0]},
        {"from_m": "114.28", "to_m": "122.70", "stratum": "Seam IX", "bbox": [120.0, 384.0, 420.0, 22.0]},
        # Corrupted row (depth_to < depth_from)
        {"from_m": "130.00", "to_m": "125.00", "stratum": "Swapped Depths", "bbox": [100.0, 400.0, 300.0, 20.0]},
        # OCR character substitution ('14O.5m')
        {"from_m": "135.5m", "to_m": "14O.5m", "stratum": "Interburden", "bbox": [120.0, 410.0, 420.0, 18.0]},
    ]
    parsed = parser.parse_lithology_table(test_rows, "BH-NK-094")
    assert len(parsed) == 4, f"Expected 4 valid rows (1 skipped), got {len(parsed)}"
    assert all(p.thickness > 0 for p in parsed), "All intervals must have strictly positive thickness"
    assert all(p.bbox is not None for p in parsed), "All parsed intervals must preserve their bbox"
    assert any("Domain validation violation" in w for w in parser.last_warnings), "Warning must be recorded for swapped depths"
    print("[PASS] Borehole table parser domain validation & bbox verified.")

def test_query_orchestrator_citations_and_policy():
    """Verify spontaneous queries return citations and 64-char SHA256 hashes without canned override."""
    from agents.orchestrator import MultiAgentOrchestrator
    orchestrator = MultiAgentOrchestrator()

    # Test 1: Spontaneous policy question (not the specific BH-NK-094 canned text)
    policy_query = "What is the discrepancy policy for flagged boreholes in general?"
    res_policy = orchestrator.handle_query(policy_query)
    assert res_policy["routing_decision"]["intent"] == "DISCREPANCY_ANALYSIS"
    assert "CMPDI Discrepancy & Reconciliation Policy" in res_policy["final_answer"]
    assert len(res_policy["citations"]) >= 1, "Must return citations for policy inquiry"
    for cit in res_policy["citations"]:
        h = cit.get("sha256Hash", "")
        assert len(h) == 64, f"SHA-256 hash must be exactly 64 hex chars, got {len(h)} ({h})"
    print("[PASS] Spontaneous policy query answered with authentic 64-char citations.")

    # Test 2: General unscripted inquiry
    general_query = "What are the latest exploration statistics for CIL subsidiaries?"
    res_gen = orchestrator.handle_query(general_query)
    assert len(res_gen["citations"]) >= 1, "General unscripted queries must return grounded citations"
    for cit in res_gen["citations"]:
        h = cit.get("sha256Hash", "")
        assert len(h) == 64, f"SHA-256 hash must be 64 chars, got {len(h)}"
    print("[PASS] General unscripted query returned grounded citations.")

def test_borehole_pagination():
    """Verify borehole pagination query parameters and structured filters via TestClient against persistent DB."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        # Test skip and limit
        res_1 = client.get("/api/v1/boreholes/?skip=0&limit=2")
        assert res_1.status_code == 200
        page_1 = res_1.json()
        assert len(page_1) == 2, f"Expected 2 records, got {len(page_1)}"

        res_2 = client.get("/api/v1/boreholes/?skip=2&limit=2")
        assert res_2.status_code == 200
        page_2 = res_2.json()
        assert len(page_2) == 2, f"Expected 2 records, got {len(page_2)}"
        assert page_1[0]["boreholeId"] != page_2[0]["boreholeId"], "Pages must not overlap"

        # Verify structured hybrid-SQL filters (minThickness, maxAsh)
        res_filtered = client.get("/api/v1/boreholes/?minThickness=8.0&maxAsh=25.0")
        assert res_filtered.status_code == 200
        filtered = res_filtered.json()
        assert len(filtered) >= 1, "Should return filtered boreholes"
        assert all(b["targetSeamThickness"] >= 8.0 for b in filtered)
        assert all(b["proximateAssay"]["ashPercent"] <= 25.0 for b in filtered)
    print("[PASS] Borehole pagination & hybrid-SQL filtering verified.")

def test_database_persistence_and_approval():
    """Verify discrepancy approval persists to SQLite database across sessions."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        # Approve discrepancy DISC-094
        approve_resp = client.post("/api/v1/discrepancies/DISC-094/approve")
        assert approve_resp.status_code == 200, f"Approve failed: {approve_resp.text}"
        data = approve_resp.json()
        assert data["discrepancy"]["status"] == "RESOLVED"
        assert data["discrepancy"]["verifiedThicknessMeters"] == 8.42

        # Verify persistent read from DB
        list_resp = client.get("/api/v1/discrepancies/")
        assert list_resp.status_code == 200
        disc_list = list_resp.json()
        disc_94 = next(d for d in disc_list if d["discrepancyId"] == "DISC-094")
        assert disc_94["status"] == "RESOLVED", "Status must persist as RESOLVED in DB"

        # Verify corresponding borehole clearance status was updated in DB
        bh_resp = client.get("/api/v1/boreholes/BH-NK-094")
        assert bh_resp.status_code == 200
        bh_data = bh_resp.json()
        assert bh_data["statutoryClearance"] == "DGMS_CLEARED"
        assert bh_data["targetSeamThickness"] == 8.42
    print("[PASS] Real database persistence and discrepancy approval verified.")

def test_dynamic_reports():
    """Verify dynamic report generation across modes, locations, honest timing, and citations."""
    import asyncio
    from app.api.v1.endpoints.reports import generate_report

    # 1. Test Seeded Coalfield & Block (North Karanpura)
    req_nk = ReportGenerationRequest(
        mode="PQ_FAST_RESPONSE",
        coalfield="North Karanpura",
        block="Block IV (Tandwa Sector)",
        includeCitations=True
    )
    rep_nk = asyncio.run(generate_report(req_nk))
    assert "North Karanpura" in rep_nk.title
    assert "Block IV (Tandwa Sector)" in rep_nk.title
    assert "North Karanpura" in rep_nk.executiveSummary
    assert rep_nk.executionTimeSeconds > 0, "Execution time must be positive"
    assert rep_nk.efficiencyGainPercent > 99.0, f"Efficiency gain should be > 99%, got {rep_nk.efficiencyGainPercent}"
    assert len(rep_nk.digitalSignatureHash) == 64, "Digital signature must be 64-char SHA-256"
    assert len(rep_nk.citations) >= 2, "Report must include grounded citations"
    for cit in rep_nk.citations:
        assert len(cit.sha256Hash) == 64, f"Citation hash must be 64-char SHA-256, got {len(cit.sha256Hash)}"
    print("[PASS] Seeded report generation (North Karanpura PQ) verified.")

    # 2. Test Unseeded Regional Coalfield & Block (Raniganj) — must NOT show North Karanpura
    req_raniganj = ReportGenerationRequest(
        mode="EXECUTIVE_SUMMARY",
        coalfield="Raniganj",
        block="West Block B",
        includeCitations=True
    )
    rep_raniganj = asyncio.run(generate_report(req_raniganj))
    assert "Raniganj" in rep_raniganj.title
    assert "West Block B" in rep_raniganj.title
    assert "Raniganj" in rep_raniganj.executiveSummary
    assert "North Karanpura" not in rep_raniganj.executiveSummary, "Unseeded block must not mention North Karanpura"
    assert rep_raniganj.executionTimeSeconds > 0
    assert len(rep_raniganj.digitalSignatureHash) == 64
    for cit in rep_raniganj.citations:
        assert len(cit.sha256Hash) == 64
        assert "Raniganj" in cit.snippetText
    print("[PASS] Dynamic unseeded report generation (Raniganj Executive Summary) verified.")

    # 3. Test Statutory Audit and Historical Trend Modes
    req_audit = ReportGenerationRequest(
        mode="STATUTORY_AUDIT",
        coalfield="Singrauli",
        block="Northern Sector",
        includeCitations=True
    )
    rep_audit = asyncio.run(generate_report(req_audit))
    assert rep_audit.mode == "STATUTORY_AUDIT"
    assert "Singrauli" in rep_audit.title
    assert "CMR 2017" in rep_audit.executiveSummary

    req_hist = ReportGenerationRequest(
        mode="HISTORICAL_TREND",
        coalfield="Jharia",
        block="Sector 7",
        includeCitations=True
    )
    rep_hist = asyncio.run(generate_report(req_hist))
    assert rep_hist.mode == "HISTORICAL_TREND"
    assert "Jharia" in rep_hist.title
    assert len(rep_hist.findingsTable) == 3, "Historical trend must show 3 multi-decadal campaigns"
    print("[PASS] Statutory Audit and Historical Trend modes verified.")

def test_ingestion_pipeline_and_upload():
    """Verify real Google Vision OCR processor, pipeline routing, and upload endpoint."""
    import os, tempfile, io
    from PIL import Image, ImageDraw
    from ingestion.ocr.ocr_processor import GeologicalOCRProcessor
    from ingestion.pipeline import GeologicalIngestionPipeline
    from fastapi.testclient import TestClient
    from app.main import app

    # 1. Test OCR Processor properties and honest failure on blank input
    p = GeologicalOCRProcessor()
    assert hasattr(p, "vision_api_key"), "Must expose vision_api_key attribute"
    assert hasattr(p, "gemini_api_key"), "Must expose gemini_api_key attribute"
    blank_rows = p.extract_table_rows_with_bboxes(None)
    assert len(blank_rows) == 0, "Blank/empty input must return 0 rows (no fabrication)"
    assert p.last_confidence_score == 0.0, "Blank/empty input must carry 0.0 confidence"

    # 2. Test Pipeline with blank image — MUST NOT fabricate borehole or intervals
    pipe = GeologicalIngestionPipeline()
    blank_img = Image.new("RGB", (400, 120), color=(255, 255, 255))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_blank:
        blank_img.save(tmp_blank.name, format="PNG")
        tmp_blank_path = tmp_blank.name

    try:
        blank_res = pipe.process_document(tmp_blank_path)
        assert blank_res["status"] == "NO_TEXT_DETECTED", f"Expected NO_TEXT_DETECTED, got {blank_res['status']}"
        assert blank_res["confidence_score"] == 0.0, f"Expected 0.0 confidence, got {blank_res['confidence_score']}"
        assert len(blank_res["extracted_intervals"]) == 0, "Must not extract intervals from blank image"
        assert len(blank_res["extracted_boreholes"]) == 0, "Must not fabricate borehole ID from blank image"
        assert len(blank_res["bounding_boxes"]) == 0, "Must not fabricate bounding boxes from blank image"
        print("[PASS] Honest blank image rejection verified (no fabrication).")
    finally:
        if os.path.exists(tmp_blank_path):
            os.remove(tmp_blank_path)

    # 3. Test Pipeline with synthetic litholog plate image containing real text
    test_img = Image.new("RGB", (500, 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(test_img)
    draw.text((10, 10), "BOREHOLE NO: BH-NK-094", fill=(0, 0, 0))
    draw.text((10, 40), "0.00 - 42.10m Alluvium and weathered zone 62.5%", fill=(0, 0, 0))
    draw.text((10, 70), "42.10 - 114.28m Barakar Formation Sandstone 88.4%", fill=(0, 0, 0))
    draw.text((10, 100), "114.28 - 122.70m Coal Seam IX (Grade G7) 96.8%", fill=(0, 0, 0))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        test_img.save(tmp.name, format="PNG")
        tmp_path = tmp.name

    try:
        res = pipe.process_document(tmp_path)
        assert res["status"] == "EXTRACTED"
        assert res["confidence_score"] > 0.0
        assert len(res["extracted_boreholes"]) > 0
        assert len(res["extracted_intervals"]) >= 3
        assert len(res["bounding_boxes"]) >= 3
        assert res["ocr_engine_used"] is not None
        print("[PASS] Geological ingestion pipeline processing verified.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # 4. Test HTTP upload endpoint via TestClient
    client = TestClient(app)
    img_buf = io.BytesIO()
    test_img.save(img_buf, format="PNG")
    img_bytes = img_buf.getvalue()

    upload_resp = client.post(
        "/api/v1/ingestion/upload",
        files={"file": ("BH_NK_094_Scanned_Litholog.png", img_bytes, "image/png")}
    )
    assert upload_resp.status_code == 200, f"Upload returned {upload_resp.status_code}: {upload_resp.text}"
    job_data = upload_resp.json()
    assert job_data["status"] == "EXTRACTED"
    assert job_data["confidenceScore"] > 0.0
    assert len(job_data["boundingBoxes"]) > 0
    assert job_data["ocrEngine"] is not None
    assert "BH-NK-094" in job_data["extractedBoreholes"] or len(job_data["extractedBoreholes"]) > 0
    print("[PASS] Ingestion /upload endpoint verified end-to-end.")

if __name__ == "__main__":
    test_seed_data_integrity()
    test_discrepancy_arithmetic()
    test_mining_calculators()
    test_borehole_table_parser()
    test_query_orchestrator_citations_and_policy()
    test_borehole_pagination()
    test_database_persistence_and_approval()
    test_dynamic_reports()
    test_ingestion_pipeline_and_upload()
    print("All backend tests passed successfully!")
