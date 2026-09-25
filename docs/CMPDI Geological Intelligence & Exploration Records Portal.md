web application/stitch/projects/6935756801596954382/screens/1e2f3eda83ff4ad894de1b38a716bf67
# CMPDI Geological Intelligence & Exploration Records Portal
## Frontend UI/UX Design Specification (Government of India / Ministry of Coal Standard)

**Design direction:** Accessible National Governance Portal conforming to GIGW 3.0 & NIC Guidelines with Source-Traceable AI Workflow  
**Prepared for:** Team Race Condition / Ministry of Coal (CMPDI & CIL Subsidiaries)  
**Problem Statement:** SIH26023 — AI-Powered Geological, Mining and Other Reporting Solution for CMPDI/CIL Subsidiaries  
**Document Version:** 2.1 (Programming Languages & Tech Stack Edition)  
**Date:** 20 September 2026  
**Reference Design System:** National Coal Portal Design System (`#0C2340` Deep Navy / NIC Light Baseline)  

---

## 1. Executive Design Vision & Purpose

Following ministerial feedback and direct prototype validation, the visual direction has transitioned from a dark, complex sci-fi telemetry screen to an **authentic, authoritative, and clean Government of India (GoI) administrative portal**. It strictly adheres to **GIGW 3.0 (Guidelines for Indian Government Websites)** and **NIC accessibility benchmarks** while delivering cutting-edge AI capabilities:

1. **Institutional Trust & Clarity**: An accessible, high-contrast light interface featuring official Government of India mastheads, Ashoka Pillar insignia, tricolor top bar, and statutory compliance registries.
2. **Simplified, Role-Driven Ergonomics**: Replaces intimidating multi-dimensional HUDs with familiar ministerial tabs, cadastral Bhuvan-style map viewers, clear tabular drill logs, and plain-language administrative terminology.
3. **Full Fact Provenance & Traceability**: Every AI-compiled geological thickness, ash percentage, proximate assay, and coal reserve metric is tied to an auditable source citation (scanned PDF plate, historical drill book, or digital sonic wireline log).
4. **Accessible to All Officials**: Designed for non-technical desk officers, chief geologists, review committee members, and parliamentary affairs personnel alike.

---

## 2. Programming Languages & Frontend Technology Stack

To build this production-grade, GIGW 3.0-compliant Government of India portal, the following programming and markup languages, libraries, and frameworks are strictly defined:

### 2.1 Core Programming & Markup Languages

| Language | Role & Purpose | Scope of Implementation |
|---|---|---|
| **TypeScript (v5.x)** | **Primary Frontend Application Language** | Strongly typed application logic, state models, UI component props, API client contracts, data models for borehole lithology, and verified fact records. Enforces runtime type-safety across complex geological assays. |
| **JavaScript (ES2023+)** | Core Execution Runtime | Underlying runtime executed by modern web browsers and Node.js environments; handles dynamic polyfills and legacy browser compatibility. |
| **HTML5 (Semantic)** | Page Structure & Accessibility | Accessible landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`), ARIA attributes (`aria-expanded`, `aria-live`, `aria-describedby`), and bilingual screen-reader metadata required by NIC / GIGW 3.0. |
| **CSS3 / PostCSS** | Layout, Styling & Spatial Theming | Flexbox, CSS Grid layouts, CSS Custom Properties (`--gov-navy-primary: #0C2340;`), print media stylesheets for Form-V dossiers, and micro-interactions. |
| **SQL (Client Data Layer / WASM - Optional)** | Client-Side Structured Queries | Deterministic client-side caching and filtering of structured borehole records via SQLite/DuckDB-WASM for offline field work. |

---

### 2.2 Framework & Core Libraries Breakdown

```
[Frontend Architecture Stack]
├── Framework: Next.js 14 / 15 (React 18 / 19 with App Router & Server Components)
├── Language: TypeScript (Strict Type Checking)
├── Styling Engine: Tailwind CSS + CSS Variables (Tokens from National Coal Design System)
├── UI Primitives: Radix UI / Headless UI (Unstyled, 100% accessible, WCAG 2.1 AA compliant)
├── GIS & Mapping: Leaflet.js / OpenLayers with Proj4js (Bhuvan WMS, GeoJSON Cadastral Layer, WGS84)
├── Tabular Data Engine: TanStack Table (React Table v8) with virtualized scrolling
├── Charts & Cross-Sections: Chart.js / Recharts / D3.js (Stratigraphic cross-sections & proximate assays)
├── Document & PDF Engines: react-pdf / PDF.js (Scanned litholog viewer with bounding-box canvas highlight)
└── Export Utilities: jsPDF & SheetJS (xlsx) for Form-V and DGMS exploration dockets
```

---

### 2.3 Key TypeScript Type Definitions (Data Contracts)

```typescript
// Core Data Contract for Sourced Geological Facts & Bounding Boxes
export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  pageNumber: number;
}

export interface FactEvidenceCitation {
  documentId: string;
  documentTitle: string;
  agency: 'MECL' | 'CMPDI' | 'GSI' | 'CIL';
  year: number;
  boundingBox?: BoundingBox;
  sha256Hash: string;
  extractionConfidence: number; // e.g., 0.982
}

export interface LithologicalInterval {
  fromDepthMeters: number;
  toDepthMeters: number;
  thicknessMeters: number;
  lithologyDescription: string;
  coreRecoveryPercent: number;
  seamCode?: 'SEAM_IX' | 'SEAM_X' | 'INTERBURDEN' | 'ALLUVIUM';
}

export interface BoreholeRecord {
  boreholeId: string;
  coalfield: string;
  sectorBlock: string;
  coordinates: {
    latitude: string;
    longitude: string;
    collarElevationMsl: number;
    datum: 'WGS84 / UTM Zone 45N';
  };
  totalDrilledDepthMeters: number;
  targetSeamThickness: number;
  coalGrade: 'G4' | 'G5' | 'Coking W-IV';
  proximateAssay: {
    ashPercent: number;
    moisturePercent: number;
    grossCalorificValueKcal: number;
  };
  statutoryClearance: 'DGMS_CLEARED' | 'UNDER_JOINT_REVIEW' | 'FLAGGED_DISCREPANCY';
  intervals: LithologicalInterval[];
  evidenceTrail: FactEvidenceCitation[];
}
```

---

## 3. Target Persona & Experience Architecture

| Persona | Core Responsibilities | Key Portal Touchpoint & Primary Action |
|---|---|---|
| **CMPDI Field & Chief Geologist** (e.g. Er. S. Mukhopadhyay) | Validating borehole core recovery, resolving historical drilling mismatches, certifying coal seam thickness | **Block Exploration Maps & Borehole Dossier**: Approve seam intervals into the National Coal Inventory with digital sign-off. |
| **Ministry Desk / Parliamentary Officer** | Preparing rapid, verified replies for Parliamentary Questions (Lok Sabha / Rajya Sabha starred questions) | **Geological Reports (PQ Mode)**: Generate structured, cited ministerial briefs with historical comparisons in < 45 seconds. |
| **Joint Technical Committee Reviewer** | Reconciling discrepancies between historical agencies (MECL 1998 vs CMPDI 2021) | **Verification & Reconciliation Queue**: Review side-by-side core box scans, sonic caliper logs, and statutory discrepancy flags. |
| **Director General of Mines Safety (DGMS) Auditor** | Verifying statutory clearance, fault line safety offsets, and UNFC 111 reserve categorization | **National Data Repository & Audit Desk**: Export statutory Form-V PDF registers and DGMS-compliant data dockets. |

---

## 4. Brand & Visual Design System (National Coal Portal)

### 4.1 Color Palette Tokens

| Design Token | Value | Applied UI Component / Meaning |
|---|---|---|
| `gov-navy-primary` | `#0C2340` | Official ministerial header, primary navigation bar, formal action triggers |
| `gov-navy-dark` | `#081729` | Masthead branding bar, active primary navigation pills, footer background |
| `surface-bg` | `#F8F9FD` | Page canvas background, clean neutral working area |
| `surface-card` | `#FFFFFF` | Form containers, tabular cards, spatial map panels, report previews |
| `border-subtle` | `#D9E2EC` | Clean 1px card outlines, table row dividers, input boundaries |
| `statutory-green` | `#137333` | UNFC 111 Proved Reserves, approved statutory clearances, verified facts |
| `alert-amber` | `#B06000` | Historical discrepancy flags, under-review borehole logs, joint audit notices |
| `warning-red` | `#C5221F` | Non-conformity warnings, DGMS safety boundary alerts, unresolved conflicts |
| `bhuvan-teal` | `#007A87` | Spatial coordinates, Bhuvan GIS overlay toggles, map layer contours |
| `text-primary` | `#1F2937` | Formal report copy, lithological descriptions, metric numerals |
| `text-secondary` | `#4B5563` | Sub-labels, datum references (WGS84), logging methodology notes |

### 4.2 Typography System
- **Primary Typography:** `Public Sans` (Google Fonts / NIC standard open font) for high clarity in government reports and administrative forms.
- **Data & Coordinate Font:** `IBM Plex Mono` / `Consolas` reserved specifically for spatial coordinates (`23° 48' 12.4" N, 85° 08' 45.1" E`), cryptographic hash footprints (SHA-256), and statutory docket numbers (`CMPDI/RI-II/NK-IV/DISC-094`).

| Hierarchy Level | Font Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| Display / Screen Title | 26–28px | SemiBold (600) | 1.25 | Screen headers (e.g. Subsurface & Borehole Geological Log Record) |
| Section Headings | 18–20px | SemiBold (600) | 1.3 | Card titles, Map View headers, Ledger groupings |
| Metric Numeric Tiles | 28–32px | Bold (700) | 1.1 | Total Sector Boreholes, Proved Reserves (MT), Compliance % |
| Table / Form Body | 13–14px | Regular (400) / Med (500) | 1.4 | Lithological descriptions, depth intervals, proximate values |
| Metadata & Badges | 11–12px | SemiBold (600) | 1.2 | UNFC 111, DGMS Cleared, Statutory Notice tags |

### 4.3 Shape & Component Language
- **Border Radius:** Restrained 4px to 6px (`rounded-md`), avoiding bubbly SaaS pill cards.
- **Elevation:** Flat surfaces with crisp 1px borders (`#D9E2EC`) and subtle 2px soft drop-shadows on interactive floating palettes.
- **Accessibility:** Minimum contrast ratio of 4.8:1 across all body text; native focus rings (`2px solid #0C2340`); skip-to-content links; bilingual English/Hindi header toggles.

---

## 5. Information Architecture & Navigation Structure

```
[Government of India Top Utility Bar] (Tricolor stripe, A- A A+, Screen Reader, Hindi/English, NIC/GIGW)
└── [Ministry Header] (Ashoka Lion, CMPDI & Coal India Wordmark, GE-BIMS Title, Authenticated Officer ID)
    └── [Persistent Primary Navigation Bar]
        ├── 1. Dashboard (National Coal Overview, KPIs, Live Sync Timers)
        ├── 2. Borehole Directory (Comprehensive 14-Sector Well Registry & Search)
        ├── 3. Block Exploration Maps (Cadastral GIS, Bhuvan Layer, Geological Cross-Sections) [Active]
        ├── 4. Geological Reports (AI Report Studio, PQ Fast-Response, Trend Summaries)
        ├── 5. Verification Queue (Discrepancy Resolution, Joint Review Dockets, Core Log Sign-Off)
        └── 6. National Data Repository (Form-V Archival, DGMS Registers, JORC/UNFC Data)
```

---

## 6. Key Functional Modules (Mapped to PRD FR-1 to FR-17)

### 6.1 Cadastral Bhuvan Spatial GIS & Geological Cross-Section
- **Interactive Topo & Cadastral Mapping:** Integrates Survey of India (WGS84 / UTM Zone 45N) grid with national Bhuvan Topo overlays using **Leaflet.js / OpenLayers**.
- **Borehole Plunges & Outcrops:** Color-coded pin markers indicating borehole status (Green = Verified, Amber = Under Review, Grey = Capped).
- **Stratigraphic Cross-Section (Line A - A'):** Plain-language 2D cross-section diagram rendered in **SVG / D3.js** showing seam horizons from Ground Level (GL) down through Alluvium (0–42m), Sandstone (42–114m), Target Coal Seam IX (114.3–122.7m), Interburden, and Seam X.
- **Fault Line Traces:** Clear statutory notation confirming fault displacement status.

### 6.2 Borehole Lithological Dossier & Proximate Analysis Deck
- **Precise Lithological Column:** Tabular breakdown built with **TanStack Table** displaying From/To depths, seam thickness, lithology classification, and core recovery percentages.
- **Proximate Quality Assay:** Highlighting Ash %, Moisture %, Gross Calorific Value (5,420 kcal/kg), and Grade designation (Grade G4 Non-Coking).
- **Core Recovery & Field Site Evidence:** Direct image scans of physical core storage boxes (Run 114.2m – 122.6m) and on-site drilling rig operations for physical audit trails.

### 6.3 Statutory Discrepancy & Joint Committee Reconciliation Flow
- **High-Visibility Statutory Callout:** Amber statutory review banner flagging discrepancies between legacy surveys (MECL 1998 rotary survey @ 6.80m) and modern digital sonic caliper logs (CMPDI 2021 @ 8.42m).
- **Reconciliation Audit Trail:** Displays digital signature hash (SHA-256), validating geologist sign-off, and net reserve impact (+1.62m seam thickness delta).
- **One-Click Authority Action:** Large ministerial CTA button: **"Approve Verified Thickness for National Coal Inventory"**.

### 6.4 AI-Powered Geological Report Studio & Parliamentary Question (PQ) Fast-Response
- **Four Distinct Reporting Modes:** Executive Summary, Historical Trend, Statutory Audit, and PQ Fast-Response.
- **Live Efficiency Benchmark:** Visible timer contrasting standard manual preparation (estimated 3h 40m) against AI compilation (00m 42s), proving 98% efficiency gain with zero unverified hallucinations.

### 6.5 Multi-Format Ingestion Desk & Bounding-Box Evidence Viewer
- **Multi-Format Pipeline:** Ingests scanned historical PDFs, raster litholog plates, geophysical wireline curves, and spreadsheets.
- **PDF.js / Canvas Overlay:** Bounding-box viewer highlighting extracted facts directly over scanned archive pages (`Page 12 · Table 3 · Row 4 · Bounding Box [x: 140, y: 382]`).

---

## 7. Statutory Compliance & Accessibility Checklist

| Guideline / Standard | Implementation Requirement | Portal Execution |
|---|---|---|
| **GIGW 3.0 Standard** | Official national emblems, bilingual support, standard footer disclaimers | Ashoka Lion crest, Ministry of Coal logo, Hindi/English language toggle, GIGW compliance badge |
| **NIC Accessibility (WCAG 2.1 AA)** | High text contrast, text-resize controls, screen reader friendly | Top bar `A- A A+` dynamic scaling, ARIA landmarks on all tabular data and form inputs |
| **DGMS Safety Compliance** | CMR 2017 Regulation 113 statutory exploration certification | Prominent DGMS cleared badge (`SEC-IV/2025/OK`) and instant export dockets |
| **UNFC 111 Standards** | UNFC classification framework for coal reserves categorization | Clear badge: *UNFC 111 Proved Reserves (14.80 Million Tonnes)* with Grade G4/G5 breakdown |
| **Data Provenance & Cryptography** | Digital verification and audit tamper-proofing | Cryptographic SHA-256 digital signature hashes attached to all technical audit notes |

---

## 8. Implementation Roadmap & Technical Hand-off

1. **Frontend Architecture:** Next.js 14/15 (App Router) + Tailwind CSS + TypeScript conforming to the National Coal Portal Design System.
2. **GIS & Map Engine:** Leaflet.js / OpenLayers configured with Bhuvan Web Map Service (WMS) tile endpoints and GeoJSON cadastral layer rendering.
3. **Tabular Data Components:** Accessible React Table (TanStack Table v8) with keyboard navigation, sorting by borehole ID, collar elevation, and clearance status.
4. **Export Engines:** Client-side PDF generation (`jsPDF`, `react-pdf`) producing standardized Form-V statutory borehole dossiers and DGMS exploration sheets.
