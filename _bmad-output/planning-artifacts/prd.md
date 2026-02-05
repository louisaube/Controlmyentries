---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success]
inputDocuments:
  - "product-brief-Controlmyentries-2026-02-05.md"
workflowType: 'prd'
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 0
classification:
  projectType: web_app
  domain: general (contrôle de gestion / comptabilité analytique)
  complexity: medium
  projectContext: greenfield
  coreStack: "Python + Polars + xlsxwriter + scipy"
  performanceNote: "Polars choisi pour la vitesse de traitement"
---

# Product Requirements Document - Controlmyentries

**Author:** BMad
**Date:** 2026-02-05

## Success Criteria

### User Success

- **Le moment "aha!"** : Sophie uploade son GL Excel, voit une barre de progression pendant ~30s, puis télécharge un fichier enrichi avec un onglet par anomalie. En ouvrant le premier onglet, elle identifie en quelques secondes un oubli qu'elle aurait mis des heures à repérer visuellement dans son TCD.
- **Temps de contrôle** : de 4 heures de contrôle visuel à ~45 minutes de revue ciblée des anomalies (facteur ×5 minimum).
- **Autonomie** : l'Excel de sortie est compréhensible sans formation. Les niveaux 1 (constat brut) et 2 (calibrage statistique) fournissent assez d'information pour décider.
- **Confiance** : 0% de faux négatifs sur les anomalies connues du contrôleur.
- **Découverte nette** : l'outil détecte des anomalies que le contrôleur n'avait pas encore identifiées — c'est la vraie valeur ajoutée au-delà de la simple automatisation.

### Business Success

- **3 mois (pilote)** : validation fonctionnelle sur données réelles d'une structure. Les 4 cas de détection (disparition, apparition, variation, récurrence) sont confirmés. Le contrôleur gagne du temps mesurable → Go pour la suite.
- **6 mois** : 3 contrôleurs dans 2 structures différentes utilisent l'outil à chaque clôture mensuelle.
- **12 mois** : 10 contrôleurs dans 5 structures, taux de rétention > 80% (ceux qui commencent continuent).
- **Monétisation** : à définir post-pilote. Le marché est « mal adressé commercialement » — l'objectif initial est de prouver la valeur.

### Technical Success

- **Performance** : traitement complet (upload → calcul → génération Excel) ≤ 30 secondes pour un GL standard. Approche KISS — une seule métrique end-to-end.
- **Scalabilité** : GL standard entre 200 et 1 000 000 de lignes. Le moteur Polars doit gérer cette plage sans dégradation critique.
- **Détection** : les 4 tests binaires (Passe 1) + Z-score adaptatif (Passe 2) fonctionnent sur données réelles.
- **Fiabilité** : faux positifs < 10% de l'ensemble des alertes générées. Seuil d'utilisabilité : si l'outil génère plus de 50 alertes sur une clôture, le taux de faux positifs doit baisser proportionnellement pour rester exploitable.
- **Baseline** : chargement de l'année N-1 comme référence statistique, une seule fois en début d'exercice.

### Measurable Outcomes

| Métrique | Cible MVP | Méthode de mesure |
|---|---|---|
| Temps de traitement end-to-end | ≤ 30s (GL standard) | Chronomètre intégré |
| Faux positifs | < 10% des alertes | Revue manuelle |
| Faux négatifs | 0% sur anomalies connues | Comparaison avec contrôle visuel |
| Découverte nette | ≥ 1 anomalie inconnue par clôture | Feedback utilisateur |
| Temps de contrôle utilisateur | De 4h à ~45min (×5) | Avant/après sur même clôture |
| Alertes max par clôture | ≤ 50 (seuil d'utilisabilité) | Comptage automatique |
| Adoption pilote (3 mois) | 1 structure, usage mensuel | Suivi d'utilisation |
| Adoption 6 mois | 3 contrôleurs, 2 structures | Nombre d'utilisateurs actifs |
| Adoption 12 mois | 10 contrôleurs, 5 structures, rétention > 80% | Suivi d'utilisation |

## Product Scope

### MVP - Minimum Viable Product

- Web app : upload Excel GL → traitement → téléchargement Excel enrichi
- Import Excel du GL + chargement baseline N-1
- Passe 1 : 4 tests binaires (disparition, apparition, variation >20%, récurrence)
- Passe 2 : Z-score adaptatif par nœud, comparaison M-12, seuil |Z| > 2
- Passe 3 : niveaux 1 (constat brut) et 2 (calibrage statistique) uniquement
- Sortie Excel enrichi avec un onglet par anomalie confirmée

### Growth Features (Post-MVP)

- Niveau 3 IA : pistes d'investigation LLM avec disclaimer
- Interface de configuration des seuils par nœud
- Zoom PCG pour contextualisation
- Affinage automatique basé sur feedback utilisateur (faux positifs marqués)

### Vision (Future)

- Dashboard web avec suivi historique des contrôles
- Connecteurs ERP natifs (SAP, Sage)
- Gestion multi-sociétés et consolidation
- API pour intégration dans les workflows existants
- Export PDF et reporting automatisé
