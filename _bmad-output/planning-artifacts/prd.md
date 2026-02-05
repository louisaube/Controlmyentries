---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain, step-06-innovation-skipped, step-07-project-type]
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
