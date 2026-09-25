"""
Borehole Lithology and Stratigraphic Table Parser.
Extracts depth intervals, lithological descriptions, coal seams, and thickness metrics.
Includes OCR text sanitization, domain constraint validation, and coordinate bbox tracking.
"""

from typing import List, Dict, Any, Optional
import re
from pydantic import BaseModel, Field

class LithologyInterval(BaseModel):
    borehole_id: str
    depth_from: float = Field(..., description="Top depth in meters")
    depth_to: float = Field(..., description="Bottom depth in meters")
    thickness: float = Field(..., description="Interval thickness in meters")
    stratum_type: str = Field(..., description="E.g., Coal, Sandstone, Shale, Carbonaceous Shale")
    seam_name: Optional[str] = Field(None, description="Seam designation, e.g., Seam I, Seam II Top")
    core_recovery_percent: Optional[float] = Field(None, description="Core recovery percentage")
    bbox: Optional[List[float]] = Field(None, description="Coordinate bounding box [x, y, w, h]")

class BoreholeTableParser:
    def __init__(self):
        self.last_warnings: List[str] = []

    def _sanitize_float(self, value: Any) -> Optional[float]:
        """
        Sanitizes OCR-extracted numeric strings:
        - Handles common OCR substitutions (e.g. 'O'/'o' -> '0', 'l'/'I' -> '1')
        - Strips whitespace and depth units (e.g. '42.10m' -> 42.10)
        - Defensively catches TypeError / ValueError without crashing table parse
        """
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        # Remove units like 'm', 'meters', '%', etc.
        s = re.sub(r'[a-zA-Z%]', lambda m: '0' if m.group(0) in ['O', 'o'] else ('1' if m.group(0) in ['l', 'I'] else ''), s).strip()

        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def parse_lithology_table(self, rows: List[Dict[str, Any]], borehole_id: str) -> List[LithologyInterval]:
        """
        Parses normalized table rows into structured LithologyInterval records.
        
        Applies strict domain validation & resilience:
        - Ignores or repairs malformed OCR text without crashing the entire parse.
        - Enforces domain rule: depth_to must be strictly >= depth_from.
        - Populates bounding box (bbox) coordinates to power FR-13 evidence viewer.
        """
        parsed_intervals: List[LithologyInterval] = []
        self.last_warnings = []

        for idx, row in enumerate(rows):
            raw_from = row.get("depth_from", row.get("from_m", row.get("from", None)))
            raw_to = row.get("depth_to", row.get("to_m", row.get("to", None)))

            depth_from = self._sanitize_float(raw_from)
            depth_to = self._sanitize_float(raw_to)

            # OCR Malformed Numeric Check
            if depth_from is None or depth_to is None:
                self.last_warnings.append(
                    f"Row {idx + 1} for {borehole_id}: Unparseable numeric depths (from='{raw_from}', to='{raw_to}'). Row flagged for manual review."
                )
                continue

            # Domain Constraint Validation: depth_to must be >= depth_from
            if depth_to < depth_from:
                self.last_warnings.append(
                    f"Row {idx + 1} for {borehole_id}: Domain validation violation: depth_to ({depth_to}m) < depth_from ({depth_from}m). Row skipped to prevent negative thickness."
                )
                continue

            thickness = round(depth_to - depth_from, 2)

            # Preserve Bounding Box for Visual Source-Proof (PRD FR-13)
            bbox = row.get("bbox") or row.get("sourceBoundingBox") or row.get("source_bbox")

            # Core Recovery percentage extraction
            raw_recovery = row.get("recovery_pct", row.get("core_recovery", row.get("coreRecoveryPercent")))
            recovery_pct = self._sanitize_float(raw_recovery)

            interval = LithologyInterval(
                borehole_id=borehole_id,
                depth_from=depth_from,
                depth_to=depth_to,
                thickness=thickness,
                stratum_type=row.get("stratum", row.get("stratum_type", "Unknown Strata")),
                seam_name=row.get("seam_name", row.get("seamCode")),
                core_recovery_percent=recovery_pct,
                bbox=bbox
            )
            parsed_intervals.append(interval)

        return parsed_intervals

if __name__ == "__main__":
    parser = BoreholeTableParser()
    test_rows = [
        {"from_m": "0.00", "to_m": "42.10", "stratum": "Alluvium", "bbox": [120.0, 340.0, 420.0, 18.0]},
        {"from_m": "42.10", "to_m": "114.28", "stratum": "Sandstone", "bbox": [120.0, 362.0, 420.0, 18.0]},
        {"from_m": "114.28", "to_m": "122.70", "stratum": "Seam IX", "bbox": [120.0, 384.0, 420.0, 22.0]},
        # OCR corrupted row (digits swapped / depth_to < depth_from)
        {"from_m": "130.00", "to_m": "125.00", "stratum": "Corrupted Row", "bbox": [100.0, 400.0, 300.0, 20.0]},
        # OCR noisy text row (with letters like '4O.5m')
        {"from_m": "135.5m", "to_m": "14O.5m", "stratum": "Interburden", "bbox": [120.0, 410.0, 420.0, 18.0]},
    ]

    results = parser.parse_lithology_table(test_rows, "BH-NK-094")
    print(f"Parsed {len(results)} valid intervals successfully:")
    for r in results:
        print(f" - {r.depth_from}m -> {r.depth_to}m (Thk: {r.thickness}m, Strata: {r.stratum_type}, BBox: {r.bbox})")
    print("\nWarnings captured during parsing:")
    for w in parser.last_warnings:
        print(f" - {w}")
