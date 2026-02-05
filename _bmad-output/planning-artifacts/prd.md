---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain, step-06-innovation-skipped, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish]
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

## Executive Summary

**Controlmyentries** est un outil web de détection automatique d'anomalies dans les écritures comptables. Il analyse un export Excel du Grand Livre (GL) via un entonnoir à 3 passes — tests binaires, calibrage statistique par Z-score adaptatif, et restitution progressive — pour identifier en quelques secondes les oublis, disparitions, apparitions et variations anormales que les contrôleurs de gestion mettent des heures à repérer visuellement.

**Problème** : le contrôle des charges comptables par TCD est long (4h par clôture), sujet à erreur humaine, et quand une anomalie n'est pas détectée, elle fausse deux mois consécutifs (sous-évaluation puis sur-évaluation), créant des variations pénibles sans régression comptable possible.

**Solution** : une web app SaaS stateless (modèle ilovepdf) — upload Excel → traitement Polars en ≤ 30s → téléchargement d'un rapport Excel enrichi avec un onglet par anomalie. Zéro installation, zéro stockage de données côté serveur.

**Différenciateurs** : entonnoir 3 passes (binaire → statistique → restitution), Z-score adaptatif par nœud (Compte G × Analytique), comparaison M-12 pour neutraliser la saisonnalité, transparence totale (données chiffrées, pas de boîte noire).

**Utilisateurs cibles** : contrôleurs de gestion (Sophie, réseau de crèches) et chefs comptables (Marc, PME industrielle). Le DAF est consommateur secondaire des résultats.

**Marché** : mal adressé commercialement — les grandes entreprises ne peuvent pas développer leurs propres outils, et les solutions existantes sont coûteuses ou inadaptées. Ce n'est pas du rapprochement comptable, c'est du contrôle de charges.

## Success Criteria

### User Success

- **Le moment "aha!"** : Sophie uploade son GL, voit une barre de progression pendant ~30s, puis télécharge un rapport enrichi. En ouvrant le premier onglet, elle identifie en quelques secondes un oubli qu'elle aurait mis des heures à repérer dans son TCD.
- **Temps de contrôle** : de 4 heures de contrôle visuel à ~45 minutes de revue ciblée (facteur ×5 minimum).
- **Autonomie** : l'Excel de sortie est compréhensible sans formation. Les niveaux 1 (constat brut) et 2 (calibrage statistique) fournissent assez d'information pour décider.
- **Confiance** : 0% de faux négatifs sur les anomalies connues du contrôleur.
- **Découverte nette** : l'outil détecte des anomalies que le contrôleur n'avait pas encore identifiées — c'est la vraie valeur ajoutée au-delà de la simple automatisation.

### Business Success

- **3 mois (pilote)** : validation fonctionnelle sur données réelles d'une structure. Les 4 cas de détection sont confirmés. Le contrôleur gagne du temps mesurable → Go pour la suite.
- **6 mois** : 3 contrôleurs dans 2 structures utilisent l'outil à chaque clôture mensuelle.
- **12 mois** : 10 contrôleurs dans 5 structures, taux de rétention > 80%.
- **Monétisation** : à définir post-pilote. L'objectif initial est de prouver la valeur.

### Technical Success

- **Performance** : traitement end-to-end ≤ 30 secondes pour un GL standard. Approche KISS — une seule métrique.
- **Scalabilité** : GL de 200 à 1 000 000 de lignes sans dégradation critique.
- **Détection** : les 4 tests binaires (Passe 1) + Z-score adaptatif (Passe 2) fonctionnent sur données réelles.
- **Fiabilité** : faux positifs < 10% des alertes. Seuil d'utilisabilité : ≤ 50 alertes par clôture.
- **Baseline** : chargement N-1 comme référence statistique, une seule fois en début d'exercice.

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

## Product Scope & Phased Development

### MVP Strategy

**Approche : Problem-Solving MVP** — Valider que l'entonnoir 3 passes détecte des anomalies réelles sur des données réelles. Pas de polish, pas de features avancées — juste la preuve que ça marche et que ça fait gagner du temps.

**Ressources :** 1 développeur full-stack (Python + front SPA). Statistiques classiques, pas besoin d'équipe data science.

### MVP Feature Set (Phase 1)

**Parcours supportés :** Sophie happy path, Sophie onboarding, Sophie edge case, Marc PME, DAF résultats.

**Must-Have :**

| Feature | Justification |
|---|---|
| Upload Excel GL via web | Point d'entrée unique |
| Upload/download baseline pré-calculée (Option B) | Stateless + Z-score possible |
| Passe 1 — 4 tests binaires | Disparition, apparition, variation, récurrence |
| Passe 2 — Z-score adaptatif par nœud | Calibrage statistique, neutralisation saisonnalité M-12 |
| Passe 3 — Niveaux 1 et 2 | Restitution exploitable sans IA |
| Excel de sortie multi-onglets | Format familier, un onglet par anomalie |
| Onglet Synthèse | Pour le DAF, métriques agrégées |
| Validation format d'entrée | Rejet propre avec message si colonnes manquantes |
| Barre de progression WebSocket | Feedback temps réel pendant le traitement |
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

### Phase 2 — Intelligence (après pilote validé)

- Niveau 3 IA : pistes d'investigation LLM avec disclaimer systématique
- Interface de mapping colonnes configurable (Sage, Cegid, EBP nativement)
- Configuration des seuils par nœud via interface
- Zoom PCG pour contextualisation
- Affinage automatique basé sur feedback (marquer les faux positifs)
- Comptes utilisateurs + historique des baselines

### Phase 3 — Plateforme (si traction confirmée)

- Dashboard web avec suivi historique des contrôles
- Connecteurs ERP natifs (import automatisé)
- Gestion multi-sociétés et consolidation
- API pour intégration workflows existants
- Export PDF et reporting automatisé
- Audit trail pour conformité

### Risk Mitigation Strategy

| Type | Risque | Mitigation |
|---|---|---|
| Technique | Seuils non calibrés | Pilote 3 mois, seuils ajustables en config |
| Technique | Z-score faible premiers mois | Indice de confiance, mode dégradé Passe 1 seule |
| Marché | Contrôleurs ne font pas confiance | Niveaux 1+2 montrent les données brutes, pas de boîte noire |
| Marché | Marché trop petit | Pilote gratuit, mesure de l'intérêt avant v2 |
| Ressources | Moins de ressources que prévu | MVP réductible à Passe 1 seule + Excel basique |

## User Journeys

### Parcours 1 — Sophie, le contrôle mensuel (happy path)

**Scène d'ouverture** : Vendredi 5 décembre, 14h. Sophie vient de recevoir l'export GL du mois de novembre pour ses 8 crèches. Avant Controlmyentries, elle ouvrait son TCD géant, comparait visuellement les colonnes mois par mois, ligne par ligne. 4 heures de travail répétitif, les yeux fatigués, avec la peur permanente de rater un oubli.

**Action montante** : Sophie ouvre Controlmyentries dans son navigateur. Elle uploade le fichier GL de novembre (150 000 lignes). La barre de progression avance. 25 secondes plus tard, un bouton « Télécharger le rapport » apparaît.

**Climax** : Sophie ouvre l'Excel. Premier onglet : « Disparition — 6061×CRECHE03 ». Le constat : *« Ce nœud était actif de janvier à octobre (moyenne 2 400€/mois) et a disparu en novembre. Z-score : -3.2 »*. En 10 secondes, elle a trouvé ce qui lui aurait pris 45 minutes à repérer.

**Résolution** : En 40 minutes au lieu de 4 heures, Sophie a revu les 12 anomalies détectées, corrigé 8 oublis réels, et classé 4 faux positifs. Elle envoie la synthèse à sa DAF avec confiance.

### Parcours 2 — Sophie, première utilisation (onboarding)

**Scène d'ouverture** : Janvier, début d'exercice. Sophie découvre Controlmyentries et charge sa baseline N-1 (le GL complet de l'année précédente).

**Action montante** : Elle uploade son GL 2025 complet (800 000 lignes). L'outil calcule les statistiques de référence par nœud. Résumé : « 342 nœuds identifiés, baseline calculée sur 12 mois ».

**Climax** : En février, première clôture avec l'outil. 3 anomalies détectées, dont une CCA oubliée sur un contrat de maintenance que Sophie n'avait **pas** vue. C'est le moment de découverte nette.

**Résolution** : Sophie est convaincue. L'outil a trouvé quelque chose qu'elle aurait raté. Elle l'intègre dans sa routine mensuelle.

### Parcours 3 — Marc, contexte PME (variante)

**Scène d'ouverture** : Marc est chef comptable d'une PME industrielle de 200 salariés. Son GL est plus petit (5 000 lignes, 80 nœuds) mais les enjeux sont différents : charges inter-sites, provisions complexes, DAF exigeant.

**Action montante** : Marc uploade son GL mensuel. Traitement en 3 secondes. 5 alertes.

**Climax** : Alerte de récurrence : « La provision pour garantie client (6815×PRODUIT) passée tous les mois depuis 18 mois ne figure pas en novembre ». Sans l'outil, un mois sous-provisionné créant la « variation pénible ».

**Résolution** : Marc corrige, clôture en confiance. Le DAF valide la démarche.

### Parcours 4 — Sophie, fichier problématique (edge case)

**Scène d'ouverture** : Sophie uploade un GL exporté par un collègue avec un format de colonnes différent.

**Action montante** : Message clair : « Les colonnes attendues (Compte G, Analytique, Montant, Date) n'ont pas été trouvées. Voici les colonnes détectées : [...]. »

**Climax** : Pas de crash, pas de résultat faux. L'outil refuse de traiter plutôt que de deviner.

**Résolution** : Sophie demande le bon export, re-uploade, traitement normal. La confiance est préservée.

### Parcours 5 — Le DAF, consommateur de résultats (secondaire)

**Scène d'ouverture** : Le DAF reçoit de Sophie le rapport Excel en pièce jointe après chaque clôture.

**Action montante** : Il ouvre l'onglet « Synthèse » — anomalies détectées, corrigées, faux positifs.

**Climax** : En un coup d'œil, 8 anomalies sur 12 réelles et corrigées. Confiance dans la qualité de la clôture.

**Résolution** : Le DAF utilise ces chiffres dans son reporting. La qualité comptable est documentée et démontrable.

### Journey Requirements Summary

| Parcours | Capabilities révélées |
|---|---|
| Sophie happy path | Upload Excel, traitement Polars, rapport multi-onglets, barre de progression |
| Sophie onboarding | Chargement baseline N-1, calcul statistiques de référence, résumé des nœuds |
| Marc PME | Scalabilité vers le bas (petits GL), même pertinence sur petit volume |
| Sophie edge case | Validation format d'entrée, messages d'erreur clairs, rejet gracieux |
| DAF résultats | Onglet synthèse, métriques agrégées (détectées/corrigées/faux positifs) |

## Domain-Specific Requirements

### Modèle de données et confidentialité

- **Architecture stateless** : modèle ilovepdf — upload → traitement en mémoire → téléchargement direct. Aucune donnée persistée côté serveur.
- **RGPD simplifié** : pas de données personnelles stockées, pas de base de données utilisateur pour le MVP. Traitement éphémère.
- **Hébergement SaaS** : service accessible sur internet, pas d'installation côté client.

### Gestion de la baseline N-1

- **Recommandation : Option B — Baseline pré-calculée.** L'utilisateur uploade le GL N-1 une fois. L'outil calcule les statistiques de référence (moyenne, écart-type par nœud) et génère un fichier « baseline.json » téléchargeable. À chaque clôture, l'utilisateur uploade ce fichier baseline + le GL du mois. Aucune donnée persistée côté serveur. Fichier léger (quelques Ko pour 500 nœuds).
- **Alternative (Option A)** : double upload du GL N-1 complet + GL du mois à chaque clôture. Plus de friction, mais zéro fichier intermédiaire.

### Rigueur statistique

- **Seuils initiaux** : |Z| > 2 et variation > 20% sont des hypothèses de départ, à calibrer pendant le pilote de 3 mois.
- **Saisonnalité** : comparaison M vs M-12 neutralise la saisonnalité. Limitation : un événement exceptionnel en M-12 faussera la comparaison.
- **Premiers mois** : fiabilité statistique plus faible. L'outil signale un indice de confiance réduit.
- **Disclaimer** : « Cet outil est une aide à la détection, pas un certificat d'absence d'anomalie. »

### Format d'entrée du GL

- **Colonnes minimales** : Compte Général, Section Analytique, Montant, Date (ou Période/Mois).
- **MVP** : format standardisé avec colonnes nommées. L'utilisateur adapte son export ou utilise un template fourni.
- **v2** : interface de mapping configurable pour supporter différents logiciels comptables nativement.

### Risques domaine

| Risque | Impact | Mitigation |
|---|---|---|
| GL mal formaté | Résultats faux ou crash | Validation stricte, rejet avec message explicite |
| Seuils mal calibrés | Trop de faux positifs → perte de confiance | Pilote 3 mois, seuils ajustables en config |
| Baseline absente ou corrompue | Z-score impossible | Message d'erreur, mode dégradé Passe 1 seule |
| Données sensibles en transit | Fuite comptable | HTTPS obligatoire, traitement éphémère, zéro log de données |
| Événement exceptionnel en M-12 | Fausse anomalie saisonnière | Indice de confiance, exclusion de mois atypiques en v2 |

## Web App Specific Requirements

### Architecture

Controlmyentries est une **SPA (Single Page Application)** de type outil de traitement, modèle ilovepdf. Interface minimale : zone d'upload, barre de progression temps réel, bouton de téléchargement. Pas de navigation multi-pages, pas d'authentification pour le MVP. Une **landing page** distincte présente le produit.

### Browser Matrix

| Navigateur | Support | Notes |
|---|---|---|
| Chrome (dernières 2 versions) | Full | Cible principale |
| Edge (dernières 2 versions) | Full | Chromium-based |
| Firefox | Non requis MVP | Non testé |
| Safari | Non requis MVP | Non testé |
| IE11 | Non supporté | Obsolète |

### Responsive Design

- **Desktop-first** : usage principal sur poste de travail en entreprise
- **Tablette** : fonctionnel mais non optimisé
- **Mobile** : non ciblé

### Performance Targets

| Métrique | Cible | Mesure |
|---|---|---|
| First Contentful Paint (FCP) | < 1.5s | Lighthouse |
| Time to Interactive (TTI) | < 3s | Lighthouse |
| Upload start to progress bar | < 500ms | UX perception |
| Traitement serveur | ≤ 30s (GL standard) | Chronomètre intégré |
| Download ready → fichier reçu | < 2s | Taille fichier résultat |

### Real-Time Communication

- **WebSocket** (ou SSE) pour la barre de progression pendant le traitement
- Étapes : validation du format → Passe 1 → Passe 2 → Passe 3 → Terminé
- Fallback polling si WebSocket indisponible (proxy d'entreprise restrictif)

### SEO Strategy

- **Landing page** : page dédiée optimisée SEO, cas d'usage, CTA vers l'outil
- **Mots-clés** : « contrôle comptable automatique », « détection anomalies GL », « outil contrôle de gestion »
- **SPA outil** : pas de SEO (contenu dynamique)
- **Meta tags et Open Graph** : partage LinkedIn (cible B2B)

### Accessibilité — WCAG 2.2 AAA

- **Niveau cible** : WCAG 2.2 **AAA**
- Upload : drag & drop + bouton classique, label accessible
- Progression : `role="progressbar"`, `aria-valuenow`, live region
- Téléchargement : focus visible, label explicite
- Erreurs : `role="alert"`, liés au champ source
- **Contraste AAA** : ≥ 7:1 texte normal, ≥ 4.5:1 texte large
- **Clavier** : toutes actions au clavier (Tab, Enter, Escape)
- **WCAG 2.2** : focus not obscured (2.4.11), dragging alternative (2.5.7), target size 24×24px (2.5.8)
- **AAA** : pas de limite de temps (2.2.3), texte redimensionnable 200% (1.4.8), navigation cohérente (3.2.3)

### Implementation Considerations

- **Framework SPA** : à définir en architecture (React, Vue, Svelte, ou HTMX + Alpine)
- **Backend** : Python (FastAPI recommandé — async, WebSocket natif)
- **Landing page** : peut être statique ou générée (Astro) — séparée de la SPA outil
- **File upload** : limite 20 Mo (NFR27)
- **HTTPS obligatoire**, **CORS strict**, **CSP restrictive**

## Functional Requirements

### Data Import & Validation

- **FR1** : L'utilisateur peut uploader un fichier Excel contenant un export du Grand Livre (GL)
- **FR2** : Le système valide le fichier pour la présence des colonnes requises (Compte Général, Section Analytique, Montant, Date/Période)
- **FR3** : Le système rejette les fichiers invalides avec un message d'erreur listant colonnes détectées vs attendues
- **FR4** : L'utilisateur peut uploader un fichier baseline pré-calculé (JSON) pour la comparaison statistique
- **FR5** : L'utilisateur peut générer un fichier baseline en uploadant un GL N-1 complet (12 mois)
- **FR6** : Le système produit un fichier baseline téléchargeable conservé sur le poste de l'utilisateur
- **FR7** : L'utilisateur peut soumettre simultanément baseline + GL du mois courant pour lancer l'analyse

### Anomaly Detection — Pass 1 (Binary Tests)

- **FR8** : Le système détecte la disparition d'un nœud (actif les mois précédents, absent au mois M)
- **FR9** : Le système détecte l'apparition d'un nœud (absent de l'historique, présent au mois M)
- **FR10** : Le système détecte une variation brute (écart > 20% par rapport à la tendance)
- **FR11** : Le système détecte une interruption de récurrence (suite d'écritures régulières qui s'arrête)

### Anomaly Detection — Pass 2 (Statistical Calibration)

- **FR12** : Le système calcule un Z-score adaptatif par nœud (moyenne et écart-type propres à chaque nœud Compte G × Analytique)
- **FR13** : Le système compare M vs M-12 pour neutraliser la saisonnalité
- **FR14** : Le système signale les anomalies dont |Z| > 2
- **FR15** : Le système fonctionne en mode dégradé (Passe 1 seule) lorsque la baseline est insuffisante

### Report Generation — Pass 3 (Restitution)

- **FR16** : Le système génère un fichier Excel enrichi avec un onglet par anomalie confirmée
- **FR17** : Chaque onglet contient un constat factuel de Niveau 1 (description de l'anomalie)
- **FR18** : Chaque onglet contient les données statistiques de Niveau 2 (Z-score, moyenne, écart-type, historique)
- **FR19** : Le système génère un onglet Synthèse avec métriques agrégées (nombre, types, répartition)
- **FR20** : L'utilisateur peut télécharger le rapport au format Excel

### Real-Time Processing Feedback

- **FR21** : Le système affiche une barre de progression pendant le traitement
- **FR22** : Le système communique les étapes en temps réel (validation, Passe 1, Passe 2, Passe 3, terminé)
- **FR23** : Le système affiche le temps de traitement total à la fin de l'analyse

### Confidence & Transparency

- **FR24** : Le système affiche un indice de confiance réduit pour les premiers mois de l'exercice
- **FR25** : Le système affiche un disclaimer permanent : « Aide à la détection, pas certificat d'absence d'anomalie »
- **FR26** : Le système montre la base statistique de chaque détection (données chiffrées, pas de boîte noire)

### Landing Page & Product Discovery

- **FR27** : Les visiteurs accèdent à une landing page présentant le produit, les cas d'usage et la proposition de valeur
- **FR28** : La landing page est optimisée SEO
- **FR29** : La landing page contient un appel à l'action dirigeant vers l'outil

### Accessibility

- **FR30** : Toutes les interactions sont accessibles via navigation clavier
- **FR31** : Le système fournit une alternative au drag-and-drop pour l'upload
- **FR32** : Le système annonce les changements d'état aux lecteurs d'écran
- **FR33** : Les messages d'erreur sont programmatiquement liés à leur source

## Non-Functional Requirements

### Performance

- **NFR1** : Traitement end-to-end ≤ 30 secondes pour un GL de 500 nœuds / 50 000 lignes
- **NFR2** : Traitement ≤ 2 minutes pour un GL de 1 000 000 de lignes
- **NFR3** : Barre de progression mise à jour au moins toutes les 5 secondes
- **NFR4** : First Contentful Paint < 1.5 seconde
- **NFR5** : Time to Interactive < 3 secondes
- **NFR6** : Génération Excel de sortie < 5 secondes

### Security

- **NFR7** : HTTPS (TLS 1.2+) pour toutes les communications
- **NFR8** : Aucune donnée comptable persistée côté serveur (architecture stateless)
- **NFR9** : Logs métadonnées uniquement (nombre de lignes, nœuds, temps) — jamais de valeurs comptables
- **NFR10** : Aucun fichier conservé après téléchargement
- **NFR11** : CSP interdit les scripts externes non contrôlés
- **NFR12** : CORS strict (même domaine uniquement)

### Scalability

- **NFR13** : 10 traitements simultanés au MVP
- **NFR14** : 50 traitements simultanés à 12 mois sans dégradation > 20%
- **NFR15** : Traitement isolé par requête (un GL lent ne bloque pas les autres)
- **NFR16** : File d'attente activée au-delà du seuil, avec message d'attente à l'utilisateur

### Accessibility

- **NFR17** : Interface WCAG 2.2 AAA
- **NFR18** : Contraste ≥ 7:1 texte normal, ≥ 4.5:1 texte large
- **NFR19** : Toutes fonctionnalités utilisables au clavier seul
- **NFR20** : Changements d'état annoncés via ARIA live regions
- **NFR21** : Cibles interactives ≥ 24×24 pixels (WCAG 2.5.8)
- **NFR22** : Texte redimensionnable à 200% sans perte (WCAG 1.4.8)

### Reliability

- **NFR23** : Disponibilité 99% heures ouvrées (8h-20h, lun-ven), **99.9% les 5 premiers jours ouvrés** (période de clôture)
- **NFR24** : Sortie **atomique** — jamais de résultat partiel. Erreur en cours de traitement = aucun fichier généré + message explicite
- **NFR25** : Redémarrage automatique en cas de crash serveur
- **NFR26** : Temps de rétablissement < 30 minutes

### File Limits & Timeouts

- **NFR27** : Rejet des fichiers > **20 Mo** avec message explicite
- **NFR28** : Timeout 5 minutes par traitement — interruption avec message d'erreur au-delà
