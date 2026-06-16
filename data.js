// =============================================================================
// Données du concours, synchronisées à la main depuis le Catalogue des projets IA (Notion).
// C'est le SEUL fichier à éditer pour faire vivre le leaderboard.
//
// Ajouter un process validé par un team lead = ajouter un objet dans PROCESSES :
//   { id: "slug-unique-stable", name: "Nom lisible", author: "Prénom", bu: "SEO", notion: "https://..." }
// Le champ id ne doit JAMAIS changer une fois posé : c'est lui qui relie le process à ses votes en base.
// Le +10 de publication est automatique (compté par l'app), pas besoin de le saisir.
// =============================================================================

window.PROCESSES = [
  // Exemple de format (à retirer, en attente des premiers process validés) :
  // { id: "cr-call-auto", name: "CR de call automatisé (Fathom + Notion)", author: "Thibault", bu: "SEO", notion: "" },
];

// Liste de suggestions de noms pour le champ de vote (autocomplétion, saisie libre quand même possible).
// À compléter avec l'ensemble des collaborateurs datashake.
window.TEAM = [
  "Alex", "Anthony", "Charlotte", "Damien", "Estelle", "Eve", "Florence",
  "Jeremy", "Julian", "Marie", "Morgane", "Olivia", "Pierre", "Remy",
  "Ruben", "Ryan", "Theo", "Thibault", "Vincent"
];
