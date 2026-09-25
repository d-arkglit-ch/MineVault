from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.database import get_db
from app.db.models import BoreholeModel, LithologicalIntervalModel
from app.models.schemas import BoreholeRecord, LithologicalInterval

router = APIRouter()


@router.get("/", response_model=List[BoreholeRecord], summary="List all boreholes with pagination and structured filters")
def list_boreholes(
    coalfield: Optional[str] = Query(None, description="Filter by coalfield"),
    block: Optional[str] = Query(None, description="Filter by block"),
    status: Optional[str] = Query(None, description="Filter by statutory clearance status"),
    min_thickness: Optional[float] = Query(None, alias="minThickness", ge=0.0, description="Minimum seam thickness in meters"),
    max_ash: Optional[float] = Query(None, alias="maxAsh", ge=0.0, le=100.0, description="Maximum ash percentage"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Returns paginated list of boreholes from persistent database with coordinates,
    seam thickness, coal grade, and statutory clearance status.
    Supports structured hybrid-SQL filtering (coalfield, block, status, minThickness, maxAsh).
    """
    query = db.query(BoreholeModel)

    if coalfield and isinstance(coalfield, str):
        query = query.filter(BoreholeModel.coalfield.ilike(f"%{coalfield.strip()}%"))
    if block and isinstance(block, str):
        query = query.filter(BoreholeModel.sector_block.ilike(f"%{block.strip()}%"))
    if status and isinstance(status, str):
        query = query.filter(func.lower(BoreholeModel.statutory_clearance) == status.strip().lower())
    if min_thickness is not None:
        query = query.filter(BoreholeModel.target_seam_thickness >= min_thickness)
    if max_ash is not None:
        query = query.filter(BoreholeModel.ash_percent <= max_ash)

    results = query.offset(skip).limit(limit).all()
    return [b.to_schema() for b in results]


@router.get("/intervals/search", response_model=List[LithologicalInterval], summary="Search normalized lithological intervals")
def search_intervals(
    seam_code: Optional[str] = Query(None, alias="seamCode", description="Filter by seam code (e.g. SEAM_IX)"),
    min_thickness: Optional[float] = Query(None, alias="minThickness", ge=0.0, description="Minimum interval thickness in meters"),
    max_recovery: Optional[float] = Query(None, alias="maxRecovery", ge=0.0, le=100.0, description="Find intervals below core recovery threshold"),
    min_recovery: Optional[float] = Query(None, alias="minRecovery", ge=0.0, le=100.0, description="Find intervals above core recovery threshold"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Executes granular SQL queries over normalized lithological intervals.
    Example: Find coal seams above 8 meters, or intervals with core recovery below 90%.
    """
    query = db.query(LithologicalIntervalModel)

    if seam_code:
        query = query.filter(LithologicalIntervalModel.seam_code.ilike(f"%{seam_code.strip()}%"))
    if min_thickness is not None:
        query = query.filter(LithologicalIntervalModel.thickness_meters >= min_thickness)
    if max_recovery is not None:
        query = query.filter(LithologicalIntervalModel.core_recovery_percent <= max_recovery)
    if min_recovery is not None:
        query = query.filter(LithologicalIntervalModel.core_recovery_percent >= min_recovery)

    results = query.limit(limit).all()
    return [it.to_schema() for it in results]


@router.get("/{borehole_id}", response_model=BoreholeRecord, summary="Get borehole dossier")
def get_borehole_dossier(borehole_id: str, db: Session = Depends(get_db)):
    """
    Returns the comprehensive geological dossier for a single borehole,
    including lithological intervals, proximate assay, and evidence citations from persistent storage.
    """
    record = db.query(BoreholeModel).filter(
        func.lower(BoreholeModel.borehole_id) == borehole_id.strip().lower()
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Borehole {borehole_id} not found in National Coal Registry."
        )

    return record.to_schema()


@router.get("/{borehole_id}/intervals", response_model=List[LithologicalInterval], summary="Get normalized intervals for a borehole")
def get_borehole_intervals(
    borehole_id: str,
    seam_code: Optional[str] = Query(None, alias="seamCode"),
    min_thickness: Optional[float] = Query(None, alias="minThickness"),
    db: Session = Depends(get_db)
):
    """Returns normalized lithological intervals for a specific borehole with optional SQL filters."""
    query = db.query(LithologicalIntervalModel).filter(
        func.lower(LithologicalIntervalModel.borehole_id) == borehole_id.strip().lower()
    )
    if seam_code:
        query = query.filter(LithologicalIntervalModel.seam_code.ilike(f"%{seam_code.strip()}%"))
    if min_thickness is not None:
        query = query.filter(LithologicalIntervalModel.thickness_meters >= min_thickness)

    intervals = query.order_by(LithologicalIntervalModel.from_depth_meters.asc()).all()
    return [it.to_schema() for it in intervals]
