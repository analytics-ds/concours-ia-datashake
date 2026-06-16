// =============================================================================
// ⚠️ ÉTAT DE TEST (2026-06-16) — temporaire.
// 3 process fictifs + liste de votants réduite à 4 personnes, pour tester le live.
// À NETTOYER au go de Damien : restaurer la vraie version via git
//   (git checkout HEAD~N -- data.js) ou recharger PROCESSES=[] + la liste TEAM complète des 74 noms,
//   puis supprimer les votes de test : delete from votes where process_id like 'test-%';
// La vraie liste TEAM (74 collaborateurs) est dans l'historique git.
// =============================================================================

window.PROCESSES = [
  { id: "test-remy", name: "Synthèse hebdo des perfs toutes BU", author: "Rémy Bendayan", bu: "Direction", notion: "" },
  { id: "test-antho", name: "Préparation automatisée des points clients", author: "Anthony Chelly", bu: "Direction", notion: "" },
  { id: "test-damien", name: "Brief SEO généré en autonomie", author: "Damien Borieu", bu: "SEO", notion: "" },
];

// Votants possibles pendant le test (liste réduite).
window.TEAM = [
  "👑 Rémy Bendayan",
  "👑 Anthony Chelly",
  "🔍 Damien Borieu",
  "🛠️ Clara Magnin"
];
