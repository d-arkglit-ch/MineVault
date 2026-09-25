import sys
from pathlib import Path

# Ensure repo root and backend directory are in sys.path
for parent in Path(__file__).resolve().parents:
    if (parent / "agents").exists() and (parent / "backend").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        if str(parent / "backend") not in sys.path:
            sys.path.insert(0, str(parent / "backend"))
        break

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.database import init_db, SessionLocal
from app.db.seed_db import seed_database

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="CMPDI Geological Intelligence & Exploration Records Portal (SIH26023)",
    version="2.1.0"
)

@app.on_event("startup")
def startup_db_init():
    """Initializes SQLite schema and idempotently seeds default records on startup."""
    init_db()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# Configure allowed origins explicitly (CORS spec disallows "*" with allow_credentials=True)
allowed_origins = list(settings.BACKEND_CORS_ORIGINS)
if settings.FRONTEND_ORIGIN not in allowed_origins:
    allowed_origins.append(settings.FRONTEND_ORIGIN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API V1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "CMPDI Geological Intelligence Backend",
        "version": "2.1.0",
        "compliance": "GIGW 3.0 & NIC Compliant API Standard"
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to CMPDI Geological Intelligence & Exploration Records Portal API (SIH26023)",
        "docs": "/docs",
        "endpoints": {
            "boreholes": f"{settings.API_V1_STR}/boreholes",
            "discrepancies": f"{settings.API_V1_STR}/discrepancies",
            "reports": f"{settings.API_V1_STR}/reports",
            "query": f"{settings.API_V1_STR}/query",
            "ingestion": f"{settings.API_V1_STR}/ingestion"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
