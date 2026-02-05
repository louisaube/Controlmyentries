---
stepsCompleted: [1, 2]
inputDocuments:
  - "prd.md"
  - "product-brief-Controlmyentries-2026-02-05.md"
  - "prd-validation-report.md"
---

# UX Design Specification — Controlmyentries

**Author:** Louis Aubé
**Date:** 2026-02-05

---

## Executive Summary

### Project Vision

Controlmyentries est un outil web SaaS stateless (modèle ilovepdf) de détection automatique d'anomalies comptables. L'expérience UX cible est la simplicité radicale : upload → attente engageante (≤30s) → téléchargement d'un rapport Excel enrichi. Zéro inscription, zéro persistance, zéro friction.

### Target Users

- **Sophie** (persona primaire) : contrôleuse de gestion, réseau de crèches, clôture mensuelle, GL 500+ nœuds, desktop au bureau. Expertise comptable forte, tech-savvy moyenne. Frustrée par le contrôle visuel TCD (4h, oublis fréquents).
- **Marc** (variante) : chef comptable PME, GL plus petit (~100 nœuds), même workflow simplifié.
- **DAF** (secondaire) : consommateur des résultats, lit l'onglet Synthèse du rapport Excel. N'utilise pas l'outil directement.

### Key Design Challenges

1. **Double upload & concept de baseline** : l'utilisateur doit comprendre et gérer deux fichiers (baseline.json + GL mensuel). L'onboarding première utilisation (génération de baseline depuis GL N-1) est le principal point de friction.
2. **Attente de 30 secondes engageante** : transformer une attente passive en anticipation active via feedback temps réel (5 étapes WebSocket, barre de progression, compteur d'anomalies).
3. **WCAG 2.2 AAA sans compromis esthétique** : contraintes de contraste (7:1), tailles de cibles (24×24px), navigation clavier intégrale. Doit rester visuellement professionnel.
4. **Gestion de fichier côté client** : baseline.json stocké sur le poste de l'utilisateur entre les clôtures mensuelles. Risque de perte ou confusion.

### Design Opportunities

1. **Simplicité radicale** : une page, une action, valeur immédiate. Drop zone dominante, zéro navigation complexe.
2. **Moment "aha" orchestré** : compteur d'anomalies détectées en temps réel pendant le traitement → révélation progressive de la valeur.
3. **Accessibilité comme identité** : typographie forte, contrastes nets, palette épurée = sérieux comptable + WCAG AAA natif.
4. **Desktop-first** : espace généreux pour des visualisations claires du processus et des états.
