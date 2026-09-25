# Product Requirement Document (PRD) — v2.0

**Project Name:** CMPDI Geological Intelligence & Exploration Records Portal
**Problem Statement:** SIH26023 — AI-Powered Geological, Mining and Other Reporting Solution for CMPDI/CIL Subsidiaries
**Sponsoring Organization:** Ministry of Coal
**Team:** Race Condition
**Document Version:** 2.0 (aligned to Frontend Design Specification v2.1)
**Date:** 20 September 2026

---

## 1. Overview

### 1.1 Purpose
CMPDI/CIL subsidiaries manually compile geological and mining data from scanned PDFs, historical drill books, sonic wireline logs, and spreadsheets to produce reports and respond to administrative and parliamentary inquiries. This is slow, expert-dependent, and error-prone.

This product is a **Government of India–standard portal** (GIGW 3.0 / NIC compliant) that automates document ingestion, geological data validation, reserve/report generation, and natural-language querying — with every AI-compiled fact (seam thickness, ash %, reserve tonnage) tied to an auditable source citation.

### 1.2 Background
- Data sources: scanned PDFs, raster litholog plates, geophysical wireline curves, spreadsheets, historical archives
- Current workflow: manual, expert-dependent, slow, error-prone
- Objective: automate processing and reporting while strengthening data validation, consistency, and traceability across historical (e.g. MECL 1998) and contemporary (e.g. CMPDI 2021) datasets

### 1.3 Goals
- Reduce report preparation time — demoed live (target: manual ~3h 40m vs. AI ~42 seconds, ≥98% efficiency gain)
- Maximize structured-extraction and report accuracy, displayed as a quantified %
- Maximize automation of repetitive reporting/response workflows
- Enable faster, verified responses to parliamentary and high-priority inquiries (target: under 45 seconds)
- Improve data accessibility, transparency, and standardization across CIL subsidiaries
- Build a scalable, statutorily compliant foundation for future digital transformation

### 1.4 Non-Goals (out of scope for hackathon prototype)
- Full production DGMS/GIGW certification (design conforms to the standard; formal certification is out of scope)
- Complete historical archive digitization (seeded demo dataset only)
- Multi-tenant national rollout across all CIL subsidiaries (single demo tenant)
- Native mobile applications (responsive web only)
- Live Bhuvan WMS production credentials (mocked/sandboxed tile layer acceptable for demo)

---

## 2. Target Personas

| Persona | Core Responsibilities | Primary Portal Action |
|---|---|---|
| **CMPDI Field & Chief Geologist** | Validates core recovery, resolves historical drilling mismatches, certifies seam thickness | Approves seam intervals into the National Coal Inventory via digital sign-off (Block Exploration Maps & Borehole Dossier) |
| **Ministry Desk / Parliamentary Officer** | Prepares rapid, verified replies for Lok Sabha/Rajya Sabha starred questions | Generates structured, cited ministerial briefs in PQ Fast-Response mode |
| **Joint Technical Committee Reviewer** | Reconciles discrepancies between historical agencies (e.g. MECL vs. CMPDI) | Reviews side-by-side evidence and statutory discrepancy flags in the Verification & Reconciliation Queue |
| **DGMS Auditor** | Verifies statutory clearance, safety offsets, UNFC reserve categorization | Exports Form-V registers and DGMS-compliant data dockets from the National Data Repository |

---

## 3. Information Architecture

```
[GoI Top Utility Bar] — Tricolor stripe, A-/A/A+ text scaling, screen reader toggle, Hindi/English
└── [Ministry Header] — Ashoka emblem, CMPDI & Coal India wordmark, authenticated officer ID
    └── [Primary Navigation]
        1. Dashboard — national overview, KPIs, live sync timers
        2. Borehole Directory — sector-wide well registry & search
        3. Block Exploration Maps — cadastral GIS, Bhuvan layer, cross-sections
        4. Geological Reports — AI Report Studio, PQ Fast-Response, trend summaries
        5. Verification Queue — discrepancy resolution, joint review, sign-off
        6. National Data Repository — Form-V archive, DGMS registers, UNFC data
```

---

## 4. Core Data Contracts

The system is built around three linked data entities (full TypeScript definitions maintained in the frontend design spec):

- **BoreholeRecord** — coalfield, sector/block, coordinates (WGS84/UTM Zone 45N), drilled depth, target seam thickness, coal grade, proximate assay (ash %, moisture %, GCV), statutory clearance status, lithological intervals, evidence trail
- **LithologicalInterval** — from/to depth, thickness, lithology description, core recovery %, seam code
- **FactEvidenceCitation** — document ID/title, source agency (MECL / CMPDI / GSI / CIL), year, bounding box, SHA-256 hash, extraction confidence score

Every fact surfaced anywhere in the portal must resolve back to a `FactEvidenceCitation`.

---

## 5. Functional Requirements (mapped to design spec modules)

### 5.1 Core (mandated by problem statement)
| ID | Requirement | Portal Module |
|---|---|---|
| FR-1 | Automated Report Generation Platform | Geological Reports (§6.4) |
| FR-2 | Automated Word Cloud / Topic Identification | Geological Reports — Trend Summaries |
| FR-3 | AI-Based Query and Response System | Geological Reports / Dashboard |
| FR-4 | Multi-format ingestion (scanned PDFs, litholog plates, wireline curves, spreadsheets) | Multi-Format Ingestion Desk (§6.5) |
| FR-5 | Data validation, consistency-checking, traceability across historical/contemporary datasets | Statutory Discrepancy & Reconciliation Flow (§6.3) |

### 5.2 Differentiator Features
| ID | Requirement | Portal Module | Priority |
|---|---|---|---|
| FR-6 | Live before/after time comparison (manual vs. AI) | Geological Reports — Live Efficiency Benchmark | Must-ship |
| FR-7 | Source-traceable report generation (citation per fact) | All modules — Evidence Trail | Must-ship |
| FR-8 | Conflict timeline for discrepant data across sources/dates | Verification & Reconciliation Queue (§6.3) | Must-ship |
| FR-9 | Parliamentary Question fast-response mode (<45s, formal format) | Geological Reports — PQ Fast-Response | Must-ship |
| FR-10 | Report Type Selector: Executive Summary / Historical Trend / Statutory Audit / PQ Fast-Response | Geological Reports | Must-ship |
| FR-11 | Audit / Compliance Dashboard | Dashboard | Should-ship |
| FR-12 | Auto-generated historical trend / stratigraphic cross-section charts | Block Exploration Maps (§6.1) | Should-ship |
| FR-13 | Bounding-box evidence viewer (PDF.js + canvas overlay) | Multi-Format Ingestion Desk (§6.5) | Must-ship |
| FR-14 | Hybrid SQL + RAG retrieval engine | Core Agent (backend) | Must-ship |
| FR-15 | Verified Fact Object with human sign-off ("Approve Verified Thickness for National Coal Inventory") | Statutory Discrepancy Flow (§6.3) | Should-ship |
| FR-16 | Cryptographic traceability (SHA-256 hash per document/citation) | All evidence citations | Should-ship |
| FR-17 | Interactive cadastral GIS map (Bhuvan WMS, borehole pins, cross-sections) | Block Exploration Maps (§6.1) | Should-ship |

---

## 6. Non-Functional & Compliance Requirements

| Standard | Requirement | Execution |
|---|---|---|
| GIGW 3.0 | National emblems, bilingual support, statutory footer | Ashoka crest, Ministry logo, Hindi/English toggle |
| NIC / WCAG 2.1 AA | Contrast, text scaling, screen-reader support | A-/A/A+ control, ARIA landmarks on all data views, min. 4.8:1 contrast |
| DGMS Safety (CMR 2017 Reg. 113) | Statutory exploration certification | DGMS-cleared badge, instant export dockets |
| UNFC 111 | Reserve classification | Clear reserve badge with grade breakdown |
| Data Provenance | Tamper-evident audit trail | SHA-256 hash on every citation |

**Performance:** Standard report generation target ≤60 seconds; PQ Fast-Response target <45 seconds.
**Accessibility:** All primary workflows keyboard-navigable; screen-reader compatible.
**Usability:** Designed for non-technical desk officers — plain-language terminology throughout, no unexplained jargon.

---

## 7. Success Metrics (Expected Benefits, per PS)

| Metric | Target / Demo Approach |
|---|---|
| Report preparation time reduction | Live timer: manual baseline (~3h 40m) vs. AI (~42s) |
| Structured extraction accuracy | Confidence-scored extraction (target ≥95%), spot-checked against seed dataset |
| Automation of repetitive workflows | % of report auto-populated without manual edit |
| Parliamentary/high-priority response speed | PQ Fast-Response mode, target <45 seconds |
| Data accessibility & transparency | Dashboard visibility + citation trail on every fact |

---

## 8. Milestones (10-Day Build Plan)

| Days | Milestone |
|---|---|
| 1–2 | Finalize data contracts, seed borehole/document dataset, architecture lock |
| 3–4 | Ingestion pipeline (OCR, bounding-box capture) + Core Agent (RAG + SQL hybrid) |
| 5–6 | Report Studio (4 modes), Verification Queue, Conflict Timeline |
| 7–8 | Bounding-box viewer, GIS map (Block Exploration Maps), Dashboard, full integration |
| 9 | End-to-end testing, PPT and idea submission drafting |
| 10 | Final rehearsal and submission |

---

## 9. Risks & Open Questions

- **OCR accuracy on legacy scans** (e.g. 1998 MECL survey documents) — fallback manual-correction path needed for demo reliability
- **Bhuvan WMS access** — may require a mocked/sandboxed tile layer if live credentials aren't available in time
- **LLM rate limits (free tier)** — pre-cache demo queries as fallback
- **Scope size** — 17 features across a full GIGW-compliant portal in 10 days is ambitious; daily must-ship vs. nice-to-have triage is required
- **Domain accuracy** — geological/statutory terminology (UNFC, DGMS clauses, seam codes) should be spot-checked against real reference material

---

## 10. Appendix

- Full PS26023 text: Ministry of Coal, SIH 2026 catalogue
- Frontend Design Specification: *CMPDI Geological Intelligence & Exploration Records Portal — Frontend UI/UX Design Specification v2.1*
- Reference prototype reviewed for feature inspiration: "CMPDI Geological Intelligence System"
