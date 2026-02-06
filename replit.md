# Controlmyentries

## Overview

Controlmyentries is a web-based budget monitoring anomaly detection tool for accountants and financial controllers. Users upload an Excel export of their General Ledger (Grand Livre / GL), and the system runs a 3-pass analysis pipeline to detect anomalies in accounting entries:

1. **Pass 1 (Binary):** Pattern-based detection — disappearance, appearance, >20% variation, broken recurrence
2. **Pass 2 (Z-score):** Statistical anomaly detection using adaptive per-node Z-scores with M-12 seasonality comparison
3. **Pass 3 (Report):** Generates a multi-tab Excel report with findings, statistics, and synthesis

The app follows an "ilovepdf" SaaS model: stateless, no accounts, no data storage. Upload → process (≤30s) → download report. A baseline JSON file (generated from prior year GL data) enables the statistical pass.

The project uses the **BMad Method** for structured AI-driven development. Planning artifacts (PRD, architecture, epics, UX design) are in `_bmad-output/planning-artifacts/`. The BMad framework itself lives in `_bmad/` and should not be modified.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend (Python + FastAPI)

- **Location:** `api/`
- **Framework:** FastAPI with Uvicorn, running on port 8080
- **Entry point:** `api/main.py` runs uvicorn; `api/app.py` creates the FastAPI app
- **Configuration:** Pydantic Settings in `api/core/config.py`, loads from `.env`
- **Key settings:** max file size 20MB, analysis timeout 300s, WebSocket heartbeat 30s
- **Routes:** `api/routes.py` — `/api/health`, `/api/analyze` (file upload), `/api/generate-baseline`
- **Error format:** RFC 7807 Problem Details (`api/models/errors.py`)

#### Analysis Pipeline (`api/services/`)
- `validator.py` — File validation, column detection with fuzzy matching for French/English column names
- `baseline.py` — Generate baseline.json from historical GL data (N-1 year)
- `pass1.py` — Binary pattern detection (disparition, apparition, variation, recurrence)
- `pass2.py` — Z-score statistical analysis using scipy
- `pass3.py` — Excel report generation using xlsxwriter
- `pipeline.py` — Orchestrates all passes with WebSocket progress updates

#### Data Processing Libraries
- **Polars** (not Pandas) for DataFrame operations — chosen for speed
- **scipy** for statistical calculations (Z-scores)
- **xlsxwriter** for Excel report generation

#### WebSocket
- `api/core/websocket.py` — ConnectionManager for real-time progress updates during analysis
- 5-step progress tracking: Validation → Pass 1 → Pass 2 → Report → Complete

#### Models (`api/models/`)
- `analysis.py` — Anomaly types, severity levels, pass results
- `baseline.py` — Baseline file structure with per-node statistics
- `errors.py` — RFC 7807 error responses

### Frontend (React + TypeScript + Vite)

- **Location:** `frontend/`
- **Framework:** React 18 with TypeScript, bundled by Vite
- **Styling:** Tailwind CSS with custom color palette (primary, success, error, warning)
- **Dev server:** Port 5000 with proxy to backend on port 8080 for `/api` and `/ws`
- **Build output:** `frontend/dist/` (copied to `static/` for production serving by FastAPI)
- **Path aliases:** `@/` maps to `frontend/src/`

#### Key Components (`frontend/src/components/`)
- `DropZone` — File upload with react-dropzone, accepts .xlsx, .xls, .csv, .json
- `FileCard` — Displays uploaded file with status indicators
- `ProgressTracker` — 5-step progress visualization during analysis
- `ResultCard` — Shows analysis results with anomaly count and confidence index
- `LandingPage` — Marketing/SEO landing page
- `StatusMessage` — Reusable alert component (info/success/warning/error)

#### Hooks (`frontend/src/hooks/`)
- `useFileUpload` — File state management, type detection (JSON→baseline, Excel/CSV→GL)
- `useWebSocket` — WebSocket connection for real-time progress updates

#### Accessibility
- WCAG 2.2 AAA target: 7:1 contrast ratio, 24px touch targets, keyboard navigation
- Focus-visible styles, ARIA labels, skip-link support

### Deployment Architecture

- **Platform:** Replit — single process serving both API and static frontend
- **No Docker** — direct process execution
- **No database** — fully stateless, files processed in memory/temp storage
- **Static serving:** FastAPI mounts `static/` directory for built frontend assets
- **Single port:** 8080 for everything (API + static + WebSocket)

### Build & Development

- `make dev` — Starts development server with hot reload
- `make build` — Builds frontend to static/
- `make test` — Runs pytest
- `make lint` — Runs ruff + eslint
- `make check` — Full lint + typecheck + test
- Frontend dev server runs on port 5000 and proxies API calls to port 8080

### Testing

- **Backend:** pytest with FastAPI TestClient (`api/tests/`)
- **Fixtures:** `conftest.py` provides a `client` fixture

### Language Note

The application UI and all user-facing text is in **French**. Error messages, labels, descriptions are all in French. Code comments and variable names are in English.

## External Dependencies

### Python Packages (via pyproject.toml)
- **FastAPI** — Web framework
- **Uvicorn** — ASGI server
- **Polars** — High-performance DataFrame library for data processing
- **scipy** — Statistical computations (Z-score calculations)
- **xlsxwriter** — Excel report generation
- **websockets** — WebSocket support
- **python-multipart** — File upload handling
- **pydantic-settings** — Configuration management

### JavaScript Packages (via frontend/package.json)
- **React 18** + **ReactDOM** — UI framework
- **react-dropzone** — Drag-and-drop file upload
- **Vite** — Build tool and dev server
- **Tailwind CSS** — Utility-first CSS framework
- **TypeScript** — Type safety

### External Services
- **None** — The application is fully self-contained with no external API calls, no database, no authentication, and no third-party service integrations. All processing happens locally on the server.