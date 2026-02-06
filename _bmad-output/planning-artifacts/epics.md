---
stepsCompleted: [1, 2, 3, 4]
status: 'complete'
completedAt: '2026-02-06'
inputDocuments:
  - "prd.md"
  - "architecture.md"
  - "ux-design-specification.md"
---

# Controlmyentries - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Controlmyentries, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Data Import & Validation (FR1-FR7)**
- FR1: L'utilisateur peut uploader un fichier Excel contenant un export du Grand Livre (GL)
- FR2: Le système valide le fichier pour la présence des colonnes requises (Compte Général, Section Analytique, Montant, Date/Période)
- FR3: Le système rejette les fichiers invalides avec un message d'erreur listant colonnes détectées vs attendues
- FR4: L'utilisateur peut uploader un fichier baseline pré-calculé (JSON) pour la comparaison statistique
- FR5: L'utilisateur peut générer un fichier baseline en uploadant un GL N-1 complet (12 mois)
- FR6: Le système produit un fichier baseline téléchargeable conservé sur le poste de l'utilisateur
- FR7: L'utilisateur peut soumettre simultanément baseline + GL du mois courant pour lancer l'analyse

**Anomaly Detection — Pass 1 (FR8-FR11)**
- FR8: Le système détecte la disparition d'un nœud (actif les mois précédents, absent au mois M)
- FR9: Le système détecte l'apparition d'un nœud (absent de l'historique, présent au mois M)
- FR10: Le système détecte une variation brute (écart > 20% par rapport à la tendance)
- FR11: Le système détecte une interruption de récurrence (suite d'écritures régulières qui s'arrête)

**Anomaly Detection — Pass 2 (FR12-FR15)**
- FR12: Le système calcule un Z-score adaptatif par nœud (moyenne et écart-type propres à chaque nœud Compte G × Analytique)
- FR13: Le système compare M vs M-12 pour neutraliser la saisonnalité
- FR14: Le système signale les anomalies dont |Z| > 2
- FR15: Le système fonctionne en mode dégradé (Passe 1 seule) lorsque la baseline est insuffisante

**Report Generation — Pass 3 (FR16-FR20)**
- FR16: Le système génère un fichier Excel enrichi avec un onglet par anomalie confirmée
- FR17: Chaque onglet contient un constat factuel de Niveau 1 (description de l'anomalie)
- FR18: Chaque onglet contient les données statistiques de Niveau 2 (Z-score, moyenne, écart-type, historique)
- FR19: Le système génère un onglet Synthèse avec métriques agrégées (nombre, types, répartition)
- FR20: L'utilisateur peut télécharger le rapport au format Excel

**Real-Time Processing Feedback (FR21-FR23)**
- FR21: Le système affiche une barre de progression pendant le traitement
- FR22: Le système communique les étapes en temps réel (validation, Passe 1, Passe 2, Passe 3, terminé)
- FR23: Le système affiche le temps de traitement total à la fin de l'analyse

**Confidence & Transparency (FR24-FR26)**
- FR24: Le système affiche un indice de confiance (%) basé sur le nombre de mois d'historique disponibles
- FR25: Le système affiche un disclaimer permanent : « Aide à la détection, pas certificat d'absence d'anomalie »
- FR26: Le système montre la base statistique de chaque détection (données chiffrées, pas de boîte noire)

**Landing Page & Product Discovery (FR27-FR29)**
- FR27: Les visiteurs accèdent à une landing page présentant le produit, les cas d'usage et la proposition de valeur
- FR28: La landing page atteint un score Lighthouse SEO ≥ 90 et inclut meta tags, Open Graph, et structured data
- FR29: La landing page contient un appel à l'action dirigeant vers l'outil

**Accessibility (FR30-FR33)**
- FR30: Toutes les interactions sont accessibles via navigation clavier
- FR31: Le système fournit une alternative au drag-and-drop pour l'upload
- FR32: Le système annonce les changements d'état aux lecteurs d'écran
- FR33: Les messages d'erreur sont programmatiquement liés à leur source

### NonFunctional Requirements

**Performance (NFR1-NFR6)**
- NFR1: Traitement end-to-end ≤ 30 secondes pour un GL de 500 nœuds / 50 000 lignes
- NFR2: Traitement ≤ 2 minutes pour un GL de 1 000 000 de lignes
- NFR3: Barre de progression mise à jour au moins toutes les 5 secondes
- NFR4: First Contentful Paint < 1.5 seconde
- NFR5: Time to Interactive < 3 secondes
- NFR6: Génération Excel de sortie < 5 secondes

**Security (NFR7-NFR12)**
- NFR7: HTTPS (TLS 1.2+) pour toutes les communications
- NFR8: Aucune donnée comptable persistée côté serveur (architecture stateless)
- NFR9: Logs métadonnées uniquement — jamais de valeurs comptables
- NFR10: Aucun fichier conservé après téléchargement
- NFR11: CSP interdit les scripts externes non contrôlés
- NFR12: CORS strict (même domaine uniquement)

**Scalability (NFR13-NFR16)**
- NFR13: 10 traitements simultanés au MVP
- NFR14: 50 traitements simultanés à 12 mois sans dégradation > 20%
- NFR15: Traitement isolé par requête
- NFR16: File d'attente activée au-delà du seuil

**Accessibility (NFR17-NFR22)**
- NFR17: Interface WCAG 2.2 AAA
- NFR18: Contraste ≥ 7:1 texte normal, ≥ 4.5:1 texte large
- NFR19: Toutes fonctionnalités utilisables au clavier seul
- NFR20: Changements d'état annoncés via ARIA live regions
- NFR21: Cibles interactives ≥ 24×24 pixels
- NFR22: Texte redimensionnable à 200% sans perte

**Reliability (NFR23-NFR26)**
- NFR23: Disponibilité 99% heures ouvrées, 99.9% période de clôture
- NFR24: Sortie atomique — jamais de résultat partiel
- NFR25: Redémarrage automatique en cas de crash serveur
- NFR26: Temps de rétablissement < 30 minutes

**File Limits & Timeouts (NFR27-NFR28)**
- NFR27: Rejet des fichiers > 20 Mo avec message explicite
- NFR28: Timeout 5 minutes par traitement

### Additional Requirements

**From Architecture:**
- Starter: FastAPI + Vite React + Tailwind (no Docker, Replit deployment)
- Backend split pattern: main.py / app.py / routes.py
- 5 services: validator.py, pass1.py, pass2.py, pass3.py, websocket.py
- 5 frontend components: DropZone, FileCard, ProgressTracker, ResultCard, StatusMessage
- API endpoints: POST /api/analyze, POST /api/generate-baseline, GET /api/health, WS /ws/progress/{job_id}
- Error format: RFC 7807
- State management: React useState/useReducer (state machine)

**From UX Design:**
- Single drop zone accepting 1-2 files with auto-detection via dates
- WebSocket 5-step progression with live anomaly counter
- WCAG 2.2 AAA compliance (7:1 contrast, 24px targets)
- Skeleton loading if > 100ms
- Double-submit prevention on buttons
- Session persistence (sessionId + 15min TTL)

### FR Coverage Map

| FR | Epic | Description |
|---|---|---|
| FR1 | Epic 2 | Upload Excel GL |
| FR2 | Epic 2 | Validation colonnes |
| FR3 | Epic 2 | Rejet avec message |
| FR4 | Epic 3 | Upload baseline JSON |
| FR5 | Epic 3 | Générer baseline depuis N-1 |
| FR6 | Epic 3 | Download baseline |
| FR7 | Epic 6 | Soumettre baseline + GL |
| FR8 | Epic 4 | Disparition nœud |
| FR9 | Epic 4 | Apparition nœud |
| FR10 | Epic 4 | Variation brute |
| FR11 | Epic 4 | Interruption récurrence |
| FR12 | Epic 4 | Z-score adaptatif |
| FR13 | Epic 4 | Comparaison M vs M-12 |
| FR14 | Epic 4 | Signalement |Z| > 2 |
| FR15 | Epic 4 | Mode dégradé |
| FR16 | Epic 5 | Excel multi-onglets |
| FR17 | Epic 5 | Niveau 1 constat |
| FR18 | Epic 5 | Niveau 2 statistiques |
| FR19 | Epic 5 | Onglet Synthèse |
| FR20 | Epic 5 | Download rapport |
| FR21 | Epic 7 | Barre progression |
| FR22 | Epic 7 | Étapes temps réel |
| FR23 | Epic 7 | Temps total |
| FR24 | Epic 8 | Indice confiance |
| FR25 | Epic 8 | Disclaimer |
| FR26 | Epic 8 | Base statistique visible |
| FR27 | Epic 9 | Landing page |
| FR28 | Epic 9 | Lighthouse SEO ≥ 90 |
| FR29 | Epic 9 | CTA vers outil |
| FR30 | Epic 10 | Navigation clavier |
| FR31 | Epic 2 | Alternative drag-drop |
| FR32 | Epic 10 | Annonces screen reader |
| FR33 | Epic 10 | Erreurs liées source |

## Epic List

### Epic 1: Project Skeleton
Infrastructure de base fonctionnelle pour le développement.
**FRs covered:** Aucun (prérequis technique)
**Scope:** Setup Replit, api/, frontend/, health check, static serving

### Epic 2: File Upload & Validation
L'utilisateur peut uploader un GL et voir s'il est valide.
**FRs covered:** FR1, FR2, FR3, FR31
**Scope:** DropZone, FileCard, validation colonnes, messages d'erreur

### Epic 3: Baseline Management
L'utilisateur peut créer sa baseline pour les analyses futures.
**FRs covered:** FR4, FR5, FR6
**Scope:** Upload GL N-1, calcul statistiques, download baseline.json

### Epic 4: Anomaly Detection Engine
Le système détecte les anomalies dans le GL (Pass 1 + Pass 2).
**FRs covered:** FR8, FR9, FR10, FR11, FR12, FR13, FR14, FR15
**Scope:** 4 détecteurs binaires, Z-score adaptatif, mode dégradé

### Epic 5: Report Generation
L'utilisateur télécharge un rapport Excel exploitable.
**FRs covered:** FR16, FR17, FR18, FR19, FR20
**Scope:** Excel multi-onglets, Niveau 1+2, Synthèse DAF

### Epic 6: Full Analysis Flow
Sophie peut faire son contrôle mensuel end-to-end.
**FRs covered:** FR7
**Scope:** Upload baseline + GL → pipeline complet → rapport

### Epic 7: Real-Time Feedback
L'utilisateur voit la progression pendant le traitement.
**FRs covered:** FR21, FR22, FR23
**Scope:** WebSocket, 5 étapes, compteur anomalies, temps total

### Epic 8: Trust & Transparency
L'utilisateur comprend et fait confiance aux résultats.
**FRs covered:** FR24, FR25, FR26
**Scope:** Indice confiance, disclaimer, données statistiques visibles

### Epic 9: Landing Page
Les prospects découvrent le produit.
**FRs covered:** FR27, FR28, FR29
**Scope:** Page SEO, meta tags, Open Graph, CTA

### Epic 10: Accessibility Polish
Tous les utilisateurs peuvent utiliser l'outil.
**FRs covered:** FR30, FR32, FR33
**Scope:** WCAG 2.2 AAA, clavier, ARIA, focus management

---

## Epic 1: Project Skeleton

### Story 1.1: Initialize Replit Project Structure

As a **developer**,
I want **a properly configured Replit project with Python backend and React frontend structure**,
So that **I can start implementing features immediately**.

**Acceptance Criteria:**

**Given** a new Replit project
**When** I open the workspace
**Then** the following structure exists:
- `api/main.py`, `api/app.py`, `api/routes.py`
- `api/core/config.py` with Pydantic settings
- `frontend/` with Vite React template
- `.replit` and `replit.nix` configured
- `pyproject.toml` and `package.json`
**And** `make dev` starts the development server

---

### Story 1.2: Health Check Endpoint

As a **operations engineer**,
I want **a health check endpoint**,
So that **I can monitor the application availability**.

**Acceptance Criteria:**

**Given** the API is running
**When** I send GET `/api/health`
**Then** I receive HTTP 200 with `{"status": "ok"}`

---

### Story 1.3: Frontend Skeleton with Static Serving

As a **developer**,
I want **the React frontend skeleton served by FastAPI**,
So that **I have a working full-stack setup**.

**Acceptance Criteria:**

**Given** the frontend is built
**When** I access the root URL `/`
**Then** the React app loads with "Controlmyentries" title

---

## Epic 2: File Upload & Validation

### Story 2.1: DropZone Component

As a **user**,
I want **to drag and drop my GL file onto the page**,
So that **I can easily upload my data**.

**Acceptance Criteria:**

**Given** I am on the main page
**When** I drag a file over the drop zone
**Then** the zone highlights to show it's active
**When** I drop an Excel file (.xlsx, .xls, .csv)
**Then** the file is accepted and shown in a FileCard
**And** a "Choisir fichier(s)" button is available as alternative (FR31)

---

### Story 2.2: File Validation Service

As a **user**,
I want **my file to be validated for correct format**,
So that **I know immediately if something is wrong**.

**Acceptance Criteria:**

**Given** I upload a file
**When** the file has columns: Compte Général, Section Analytique, Montant, Date
**Then** validation passes and FileCard shows green checkmark

**Given** I upload a file with missing columns
**When** validation runs
**Then** I see error message: "Colonnes attendues: X, Y. Détectées: A, B" (FR3)

---

### Story 2.3: Upload API Endpoint

As a **developer**,
I want **a POST /api/analyze endpoint accepting multipart files**,
So that **the frontend can submit files for processing**.

**Acceptance Criteria:**

**Given** a valid file is uploaded
**When** POST /api/analyze is called
**Then** the file is received and validated
**And** a job_id is returned for progress tracking

---

## Epic 3: Baseline Management

### Story 3.1: Generate Baseline Endpoint

As a **user**,
I want **to generate a baseline from my N-1 GL**,
So that **I can use it for future monthly analyses**.

**Acceptance Criteria:**

**Given** I upload a GL N-1 file (12 months of data)
**When** POST /api/generate-baseline is called
**Then** statistics are calculated per node (Compte G × Analytique)
**And** a baseline.json file is generated with version and date (FR5, FR6)

---

### Story 3.2: Baseline Download

As a **user**,
I want **to download my generated baseline**,
So that **I can save it locally and reuse it**.

**Acceptance Criteria:**

**Given** baseline generation is complete
**When** I click "Télécharger la baseline"
**Then** a JSON file downloads with format: `{"version": "1.0", "generated": "...", "nodes": [...]}`

---

### Story 3.3: Baseline Upload for Analysis

As a **user**,
I want **to upload my saved baseline along with current GL**,
So that **the analysis can use my reference data**.

**Acceptance Criteria:**

**Given** I have a baseline.json file
**When** I upload it with my current GL
**Then** both files are accepted
**And** the system auto-detects which is which via dates (FR4)

---

## Epic 4: Anomaly Detection Engine

### Story 4.1: Pass 1 - Disappearance Detector

As a **user**,
I want **the system to detect nodes that disappeared**,
So that **I can find missing entries**.

**Acceptance Criteria:**

**Given** a node was active in previous months
**When** it's absent in month M
**Then** a "Disparition" anomaly is flagged (FR8)

---

### Story 4.2: Pass 1 - Appearance Detector

As a **user**,
I want **the system to detect new nodes**,
So that **I can review unexpected entries**.

**Acceptance Criteria:**

**Given** a node didn't exist in history
**When** it appears in month M with significant amount
**Then** an "Apparition" anomaly is flagged (FR9)

---

### Story 4.3: Pass 1 - Variation Detector

As a **user**,
I want **the system to detect brutal variations**,
So that **I can investigate unusual changes**.

**Acceptance Criteria:**

**Given** a node has historical values
**When** current month varies > 20% from trend
**Then** a "Variation" anomaly is flagged (FR10)

---

### Story 4.4: Pass 1 - Recurrence Detector

As a **user**,
I want **the system to detect broken recurrence patterns**,
So that **I don't miss regular entries**.

**Acceptance Criteria:**

**Given** a node had regular entries (e.g., monthly provision)
**When** the pattern breaks in month M
**Then** a "Récurrence interrompue" anomaly is flagged (FR11)

---

### Story 4.5: Pass 2 - Z-Score Calculator

As a **user**,
I want **statistical calibration of anomalies**,
So that **I get fewer false positives**.

**Acceptance Criteria:**

**Given** a baseline with node statistics
**When** analysis runs
**Then** Z-score is calculated per node using its own mean/stddev (FR12)
**And** M vs M-12 comparison neutralizes seasonality (FR13)
**And** anomalies with |Z| > 2 are flagged (FR14)

---

### Story 4.6: Pass 2 - Degraded Mode

As a **user**,
I want **the system to work even without sufficient baseline**,
So that **I can still get some results**.

**Acceptance Criteria:**

**Given** baseline has < 6 months of data
**When** analysis runs
**Then** only Pass 1 results are shown
**And** a "Confiance limitée" badge is displayed (FR15)

---

## Epic 5: Report Generation

### Story 5.1: Excel Multi-Tab Report

As a **user**,
I want **an Excel report with one tab per anomaly**,
So that **I can review each issue separately**.

**Acceptance Criteria:**

**Given** anomalies are detected
**When** report is generated
**Then** Excel file has one tab per anomaly type (FR16)

---

### Story 5.2: Level 1 - Factual Statement

As a **user**,
I want **each anomaly tab to show the factual finding**,
So that **I understand what was detected**.

**Acceptance Criteria:**

**Given** an anomaly tab
**When** I open it
**Then** I see: node identifier, anomaly type, current value, expected value (FR17)

---

### Story 5.3: Level 2 - Statistical Data

As a **user**,
I want **to see the statistical basis for each anomaly**,
So that **I can judge its significance**.

**Acceptance Criteria:**

**Given** an anomaly with Z-score
**When** I view the tab
**Then** I see: Z-score, mean, stddev, historical values (FR18)

---

### Story 5.4: Synthesis Tab

As a **DAF**,
I want **a summary tab with aggregated metrics**,
So that **I can quickly assess the control quality**.

**Acceptance Criteria:**

**Given** analysis is complete
**When** I open the Synthèse tab
**Then** I see: total anomalies, by type, severity distribution (FR19)

---

### Story 5.5: Report Download

As a **user**,
I want **to download the Excel report**,
So that **I can work with it offline**.

**Acceptance Criteria:**

**Given** report generation is complete
**When** I click "Télécharger le rapport"
**Then** Excel file downloads immediately (FR20)

---

## Epic 6: Full Analysis Flow

### Story 6.1: Integrated Analysis Pipeline

As a **Sophie**,
I want **to submit baseline + GL and get a complete report**,
So that **I can do my monthly control end-to-end**.

**Acceptance Criteria:**

**Given** I upload baseline.json + current GL
**When** I click "Analyser"
**Then** validation → Pass 1 → Pass 2 → Pass 3 runs in sequence
**And** I can download the report when complete (FR7)

---

## Epic 7: Real-Time Feedback

### Story 7.1: WebSocket Progress Connection

As a **developer**,
I want **a WebSocket endpoint for progress updates**,
So that **the frontend can show real-time feedback**.

**Acceptance Criteria:**

**Given** analysis starts
**When** client connects to /ws/progress/{job_id}
**Then** messages are sent for each step

---

### Story 7.2: ProgressTracker Component

As a **user**,
I want **to see a progress bar during processing**,
So that **I know the system is working**.

**Acceptance Criteria:**

**Given** analysis is running
**When** I watch the screen
**Then** I see 5 steps: Validation, Pass 1, Pass 2, Pass 3, Terminé (FR21, FR22)
**And** current step is highlighted with animation

---

### Story 7.3: Live Anomaly Counter

As a **user**,
I want **to see anomalies count as they're detected**,
So that **I have immediate feedback**.

**Acceptance Criteria:**

**Given** Pass 1/2 is running
**When** anomalies are found
**Then** counter updates live with bounce animation

---

### Story 7.4: Processing Time Display

As a **user**,
I want **to see the total processing time**,
So that **I know how fast the analysis was**.

**Acceptance Criteria:**

**Given** analysis completes
**When** ResultCard appears
**Then** total time is displayed: "Analyse terminée en 24s" (FR23)

---

## Epic 8: Trust & Transparency

### Story 8.1: Confidence Index

As a **user**,
I want **to see a confidence index for the analysis**,
So that **I know how reliable the results are**.

**Acceptance Criteria:**

**Given** analysis has baseline
**When** results are shown
**Then** confidence % is displayed based on months of history
**And** if < 6 months: "Confiance limitée" badge (FR24)

---

### Story 8.2: Permanent Disclaimer

As a **user**,
I want **to see a disclaimer about the tool's limitations**,
So that **I don't over-rely on automated detection**.

**Acceptance Criteria:**

**Given** I'm on the tool page
**When** I view results
**Then** I see: "Aide à la détection, pas certificat d'absence d'anomalie" (FR25)

---

### Story 8.3: Statistical Transparency

As a **user**,
I want **to see the data behind each detection**,
So that **I can verify the tool's reasoning**.

**Acceptance Criteria:**

**Given** an anomaly is detected
**When** I view details
**Then** I see all statistical inputs (mean, stddev, Z-score, historical values) (FR26)

---

## Epic 9: Landing Page

### Story 9.1: SEO-Optimized Landing Page

As a **prospect**,
I want **to find Controlmyentries via search**,
So that **I can discover the tool**.

**Acceptance Criteria:**

**Given** a search for "contrôle comptable automatique"
**When** results appear
**Then** Controlmyentries landing page is indexed (FR27)
**And** Lighthouse SEO score ≥ 90 (FR28)

---

### Story 9.2: Landing Page Content

As a **prospect**,
I want **to understand what the tool does**,
So that **I can decide if it's useful**.

**Acceptance Criteria:**

**Given** I land on the page
**When** I read the content
**Then** I understand: problem, solution, how it works, testimonials
**And** meta tags and Open Graph are set for LinkedIn sharing

---

### Story 9.3: Call to Action

As a **prospect**,
I want **a clear CTA to try the tool**,
So that **I can start using it**.

**Acceptance Criteria:**

**Given** I'm on the landing page
**When** I click "Essayer gratuitement"
**Then** I'm redirected to the tool (FR29)

---

## Epic 10: Accessibility Polish

### Story 10.1: Keyboard Navigation

As a **keyboard user**,
I want **to use the entire tool without a mouse**,
So that **I can complete my workflow**.

**Acceptance Criteria:**

**Given** I'm on the tool
**When** I use Tab, Enter, Escape
**Then** I can: upload files, start analysis, download report (FR30)
**And** focus is always visible with 2px ring

---

### Story 10.2: Screen Reader Announcements

As a **screen reader user**,
I want **state changes to be announced**,
So that **I know what's happening**.

**Acceptance Criteria:**

**Given** I use a screen reader
**When** progress updates or errors occur
**Then** I hear announcements via aria-live regions (FR32)

---

### Story 10.3: Error Accessibility

As a **user with disabilities**,
I want **errors to be properly linked to their source**,
So that **I can fix issues easily**.

**Acceptance Criteria:**

**Given** a validation error occurs
**When** it's displayed
**Then** it's linked to the input via aria-describedby (FR33)
**And** role="alert" announces it immediately
