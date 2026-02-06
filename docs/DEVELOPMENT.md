# Development Guide

## Quick Start

```bash
# Install dependencies
make install

# Start development server
make dev

# Run tests
make test

# Build frontend
make build
```

## Project Structure

```
controlmyentries/
├── api/          # FastAPI backend
├── frontend/     # React SPA
├── static/       # Frontend build (served by FastAPI)
└── docs/         # Documentation
```

## Development Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start dev server with hot reload |
| `make test` | Run pytest |
| `make lint` | Run ruff + eslint |
| `make build` | Build frontend to static/ |
| `make check` | Full lint + typecheck + test |
