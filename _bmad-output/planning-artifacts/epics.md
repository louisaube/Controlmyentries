---
stepsCompleted: [1]
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

{{requirements_coverage_map}}

## Epic List

{{epics_list}}
