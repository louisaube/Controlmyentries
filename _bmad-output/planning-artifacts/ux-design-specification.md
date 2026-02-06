---
stepsCompleted: [1, 2, 3, 4, 5]
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

## Desired Emotional Response

### Primary Emotional Goals

| Émotion cible | Moment | Traduction UX |
|---|---|---|
| **Soulagement** | Après l'analyse | "Enfin, je n'ai plus à scanner des colonnes pendant 4 heures" |
| **Confiance** | Tout au long | "L'outil me montre ses calculs, je peux vérifier" |
| **Efficacité** | Upload → résultat | "C'est fait en 30 secondes, je passe à autre chose" |
| **Découverte** | Lecture du rapport | "Il a trouvé un oubli de CCA que je n'avais pas vu" |

L'émotion dominante est le **soulagement productif** — la sensation qu'une tâche pénible et risquée (le contrôle visuel TCD) est désormais automatisée et fiable.

### Emotional Journey Mapping

| Étape du parcours | Émotion attendue | Émotion à éviter |
|---|---|---|
| **Découverte / Landing** | Curiosité professionnelle, crédibilité immédiate | Méfiance ("encore un outil gadget") |
| **Premier upload (onboarding)** | Guidé, rassuré | Confusion ("quel fichier mettre où ?") |
| **Attente (30s)** | Anticipation active, impatience positive | Anxiété ("ça marche ?"), ennui |
| **Réception du rapport** | Satisfaction immédiate, "ça a marché" | Déception ("c'est tout ?") |
| **Lecture détaillée** | Découverte, "aha moment" | Confusion ("je ne comprends pas les scores") |
| **Retour M+1** | Familiarité, routine efficace | Friction ("où est mon baseline ?") |
| **Erreur fichier** | Compréhension, action claire | Frustration, culpabilité |

### Micro-Emotions

- **Confiance vs Scepticisme** : CRITIQUE. Sophie est experte comptable — elle ne fera confiance qu'à un outil qui montre ses méthodes. Chaque Z-score affiché, chaque donnée source visible = confiance construite.
- **Accomplissement vs Frustration** : Sophie doit sentir qu'elle a FAIT son travail de contrôle, pas que l'outil l'a remplacée. Le rapport est son livrable, elle l'a "produit".
- **Excitation vs Anxiété** : pendant les 30 secondes, le compteur d'anomalies transforme l'anxiété de l'attente en excitation de la découverte.
- **Delight vs Simple satisfaction** : on vise la satisfaction fiable (comptable), pas le delight spectaculaire. Un outil sérieux, pas un jouet.

### Design Implications

| Émotion cible | Implication UX |
|---|---|
| Soulagement | Le flow complet upload→résultat doit être réalisable en < 2 minutes |
| Confiance | Transparence des calculs dans le rapport, pas de boîte noire |
| Efficacité | Zéro étape superflue, auto-download du rapport |
| Découverte | Compteur d'anomalies en temps réel, onglets par catégorie dans Excel |
| Guidé (onboarding) | Copie explicative inline, zones visuellement distinctes baseline/GL |
| Pas de confusion | Messages d'erreur avec colonnes détectées vs attendues |
| Anticipation (attente) | Barre de progression 5 étapes + compteur d'anomalies live |
| Familiarité (retour) | localStorage pour le dernier baseline, état visuel "prêt à relancer" |

### Emotional Design Principles

1. **Sérieux comptable, pas ludique** : ton professionnel, pas de gamification. Les comptables veulent un outil fiable, pas un jouet. Pas d'animations gratuites, pas d'emojis, pas de confetti.
2. **Transparence = confiance** : ne jamais cacher un calcul. Si l'outil détecte une anomalie, l'utilisateur doit pouvoir comprendre POURQUOI en < 10 secondes.
3. **L'attente est investie** : les 30 secondes sont conçues comme un moment de valeur (progression + compteur), pas comme un temps mort à minimiser visuellement.
4. **Erreur = aide, pas reproche** : chaque message d'erreur guide vers la solution. Jamais de "fichier invalide" sans explication actionnable.
5. **L'utilisateur reste l'expert** : l'outil détecte, l'utilisateur décide. Le rapport est un assistant, pas un juge. Vocabulaire : "détecté", "suggéré", jamais "erreur" ou "faute".

## UX Pattern Analysis & Inspiration

### Inspiring Products Analysis

#### 1. ilovepdf.com — Le modèle direct

| Aspect | Ce qu'ils font bien | Leçon pour Controlmyentries |
|---|---|---|
| **Onboarding** | Zéro — l'outil est auto-explicatif | Notre page doit être lisible en 5 secondes |
| **Upload** | Drop zone centrale massive | Copier ce pattern — zone unique même pour multi-fichiers |
| **Traitement** | Barre de progression simple | On fait MIEUX : 5 étapes détaillées + compteur live |
| **Download** | Bouton Download visible post-traitement | Bouton explicite (pas auto-download silencieux) |

**Pattern clé :** la page EST l'outil. Pas de navigation, pas de compte.

**Adaptation nécessaire :** ilovepdf gère UN fichier. Nous gérons 1-2 fichiers avec détection automatique via dates.

#### 2. Lighthouse / PageSpeed Insights — L'analyse technique lisible

| Aspect | Ce qu'ils font bien | Leçon pour Controlmyentries |
|---|---|---|
| **Score global** | Un chiffre unique (0-100) avec code couleur | Notre "X anomalies détectées" |
| **Progression** | Étapes visibles pendant l'analyse | Nos 5 étapes WebSocket (upgrade vs leur polling HTTP) |
| **Résultats** | Hiérarchie Synthèse → catégories → détails | Structure du rapport Excel |

**Pattern clé :** le résultat est auto-explicatif grâce à une hiérarchie claire.

#### 3. Stripe — L'onboarding bifurqué

| Aspect | Ce qu'ils font bien | Leçon pour Controlmyentries |
|---|---|---|
| **Setup flow** | Première visite = configuration guidée pas à pas | Premier usage = upload N-1 → génération baseline |
| **Daily flow** | Visites suivantes = accès direct au dashboard | Usages suivants = baseline + GL → rapport |
| **Détection d'état** | Le système sait si le setup est fait | Détection automatique : 1 fichier = premier usage possible, 2 fichiers = usage récurrent |

**Pattern clé :** ne pas traiter le premier usage comme les suivants.

#### 4. Notion — La structure hiérarchique

| Aspect | Ce qu'ils font bien | Leçon pour Controlmyentries |
|---|---|---|
| **Blocs hiérarchiques** | Header → sous-sections → détails repliables | Structure des onglets Excel (Synthèse → Catégorie → Détail) |

### Transferable UX Patterns

#### Patterns d'interaction

1. **Drop zone unique intelligente** : une seule zone accepte 1-2 fichiers. Le système détecte automatiquement baseline vs GL via les colonnes de date. Pas de labellisation manuelle.
2. **Détection auto du contexte** : si < 6 mois d'historique détecté dans un fichier unique → conseil inline "Nous recommandons de charger également votre GL de l'année précédente pour une détection plus fiable". L'utilisateur dépose le second fichier, le système reconnaît automatiquement via les dates.
3. **Feedback explicite post-détection** : après upload de 2 fichiers, afficher clairement "Fichier 1 : GL 2024 (référence) ✓ | Fichier 2 : GL janvier 2025 (à analyser) ✓". Si ambiguïté → message clair avec boutons radio pour préciser.
4. **Progression WebSocket 5 étapes** (adaptation Lighthouse) : upgrade technique vs polling. Compteur d'anomalies live.
5. **Bouton download explicite** (correction ilovepdf) : pas d'auto-download silencieux (risque popup-blocker + WCAG). Fichier prêt → bouton "Télécharger le rapport" immédiatement visible.
6. **Alternative clavier équivalente** (WCAG AAA) : bouton "Choisir fichier(s)" aussi visible que la drop zone.
7. **Nom de fichier explicite** : le rapport téléchargé s'appelle `Controlmyentries_Rapport_2025-01_[Entité].xlsx`, pas `report.xlsx`. Facilite l'archivage professionnel.

#### Patterns visuels

1. **Hiérarchie Synthèse → Détail** : compteur principal visible immédiatement, détails en drill-down (rapport Excel).
2. **Code couleur sémantique + formes** : vert/orange/rouge + icônes pour WCAG (daltonisme).
3. **Ton professionnel sobre** : palette réduite, pas de décorations.

#### Patterns de micro-copie

1. **Vocabulaire utilisateur, pas technique** : jamais "baseline" dans l'UI → "GL de l'année précédente" ou "historique de référence".
2. **Micro-copie progressive** :
   - Premier usage : "Déposez votre Grand Livre de l'année précédente (2024)"
   - Usages suivants : "Déposez votre GL mensuel"
   - Pendant traitement : "Analyse en cours... 3 anomalies détectées"
   - Résultat : "Rapport prêt — 12 anomalies à examiner"

### Anti-Patterns to Avoid

1. **Deux zones de drop séparées** : confusion "lequel où ?". → Zone unique + détection auto via dates.
2. **Traiter premier usage = usages suivants** : si Sophie arrive sans historique et voit "déposez 2 fichiers", elle est perdue. → Détection du contexte + guidage adapté.
3. **Auto-download silencieux** : bloqué par navigateurs modernes. → Bouton explicite.
4. **Drop-zone sans alternative clavier** : échec WCAG AAA. → Bouton équivalent visible.
5. **localStorage seul pour baseline** : risque de perte (cache vidé, autre navigateur). → localStorage + download explicite du fichier de référence à chaque génération.
6. **Résultats in-browser** : le livrable EST le fichier Excel. Pas de tableau web. (Note : un preview web léger type WeTransfer a été discuté et explicitement écarté pour le MVP — KISS.)
7. **Configuration pré-analyse** : le Z-score s'adapte seul. Zéro paramètre.
8. **Jargon technique dans l'UI** : "baseline", "Z-score" → vocabulaire métier comptable uniquement.

### Design Inspiration Strategy

**Adopter :**
- Drop zone centrale dominante (ilovepdf)
- Bouton download explicite post-traitement
- Hiérarchie Synthèse → Détail (Lighthouse/Notion)
- Nom de fichier explicite pour archivage pro

**Adapter :**
- Zone unique multi-fichiers avec détection auto via dates (notre innovation)
- Onboarding bifurqué setup/daily (Stripe) → premier usage vs récurrent
- WebSocket progression (upgrade vs Lighthouse polling)
- localStorage + fallback download explicite pour fichier de référence
- Feedback explicite post-détection ("Fichier 1 = référence ✓")
- Micro-copie progressive sans jargon technique

**Éviter :**
- Dual-drop zones labellisées → zone unique intelligente
- Auto-download silencieux → bouton explicite
- Premier = suivant → détection contexte + guidage adapté
- Preview web des résultats → MVP KISS, le fichier Excel EST le livrable
