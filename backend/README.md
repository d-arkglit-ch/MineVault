# Backend Sub-Team: FastAPI Application

## Overview
The `/backend` service is the central RESTful API gateway for the **AI-Powered Geological, Mining, and Reporting Solution (SIH26023)**. Built on FastAPI, it coordinates document storage, database persistence, asynchronous ingestion jobs, vector embeddings, and agent orchestration.

---

## Directory Structure
```
backend/
├── app/
│   ├── api/                 # API endpoint routers (v1)
│   │   ├── endpoints/
│   │   │   ├── documents.py # Upload, status, metadata
│   │   │   ├── query.py     # NL query & streaming responses
│   │   │   ├── reports.py   # Automated CMPDI report generation
│   │   │   └── boreholes.py # Borehole and seam CRUD
│   │   └── api.py           # API router aggregator
│   ├── core/                # Configuration and security
│   │   └── config.py        # Pydantic BaseSettings & env vars
│   ├── db/                  # Database connections & session management
│   │   └── session.py       # Async SQLAlchemy session
│   ├── models/              # Pydantic schemas and ORM models
│   │   └── schemas.py       # Request / Response schemas
│   ├── services/            # Business logic and external agent wrappers
│   └── main.py              # Application entrypoint & middleware
├── requirements.txt         # Python dependencies
├── .env.example             # Template environment variables
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Virtual environment tool (`venv` or `conda`)

### Setup Instructions
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload --port 8000
```

### Interactive API Documentation
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
