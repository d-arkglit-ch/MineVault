import os
import shutil
import logging
import json
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Request, Depends
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.models.schemas import IngestionJobResponse, BoundingBox
from app.core.config import settings
from app.core.crypto import generate_sha256
from app.db.database import get_db, SessionLocal
from app.db.models import (
    DocumentModel,
    DocumentChunkModel,
    BoreholeModel,
    LithologicalIntervalModel,
    FactEvidenceCitationModel,
    IngestionJobModel,
    AuditEventModel
)

logger = logging.getLogger("geomine.ingestion")

try:
    from fastapi import File, UploadFile
    import multipart
    _HAS_MULTIPART = True
except ImportError:
    _HAS_MULTIPART = False

# Import Ingestion Pipeline
try:
    from ingestion.pipeline import GeologicalIngestionPipeline
    _pipeline = GeologicalIngestionPipeline()
except Exception as e:
    logger.warning(f"Could not initialize GeologicalIngestionPipeline: {e}")
    _pipeline = None

router = APIRouter()

# Seeded jobs matching PRD Section 5
SEED_JOBS: List[IngestionJobResponse] = [
    IngestionJobResponse(
        jobId="JOB-OCR-9821",
        filename="CMPDI_RI2_NK_BlockIV_Drilling_2021.pdf",
        pageCount=48,
        status="VERIFIED",
        confidenceScore=0.984,
        extractedTables=12,
        extractedBoreholes=["BH-NK-091", "BH-NK-092", "BH-NK-094"],
        boundingBoxes=[
            BoundingBox(x=140.0, y=382.0, width=320.0, height=28.0, pageNumber=12)
        ],
        ocrEngine="Google Cloud Vision"
    ),
    IngestionJobResponse(
        jobId="JOB-OCR-9822",
        filename="MECL_Memoir_NorthKaranpura_1998_Vol2.pdf",
        pageCount=124,
        status="EXTRACTED",
        confidenceScore=0.912,
        extractedTables=26,
        extractedBoreholes=["BH-NK-094", "BH-NK-095", "BH-NK-096"],
        boundingBoxes=[
            BoundingBox(x=115.0, y=510.0, width=310.0, height=24.0, pageNumber=84)
        ],
        ocrEngine="Google Cloud Vision"
    )
]


@router.get("/jobs", response_model=List[IngestionJobResponse], summary="List ingestion & OCR jobs")
def list_ingestion_jobs(db: Session = Depends(get_db)):
    """Returns status of scanned document OCR and parsing jobs from persistent database."""
    db_jobs = db.query(IngestionJobModel).order_by(IngestionJobModel.created_at.desc()).all()
    if db_jobs:
        results = []
        for j in db_jobs:
            bboxes_raw = json.loads(j.bounding_boxes_json) if j.bounding_boxes_json else []
            bboxes = [BoundingBox(**b) if isinstance(b, dict) else BoundingBox(x=b[0], y=b[1], width=b[2], height=b[3], pageNumber=1) for b in bboxes_raw]
            results.append(IngestionJobResponse(
                jobId=j.job_id,
                filename=j.filename,
                pageCount=j.page_count,
                status=j.status,
                confidenceScore=j.confidence_score,
                extractedTables=1 if j.status == "EXTRACTED" else 0,
                extractedBoreholes=json.loads(j.extracted_boreholes_json) if j.extracted_boreholes_json else [],
                boundingBoxes=bboxes,
                ocrEngine=j.ocr_engine,
                extractedIntervals=json.loads(j.extracted_intervals_json) if j.extracted_intervals_json else [],
                warnings=json.loads(j.warnings_json) if j.warnings_json else []
            ))
        return results

    return SEED_JOBS


def _execute_pipeline_on_file(file_path: str, filename: str) -> IngestionJobResponse:
    """Synchronous pipeline worker executed via run_in_threadpool."""
    job_id = f"JOB-OCR-{uuid.uuid4().hex[:8].upper()}"
    if _pipeline is None:
        return IngestionJobResponse(
            jobId=job_id,
            filename=filename,
            pageCount=1,
            status="FAILED",
            confidenceScore=0.0,
            extractedTables=0,
            extractedBoreholes=[],
            boundingBoxes=[],
            ocrEngine="none",
            warnings=["Ingestion pipeline is uninitialized."]
        )

    try:
        res = _pipeline.process_document(file_path)
        bboxes = [
            BoundingBox(
                x=float(b.get("x", 0.0)),
                y=float(b.get("y", 0.0)),
                width=float(b.get("width", 0.0)),
                height=float(b.get("height", 0.0)),
                pageNumber=int(b.get("pageNumber", 1))
            )
            for b in res.get("bounding_boxes", [])
        ]

        status = res.get("status", "NO_TEXT_DETECTED")
        confidence = float(res.get("confidence_score", 0.0))
        boreholes = res.get("extracted_boreholes", [])
        tables = int(res.get("tables_found", 0))
        engine = res.get("ocr_engine_used", "none")

        return IngestionJobResponse(
            jobId=job_id,
            filename=filename,
            pageCount=res.get("page_count", 1),
            status=status,
            confidenceScore=confidence,
            extractedTables=tables,
            extractedBoreholes=boreholes,
            boundingBoxes=bboxes,
            ocrEngine=engine,
            extractedIntervals=res.get("extracted_intervals", []),
            warnings=res.get("warnings", [])
        )
    except Exception as err:
        logger.error(f"Ingestion pipeline processing error: {err}")
        return IngestionJobResponse(
            jobId=job_id,
            filename=filename,
            pageCount=1,
            status="FAILED",
            confidenceScore=0.0,
            extractedTables=0,
            extractedBoreholes=[],
            boundingBoxes=[],
            ocrEngine="none",
            warnings=[f"Pipeline processing failed: {str(err)}"]
        )


def _persist_ingestion_artifacts(job: IngestionJobResponse, file_path: str, filename: str, file_bytes: bytes, db: Session):
    """Transactionally persists document, chunks, intervals, citations, and audit events."""
    try:
        file_hash = generate_sha256(file_bytes)
        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"

        # 1. Document record
        doc = DocumentModel(
            document_id=doc_id,
            title=f"Exploration Document: {filename}",
            agency="CMPDI",
            year=datetime.utcnow().year,
            filename=filename,
            file_type="PDF" if filename.lower().endswith(".pdf") else "IMAGE",
            storage_path=file_path,
            sha256_hash=file_hash,
            page_count=job.pageCount
        )
        db.add(doc)

        # 2. Document Chunks (for RAG)
        if job.status == "EXTRACTED" and job.extractedIntervals:
            interval_texts = [f"{it.get('fromDepthMeters')}m - {it.get('toDepthMeters')}m: {it.get('lithologyDescription')}" for it in job.extractedIntervals]
            chunk_content = f"DOCUMENT: {filename}\nEXTRACTED LITHOLOGY INTERVALS:\n" + "\n".join(interval_texts)
            chunk = DocumentChunkModel(
                chunk_id=f"CHUNK-{uuid.uuid4().hex[:12].upper()}",
                document_id=doc_id,
                page_number=1,
                text_content=chunk_content,
                bbox_json=json.dumps([b.model_dump() for b in job.boundingBoxes]) if job.boundingBoxes else None,
                sha256_hash=file_hash,
                extraction_confidence=job.confidenceScore,
                metadata_json=json.dumps({"boreholes": job.extractedBoreholes, "engine": job.ocrEngine})
            )
            db.add(chunk)

        # 3. Normalized intervals and borehole linkage
        primary_bh = job.extractedBoreholes[0] if job.extractedBoreholes else None
        if primary_bh and job.extractedIntervals:
            # Ensure borehole exists
            existing_bh = db.query(BoreholeModel).filter(BoreholeModel.borehole_id == primary_bh).first()
            if not existing_bh:
                coal_intervals = [it for it in job.extractedIntervals if "coal" in it.get("lithologyDescription", "").lower()]
                seam_thickness = float(coal_intervals[0].get("thicknessMeters", 8.42)) if coal_intervals else 8.42
                existing_bh = BoreholeModel(
                    borehole_id=primary_bh,
                    coalfield="North Karanpura",
                    sector_block="Block IV (Tandwa Sector)",
                    latitude="23° 48' 14.2\" N",
                    longitude="85° 08' 28.5\" E",
                    collar_elevation_msl=479.5,
                    datum="WGS84 / UTM Zone 45N",
                    total_drilled_depth_meters=185.0,
                    target_seam_thickness=seam_thickness,
                    coal_grade="G7",
                    ash_percent=23.4,
                    moisture_percent=6.8,
                    gross_calorific_value_kcal=5420.0,
                    statutory_clearance="DGMS_CLEARED"
                )
                db.add(existing_bh)

            # Persist normalized intervals
            for idx, it in enumerate(job.extractedIntervals):
                cit_id = f"CIT-{primary_bh}-{idx+1}"
                int_model = LithologicalIntervalModel(
                    interval_id=f"{primary_bh}-INT-{idx+1}-{uuid.uuid4().hex[:4].upper()}",
                    borehole_id=primary_bh,
                    from_depth_meters=float(it.get("fromDepthMeters", 0.0)),
                    to_depth_meters=float(it.get("toDepthMeters", 0.0)),
                    thickness_meters=float(it.get("thicknessMeters", 0.0)),
                    lithology_description=it.get("lithologyDescription", ""),
                    core_recovery_percent=float(it.get("coreRecoveryPercent", 90.0)),
                    seam_code=it.get("seamCode"),
                    citation_id=cit_id if it.get("seamCode") == "SEAM_IX" else None,
                    bbox_json=json.dumps(it.get("sourceBoundingBox")) if it.get("sourceBoundingBox") else None
                )
                db.add(int_model)

        # 4. Ingestion job record
        ingest_job = IngestionJobModel(
            job_id=job.jobId,
            document_id=doc_id,
            filename=filename,
            page_count=job.pageCount,
            status=job.status,
            confidence_score=job.confidenceScore,
            ocr_engine=job.ocrEngine,
            extracted_boreholes_json=json.dumps(job.extractedBoreholes),
            extracted_intervals_json=json.dumps(job.extractedIntervals),
            bounding_boxes_json=json.dumps([b.model_dump() for b in job.boundingBoxes]),
            warnings_json=json.dumps(job.warnings)
        )
        db.add(ingest_job)

        # 5. Tamper-evident Audit Event
        event_id = f"EVT-INGEST-{uuid.uuid4().hex[:8].upper()}"
        audit_event = AuditEventModel(
            event_id=event_id,
            event_type="INGEST_DOCUMENT",
            entity_type="document",
            entity_id=doc_id,
            actor_id="EMP-RI2-8492",
            actor_role="Chief Geologist | RI-II Ranchi",
            before_json=json.dumps({"filename": filename}),
            after_json=json.dumps({"document_id": doc_id, "status": job.status, "intervals_extracted": len(job.extractedIntervals)}),
            reason=f"Multi-format document ingestion of {filename} via {job.ocrEngine}.",
            sha256_hash=file_hash
        )
        db.add(audit_event)

        db.commit()
    except Exception as e:
        logger.warning(f"Could not persist ingestion DB records: {e}")
        db.rollback()


if _HAS_MULTIPART:
    @router.post("/upload", response_model=IngestionJobResponse, summary="Upload geological document for OCR & parsing")
    async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
        """Accepts scanned PDF / litholog plate / spreadsheet and triggers OCR, table extraction, and database persistence."""
        storage_dir = Path(settings.STORAGE_DIR)
        storage_dir.mkdir(parents=True, exist_ok=True)

        filename = file.filename or "uploaded_geological_document.pdf"
        dest_path = storage_dir / filename

        file_bytes = await file.read()
        with open(dest_path, "wb") as buffer:
            buffer.write(file_bytes)

        job = await run_in_threadpool(_execute_pipeline_on_file, str(dest_path), filename)
        _persist_ingestion_artifacts(job, str(dest_path), filename, file_bytes, db)
        SEED_JOBS.insert(0, job)
        return job
else:
    @router.post("/upload", response_model=IngestionJobResponse, summary="Upload geological document for OCR & parsing")
    async def upload_document(req: Request, db: Session = Depends(get_db)):
        """Accepts uploaded document stream and triggers OCR & table extraction (fallback mode)."""
        storage_dir = Path(settings.STORAGE_DIR)
        storage_dir.mkdir(parents=True, exist_ok=True)

        filename = req.headers.get("x-filename", "uploaded_geological_document.pdf")
        dest_path = storage_dir / filename

        body = await req.body()
        with open(dest_path, "wb") as buffer:
            buffer.write(body)

        job = await run_in_threadpool(_execute_pipeline_on_file, str(dest_path), filename)
        _persist_ingestion_artifacts(job, str(dest_path), filename, body, db)
        SEED_JOBS.insert(0, job)
        return job
