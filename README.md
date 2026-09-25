# SIH-26023: AI-Powered Geological, Mining, and Reporting Solution
### Smart India Hackathon 2026 | Problem Statement ID: SIH26023
**Organization:** Central Mine Planning & Design Institute (CMPDI) / Coal India Limited (CIL)  
**Team Name:** racecondition

---

## 📌 Project Overview
CMPDI and Coal India Limited subsidiaries manage vast repositories of historical exploration reports, borehole lithology logs, drill-hole cross-sections, and mine planning records stored across legacy formats (scanned PDFs, raster charts, spreadsheets).

This platform delivers an **end-to-end intelligent pipeline** that:
1. **Ingests & Preprocesses** scanned geological reports using specialized computer vision and OCR.
2. **Structures Lithological & Seam Data** with high-precision table extraction.
3. **Applies Multi-Agent Intelligence** (Router, Core Geological Analyst, Validation Agent) with deterministic mining formulas.
4. **Validates All Outputs** against physical constraints and provides 100% auditable bounding-box citations to source documents.
5. **Generates Automated Statutory Reports** and provides an interactive web workspace for geologists, mining engineers, and executives.

---

## 📂 Repository & Sub-Team Architecture

```
sih-26023-geological-mining/
├── frontend/             # Next.js 14+ Web Application (UI / UX Sub-team)
│   ├── src/app/          # Next.js App Router pages
│   ├── src/components/   # Modular React & Tailwind components
│   └── package.json      # Dependencies and scripts
│
├── backend/              # FastAPI Application (API & Service Sub-team)
│   ├── app/main.py       # API entrypoint & middleware
│   ├── app/api/          # RESTful v1 endpoints
│   ├── app/core/         # Configuration & environment settings
│   ├── app/models/       # Pydantic data schemas
│   └── requirements.txt  # Python backend dependencies
│
├── ingestion/            # OCR & Parsing Pipeline (Data Engineering Sub-team)
│   ├── ocr/              # Image preprocessing & OCR wrappers
│   ├── parsers/          # Lithology and table extractors
│   ├── pipeline.py       # Master ingestion orchestrator
│   └── requirements.txt  # Ingestion dependencies
│
├── agents/               # Multi-Agent Intelligence Engine (AI/Agentic Sub-team)
│   ├── router/           # Query classification & dispatch
│   ├── core/             # Geological reasoning & mining calculators
│   ├── validation/       # Physical constraint & citation verification
│   ├── orchestrator.py   # Multi-agent coordinator
│   └── requirements.txt  # Agent dependencies
│
└── docs/                 # Central Project Documentation
    ├── prd.md            # Product Requirements Document
    ├── techstack.md      # Detailed Technology Stack Specifications
    ├── design_doc.md     # Architecture & System Design Document
    └── readme.md         # Documentation Index
```

---

## 🚀 Quickstart Guide

### 1. Documentation
Browse the specifications in [`/docs`](./docs):
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
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# API docs at http://localhost:8000/docs
```

### 4. Agents Pipeline Test
```bash
cd agents
pip install -r requirements.txt
python orchestrator.py
```

### 5. Ingestion Pipeline Test
```bash
cd ingestion
pip install -r requirements.txt
python pipeline.py
```

---

## 🛡️ License & Attribution
Developed for Smart India Hackathon (SIH 2026) under Problem Statement SIH26023.
