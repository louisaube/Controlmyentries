---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys]
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

## User Journeys

### Parcours 1 — Sophie, le contrôle mensuel (happy path)

**Scène d'ouverture** : Vendredi 5 décembre, 14h. Sophie vient de recevoir l'export GL du mois de novembre pour ses 8 crèches. Avant Controlmyentries, elle ouvrait son TCD géant, comparait visuellement les colonnes mois par mois, ligne par ligne. 4 heures de travail répétitif, les yeux fatigués, avec la peur permanente de rater un oubli.

**Action montante** : Sophie ouvre Controlmyentries dans son navigateur. Elle uploade le fichier GL de novembre (150 000 lignes). La barre de progression avance. 25 secondes plus tard, un bouton « Télécharger le rapport » apparaît.

**Climax** : Sophie ouvre l'Excel. Premier onglet : « Disparition — 6061×CRECHE03 ». Le constat : *« Ce nœud était actif de janvier à octobre (moyenne 2 400€/mois) et a disparu en novembre. Z-score : -3.2 »*. Sophie reconnaît immédiatement : c'est le loyer de la crèche des Lilas, la comptable a oublié de passer l'écriture. En 10 secondes, elle a trouvé ce qui lui aurait pris 45 minutes à repérer.

**Résolution** : En 40 minutes au lieu de 4 heures, Sophie a revu les 12 anomalies détectées, corrigé 8 oublis réels, et classé 4 faux positifs. Elle envoie la synthèse à sa DAF avec confiance. Les deux tableaux du mois (novembre et décembre à venir) seront justes.

### Parcours 2 — Sophie, première utilisation (onboarding)

**Scène d'ouverture** : Janvier, début d'exercice. Sophie découvre Controlmyentries. Elle doit charger sa baseline N-1 (le GL complet de l'année précédente).

**Action montante** : Elle uploade son GL 2025 complet (800 000 lignes). L'outil calcule les statistiques de référence par nœud. Sophie voit un résumé : « 342 nœuds identifiés, baseline calculée sur 12 mois ». Elle ne comprend pas tout mais c'est clair et rassurant.

**Climax** : En février, première clôture avec l'outil. Sophie uploade le GL de janvier. L'outil compare avec la baseline N-1 et détecte 3 anomalies. Dont une qu'elle n'avait **pas** vue : une CCA oubliée sur un contrat de maintenance. C'est le moment de découverte nette.

**Résolution** : Sophie est convaincue. L'outil a trouvé quelque chose qu'elle aurait raté. Elle l'intègre dans sa routine mensuelle.

### Parcours 3 — Marc, contexte PME (variante)

**Scène d'ouverture** : Marc est chef comptable d'une PME industrielle de 200 salariés. Son GL est plus petit (5 000 lignes, 80 nœuds) mais les enjeux sont différents : charges inter-sites, provisions complexes, et un DAF exigeant qui veut des clôtures rapides.

**Action montante** : Marc uploade son GL mensuel. Traitement en 3 secondes. 5 alertes.

**Climax** : Une alerte de récurrence : « La provision pour garantie client (6815×PRODUIT) passée tous les mois depuis 18 mois ne figure pas en novembre ». Marc avait simplement oublié. Sans l'outil, il aurait livré la clôture avec un mois sous-provisionné, créant exactement la « variation pénible » décrite dans le brief.

**Résolution** : Marc corrige, clôture en confiance. Il montre le rapport à son DAF qui valide la démarche.

### Parcours 4 — Sophie, fichier problématique (edge case)

**Scène d'ouverture** : Sophie uploade le GL d'avril. Le fichier a été exporté par un collègue et le format des colonnes n'est pas le même que d'habitude.

**Action montante** : L'outil détecte que le mapping des colonnes ne correspond pas. Message clair : « Les colonnes attendues (Compte G, Analytique, Montant, Date) n'ont pas été trouvées. Voici les colonnes détectées : [...]. Veuillez vérifier le format d'export. »

**Climax** : Pas de crash, pas de résultat faux. L'outil refuse de traiter plutôt que de deviner.

**Résolution** : Sophie demande le bon export à son collègue, re-uploade, et le traitement se fait normalement. La confiance est préservée.

### Parcours 5 — Le DAF, consommateur de résultats (secondaire)

**Scène d'ouverture** : Le DAF ne touche pas l'outil directement. Il reçoit de Sophie un mail avec le rapport Excel en pièce jointe après chaque clôture.

**Action montante** : Il ouvre l'onglet « Synthèse » qui liste les anomalies détectées, le nombre corrigé, et le nombre classé comme faux positifs.

**Climax** : En un coup d'œil, le DAF voit que 8 anomalies sur 12 étaient réelles et corrigées. Il a confiance dans la qualité de la clôture.

**Résolution** : Le DAF utilise ces chiffres dans son reporting au conseil. La qualité comptable est documentée et démontrable.

### Journey Requirements Summary

| Parcours | Capabilities révélées |
|---|---|
| Sophie happy path | Upload Excel, traitement Polars, génération rapport multi-onglets, barre de progression |
| Sophie onboarding | Chargement baseline N-1, calcul statistiques de référence, résumé des nœuds identifiés |
| Marc PME | Scalabilité vers le bas (petits GL), même pertinence sur petit volume |
| Sophie edge case | Validation du format d'entrée, messages d'erreur clairs, rejet gracieux des fichiers mal formatés |
| DAF résultats | Onglet synthèse dans l'Excel de sortie, métriques agrégées (détectées/corrigées/faux positifs) |
