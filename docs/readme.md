# Documentation Index

Welcome to the project documentation repository for **SIH26023: AI-Powered Geological, Mining, and Reporting Solution**.

---

## Document Index

| Document | Description | Target Audience |
| :--- | :--- | :--- |
| [**PRD (Product Requirements Document)**](./prd.md) | High-level goals, problem statement, user personas, functional and non-functional requirements, and milestones. | Product Managers, Stakeholders, Evaluators |
| [**Tech Stack Specification**](./techstack.md) | Technical stack choices, framework versions, libraries, database, and infrastructure design. | Full Stack Engineers, DevOps, Lead Architects |
| [**System Architecture & Design Doc**](./design_doc.md) | End-to-end architecture, multi-agent reasoning flow, ingestion pipeline, database schema, and validation rules. | AI/ML Engineers, Backend Developers, System Architects |

---

## Sub-Team Folder Alignment

All codebase assets in this repository are partitioned across specialized sub-teams:

- **`/frontend`**: Next.js 14+ application (Chat UI, Document Viewer, Borehole Visualizer, Report Studio)
- **`/backend`**: FastAPI asynchronous application (REST API, Auth, Background Tasks, DB Orchestration)
- **`/ingestion`**: Document OCR and layout extraction pipeline (PyMuPDF, EasyOCR, Table Parsers)
- **`/agents`**: Multi-agent intelligence engine (Router Agent, Core Mining Agent, Validation Agent)
- **`/docs`**: Centralized documentation (PRD, Tech Stack, Design Doc, Guides)
