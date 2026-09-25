# Ingestion Sub-Team: OCR & Parsing Scripts

## Overview
The `/ingestion` directory is responsible for ingesting, preprocessing, digitizing, and parsing complex geological documents, including scanned Geological Reports (GRs), borehole lithology logs, drill cross-sections, and chemical analysis tables.

---

## Directory Structure
```
ingestion/
├── ocr/
│   ├── ocr_processor.py     # OCR engine wrapper (Tesseract/EasyOCR) & image preprocessing
│   └── deskew.py            # Computer vision deskewing & binarization
├── parsers/
│   ├── borehole_parser.py   # Lithological log & depth interval extractor
│   ├── table_parser.py      # Multi-page table detection & structure preservation
│   └── quality_parser.py    # Proximate & ultimate analysis extractor
├── pipeline.py              # Master pipeline orchestrator
├── requirements.txt         # Subsystem Python dependencies
└── README.md
```

---

## Key Responsibilities
1. **Document Classification**: Detect digital PDFs vs. raster scans to bypass redundant OCR when digital text layers exist.
2. **Preprocessing**: Apply OpenCV adaptive thresholding, contrast stretching, and rotation correction to historical degraded documents.
3. **Table & Lithology Extraction**: Structure borehole logs (`Depth From`, `Depth To`, `Thickness`, `Lithology`, `Seam Name`) with bounding-box coordinate tracking.
4. **Vector & Relational Handoff**: Emit structured JSON and relational records directly to the PostgreSQL database and ChromaDB vector store.

---

## Getting Started
```bash
# Navigate to ingestion directory
cd ingestion

# Install dependencies
pip install -r requirements.txt

# Run the test pipeline
python pipeline.py
```
