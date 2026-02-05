---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - "conversation-context: Description BMAD (Budget Monitoring Anomaly Detection)"
date: 2026-02-05
author: BMad
projectName: Controlmyentries
---

# Product Brief: Controlmyentries

## Executive Summary

Controlmyentries (BMAD - Budget Monitoring Anomaly Detection) est un outil de contrôle automatisé des charges comptables. Chaque mois, il analyse le grand livre exporté en Excel par nœud (Compte Général × Analytique) pour répondre à deux questions : ai-je oublié une charge ? Ai-je une charge qui dérape ?

Le système fonctionne en entonnoir à 3 passes : un filtre binaire évacue ~80% des nœuds normaux, un calibrage statistique (Z-score adaptatif par nœud) élimine les faux positifs, puis une restitution progressive présente un dossier actionnable pour chaque anomalie confirmée (~30 nœuds).

La sortie est un fichier Excel enrichi, directement exploitable par le contrôleur de gestion. Aucune installation, aucun serveur, aucun connecteur ERP. L'objectif : remplacer le contrôle visuel fastidieux sur TCD (~500 nœuds) par un panorama des oublis en quelques secondes.

---

## Core Vision

### Problem Statement

Les contrôleurs de gestion vérifient chaque mois l'exhaustivité et la maîtrise des charges en parcourant visuellement des TCD Excel (~500 nœuds Compte G × Analytique, regroupés). Ce processus est long, sujet aux oublis, et ne bénéficie d'aucune mémoire statistique du comportement normal de chaque nœud.

Dans les grandes structures, les contrôleurs n'ont pas la possibilité de développer leurs propres outils (contraintes DSI) et les solutions du marché (Blackline, FloQast, modules ERP) adressent le rapprochement comptable, pas la détection d'anomalies sur les tendances par nœud. Le besoin est mal adressé commercialement.

### Problem Impact

Une charge oubliée au mois M crée un double effet : M est sous-évalué, M+1 est sur-évalué par le rattrapage. Sans régression comptable, ces deux mois restent faussés définitivement, générant des variations pénibles qui polluent l'analyse des tendances et compromettent la fiabilité des décisions de gestion.

### Why Existing Solutions Fall Short

- **TCD Excel** : aucune automatisation, aucune mémoire historique, contrôle 100% visuel
- **Modules ERP (SAP FCC, etc.)** : font du reporting, pas de la détection d'anomalies calibrée par nœud
- **Outils de rapprochement (Blackline, FloQast)** : matching entre pièces comptables - problème différent, pas de détection de tendances
- **Shadow IT** : dans les grandes structures, développer son propre outil est interdit ou découragé par la DSI
- **Aucun outil dédié** : le besoin est fondamental mais mal adressé commercialement

### Proposed Solution

Un entonnoir en 3 passes, alimenté par un export Excel du grand livre. Initialisation : chargement de l'année N-1 en début d'exercice (12 mois de baseline pour le Z-score).

1. **Passe 1 - Le gros** : Règles binaires (disparition, apparition, variation >20%, récurrence) pour évacuer ~400 nœuds normaux. Ratisse large pour garantir 0% de faux négatifs. Zéro statistique.
2. **Passe 2 - Le calibrage** : Z-score adaptatif par nœud. Chaque nœud connaît sa propre moyenne et son propre écart-type historique. Comparaison M-12 pour neutraliser la saisonnalité. Seuils configurables (défaut |Z| > 2) pour viser 0% de faux positifs.
3. **Passe 3 - La restitution** : Dossier de cas pour chaque anomalie confirmée, avec 3 niveaux progressifs :
   - Niveau 1 : constat brut (toujours disponible)
   - Niveau 2 : calibrage statistique (si la stats apporte quelque chose)
   - Niveau 3 : explication IA (suggère des pistes, jamais d'affirmation - disclaimer systématique, à cadrer contre les hallucinations)

Sortie : fichier Excel enrichi avec suffisamment de données pour décider.

### Key Differentiators

- **Zéro friction** : Excel en entrée, Excel en sortie. Pas d'installation, pas de serveur, pas de connecteur ERP. Utilisable sans demander la permission à la DSI
- **Simplicité conceptuelle** : un entonnoir lisible, pas une boîte noire
- **Calibrage par nœud** : chaque nœud a sa propre baseline historique, éliminant les faux positifs sur les postes naturellement volatiles
- **Restitution progressive** : l'humain décide à quel niveau il a compris - respect de l'intelligence de l'utilisateur
- **Seuils configurables** : l'utilisateur ajuste à son contexte, pas de paramètres figés en dur
- **Vitesse** : panorama complet en quelques secondes vs. heures de contrôle visuel
- **Positionnement unique** : détection d'anomalies par nœud, pas du rapprochement comptable - aucun concurrent direct identifié sur ce créneau

## Target Users

### Primary Users

**Sophie - Contrôleuse de gestion, réseau de crèches (12 établissements)**

- **Contexte** : Responsable du suivi budgétaire mensuel sur 12 crèches. Chaque crèche génère ~40 nœuds (Compte G × Analytique). Total : ~500 nœuds à vérifier chaque mois.
- **Quotidien** : En période de clôture, elle exporte le GL depuis l'ERP, construit un TCD (mois en colonnes, comptes × analytique en lignes) et parcourt visuellement chaque ligne pour repérer disparitions, apparitions et variations anormales. Processus long et ingrat.
- **Frustration** : Le temps de contrôle. Savoir qu'on passe des heures à chercher l'aiguille dans 500 lignes, avec le risque permanent d'en rater une.
- **Moment "aha"** : Ouvrir le fichier Excel de sortie et voir immédiatement les 30 dossiers à traiter, chacun avec son constat en une ligne. Respirer.

**Marc - Chef comptable, PME industrielle (CA 15M€)**

- **Contexte** : Responsable de la qualité des comptes et de la rapidité de clôture. Pression de la direction pour sortir des chiffres fiables plus vite. Pas le droit de développer ses propres outils (contrainte DSI), pas le budget pour un module ERP dédié.
- **Quotidien** : Vérifie les charges par nature et par centre de coût. Les comptes ne sont pas les mêmes que dans le secteur de Sophie, les charges variables et fixes non plus. Mais le problème est identique : contrôle visuel sur TCD.
- **Frustration** : Quand une charge oubliée passe à travers et qu'il faut rattraper au mois suivant, créant deux mois faussés et des variations pénibles dans le reporting.
- **Moment "aha"** : En début d'année, charger N-1 comme baseline, puis chaque mois obtenir un panorama fiable en quelques secondes. Gagner en sérénité.

**Note** : Pas de différence notable entre le profil "contrôleur de gestion" et "chef comptable". Le besoin, le workflow et la douleur sont identiques. Les comptes et la structure analytique changent d'un secteur/société à l'autre, mais l'outil est agnostique : il travaille sur la structure Compte G × Analytique quel que soit le plan comptable.

### Secondary Users

**Le DAF / Directeur financier**

- Ne manipule pas l'outil directement, mais bénéficie des résultats : une clôture plus rapide, des chiffres plus fiables, moins de corrections a posteriori.
- C'est le décideur d'adoption : il autorise (ou non) l'usage de l'outil.
- Son critère : est-ce que la qualité comptable s'améliore visiblement ?

### User Journey

1. **Découverte** : Un pair contrôleur de gestion recommande l'outil, ou l'utilisateur cherche une solution à son problème de contrôle visuel.
2. **Onboarding** : En début d'année, l'utilisateur exporte son GL N-1 au format Excel et le charge comme baseline (une seule fois).
3. **Usage mensuel** : À chaque clôture, export du GL du mois M → import dans l'outil → panorama des anomalies en quelques secondes → traitement des dossiers dans l'Excel de sortie.
4. **Moment de valeur** : La première fois qu'une charge oubliée est détectée au mois M au lieu d'être rattrapée à M+1. L'utilisateur réalise qu'il protège deux mois de P&L d'un coup.
5. **Routine** : L'outil devient un réflexe de clôture. Le temps de contrôle passe de plusieurs heures à quelques minutes. L'utilisateur affine ses seuils au fil des mois.

## Success Metrics

### Métriques utilisateur (Sophie/Marc)

Le succès se mesure à la capacité de l'outil à détecter les cas réels que le contrôleur traque visuellement aujourd'hui :

| Cas de détection | Question posée | Passe concernée |
|---|---|---|
| Suite d'écritures qui s'arrête | Facture récurrente manquante ? | Passe 1 (Récurrence) |
| Charge absente sur un mois | Oubli de comptabilisation ? | Passe 1 (Disparition) |
| Double charge sur un mois | Avance prise, doublon ? | Passe 1 (Variation) |
| CCA oubliée | 2 factures sans étalement ? | Passe 1 (Variation) + Passe 2 |

**Critère de succès utilisateur** : l'outil détecte au moins aussi bien que le contrôle visuel sur TCD, en quelques secondes au lieu de plusieurs heures.

### Objectifs qualité

- **Faux négatifs** : objectif 0%. L'outil ne doit rater aucune anomalie réelle. C'est la condition non négociable de la confiance utilisateur.
- **Faux positifs** : objectif 0%. Chaque alerte doit être pertinente. Si l'utilisateur perd du temps sur du bruit, il revient au TCD.

Note : ces objectifs sont asymptotiques. En pratique, les seuils configurables (Passe 1 : variation >20%, Passe 2 : |Z| > 2) seront ajustés empiriquement sur données réelles pour s'en approcher au maximum.

### Business Objectives

À ce stade du projet, les KPIs business ne sont pas quantifiables (pas de données de benchmark). Ils seront définis après un premier pilote :

- **Temps de contrôle** : mesurer le temps avant/après sur un cycle de clôture
- **Anomalies détectées** : nombre de vrais positifs par mois
- **Taux d'adoption** : est-ce que l'outil est utilisé chaque mois ou abandonné

### Key Performance Indicators

| KPI | Mesure | Cible |
|---|---|---|
| Taux de faux négatifs | Anomalies réelles non détectées / total anomalies | 0% |
| Taux de faux positifs | Alertes non pertinentes / total alertes | 0% |
| Temps de contrôle | Minutes par cycle de clôture | À mesurer (baseline = actuel) |
| Couverture | Nœuds analysés / nœuds totaux du GL | 100% |
| Adoption | Utilisation mensuelle effective | Chaque clôture |

## MVP Scope

### Core Features

**Import & Structuration**
- Import d'un export Excel du Grand Livre (GL)
- Chargement initial de l'année N-1 comme baseline (12 mois, une seule fois en début d'exercice)
- Structuration automatique par nœud (Compte Général × Analytique)

**Passe 1 - Filtre binaire (4 tests)**
- Détection de disparition : un nœud actif les mois précédents qui disparaît au mois M
- Détection d'apparition : un nœud absent historiquement qui apparaît au mois M
- Détection de variation brute : écart > 20% par rapport à la tendance
- Détection de récurrence : une suite d'écritures régulières qui s'interrompt

**Passe 2 - Calibrage statistique**
- Z-score adaptatif par nœud (moyenne et écart-type propres à chaque nœud)
- Comparaison M vs M-12 pour neutraliser la saisonnalité
- Seuil par défaut : |Z| > 2

**Passe 3 - Restitution (Niveaux 1 et 2 uniquement)**
- Niveau 1 : constat brut - description factuelle de l'anomalie détectée
- Niveau 2 : calibrage statistique - données chiffrées (Z-score, moyenne, écart-type, historique)
- Niveau 3 (IA) : reporté à la v2

**Sortie**
- Fichier Excel enrichi avec un onglet par anomalie confirmée
- Suffisamment de données pour que le contrôleur décide sans outil supplémentaire

### Out of Scope for MVP

**Reporté en v2 (intelligence)**
- Niveau 3 - Explication IA (LLM) : suggère des pistes d'investigation, avec disclaimer systématique. Nécessite un cadrage rigoureux contre les hallucinations
- Zoom PCG : navigation dans le plan comptable pour contextualiser les anomalies
- Seuils configurables par l'utilisateur via interface (en MVP, les seuils sont modifiables dans le code/config)

**Reporté en v3+ (plateforme)**
- Connecteurs ERP directs (SAP, Sage, etc.)
- Dashboard web / interface graphique
- Gestion multi-sociétés
- Export PDF / reporting automatisé
- Historique des contrôles et traçabilité des décisions

### MVP Success Criteria

| Critère | Description | Validation |
|---|---|---|
| Détection fonctionnelle | Les 4 cas de détection (disparition, apparition, variation, récurrence) fonctionnent sur données réelles | Test sur GL réel d'un exercice complet |
| Performance | Traitement d'un GL de 500 nœuds en < 1 minute | Mesure chronométrée |
| Exploitabilité | L'Excel de sortie est compréhensible sans formation | Test utilisateur (Sophie ou Marc) |
| Taux de faux positifs | Inférieur à 10% sur un cycle de clôture réel | Revue manuelle des alertes |
| Taux de faux négatifs | 0% sur les anomalies connues du contrôleur | Comparaison avec contrôle visuel |

**Go/No-go** : Pilote de 3 mois sur données réelles d'une structure existante. Si les 4 cas de détection sont validés et que le contrôleur gagne du temps, on passe en v2.

### Future Vision

**v2 - Intelligence (post-pilote)**
- Niveau 3 IA : pistes d'investigation générées par LLM avec disclaimer systématique
- Interface de configuration des seuils par nœud
- Zoom PCG pour contextualisation
- Affinage automatique des seuils basé sur le feedback utilisateur (faux positifs marqués)

**v3 - Plateforme (si traction confirmée)**
- Interface web avec dashboard de suivi
- Connecteurs ERP natifs pour import automatisé
- Gestion multi-sociétés et consolidation
- Historique des contrôles et audit trail
- Export PDF et reporting automatisé pour le DAF
- API pour intégration dans les workflows existants
