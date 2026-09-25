import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.db.database import get_db
from app.db.models import DiscrepancyModel, BoreholeModel, AuditEventModel
from app.models.schemas import DiscrepancyItem
from app.core.crypto import generate_sha256

router = APIRouter()


@router.get("/", response_model=List[DiscrepancyItem], summary="List statutory discrepancy queue")
def list_discrepancies(db: Session = Depends(get_db)):
    """
    Returns pending and resolved discrepancies from persistent database
    between historical survey agencies (e.g. MECL 1998 rotary survey vs. CMPDI 2021 sonic caliper logs).
    """
    results = db.query(DiscrepancyModel).all()
    return [d.to_schema() for d in results]


@router.get("/audit/trail", summary="List statutory audit sign-off events")
def list_audit_trail(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """
    Returns chronological tamper-evident audit events recorded during statutory approvals.
    """
    events = db.query(AuditEventModel).order_by(AuditEventModel.created_at.desc()).all()
    return [
        {
            "eventId": e.event_id,
            "eventType": e.event_type,
            "entityType": e.entity_type,
            "entityId": e.entity_id,
            "actorId": e.actor_id,
            "actorRole": e.actor_role,
            "beforeState": json.loads(e.before_json) if e.before_json else {},
            "afterState": json.loads(e.after_json) if e.after_json else {},
            "reason": e.reason,
            "sha256Hash": e.sha256_hash,
            "createdAt": e.created_at.isoformat() if e.created_at else None
        }
        for e in events
    ]


@router.post("/{discrepancy_id}/approve", summary="Approve verified thickness for National Coal Inventory")
def approve_discrepancy(discrepancy_id: str, db: Session = Depends(get_db)):
    """
    Simulates digital sign-off by Chief Geologist, certifying verified thickness
    into the National Coal Inventory with cryptographic audit hash and persisting to SQLite.
    Creates an immutable, tamper-evident AuditEventModel record.
    """
    disc = db.query(DiscrepancyModel).filter(
        func.lower(DiscrepancyModel.discrepancy_id) == discrepancy_id.strip().lower()
    ).first()

    if not disc:
        raise HTTPException(
            status_code=404,
            detail=f"Discrepancy record {discrepancy_id} not found."
        )

    bh = db.query(BoreholeModel).filter(
        func.lower(BoreholeModel.borehole_id) == disc.borehole_id.strip().lower()
    ).first()

    before_state = {
        "discrepancyStatus": disc.status,
        "verifiedThicknessMeters": disc.verified_thickness_meters,
        "targetSeamThickness": bh.target_seam_thickness if bh else None,
        "statutoryClearance": bh.statutory_clearance if bh else None
    }

    # Apply digital sign-off
    disc.status = "RESOLVED"
    disc.verified_thickness_meters = disc.reported_thickness_b

    # Update corresponding borehole in persistent storage
    if bh:
        bh.statutory_clearance = "DGMS_CLEARED"
        bh.target_seam_thickness = disc.reported_thickness_b

    after_state = {
        "discrepancyStatus": disc.status,
        "verifiedThicknessMeters": disc.verified_thickness_meters,
        "targetSeamThickness": bh.target_seam_thickness if bh else None,
        "statutoryClearance": bh.statutory_clearance if bh else None
    }

    # Generate tamper-evident audit record
    event_id = f"EVT-SIGNOFF-{uuid.uuid4().hex[:8].upper()}"
    actor_id = "EMP-RI2-8492"
    actor_role = "Chief Geologist | RI-II Ranchi"
    reason = (
        f"Chief Geologist approved verified thickness for {disc.borehole_id} ({disc.seam}). "
        f"Reconciled {disc.agency_a} ({disc.reported_thickness_a}m) with {disc.agency_b} digital wireline logs ({disc.reported_thickness_b}m)."
    )
    timestamp_str = datetime.utcnow().isoformat()
    audit_hash = generate_sha256(f"{event_id}:{actor_id}:{disc.discrepancy_id}:{disc.reported_thickness_b}:{timestamp_str}")

    audit_event = AuditEventModel(
        event_id=event_id,
        event_type="APPROVE_THICKNESS",
        entity_type="discrepancy",
        entity_id=disc.discrepancy_id,
        actor_id=actor_id,
        actor_role=actor_role,
        before_json=json.dumps(before_state),
        after_json=json.dumps(after_state),
        reason=reason,
        sha256_hash=audit_hash
    )

    db.add(audit_event)
    db.commit()
    db.refresh(disc)

    return {
        "message": f"Discrepancy {discrepancy_id} officially resolved and approved.",
        "discrepancy": disc.to_schema(),
        "auditEventId": event_id,
        "auditHash": audit_hash,
        "statutoryNotice": "Updated into National Coal Inventory under UNFC 111 Proved Reserves."
    }
