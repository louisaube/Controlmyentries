---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - "prd.md"
  - "product-brief-Controlmyentries-2026-02-05.md"
  - "ux-design-specification.md"
workflowType: 'architecture'
project_name: 'Controlmyentries'
user_name: 'BMad'
date: '2026-02-06'
---

# Architecture Decision Document — Controlmyentries

_Ce document se construit collaborativement, étape par étape. Les sections sont ajoutées au fur et à mesure des décisions architecturales._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (33 FR) :**

| Catégorie | FR | Implication archi |
|---|---|---|
| Data Import | FR1-FR7 | File upload, validation, baseline JSON |
| Passe 1 Binaire | FR8-FR11 | 4 détecteurs en pipeline |
| Passe 2 Z-score | FR12-FR15 | Calcul statistique par nœud, fallback mode |
| Passe 3 Rapport | FR16-FR20 | Génération Excel multi-onglets |
| Real-time | FR21-FR23 | WebSocket progression 5 étapes |
| Confiance | FR24-FR26 | Indice confiance, disclaimer |
| Landing | FR27-FR29 | Page SEO séparée |
| Accessibilité | FR30-FR33 | WCAG 2.2 AAA |

**Non-Functional Requirements (28 NFR) :**

| Catégorie | NFR clés | Contrainte archi |
|---|---|---|
| Performance | NFR1-NFR6 | ≤30s traitement, FCP <1.5s, TTI <3s |
| Security | NFR7-NFR12 | Stateless, HTTPS, CORS strict, CSP, zero log data |
| Scalability | NFR13-NFR16 | 10→50 concurrent, queue si saturé |
| Accessibility | NFR17-NFR22 | WCAG 2.2 AAA, 7:1 contraste, 24px targets |
| Reliability | NFR23-NFR26 | 99%/99.9% clôture, atomic output, auto-restart |
| Limits | NFR27-NFR28 | 20Mo max, timeout 5min |

### Scale & Complexity

| Indicateur | Valeur |
|---|---|
| Domaine | Web App SaaS stateless (modèle ilovepdf) |
| Complexité | **Medium** |
| Real-time | WebSocket progression (pas de collab) |
| Multi-tenant | Non (stateless, pas de comptes) |
| Compliance | RGPD simplifié (pas de storage) |
| Intégrations | Aucune (upload manuel) |

### Technical Constraints & Dependencies

**Stack confirmé :**
- Backend : Python + FastAPI (async, WebSocket natif)
- Traitement : Polars (performance), scipy (Z-score), xlsxwriter (Excel)
- Frontend : React SPA (Tailwind + react-dropzone)

**Contraintes :**
1. **Stateless** : aucune persistence serveur, traitement éphémère
2. **Atomic output** : jamais de résultat partiel
3. **File-based baseline** : JSON versionné téléchargé/ré-uploadé par l'utilisateur
4. **Desktop-first** : Chrome/Edge support, mobile non ciblé

### Cross-Cutting Concerns

| Concern | Impact |
|---|---|
| **Error handling** | Validation stricte, messages avec colonnes détectées vs attendues |
| **Progress feedback** | WebSocket 5 étapes + compteur anomalies live |
| **Accessibility** | ARIA partout, keyboard nav, focus management |
| **Security** | HTTPS, CSP, CORS, zero logging, ephemeral processing |
| **File validation** | Format strict, rejet gracieux, limite 20Mo |

### Architectural Decisions (Party Mode)

**Topology : Monolith KISS**
- Single container : FastAPI (API + static SPA servie)
- Pas de split CDN/API — simplicité maximale
- Sizing : **2GB RAM minimum** (10 concurrent × ~80MB per GL)

**Protocol Pattern :**
```
Client ──HTTP POST multipart──> Server (upload files)
Client ──WS connect──> Server
Server ──WS messages──> Client (5 steps + counter)
Server ──WS final──> Client (downloadUrl)
Client ──HTTP GET──> Server (download report)
```
- WebSocket = feedback uniquement, upload = HTTP multipart classique
- Cleanup temp files on response complete

**Testabilité :**
- Endpoint `/api/analyze` sync (sans WebSocket) pour tests automatisés
- Locust + fixtures synthétiques pour load testing

**Baseline Format (versionné) :**
```json
{
  "version": "1.0",
  "generated": "2025-01-15",
  "project": "Controlmyentries",
  "nodes": [...]
}
```

### Delivery Milestones

| Milestone | Scope | Testable |
|---|---|---|
| **M1** | Upload + validation + download stub | ✓ |
| **M2** | Passe 1 : 4 détecteurs binaires | ✓ |
| **M3** | Passe 2 : Z-score + baseline | ✓ |
| **M4** | Passe 3 : Excel multi-onglets | ✓ |
| **M5** | WebSocket progress, landing, WCAG audit | ✓ |

## Starter Template Evaluation

### Primary Technology Domain

**Full-stack Web App SaaS stateless** — Backend Python/FastAPI + Frontend React SPA

### Starter Options Considered

**Backend :**
- FastAPI vanilla (structure manuelle) → **Sélectionné** — simplicité maximale pour app stateless
- tiangolo/full-stack-fastapi-template → Rejeté — inclut PostgreSQL, Auth, migrations (inutile)

**Frontend :**
- Vite + React + TypeScript → **Sélectionné** — build rapide, moderne, léger
- Create React App → Rejeté — déprécié, build lent
- Next.js → Rejeté — SSR/SSG inutile pour SPA servie en static

### Selected Approach: Minimal Custom Structure

**Rationale :**
- App stateless simple = pas besoin de starter complexe
- FastAPI vanilla + Vite React = contrôle total, zéro cruft
- Monolith : FastAPI sert le build React en static

### Initialization Commands

**Backend :**
```bash
mkdir -p api/{core,services,models}
pip install fastapi uvicorn[standard] python-multipart polars scipy xlsxwriter websockets
```

**Frontend :**
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install tailwindcss postcss autoprefixer react-dropzone
npx tailwindcss init -p
```

### Project Structure

```
controlmyentries/
├── api/
│   ├── main.py              # FastAPI app + routes
│   ├── core/
│   │   ├── config.py        # Settings
│   │   └── websocket.py     # WS manager
│   ├── services/
│   │   ├── validator.py     # File validation
│   │   ├── pass1.py         # Binary tests
│   │   ├── pass2.py         # Z-score
│   │   └── pass3.py         # Excel generation
│   └── models/
│       ├── baseline.py      # Baseline schema
│       └── analysis.py      # Analysis result
├── frontend/
│   ├── src/
│   │   ├── components/      # 5 UI components
│   │   ├── hooks/           # useWebSocket, useFileUpload
│   │   └── App.tsx
│   └── dist/                # Build output → served by FastAPI
├── .replit               # Run command + deployment
├── replit.nix            # Nix packages
├── pyproject.toml        # Python dependencies
└── README.md
```

### Architectural Decisions Provided

| Decision | Choice | Rationale |
|---|---|---|
| Language Backend | Python 3.11+ | Polars/scipy ecosystem |
| Language Frontend | TypeScript | Type safety |
| Styling | Tailwind CSS | Design tokens définis UX spec |
| Build Tool | Vite | Fast HMR, optimized builds |
| Testing | pytest (back) + Vitest (front) | Native to each ecosystem |
| Linting | ruff (back) + ESLint (front) | Fast, modern |

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation) :**
- Stateless architecture : aucune persistence serveur ✓
- File validation strategy : whitelist MIME + extension ✓
- WebSocket + HTTP fallback pour progress ✓

**Important Decisions (Shape Architecture) :**
- Pydantic pour validation schéma ✓
- React state local (pas de Redux) ✓
- Replit pour hosting ✓

**Deferred Decisions (Post-MVP) :**
- Rate limiting (si abuse détecté)
- Custom domain
- Multi-region (si besoin)

### Data Architecture

| Decision | Choice | Rationale |
|---|---|---|
| Database | None | Stateless, traitement éphémère |
| Validation | Pydantic 2.x | FastAPI natif, type safety |
| Baseline format | JSON versionné | Client-side storage |
| Temp files | Python tempfile | Auto-cleanup on process |

### Authentication & Security

| Decision | Choice | Rationale |
|---|---|---|
| Authentication | None (MVP) | Pas de comptes utilisateurs |
| Transport | HTTPS | Fourni par Replit |
| CSP | `default-src 'self'` | Scripts same-origin |
| CORS | Same-domain only | API et SPA colocalisés |
| File validation | MIME whitelist | Excel/CSV uniquement |

### API & Communication Patterns

**Endpoints :**
```
POST /api/analyze          # Upload GL + baseline → rapport
POST /api/generate-baseline # Upload GL N-1 → baseline JSON
GET  /api/health           # Health check
WS   /ws/progress/{job_id} # Real-time progress
```

**Error Response Format (RFC 7807) :**
```json
{
  "type": "validation_error",
  "title": "Colonnes manquantes",
  "status": 400,
  "detail": "Colonnes attendues: Date, Compte, Montant"
}
```

### Frontend Architecture

| Decision | Choice | Rationale |
|---|---|---|
| State management | useState/useReducer | 5 composants, flux linéaire |
| Data fetching | Native fetch | Pas de cache (stateless) |
| Routing | None (SPA state machine) | Single page |
| WebSocket | Native WebSocket API | Simple |

### Infrastructure & Deployment

| Decision | Choice | Rationale |
|---|---|---|
| Platform | **Replit (Hacker plan)** | Zéro config, IDE intégré, 2GB RAM |
| CI/CD | **Replit auto-deploy** | Push GitHub = deploy |
| Container | **None** | Runtime Nix natif |
| Config | **replit.nix + .replit** | Standard Replit |
| Monitoring | **Replit metrics** | Intégré |
| Secrets | **Replit Secrets** | UI intégrée |

**Configuration Replit :**

`.replit` :
```toml
run = "uvicorn api.main:app --host 0.0.0.0 --port 8080"
entrypoint = "api/main.py"

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8080"]
```

`replit.nix` :
```nix
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.nodejs_20
  ];
}
```

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Conflits potentiels identifiés :** 12 zones où les agents AI pourraient décider différemment

### Naming Patterns

**Python (Backend) :**

| Élément | Convention | Exemple |
|---|---|---|
| Fichiers | snake_case | `file_validator.py` |
| Classes | PascalCase | `class AnalysisResult` |
| Fonctions | snake_case | `def validate_file()` |
| Variables | snake_case | `anomaly_count` |
| Constants | UPPER_SNAKE | `MAX_FILE_SIZE` |

**TypeScript (Frontend) :**

| Élément | Convention | Exemple |
|---|---|---|
| Fichiers composants | PascalCase | `DropZone.tsx` |
| Fichiers hooks | camelCase | `useWebSocket.ts` |
| Composants | PascalCase | `function DropZone()` |
| Variables/fonctions | camelCase | `const anomalyCount` |
| Types/Interfaces | PascalCase | `interface AnalysisState` |

**API :**

| Élément | Convention | Exemple |
|---|---|---|
| Endpoints | kebab-case, pluriel si collection | `/api/analyze`, `/api/health` |
| Query params | snake_case | `?job_id=123` |
| JSON fields | snake_case | `{ "anomaly_count": 12 }` |

### Structure Patterns

**Backend (`api/`) :**
```
api/
├── main.py           # FastAPI app, routes, static mount
├── core/
│   ├── config.py     # Pydantic settings
│   └── websocket.py  # ConnectionManager
├── services/
│   ├── validator.py  # File validation
│   ├── pass1.py      # Binary detectors
│   ├── pass2.py      # Z-score analysis
│   └── pass3.py      # Excel generation
├── models/
│   ├── baseline.py   # Pydantic schemas
│   └── analysis.py   # Response models
└── tests/
    └── test_*.py     # Tests par service
```

**Frontend (`frontend/src/`) :**
```
src/
├── components/
│   ├── DropZone.tsx
│   ├── FileCard.tsx
│   ├── ProgressTracker.tsx
│   ├── ResultCard.tsx
│   └── StatusMessage.tsx
├── hooks/
│   ├── useWebSocket.ts
│   └── useFileUpload.ts
├── types/
│   └── index.ts      # Shared types
├── App.tsx
└── main.tsx
```

### Format Patterns

**API Response (succès) :**
```json
{
  "success": true,
  "data": { ... }
}
```

**API Response (erreur RFC 7807) :**
```json
{
  "type": "validation_error",
  "title": "Colonnes manquantes",
  "status": 400,
  "detail": "Colonnes attendues: Date, Compte, Montant"
}
```

**WebSocket Message :**
```json
{
  "step": 3,
  "step_name": "Analyse Z-score",
  "progress": 0.6,
  "anomalies_found": 7,
  "status": "processing"
}
```

**Dates :** ISO 8601 (`"2025-01-15T10:30:00Z"`)

### Communication Patterns

**État Frontend (TypeScript) :**
```typescript
type AppState = 'idle' | 'uploading' | 'processing' | 'complete' | 'error';

interface AppContext {
  state: AppState;
  files: UploadedFile[];
  progress: ProgressData | null;
  result: AnalysisResult | null;
  error: ErrorData | null;
}
```

**Transitions d'état valides :**
```
idle → uploading → processing → complete
                       ↓
idle ← ─────────── error
```

### Process Patterns

**Error Handling Backend :**
```python
# Toujours utiliser HTTPException avec RFC 7807
raise HTTPException(
    status_code=400,
    detail={
        "type": "validation_error",
        "title": "Format invalide",
        "detail": f"Colonnes attendues: {expected}, détectées: {found}"
    }
)
```

**Error Handling Frontend :**
```typescript
// Toujours setState error + afficher StatusMessage
catch (err) {
  setState('error');
  setError({ type: 'network', message: err.message });
}
```

**Loading States :**
- Backend : jamais de spinner côté serveur
- Frontend : skeleton si > 100ms, sinon rien

### Enforcement Guidelines

**Tous les agents AI DOIVENT :**

1. Utiliser snake_case pour le Python, camelCase pour le TypeScript
2. Retourner RFC 7807 pour toutes les erreurs API
3. Utiliser les types Pydantic (back) et TypeScript (front) — jamais de `any`
4. Placer les tests dans `api/tests/`
5. Utiliser `tempfile` pour les fichiers temporaires

**Vérification :**
- `ruff check` (Python) + `eslint` (TypeScript) en pre-commit
- Types stricts : `mypy --strict` + `tsc --strict`

### Anti-Patterns à éviter

| Anti-Pattern | Correct |
|---|---|
| `any` en TypeScript | Type explicite |
| `print()` pour debug | `logging.info()` |
| Path hardcodé `/tmp/file.xlsx` | `tempfile.NamedTemporaryFile()` |
| Catch exception silencieux | Raise HTTPException avec detail |
| `useState` pour chaque champ | Un seul `useReducer` pour l'état global |

