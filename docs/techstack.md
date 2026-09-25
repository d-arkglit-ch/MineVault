# Technology Stack — CMPDI Geological Intelligence & Exploration Records Portal

**Problem Statement:** SIH26023 | **Team:** Race Condition | **Date:** 20 September 2026
**Note:** Section 1 (Frontend) is carried over as specified in the Frontend UI/UX Design Specification v2.1. Sections 2–5 (Backend, AI/Data, Infra, DevOps) are defined here to complete the stack.

---

## 1. Frontend (per design specification)

| Layer | Technology |
|---|---|
| Framework | Next.js 14/15 (React 18/19, App Router, Server Components) |
| Language | TypeScript 5.x (strict mode) |
| Styling | Tailwind CSS + CSS Custom Properties (National Coal Design System tokens) |
| UI Primitives | Radix UI / Headless UI (WCAG 2.1 AA compliant) |
| GIS & Mapping | Leaflet.js / OpenLayers + Proj4js (Bhuvan WMS, GeoJSON cadastral layer, WGS84) |
| Tabular Data | TanStack Table (React Table v8), virtualized scrolling |
| Charts / Cross-sections | Recharts / Chart.js / D3.js (stratigraphic cross-sections, assay charts) |
| Document Viewer | react-pdf / PDF.js (bounding-box canvas overlay) |
| Export | jsPDF (Form-V dossiers), SheetJS/xlsx (data exports) |
| Client-side structured cache (optional) | SQLite / DuckDB-WASM for offline field filtering |

---

## 2. Backend

| Layer | Technology | Rationale |
|---|---|---|
| API Framework | **FastAPI (Python 3.11+)** | Async-native, strong typing via Pydantic maps cleanly to the frontend's TypeScript data contracts, fast to build for a hackathon timeline |
| API Style | REST (OpenAPI auto-generated) + WebSocket for live-sync dashboard timers | OpenAPI schema keeps frontend/backend contracts in sync automatically |
| Auth | Firebase Authentication (role-based: Geologist / Ministry Officer / Reviewer / Auditor) | Matches "authenticated officer ID" requirement in the design spec; fast to set up |
| Background Jobs | Celery + Redis (or lightweight `arq`) | Handles OCR/ingestion jobs asynchronously so the API stays responsive during document processing |
| File/Document Storage | Firebase Storage or local object storage (S3-compatible, e.g. MinIO for offline demo safety) | Stores raw scanned PDFs, litholog plates, wireline curve files |

---

## 3. AI / Data Layer

| Component | Technology | Purpose |
|---|---|---|
| LLM | Google Gemini (Flash for speed/cost, Pro for complex PQ drafting) | Core reasoning, report drafting, PQ Fast-Response generation |
| OCR | Google Cloud Vision API or Tesseract (offline fallback) | Extracts text from scanned PDFs and litholog plates |
| Embeddings | Gemini Embeddings or `sentence-transformers` (local fallback) | Powers semantic search over document corpus |
| Vector Store | FAISS (in-memory/local) | Fast, no external dependency — ideal for hackathon demo reliability |
| Structured Data Store | PostgreSQL (or SQLite for lighter demo) | Stores `BoreholeRecord`, `LithologicalInterval`, `FactEvidenceCitation` — enables the SQL half of the hybrid retrieval engine |
| Hybrid Retrieval Orchestration | Custom router in FastAPI (LangChain or plain Python, team's choice) | Directs numeric/structured queries to SQL, open-ended queries to RAG |
| Hashing / Integrity | Python `hashlib` (SHA-256) | Generates the tamper-evident hash shown per `FactEvidenceCitation` |

**Agent architecture (unchanged from PRD):**
- Router / Intent Agent — classifies request type
- Core Reasoning Agent — tool-calling (`search_documents`, `sql_query`, `generate_report`, `extract_topics`)
- Validation Agent — background job, populates Conflict Timeline + Verified-Fact queue

---

## 4. Infrastructure & Deployment

| Layer | Technology | Notes |
|---|---|---|
| Backend Hosting | Render / Railway | Free-tier friendly, fast redeploys during the sprint |
| Frontend Hosting | Vercel (native Next.js support) | Zero-config deploys, preview URLs per branch — useful with 6 people pushing daily |
| Database Hosting | Supabase (Postgres) or Render Postgres | Managed, free-tier viable for demo scale |
| Map Tiles | Bhuvan WMS if credentialed in time; otherwise OpenStreetMap tiles as a sandboxed fallback | Keeps the GIS module functional even without live government API access |
| Environment Config | `.env` + Doppler or simple `.env.example` convention | Keeps API keys out of the repo across 6 contributors |

---

## 5. DevOps & Team Workflow

| Aspect | Approach |
|---|---|
| Version Control | Single GitHub repo, `main` protected, feature branches per sub-team (`ingestion/`, `agents/`, `frontend/`) |
| CI | GitHub Actions — lint + type-check on PR (TypeScript `tsc`, Python `ruff`/`mypy`) |
| Code Review | Each PR requires 1 approval from a teammate outside the authoring sub-team, to catch integration issues early |
| Demo Data Safety | Pre-cache 3–5 known-good demo queries/responses as a fallback in case of live LLM/API failure during judging |
| Secrets | Never committed — `.env.example` in repo, real keys shared privately (e.g. team password manager or Firebase console access) |

---

## 6. Stack Summary (at a glance)

```
Frontend:  Next.js + TypeScript + Tailwind + Radix UI + Leaflet.js + TanStack Table + PDF.js
Backend:   FastAPI (Python) + Celery/Redis + Firebase Auth/Storage
AI/Data:   Gemini (LLM) + FAISS (vectors) + PostgreSQL (structured) + Tesseract/Vision OCR
Infra:     Vercel (frontend) + Render (backend) + Supabase (DB)
```

This stack keeps the frontend exactly as specified in the design document, while giving the backend, AI, and infrastructure layers a consistent, hackathon-realistic implementation path that a 6-person team can split cleanly across sub-teams.
