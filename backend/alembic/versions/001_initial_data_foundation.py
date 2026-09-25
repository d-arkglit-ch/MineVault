"""Initial Data Foundation Schema (8 normalized tables)

Revision ID: 001_data_foundation
Revises: 
Create Date: 2026-09-23 04:30:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001_data_foundation"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Documents
    op.create_table(
        "documents",
        sa.Column("document_id", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("agency", sa.String(length=50), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=True),
        sa.Column("storage_path", sa.String(length=500), nullable=True),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("document_id")
    )
    op.create_index(op.f("ix_documents_document_id"), "documents", ["document_id"], unique=False)

    # 2. Document Chunks
    op.create_table(
        "document_chunks",
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.String(length=50), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=False),
        sa.Column("bbox_json", sa.Text(), nullable=True),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("extraction_confidence", sa.Float(), nullable=True),
        sa.Column("embedding_json", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["documents.document_id"], ),
        sa.PrimaryKeyConstraint("chunk_id")
    )
    op.create_index(op.f("ix_document_chunks_chunk_id"), "document_chunks", ["chunk_id"], unique=False)
    op.create_index(op.f("ix_document_chunks_document_id"), "document_chunks", ["document_id"], unique=False)

    # 3. Boreholes
    op.create_table(
        "boreholes",
        sa.Column("borehole_id", sa.String(length=50), nullable=False),
        sa.Column("coalfield", sa.String(length=100), nullable=False),
        sa.Column("sector_block", sa.String(length=100), nullable=False),
        sa.Column("latitude", sa.String(length=50), nullable=True),
        sa.Column("longitude", sa.String(length=50), nullable=True),
        sa.Column("collar_elevation_msl", sa.Float(), nullable=True),
        sa.Column("datum", sa.String(length=50), nullable=True),
        sa.Column("total_drilled_depth_meters", sa.Float(), nullable=False),
        sa.Column("target_seam_thickness", sa.Float(), nullable=False),
        sa.Column("coal_grade", sa.String(length=20), nullable=False),
        sa.Column("ash_percent", sa.Float(), nullable=False),
        sa.Column("moisture_percent", sa.Float(), nullable=False),
        sa.Column("volatile_matter_percent", sa.Float(), nullable=True),
        sa.Column("fixed_carbon_percent", sa.Float(), nullable=True),
        sa.Column("gross_calorific_value_kcal", sa.Float(), nullable=False),
        sa.Column("statutory_clearance", sa.String(length=50), nullable=True),
        sa.Column("discrepancy_id", sa.String(length=50), nullable=True),
        sa.Column("core_photo_url", sa.String(length=255), nullable=True),
        sa.Column("intervals_json", sa.Text(), nullable=True),
        sa.Column("evidence_trail_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("borehole_id")
    )
    op.create_index(op.f("ix_boreholes_ash_percent"), "boreholes", ["ash_percent"], unique=False)
    op.create_index(op.f("ix_boreholes_borehole_id"), "boreholes", ["borehole_id"], unique=False)
    op.create_index(op.f("ix_boreholes_coal_grade"), "boreholes", ["coal_grade"], unique=False)
    op.create_index(op.f("ix_boreholes_coalfield"), "boreholes", ["coalfield"], unique=False)
    op.create_index(op.f("ix_boreholes_sector_block"), "boreholes", ["sector_block"], unique=False)
    op.create_index(op.f("ix_boreholes_statutory_clearance"), "boreholes", ["statutory_clearance"], unique=False)
    op.create_index(op.f("ix_boreholes_target_seam_thickness"), "boreholes", ["target_seam_thickness"], unique=False)

    # 4. Fact Evidence Citations
    op.create_table(
        "fact_evidence_citations",
        sa.Column("citation_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.String(length=50), nullable=True),
        sa.Column("document_title", sa.String(length=255), nullable=False),
        sa.Column("agency", sa.String(length=50), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("bbox_json", sa.Text(), nullable=True),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("extraction_confidence", sa.Float(), nullable=True),
        sa.Column("fact_type", sa.String(length=50), nullable=True),
        sa.Column("fact_reference_id", sa.String(length=50), nullable=False),
        sa.Column("snippet_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["documents.document_id"], ),
        sa.PrimaryKeyConstraint("citation_id")
    )
    op.create_index(op.f("ix_fact_evidence_citations_citation_id"), "fact_evidence_citations", ["citation_id"], unique=False)
    op.create_index(op.f("ix_fact_evidence_citations_document_id"), "fact_evidence_citations", ["document_id"], unique=False)
    op.create_index(op.f("ix_fact_evidence_citations_fact_reference_id"), "fact_evidence_citations", ["fact_reference_id"], unique=False)
    op.create_index(op.f("ix_fact_evidence_citations_fact_type"), "fact_evidence_citations", ["fact_type"], unique=False)

    # 5. Lithological Intervals
    op.create_table(
        "lithological_intervals",
        sa.Column("interval_id", sa.String(length=50), nullable=False),
        sa.Column("borehole_id", sa.String(length=50), nullable=False),
        sa.Column("from_depth_meters", sa.Float(), nullable=False),
        sa.Column("to_depth_meters", sa.Float(), nullable=False),
        sa.Column("thickness_meters", sa.Float(), nullable=False),
        sa.Column("lithology_description", sa.Text(), nullable=False),
        sa.Column("core_recovery_percent", sa.Float(), nullable=True),
        sa.Column("seam_code", sa.String(length=50), nullable=True),
        sa.Column("citation_id", sa.String(length=64), nullable=True),
        sa.Column("bbox_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["borehole_id"], ["boreholes.borehole_id"], ),
        sa.ForeignKeyConstraint(["citation_id"], ["fact_evidence_citations.citation_id"], ),
        sa.PrimaryKeyConstraint("interval_id")
    )
    op.create_index(op.f("ix_lithological_intervals_borehole_id"), "lithological_intervals", ["borehole_id"], unique=False)
    op.create_index(op.f("ix_lithological_intervals_core_recovery_percent"), "lithological_intervals", ["core_recovery_percent"], unique=False)
    op.create_index(op.f("ix_lithological_intervals_interval_id"), "lithological_intervals", ["interval_id"], unique=False)
    op.create_index(op.f("ix_lithological_intervals_seam_code"), "lithological_intervals", ["seam_code"], unique=False)
    op.create_index(op.f("ix_lithological_intervals_thickness_meters"), "lithological_intervals", ["thickness_meters"], unique=False)

    # 6. Discrepancies
    op.create_table(
        "discrepancies",
        sa.Column("discrepancy_id", sa.String(length=50), nullable=False),
        sa.Column("borehole_id", sa.String(length=50), nullable=False),
        sa.Column("coalfield", sa.String(length=100), nullable=False),
        sa.Column("block", sa.String(length=100), nullable=False),
        sa.Column("seam", sa.String(length=50), nullable=False),
        sa.Column("agency_a", sa.String(length=50), nullable=False),
        sa.Column("survey_year_a", sa.Integer(), nullable=False),
        sa.Column("reported_thickness_a", sa.Float(), nullable=False),
        sa.Column("method_a", sa.String(length=255), nullable=False),
        sa.Column("agency_b", sa.String(length=50), nullable=False),
        sa.Column("survey_year_b", sa.Integer(), nullable=False),
        sa.Column("reported_thickness_b", sa.Float(), nullable=False),
        sa.Column("method_b", sa.String(length=255), nullable=False),
        sa.Column("thickness_delta_meters", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("verified_thickness_meters", sa.Float(), nullable=True),
        sa.Column("reconciliation_notes", sa.Text(), nullable=False),
        sa.Column("digital_signature_hash", sa.String(length=64), nullable=False),
        sa.Column("audit_docket_no", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("discrepancy_id")
    )
    op.create_index(op.f("ix_discrepancies_borehole_id"), "discrepancies", ["borehole_id"], unique=False)
    op.create_index(op.f("ix_discrepancies_discrepancy_id"), "discrepancies", ["discrepancy_id"], unique=False)
    op.create_index(op.f("ix_discrepancies_status"), "discrepancies", ["status"], unique=False)

    # 7. Audit Events
    op.create_table(
        "audit_events",
        sa.Column("event_id", sa.String(length=50), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=50), nullable=False),
        sa.Column("actor_id", sa.String(length=50), nullable=True),
        sa.Column("actor_role", sa.String(length=100), nullable=True),
        sa.Column("before_json", sa.Text(), nullable=True),
        sa.Column("after_json", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("event_id")
    )
    op.create_index(op.f("ix_audit_events_entity_id"), "audit_events", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_events_event_id"), "audit_events", ["event_id"], unique=False)
    op.create_index(op.f("ix_audit_events_event_type"), "audit_events", ["event_type"], unique=False)

    # 8. Ingestion Jobs
    op.create_table(
        "ingestion_jobs",
        sa.Column("job_id", sa.String(length=50), nullable=False),
        sa.Column("document_id", sa.String(length=50), nullable=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("ocr_engine", sa.String(length=100), nullable=True),
        sa.Column("extracted_boreholes_json", sa.Text(), nullable=True),
        sa.Column("extracted_intervals_json", sa.Text(), nullable=True),
        sa.Column("bounding_boxes_json", sa.Text(), nullable=True),
        sa.Column("warnings_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["documents.document_id"], ),
        sa.PrimaryKeyConstraint("job_id")
    )
    op.create_index(op.f("ix_ingestion_jobs_document_id"), "ingestion_jobs", ["document_id"], unique=False)
    op.create_index(op.f("ix_ingestion_jobs_job_id"), "ingestion_jobs", ["job_id"], unique=False)


def downgrade() -> None:
    op.drop_table("ingestion_jobs")
    op.drop_table("audit_events")
    op.drop_table("discrepancies")
    op.drop_table("lithological_intervals")
    op.drop_table("fact_evidence_citations")
    op.drop_table("boreholes")
    op.drop_table("document_chunks")
    op.drop_table("documents")
