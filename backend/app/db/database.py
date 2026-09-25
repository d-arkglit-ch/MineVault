"""
Database Engine and Session Management for CMPDI Geological Intelligence Portal.
Synchronous SQLAlchemy connection over SQLite with URL scheme normalization.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Normalize DATABASE_URL for synchronous driver if sqlite+aiosqlite is provided
raw_url = settings.DATABASE_URL
if raw_url.startswith("sqlite+aiosqlite://"):
    raw_url = raw_url.replace("sqlite+aiosqlite://", "sqlite://", 1)

# Ensure relative SQLite path is resolved relative to backend directory
if raw_url.startswith("sqlite:///"):
    path_part = raw_url[len("sqlite:///"):]
    # Check if not absolute (Windows C:/ or POSIX /)
    if not (Path(path_part).is_absolute() or (len(path_part) > 1 and path_part[1] == ":")):
        backend_dir = Path(__file__).resolve().parent.parent.parent
        abs_db_path = (backend_dir / path_part).resolve().as_posix()
        raw_url = f"sqlite:///{abs_db_path}"

connect_args = {}
if raw_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    raw_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency yielding a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initializes database schema and tables."""
    from app.db import models  # noqa: F401 - ensure models are imported
    Base.metadata.create_all(bind=engine)
