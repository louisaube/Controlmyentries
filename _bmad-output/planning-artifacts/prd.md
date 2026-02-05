---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain, step-06-innovation-skipped, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional]
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

## Domain-Specific Requirements

### Modèle de données et confidentialité

- **Architecture stateless** : modèle ilovepdf — upload → traitement en mémoire → téléchargement direct. Aucune donnée comptable n'est persistée côté serveur après le traitement.
- **Pas de stockage** : ni le GL ni le rapport de sortie ne sont conservés. Le serveur ne voit les données que le temps du traitement.
- **RGPD simplifié** : pas de données personnelles stockées, pas de base de données utilisateur pour le MVP. Le traitement est éphémère.
- **Hébergement SaaS** : service accessible sur internet, pas d'installation côté client.

### Gestion de la baseline N-1

- **Question architecturale ouverte** : la baseline N-1 (12 mois de statistiques de référence) est nécessaire pour le Z-score adaptatif. Deux options :
  - **Option A — Double upload** : l'utilisateur uploade à chaque clôture le GL N-1 complet + le GL du mois courant. Zéro persistence, mais friction utilisateur (2 fichiers à chaque fois).
  - **Option B — Baseline pré-calculée** : au premier usage, l'utilisateur uploade le GL N-1. L'outil calcule les statistiques de référence (moyenne, écart-type par nœud) et génère un fichier « baseline.json » que l'utilisateur télécharge. À chaque clôture, il uploade ce fichier baseline + le GL du mois. Aucune donnée persistée côté serveur, mais la baseline vit côté client.
- **Recommandation** : Option B — la baseline pré-calculée est un fichier léger (quelques Ko pour 500 nœuds) que Sophie garde sur son poste. Moins de friction, même niveau de confidentialité.

### Rigueur statistique

- **Seuils initiaux** : |Z| > 2 et variation > 20% sont des hypothèses de départ, à calibrer pendant le pilote de 3 mois sur données réelles.
- **Saisonnalité** : la comparaison M vs M-12 (même mois de l'année précédente) neutralise la saisonnalité naturelle. Limitation connue : si un événement exceptionnel a eu lieu en M-12, il faussera la comparaison.
- **Premiers mois d'exercice** : en janvier (premier mois), le Z-score n'a qu'un seul point de l'exercice courant. La baseline N-1 compense, mais la fiabilité statistique est plus faible. L'outil doit signaler un indice de confiance réduit sur les premiers mois.
- **Faux sentiment de sécurité** : l'outil doit afficher un disclaimer clair : « Cet outil est une aide à la détection, pas un certificat d'absence d'anomalie. »

### Format d'entrée du GL

- **Diversité des exports** : chaque logiciel comptable (Sage, Cegid, EBP, Quadra, etc.) exporte un format différent.
- **Colonnes minimales requises** : Compte Général, Section Analytique, Montant, Date (ou Période/Mois).
- **Mapping MVP** : format d'entrée standardisé avec colonnes nommées. L'utilisateur doit adapter son export ou utiliser un template fourni.
- **Mapping v2** : interface de mapping configurable (« quelle colonne est le Compte G ? ») pour supporter différents formats nativement.

### Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| GL mal formaté uploadé | Résultats faux ou crash | Validation stricte du format avant traitement, rejet avec message explicite |
| Seuils mal calibrés | Trop de faux positifs → perte de confiance | Pilote de 3 mois, seuils ajustables en config |
| Baseline N-1 absente ou corrompue | Z-score impossible | Détection et message d'erreur, mode dégradé Passe 1 seule |
| Données sensibles en transit | Fuite de données comptables | HTTPS obligatoire, traitement éphémère, zéro log de données |
| Événement exceptionnel en M-12 | Fausse anomalie saisonnière | Signaler l'indice de confiance, permettre exclusion de mois atypiques en v2 |

## Web App Specific Requirements

### Project-Type Overview

Controlmyentries est une **SPA (Single Page Application)** de type outil de traitement, modèle ilovepdf. Interface minimale : zone d'upload, barre de progression temps réel, bouton de téléchargement. Pas de navigation multi-pages, pas d'authentification pour le MVP. Une **landing page** distincte présente le produit et dirige vers l'outil.

### Browser Matrix

| Navigateur | Support | Notes |
|---|---|---|
| Chrome (dernières 2 versions) | Full | Cible principale |
| Edge (dernières 2 versions) | Full | Chromium-based, même moteur |
| Firefox | Non requis MVP | Peut fonctionner mais non testé |
| Safari | Non requis MVP | Peut fonctionner mais non testé |
| IE11 | Non supporté | Obsolète |

### Responsive Design

- **Desktop-first** : l'usage principal est sur poste de travail en entreprise
- **Tablette** : fonctionnel mais non optimisé (usage marginal)
- **Mobile** : non ciblé — on n'uploade pas un GL de 800 000 lignes depuis un téléphone

### Performance Targets

| Métrique | Cible | Mesure |
|---|---|---|
| First Contentful Paint (FCP) | < 1.5s | Lighthouse |
| Time to Interactive (TTI) | < 3s | Lighthouse |
| Upload start to progress bar | < 500ms | UX perception |
| Traitement serveur | ≤ 30s (GL standard) | Chronomètre intégré |
| Download ready → fichier reçu | < 2s | Taille fichier résultat |

### Real-Time Communication

- **WebSocket** (ou SSE — Server-Sent Events) pour la barre de progression pendant le traitement
- Étapes de progression à communiquer au client :
  1. « Upload reçu, validation du format... »
  2. « Passe 1 — Tests binaires en cours... »
  3. « Passe 2 — Calibrage statistique... »
  4. « Passe 3 — Génération du rapport... »
  5. « Terminé — Téléchargez votre rapport »
- Fallback polling si WebSocket indisponible (proxy d'entreprise restrictif)

### SEO Strategy

- **Landing page** : page de présentation dédiée, optimisée SEO, avec description du produit, cas d'usage, témoignages, CTA vers l'outil
- **Mots-clés cibles** : « contrôle comptable automatique », « détection anomalies GL », « outil contrôle de gestion »
- **L'outil SPA** : pas de SEO nécessaire (contenu dynamique, pas indexable)
- **Meta tags et Open Graph** : pour le partage sur réseaux sociaux et LinkedIn (cible B2B)

### Accessibilité — WCAG 2.2 AAA

- **Niveau cible** : WCAG 2.2 **AAA** (niveau le plus exigeant)
- **Interactions clés à rendre accessibles** :
  - Upload fichier : drag & drop + bouton classique, label accessible
  - Barre de progression : `role="progressbar"`, `aria-valuenow`, annonces live region
  - Bouton téléchargement : focus visible, label explicite
  - Messages d'erreur : `role="alert"`, liés au champ en erreur
- **Contraste AAA** : ratio minimum **7:1** pour le texte normal, **4.5:1** pour le texte large
- **Navigation clavier** : toutes les actions faisables au clavier (Tab, Enter, Escape)
- **Nouveautés WCAG 2.2** : focus not obscured (2.4.11), dragging movements alternative (2.5.7), target size minimum 24×24px (2.5.8)
- **AAA spécifique** : pas de limite de temps (2.2.3), pas de contenu clignotant (2.3.2), texte redimensionnable à 200% sans perte (1.4.8), navigation cohérente (3.2.3)

### Implementation Considerations

- **Framework SPA** : à définir en architecture (React, Vue, Svelte, ou HTMX + Alpine pour la simplicité)
- **Backend** : Python (FastAPI recommandé — async, performant, WebSocket natif)
- **Landing page** : peut être statique (HTML/CSS) ou générée (Next.js, Astro) — séparée de la SPA outil
- **File upload** : limite de taille à définir (GL de 1M lignes ≈ 50-100 Mo en xlsx)
- **HTTPS obligatoire** : données comptables sensibles en transit
- **CORS** : configuration stricte (même domaine)
- **CSP** : Content Security Policy restrictive

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**Approche MVP : Problem-Solving MVP**
L'objectif est de valider que l'entonnoir 3 passes détecte des anomalies réelles sur des données réelles. Pas de polish, pas de features avancées — juste la preuve que ça marche et que ça fait gagner du temps.

**Ressources MVP :** 1 développeur full-stack (Python + front SPA). Pas besoin d'équipe data science — les statistiques sont classiques (Z-score, moyenne, écart-type).

### MVP Feature Set (Phase 1)

**Parcours supportés :**
- Sophie happy path (contrôle mensuel)
- Sophie onboarding (chargement baseline N-1)
- Sophie edge case (fichier mal formaté → rejet propre)
- Marc PME (même outil, volume plus petit)
- DAF (onglet synthèse dans l'Excel de sortie)

**Must-Have :**

| Feature | Justification |
|---|---|
| Upload Excel GL via web | Point d'entrée unique |
| Upload/download baseline pré-calculée (Option B) | Stateless + Z-score possible |
| Passe 1 — 4 tests binaires | Détection de base : disparition, apparition, variation, récurrence |
| Passe 2 — Z-score adaptatif par nœud | Calibrage statistique, neutralisation saisonnalité M-12 |
| Passe 3 — Niveaux 1 et 2 | Restitution exploitable sans IA |
| Excel de sortie multi-onglets | Format familier, un onglet par anomalie |
| Onglet Synthèse | Pour le DAF, métriques agrégées |
| Validation format d'entrée | Rejet propre avec message si colonnes manquantes |
| Barre de progression WebSocket | Feedback temps réel pendant les 30s de traitement |
| Landing page SEO | Acquisition et crédibilité |
| HTTPS | Données comptables sensibles |
| Disclaimer | « Aide à la détection, pas certificat d'absence d'anomalie » |

**Explicitement hors MVP :**
- Authentification / comptes utilisateurs
- Stockage de données côté serveur
- Niveau 3 IA (LLM)
- Configuration des seuils via interface
- Mapping de colonnes configurable
- Support multi-formats comptables

### Post-MVP Features

**Phase 2 — Intelligence (après pilote validé) :**
- Niveau 3 IA : pistes d'investigation LLM avec disclaimer systématique
- Interface de mapping colonnes configurable (Sage, Cegid, EBP nativement)
- Configuration des seuils par nœud via interface
- Zoom PCG pour contextualisation
- Affinage automatique basé sur feedback (marquer les faux positifs)
- Comptes utilisateurs + historique des baselines

**Phase 3 — Plateforme (si traction confirmée) :**
- Dashboard web avec suivi historique des contrôles
- Connecteurs ERP natifs (import automatisé)
- Gestion multi-sociétés et consolidation
- API pour intégration workflows existants
- Export PDF et reporting automatisé
- Audit trail pour conformité

### Risk Mitigation Strategy

**Risques techniques :**
- Seuils non calibrés → Pilote 3 mois, seuils ajustables en config côté code
- Z-score faible premiers mois → Indice de confiance affiché, mode dégradé Passe 1 seule

**Risques marché :**
- Contrôleurs ne font pas confiance → Niveaux 1+2 montrent les données brutes, pas de boîte noire
- Marché trop petit → Pilote gratuit, mesure de l'intérêt avant investissement v2

**Risques ressources :**
- Moins de ressources que prévu → MVP réductible à Passe 1 seule + Excel basique

## Functional Requirements

### Data Import & Validation

- **FR1** : L'utilisateur peut uploader un fichier Excel contenant un export du Grand Livre (GL)
- **FR2** : Le système valide le fichier uploadé pour la présence des colonnes requises (Compte Général, Section Analytique, Montant, Date/Période)
- **FR3** : Le système rejette les fichiers invalides avec un message d'erreur explicite listant les colonnes détectées vs attendues
- **FR4** : L'utilisateur peut uploader un fichier baseline pré-calculé (JSON) pour la comparaison statistique
- **FR5** : L'utilisateur peut générer un fichier baseline en uploadant un GL N-1 complet (12 mois)
- **FR6** : Le système produit un fichier baseline téléchargeable que l'utilisateur conserve sur son poste
- **FR7** : L'utilisateur peut soumettre simultanément un fichier baseline + un GL du mois courant pour lancer l'analyse

### Anomaly Detection — Pass 1 (Binary Tests)

- **FR8** : Le système détecte la disparition d'un nœud (nœud actif les mois précédents, absent au mois M)
- **FR9** : Le système détecte l'apparition d'un nœud (nœud absent de l'historique, présent au mois M)
- **FR10** : Le système détecte une variation brute (écart > 20% par rapport à la tendance)
- **FR11** : Le système détecte une interruption de récurrence (suite d'écritures régulières qui s'arrête)

### Anomaly Detection — Pass 2 (Statistical Calibration)

- **FR12** : Le système calcule un Z-score adaptatif par nœud (moyenne et écart-type propres à chaque nœud Compte G × Analytique)
- **FR13** : Le système compare le mois courant M avec le même mois de l'année précédente M-12 pour neutraliser la saisonnalité
- **FR14** : Le système signale les anomalies dont |Z| > 2
- **FR15** : Le système fonctionne en mode dégradé (Passe 1 seule) lorsque la baseline est insuffisante ou absente

### Report Generation — Pass 3 (Restitution)

- **FR16** : Le système génère un fichier Excel enrichi avec un onglet par anomalie confirmée
- **FR17** : Chaque onglet d'anomalie contient un constat factuel de Niveau 1 (description de ce qui s'est passé)
- **FR18** : Chaque onglet d'anomalie contient les données statistiques de Niveau 2 (Z-score, moyenne, écart-type, historique)
- **FR19** : Le système génère un onglet Synthèse avec les métriques agrégées (nombre total d'anomalies, types, répartition)
- **FR20** : L'utilisateur peut télécharger le rapport généré au format Excel

### Real-Time Processing Feedback

- **FR21** : Le système affiche une barre de progression pendant le traitement du fichier
- **FR22** : Le système communique les étapes de traitement en temps réel (validation, Passe 1, Passe 2, Passe 3, terminé)
- **FR23** : Le système affiche le temps de traitement total à la fin de l'analyse

### Confidence & Transparency

- **FR24** : Le système affiche un indice de confiance réduit pour les anomalies détectées sur les premiers mois de l'exercice
- **FR25** : Le système affiche un disclaimer permanent : « Cet outil est une aide à la détection, pas un certificat d'absence d'anomalie »
- **FR26** : Le système montre la base statistique de chaque détection (données chiffrées, pas une boîte noire)

### Landing Page & Product Discovery

- **FR27** : Les visiteurs peuvent accéder à une landing page présentant le produit, les cas d'usage et la proposition de valeur
- **FR28** : La landing page est optimisée pour les moteurs de recherche (SEO)
- **FR29** : La landing page contient un appel à l'action dirigeant vers l'outil

### Accessibility

- **FR30** : Toutes les interactions sont accessibles via navigation clavier
- **FR31** : Le système fournit une alternative au drag-and-drop pour l'upload de fichier
- **FR32** : Le système annonce les étapes de progression et changements d'état aux lecteurs d'écran
- **FR33** : Les messages d'erreur sont programmatiquement liés à leur source

## Non-Functional Requirements

### Performance

- **NFR1** : Le traitement end-to-end (upload → calcul → génération Excel) s'exécute en ≤ 30 secondes pour un GL de 500 nœuds / 50 000 lignes
- **NFR2** : Le traitement reste sous 2 minutes pour un GL de 1 000 000 de lignes
- **NFR3** : La barre de progression se met à jour au moins toutes les 5 secondes pendant le traitement
- **NFR4** : Le First Contentful Paint de la SPA est < 1.5 seconde
- **NFR5** : Le Time to Interactive de la SPA est < 3 secondes
- **NFR6** : Le fichier Excel de sortie se génère en < 5 secondes quel que soit le nombre d'anomalies

### Security

- **NFR7** : Toutes les communications client-serveur utilisent HTTPS (TLS 1.2+)
- **NFR8** : Aucune donnée comptable n'est persistée côté serveur après le traitement (architecture stateless)
- **NFR9** : Les logs contiennent uniquement des métadonnées (nombre de lignes, nombre de nœuds, temps de traitement) — jamais de valeurs comptables, montants, comptes ou libellés
- **NFR10** : Le serveur ne conserve ni le fichier uploadé ni le fichier généré après téléchargement
- **NFR11** : Le Content Security Policy (CSP) interdit le chargement de scripts externes non contrôlés
- **NFR12** : Le CORS est configuré en mode strict (même domaine uniquement)

### Scalability

- **NFR13** : Le système supporte 10 traitements simultanés au MVP (1 par contrôleur actif)
- **NFR14** : Le système supporte 50 traitements simultanés en phase de croissance (12 mois) sans dégradation > 20% des temps de traitement
- **NFR15** : Le traitement est isolé par requête (un GL lent ne bloque pas les autres)
- **NFR16** : Un mécanisme de queue (file d'attente) est activé lorsque le nombre de traitements simultanés dépasse le seuil configuré, avec message d'attente à l'utilisateur

### Accessibility

- **NFR17** : L'interface atteint le niveau WCAG 2.2 AAA
- **NFR18** : Le ratio de contraste texte/fond est ≥ 7:1 pour le texte normal, ≥ 4.5:1 pour le texte large
- **NFR19** : Toutes les fonctionnalités sont utilisables au clavier seul (sans souris)
- **NFR20** : Les changements d'état (progression, erreurs, résultats) sont annoncés aux technologies d'assistance via ARIA live regions
- **NFR21** : Les cibles interactives ont une taille minimale de 24×24 pixels (WCAG 2.5.8)
- **NFR22** : Le texte est redimensionnable à 200% sans perte de fonctionnalité (WCAG 1.4.8)

### Reliability

- **NFR23** : Le service est disponible à 99% pendant les heures ouvrées (8h-20h, lundi-vendredi), et à **99.9% les 5 premiers jours ouvrés de chaque mois** (période de clôture)
- **NFR24** : La sortie est **atomique** — le système ne produit jamais de résultat partiel. Si une erreur survient en cours de traitement, aucun fichier n'est généré et un message d'erreur explicite est affiché
- **NFR25** : Le système redémarre automatiquement en cas de crash du processus serveur
- **NFR26** : Le temps de rétablissement après incident est < 30 minutes

### File Limits & Timeouts

- **NFR27** : Le système rejette les fichiers dépassant **20 Mo** avec un message explicite
- **NFR28** : Le système impose un timeout de 5 minutes maximum par traitement — au-delà, le traitement est interrompu avec un message d'erreur
