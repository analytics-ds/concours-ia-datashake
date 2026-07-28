# Concours IA datashake, leaderboard

Leaderboard en direct du concours IA interne datashake. Les consultants partagent des process IA, et chacun vote pour ceux qu'il utilise au quotidien.

**URL publique** : https://analytics-ds.github.io/concours-ia-datashake/

## Comment ça marche

- Un process publié et validé par un team lead rapporte 10 points à son auteur.
- Chaque collègue qui l'adopte vote pour lui et ajoute 15 points.
- Score = 10 + (nombre d'adoptions x 15). Le classement se met à jour en direct.
- Un même prénom ne peut voter qu'une fois par process. Les votes sont anonymes côté public.
- Un process peut avoir plusieurs auteurs (champ Auteur de la fiche Notion) : les photos et les noms
  s'affichent tous, et le duo compte comme UN participant au classement, pas comme deux entrées.

## Lien de partage d'un process

`vote.html?p=<mot du nom du process>` affiche une page autonome : le nom, les auteurs, le résumé de la
section « Intérêt » de la fiche Notion, le compteur d'adoptions, et un champ mail qui enregistre
l'adoption dans le même système que le leaderboard.

Exemple : https://analytics-ds.github.io/concours-ia-datashake/vote.html?p=dataslide

Le paramètre `p` accepte l'id complet du process ou n'importe quel mot de son nom (premier process qui
correspond). Pratique pour partager son process dans un canal Slack sans envoyer tout le leaderboard.

## Pour les contributeurs

Le seul fichier à éditer pour ajouter des process est `data.js`. Voir `CLAUDE.md` pour le détail (workflow, architecture, backend).

Site statique, sans build. Pour le lancer en local : ouvrir `index.html` dans un navigateur (les votes tapent directement sur la base Supabase de prod, attention).
