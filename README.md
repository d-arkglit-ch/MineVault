# ⛏️ MineVault
### AI-Powered Geological Intelligence, Exploration Records & Mining Analytics System
**Smart India Hackathon 2026 | Problem Statement ID: SIH26023**  
**Organization:** Central Mine Planning & Design Institute (CMPDI) / Coal India Limited (CIL)  
**Team:** racecondition  

---

## 📌 Overview

**MineVault** is an enterprise-grade geological intelligence and exploration records platform engineered for **CMPDI** and **Coal India Limited (CIL)**. It bridges the gap between decades of unstructured historical borehole logs, geological exploration reports, and modern automated spatial analytics.

MineVault provides an end-to-end, multi-agent AI pipeline designed to ingest, digitize, validate, query, and generate statutory mining reports with mathematical determinism and cryptographic auditability.

---

## ✨ Key Capabilities

- 📄 **Intelligent Ingestion & OCR**: Automated preprocessing and high-precision table extraction from scanned PDF borehole logs, drill-hole cross-sections, and legacy lithological charts.
- 🤖 **Multi-Agent Reasoning Engine**: Specialized tripartite agent system:
  - **Router Agent**: Intent classification, entity extraction, and query routing.
  - **Core Mining Agent**: Geological domain calculations (stripping ratios, grade estimation, reserve quantification).
  - **Validation Agent**: Physical constraint validation and 100% auditable bounding-box citation tracking.
- 🗺️ **Interactive Geospatial & Borehole Exploration**: Interactive GIS mapping with drill-hole coordinates, stratigraphic depth profiles, and cross-section visualizations.
- 📊 **Automated Statutory Reporting**: On-demand generation of CMPDI-standard exploration dossiers and resource summaries.
- 🛡️ **Cryptographic Data Integrity**: SHA-256 integrity verification, audit trails, and strict physical constraint verification to eliminate AI hallucinations.

---

## 📂 Repository Architecture

```
MineVault/
├── frontend/             # Next.js 14+ Web Application (Borehole Directory, Maps, Report Studio)
│   ├── src/app/          # App Router & page views
│   ├── src/components/   # Modular React & Tailwind components
│   └── package.json      # Dependencies and scripts
│
├── backend/              # FastAPI Application (High-Performance REST APIs)
│   ├── app/main.py       # API entrypoint & middleware
│   ├── app/api/          # RESTful v1 endpoints
│   ├── app/core/         # Configuration & security settings
│   ├── app/models/       # Pydantic schemas & SQLAlchemy ORM
│   └── requirements.txt  # Python backend dependencies
│
├── ingestion/            # OCR & Parsing Pipeline (Data Engineering & CV)
│   ├── ocr/              # Image preprocessing & OCR wrappers
│   ├── parsers/          # Lithology and tabular extractors
│   ├── pipeline.py       # Master ingestion orchestrator
│   └── requirements.txt  # Ingestion dependencies
│
├── agents/               # Multi-Agent Intelligence Engine (Agentic AI)
│   ├── router/           # Query classification & dispatch
│   ├── core/             # Geological reasoning & deterministic calculators
│   ├── validation/       # Physical constraint & citation verification
│   ├── orchestrator.py   # Multi-agent coordinator
│   └── requirements.txt  # Agent dependencies
│
└── docs/                 # Central Project Documentation
    ├── prd.md            # Product Requirements Document (PRD)
    ├── techstack.md      # Detailed Technology Stack Specifications
    ├── design_doc.md     # Architecture & System Design Document
    └── readme.md         # Documentation Index
```

---

## 🚀 Quickstart Guide

### 1. Central Documentation
Detailed system specifications are available in [`/docs`](./docs):
- [Product Requirements Document (PRD)](./docs/prd.md)
- [Technology Stack](./docs/techstack.md)
- [System Architecture & Design Document](./docs/design_doc.md)

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Running on http://localhost:3000
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows (or source venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Interactive Swagger API docs at http://localhost:8000/docs
```

### 4. Multi-Agent Intelligence Engine
```bash
cd agents
pip install -r requirements.txt
python orchestrator.py
```

### 5. Ingestion & OCR Pipeline
```bash
cd ingestion
pip install -r requirements.txt
python pipeline.py
```

---

## 🛡️ License & Attribution
Developed for **Smart India Hackathon (SIH 2026)** under Problem Statement **SIH26023** for **CMPDI / Coal India Limited**.
