import hashlib
from typing import Any, Union

def generate_sha256(content: Union[str, bytes]) -> str:
    """
    Computes an authentic, 64-character hexadecimal SHA-256 hash
    from arbitrary string or bytes content.
    """
    if isinstance(content, str):
        payload = content.encode("utf-8")
    else:
        payload = content
    return hashlib.sha256(payload).hexdigest()

def generate_citation_hash(document_id: str, title: str, page: int, snippet: str) -> str:
    """
    Produces a deterministic tamper-evident cryptographic hash
    anchored to specific document coordinates and extracted text.
    """
    payload = f"{document_id}:{title}:p{page}:{snippet}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
