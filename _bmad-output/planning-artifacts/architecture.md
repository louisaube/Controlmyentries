---
stepsCompleted: [1, 2]
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

