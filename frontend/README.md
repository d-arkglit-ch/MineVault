# Frontend Sub-Team: Next.js Application

## Overview
The `/frontend` repository houses the modern Next.js 14+ application for the **AI-Powered Geological, Mining, and Reporting Solution (SIH26023)**. It provides exploration geologists, mine planners, and ministry officials with an intuitive, unified workspace for document management, conversational analysis, borehole visualization, and automated report generation.

---

## Key Features & Modules
1. **Interactive Document Hub (`/documents`)**:
   - Drag-and-drop batch upload for scanned Geological Reports (GRs) and borehole logs.
   - Real-time ingestion progress monitoring.
   - Dual-pane PDF viewer with interactive bounding-box highlight citations.
2. **Conversational AI Workspace (`/chat`)**:
   - Streaming responses with multi-agent reasoning trace visibility (Router -> Core -> Validation).
   - Dynamic tabular output and geological data card renderings.
   - Direct click-to-cite mechanism linking text directly to source PDF pages.
3. **Geological & Seam Visualizer (`/visualizer`)**:
   - 2D/3D borehole strip log viewer (lithology vs. depth).
   - Seam thickness and coal grade distribution charts.
   - Geospatial drill hole collar map.
4. **Report Studio (`/reports`)**:
   - Template-based CMPDI report builder.
   - Live editable draft preview.
   - One-click export to PDF and Word (.docx).

---

## Directory Structure
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router (pages and layouts)
│   │   ├── layout.tsx       # Root layout with navigation and providers
│   │   ├── page.tsx         # Dashboard landing page
│   │   ├── chat/            # Conversational AI assistant
│   │   ├── documents/       # Document management & PDF viewer
│   │   ├── visualizer/      # Borehole & seam data visualization
│   │   └── reports/         # Report generation studio
│   ├── components/          # Reusable UI components (shadcn/ui, custom widgets)
│   │   ├── ui/              # Base primitives (button, modal, card, tabs)
│   │   ├── chat/            # Message bubble, streaming response, citation preview
│   │   ├── document/        # PDF viewer, bounding box canvas, dropzone
│   │   └── visualizer/      # Stratigraphy chart, borehole log canvas
│   ├── hooks/               # Custom React hooks (useAgentStream, usePdfViewer)
│   ├── lib/                 # Utility functions, API clients, and constants
│   ├── types/               # TypeScript interfaces & API schemas
│   └── styles/              # Global styles and Tailwind directives
├── public/                  # Static assets and icons
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

---

## Getting Started

### Prerequisites
- Node.js 18.17+ or 20+
- npm / pnpm / yarn

### Installation
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).
