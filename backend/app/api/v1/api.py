from fastapi import APIRouter
from app.api.v1.endpoints import boreholes, discrepancies, reports, query, ingestion

api_router = APIRouter()

api_router.include_router(boreholes.router, prefix="/boreholes", tags=["Boreholes"])
api_router.include_router(discrepancies.router, prefix="/discrepancies", tags=["Verification Queue"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(query.router, prefix="/query", tags=["AI Query Assistant"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion & OCR"])
