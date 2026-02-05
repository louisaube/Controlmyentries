---
stepsCompleted: [1, 2, 3]
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

## Core User Experience

### Defining Experience

L'expérience Controlmyentries se résume en une phrase : **"Dépose. Attends 30 secondes. Découvre."**

L'action core est l'upload + lancement d'analyse. C'est le seul point d'interaction significatif. Tout le reste (landing page, onboarding, download) est au service de cette action unique. Le produit n'a qu'une seule page fonctionnelle.

Le modèle mental est celui du **photocopieur intelligent** : on pose le document, on appuie sur le bouton, on récupère le résultat enrichi.

### Platform Strategy

| Aspect | Décision |
|---|---|
| Plateforme | Web SPA, navigateur uniquement |
| Navigateurs | Chrome, Edge (support primaire), Firefox, Safari (dégradé gracieux) |
| Input | Souris + clavier (desktop-first) |
| Offline | Non requis (traitement serveur obligatoire) |
| Responsive | Desktop optimisé, tablette fonctionnel, mobile non ciblé MVP |
| Capacités device | Drag-and-drop fichier (avec alternative clavier/bouton) |

### Effortless Interactions

1. **Upload** : drag-and-drop au centre de l'écran, zone visuellement dominante. Un fichier tombe → l'analyse commence. Aucun bouton "Lancer" séparé si possible.
2. **Baseline** : pour l'utilisateur récurrent, le flow est "2 fichiers → résultat". Le système guide visuellement (zone 1 : baseline, zone 2 : GL mensuel).
3. **Download** : le rapport Excel se télécharge automatiquement dès qu'il est prêt. Pas de page de résultats intermédiaire — le livrable EST le fichier Excel.
4. **Erreur** : fichier invalide → message inline immédiat avec colonnes détectées vs attendues + bouton "Réessayer" visible. Pas de page d'erreur séparée.
5. **Retour mensuel** : le navigateur se souvient du dernier baseline.json utilisé (localStorage). Sophie retrouve son contexte instantanément.

### Critical Success Moments

| Moment | Ce qui se passe | Risque si raté |
|---|---|---|
| **Premier upload** | Sophie dépose son GL N-1, voit la progression, obtient son baseline.json | Abandon définitif si confusion ou erreur |
| **Progression en temps réel** | Les 5 étapes défilent (validation → Passe 1 → 2 → 3 → terminé) avec compteur d'anomalies | L'utilisateur pense que l'outil a planté |
| **Ouverture du rapport** | Sophie ouvre l'Excel, voit l'onglet Synthèse : "12 anomalies détectées" | Si le rapport est confus, la valeur n'est pas perçue |
| **Découverte d'anomalie inconnue** | Sophie ouvre un onglet et trouve un oubli de CCA qu'elle n'avait pas repéré | C'est le "aha" — si ça n'arrive pas, le produit n'a pas prouvé sa valeur |
| **Retour M+1** | Sophie revient le mois suivant, retrouve son baseline, relance en 10 secondes | Si le baseline est perdu, friction de réonboarding |

### Experience Principles

1. **Une page, un but** : pas de navigation, pas de menu, pas de dashboard. L'outil fait UNE chose et la fait très bien. (Modèle ilovepdf)
2. **Montre, ne demande pas** : l'outil détecte automatiquement, sans configuration utilisateur au MVP. Pas de seuils à régler, pas de paramètres. Le Z-score s'adapte seul.
3. **Confiance par la transparence** : chaque détection montre ses données (Z-score, moyenne, écart-type, historique). Pas de boîte noire. L'utilisateur peut vérifier et apprendre.
4. **Disclosure progressive** : interface minimaliste en surface → richesse statistique dans le rapport Excel. La complexité est dans le livrable, pas dans l'outil.
5. **L'attente est le spectacle** : les 30 secondes de traitement ne sont pas un "temps mort" mais un moment de revelation progressive (compteur d'anomalies, étapes franchies).
