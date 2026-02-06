# Story 1.1: Initialize Replit Project Structure

Status: ready-for-dev

## Story

As a **developer**,
I want **a properly configured Replit project with Python backend and React frontend structure**,
so that **I can start implementing features immediately**.

## Acceptance Criteria

1. **AC1 - Backend Structure:** The following backend files exist:
   - `api/main.py` - Uvicorn entry point
   - `api/app.py` - FastAPI app creation
   - `api/routes.py` - Route definitions placeholder
   - `api/__init__.py`
   - `api/core/__init__.py`, `api/core/config.py` with Pydantic Settings
   - `api/services/__init__.py`
   - `api/models/__init__.py`

2. **AC2 - Frontend Structure:** A Vite React TypeScript project exists at `frontend/`:
   - `frontend/package.json` with dependencies (react, react-dom, tailwindcss, react-dropzone)
   - `frontend/vite.config.ts`
   - `frontend/tsconfig.json`
   - `frontend/tailwind.config.js`
   - `frontend/index.html`
   - `frontend/src/main.tsx`, `frontend/src/App.tsx`

3. **AC3 - Replit Configuration:** The following configuration files exist:
   - `.replit` with run command `uvicorn api.main:app --host 0.0.0.0 --port 8080`
   - `replit.nix` with Python 3.11 and Node.js 20

4. **AC4 - Package Management:** Root package files exist:
   - `pyproject.toml` with FastAPI, uvicorn, polars, scipy, xlsxwriter, websockets, python-multipart
   - `package.json` at root level for workspace management (optional)
   - `.gitignore` with Python and Node patterns

5. **AC5 - Developer Experience:** Running `make dev` starts the development server.

## Tasks / Subtasks

- [ ] Task 1: Create Backend API Structure (AC: 1)
  - [ ] Create `api/` directory structure with `__init__.py` files
  - [ ] Create `api/main.py` with uvicorn entry point
  - [ ] Create `api/app.py` with FastAPI app and static mount
  - [ ] Create `api/routes.py` with router placeholder
  - [ ] Create `api/core/config.py` with Pydantic Settings class
  - [ ] Create `api/services/` and `api/models/` directories with `__init__.py`

- [ ] Task 2: Create Frontend Vite React Project (AC: 2)
  - [ ] Initialize Vite React TypeScript project in `frontend/`
  - [ ] Install dependencies: react-dropzone, tailwindcss, postcss, autoprefixer
  - [ ] Configure Tailwind CSS with `tailwind.config.js` and `postcss.config.js`
  - [ ] Create minimal `App.tsx` with "Controlmyentries" title
  - [ ] Configure `tsconfig.json` with strict mode and path alias `@/*`

- [ ] Task 3: Configure Replit Environment (AC: 3)
  - [ ] Create `.replit` file with run command and deployment config
  - [ ] Create `replit.nix` with Python 3.11 and Node.js 20

- [ ] Task 4: Create Package Management Files (AC: 4)
  - [ ] Create `pyproject.toml` with all Python dependencies
  - [ ] Create `.gitignore` with Python, Node, and IDE patterns
  - [ ] Create `.env.example` with environment variables template

- [ ] Task 5: Create Developer Tooling (AC: 5)
  - [ ] Create `Makefile` with dev, test, build, lint targets
  - [ ] Verify `make dev` starts uvicorn server

- [ ] Task 6: Verification
  - [ ] Run `make dev` and verify server starts on port 8080
  - [ ] Verify all directory structure matches architecture.md specification

## Dev Notes

### Architecture Requirements

**Backend Split Pattern (CRITICAL):**

```python
# api/main.py
import uvicorn
from api.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

# api/app.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router

app = FastAPI(title="Controlmyentries")
app.include_router(router, prefix="/api")
# Static mount added after frontend build exists
```

**Pydantic Settings Pattern:**

```python
# api/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    max_file_size_mb: int = 20
    analysis_timeout_sec: int = 300
    ws_heartbeat_sec: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### Project Structure Notes

The complete directory structure must match exactly:

```
controlmyentries/
├── .replit
├── replit.nix
├── pyproject.toml
├── Makefile
├── .gitignore
├── .env.example
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── app.py
│   ├── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   └── __init__.py
│   └── models/
│       └── __init__.py
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       └── App.tsx
└── static/              # Will hold frontend build
```

### Naming Conventions

**Python:** snake_case for files, functions, variables; PascalCase for classes
**TypeScript:** PascalCase for component files, camelCase for hooks/utilities

### Python Dependencies (pyproject.toml)

```toml
[project]
name = "controlmyentries"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "python-multipart>=0.0.6",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "polars>=0.20.0",
    "scipy>=1.12.0",
    "xlsxwriter>=3.1.9",
    "websockets>=12.0",
]
```

### Replit Configuration

**.replit:**
```toml
run = "uvicorn api.main:app --host 0.0.0.0 --port 8080"
entrypoint = "api/main.py"

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8080"]
```

**replit.nix:**
```nix
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.nodejs_20
  ];
}
```

### Makefile

```makefile
.PHONY: dev test build lint

dev:
	uvicorn api.app:app --reload --port 8080

test:
	pytest api/tests/ -v

build:
	cd frontend && npm run build && cp -r dist ../static

lint:
	ruff check api/ && cd frontend && npm run lint
```

### References

- [Source: architecture.md#Project Structure]
- [Source: architecture.md#Backend Split Pattern]
- [Source: architecture.md#Initialization Commands]
- [Source: architecture.md#Infrastructure & Deployment]

## Dev Agent Record

### Agent Model Used

(To be filled during implementation)

### Debug Log References

### Completion Notes List

### File List

(To be populated as files are created)
