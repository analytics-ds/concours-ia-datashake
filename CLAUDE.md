# Concours IA datashake, leaderboard

App web statique du concours IA interne datashake (sous-projet de "datashake ai"). Affiche le classement en direct des process IA partagés par les consultants, et permet de voter pour ceux qu'on utilise.

Ce repo vit **hors Google Drive** (un repo git dans Drive se corrompt). Emplacement local : `~/code/concours-ia-datashake/`. Source de la doc projet côté Drive : `200🎯 Projects/🚀 Autres projets/datashake ai/Concours IA/`.

## Le concept (Format B, "la ligue continue")

- Un consultant crée un process IA utile, le partage oralement à son team lead.
- Validé, il publie une card dans le Catalogue des projets IA (Notion) : +10 points.
- Chaque collègue qui adopte et utilise le process vote pour lui : +15 points par adoption.
- Score d'un process = 10 + (nombre de votes x 15). Podium top 1 / top 2 en fin de saison.

## Architecture

Site statique, zéro build, zéro dépendance, déployé sur GitHub Pages.

| Fichier | Rôle |
|---|---|
| `index.html` | Toute l'app (style + logique). Lit les process dans `data.js`, les votes dans Supabase via fetch. |
| `data.js` | **Le seul fichier à éditer pour faire vivre le concours.** `window.PROCESSES` (liste des process, synchronisée à la main depuis le Catalogue Notion) + `window.TEAM` (votants = `{ e: "email", n: "Nom — BU" }`, 82 actifs). |

Le vote se fait par **adresse mail `@datashake.fr`** (clé unique anti-doublon, gère les homonymes de prénom ; validation `@datashake.fr` côté front). `window.TEAM` est généré depuis l'annuaire `100🗺️ Areas/datashake/Team/Annuaire datashake - emails.md` (master de Damien) : parser le tableau (colonnes Nom, BU, Email) en objets `{e: email, n: "Nom — BU"}` triés par nom. L'annuaire vit hors du repo (dans le Drive), il n'est pas versionné ici.

**Avatars** (`photos.js` + `assets/photos/`) : chaque process affiche la photo de son auteur (podium + classement), fallback initiales si absente. `window.PHOTOS` mappe `"Nom complet" -> "assets/photos/<localpart-email>.jpg"`. Avatars 128px carrés (arrondis en CSS), ~344 Ko au total. Sources : couvertures de l'organigramme Notion (S3, URL signées expirantes -> à télécharger sur le moment) en priorité, complétées par les avatars Slack via `slack_search_users` (URL `avatars.slack-edge.com`, stables). Pour ajouter un avatar : déposer un jpg 128px dans `assets/photos/<localpart>.jpg` et ajouter la ligne dans `photos.js` (clé = nom complet = `author` du process).
| `config.js` | URL Supabase + clé publishable (publique par design, protégée par RLS). |

### Backend Supabase (projet `ejkzpzftytpeladvcfnk`, région EU)

- Table `votes` : `id`, `process_id` (text), `voter_name` (text, stocké normalisé en minuscules), `created_at`, contrainte unique `(process_id, voter_name)` qui fait l'anti-doublon.
- RLS activé. Une seule policy : INSERT autorisé pour anon. **Pas de policy SELECT** : personne ne peut lire qui a voté quoi via la clé publique, seuls les totaux sortent.
- Fonction `get_vote_counts()` (SECURITY DEFINER) : renvoie `[{process_id, votes}]` agrégé. C'est ce que le front appelle pour le classement.
- Le front insère un vote (`POST /rest/v1/votes`), un doublon renvoie 409.

Les credentials secrets (secret key, access token, mot de passe DB, clés legacy) ne sont **jamais** dans ce repo. Ils vivent dans le `.env` du master 000 data et dans Bitwarden. Seule la clé publishable est dans `config.js`.

## Charte graphique (DA datashake 2026)

L'interface suit la DA 2026 de datashake (celle de la newsletter AI, Figma "Newsletter AI"). À respecter pour toute évolution visuelle :

- **Couleurs** : noir `#101010` (texte, boutons, logo), beige `#f3ede8` (fond de page + pills/tags), blanc `#ffffff` (cartes, pastilles), gris translucide `rgba(16,16,16,0.7)` et `0.55` (textes secondaires). Accents podium chauds compatibles beige : or `#c2a14e`, argent/taupe `#a9a399`, bronze `#b07d4f`.
- **Typo** : titres en **Instrument Sans** (600), corps et labels en **Inter** (400/600/700), via Google Fonts.
- **Style** : coins peu arrondis (4px pills/boutons, 10px cartes), boutons noirs texte blanc, pills beige, épuré.
- **Logo** : `assets/logo-datashake.svg` = logo noir datashake 2026 (`logo_ds26_black.svg` de la charte), affiché tel quel (noir) sur fond clair, sans filtre. Source charte : `300🪵 Ressources/datashake/charte datashake/da 2026/`.

Ne pas revenir à l'ancienne DA bleue (#0C0D62), abandonnée.

## Faire vivre le leaderboard (workflow récurrent)

Quand Damien dit "ajoute les nouveaux process au concours" :

1. Lire le Catalogue des projets IA (Notion) et repérer les cards validées absentes de `data.js`.
2. Pour chaque nouveau process, ajouter dans `window.PROCESSES` un objet :
   `{ id: "slug-stable", name: "Nom", author: "Prénom", bu: "SEO", notion: "https://..." }`.
   L'`id` est un slug court et **stable** (ne jamais le changer après coup, il relie le process à ses votes en base).
3. `git add -A && git commit && git push`. GitHub Pages redéploie tout seul en ~1 min.

Le +10 de publication est automatique (ajouté par l'app), rien à saisir.

## Déploiement

- Repo GitHub : `analytics-ds/concours-ia-datashake` (public, compte datashake `analytics@datashake.fr`).
- GitHub Pages depuis la branche `main`, racine. URL publique dans le README.
- Aucune action manuelle après un push : Pages rebuild automatiquement.

## Modifier le schéma Supabase

Via l'API de management avec l'access token (dans le `.env`, clé `SUPABASE_CONCOURS_ACCESS_TOKEN`).
Quirk : l'endpoint `api.supabase.com` bloque les requêtes sans user-agent navigateur (Cloudflare 1010), toujours passer un `User-Agent: Mozilla/...`.
Endpoint SQL : `POST https://api.supabase.com/v1/projects/ejkzpzftytpeladvcfnk/database/query`, body `{"query":"..."}`.
