"""
Consolidated Cryptographic Utilities.
The single canonical implementation resides at backend/app/core/crypto.py.
This module re-exports from backend/app/core/crypto.py for seamless compatibility.
"""

import sys
from pathlib import Path

# Ensure project root and backend are in sys.path
_project_root = str(Path(__file__).resolve().parent.parent.parent)
_backend_path = str(Path(__file__).resolve().parent.parent.parent / "backend")
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _backend_path not in sys.path:
    sys.path.insert(0, _backend_path)

try:
    from app.core.crypto import generate_sha256, generate_citation_hash
except ImportError:
    from backend.app.core.crypto import generate_sha256, generate_citation_hash

__all__ = ["generate_sha256", "generate_citation_hash"]
