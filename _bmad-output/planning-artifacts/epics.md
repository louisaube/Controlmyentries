---
stepsCompleted: [1, 2]
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
