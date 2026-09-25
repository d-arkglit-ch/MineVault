"""
Sample Generator & Bounding Box Extractor Simulation for Ingestion Pipeline.
Provides test fixtures and mock OCR extraction with bounding box coordinates.
"""

from typing import Dict, Any, List

def generate_sample_ocr_extraction() -> Dict[str, Any]:
    """
    Returns simulated OCR extraction for CMPDI Block IV Geological Report (Page 12, Table 3).
    """
    return {
        "document_id": "CMPDI-GR-2021-NK4",
        "document_name": "CMPDI Detailed Geological Assessment Report — Block IV North Karanpura",
        "page_number": 12,
        "table_name": "Table 3: Borehole BH-NK-094 Stratigraphic Log",
        "rows": [
            {
                "interval_id": 1,
                "from_m": 0.0,
                "to_m": 42.10,
                "thickness_m": 42.10,
                "stratum": "Alluvium and weathered zone",
                "recovery_pct": 62.5,
                "bbox": [120.0, 340.0, 420.0, 18.0]
            },
            {
                "interval_id": 2,
                "from_m": 42.10,
                "to_m": 114.28,
                "thickness_m": 72.18,
                "stratum": "Barakar Formation Sandstone",
                "recovery_pct": 88.4,
                "bbox": [120.0, 362.0, 420.0, 18.0]
            },
            {
                "interval_id": 3,
                "from_m": 114.28,
                "to_m": 122.70,
                "thickness_m": 8.42,
                "stratum": "Coal Seam IX (Target Horizon)",
                "recovery_pct": 96.8,
                "bbox": [120.0, 384.0, 420.0, 22.0]
            },
            {
                "interval_id": 4,
                "from_m": 122.70,
                "to_m": 154.10,
                "thickness_m": 31.40,
                "stratum": "Interburden Shale and Siltstone",
                "recovery_pct": 92.1,
                "bbox": [120.0, 410.0, 420.0, 18.0]
            }
        ],
        "sha256": "9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311"
    }

if __name__ == "__main__":
    sample = generate_sample_ocr_extraction()
    print(f"Loaded sample OCR table for: {sample['document_name']} (Page {sample['page_number']})")
    print(f"Extracted {len(sample['rows'])} stratigraphic intervals.")
