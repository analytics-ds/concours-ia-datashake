// =============================================================================
// Données du concours, synchronisées à la main depuis le Catalogue des projets IA (Notion).
// data.js = le seul fichier à éditer pour faire vivre le leaderboard.
//
// Ajouter un process validé par un team lead = ajouter un objet dans PROCESSES :
//   { id: "slug-unique-stable", name: "Nom lisible", author: "Prénom Nom", bu: "SEO", notion: "https://..." }
// Le champ id ne doit JAMAIS changer une fois posé : il relie le process à ses votes en base.
// Le +10 de publication est automatique (compté par l'app), pas besoin de le saisir.
// =============================================================================

window.PROCESSES = [
  // En attente des premiers process validés. Exemple de format :
  // { id: "cr-call-auto", name: "CR de call automatisé (Fathom + Notion)", author: "Damien Borieu", bu: "SEO", notion: "" },
];

// Liste des collaborateurs datashake pour le champ de vote (autocomplétion).
// Emoji = équipe. Source : organigramme Notion. Noms complets car beaucoup d'homonymes de prénom.
// Emojis natifs (SEA) : 🌈 Smarties, 🦊 Foxies, 🌶️ Spicies, ☕️ Cozy, 🍪 Cookiz.
// Emojis de pôle (choisis, l'organigramme n'en a pas) : 🔍 SEO, 🎨 Studio, 💌 CRM, 🤝 Sales, 👑 Direction, 📋 Admin/RH, 🛠️ Quality/Dev, 📊 Tracking.
window.TEAM = [
  // SEO
  "🔍 Ruben Sebag", "🔍 Damien Borieu", "🔍 Charlie Limbour", "🔍 Manon Masa",
  "🔍 Jérôme Chamberlain", "🔍 Valentin Lefevre", "🔍 Thibaut Guisnet",
  "🔍 Théo Steinlen", "🔍 Kiara Jules-Rosette", "🔍 Pierre Gaudard",
  "🔍 Audrey Chambon", "🔍 Léo Cottu", "🔍 Manon Lamache", "🔍 Hugo Husson",
  // SEA - Cookiz 🍪
  "🍪 Florence Pernet", "🍪 Elia Manguso", "🍪 Bérangère Chateigner",
  "🍪 Juliette Covat", "🍪 Matthieu Soum", "🍪 Constance De Beaulieau",
  // SEA - Cozy ☕️
  "☕️ Alex Kartalyan", "☕️ Laurine Hidalgo", "☕️ Dorian Richard",
  "☕️ Paul Ferreira", "☕️ Tom Hamze", "☕️ Hugo Rabain", "☕️ Clara Husset",
  "☕️ Maëva Mayé", "☕️ Maëva Garbez",
  // SEA - Foxies 🦊
  "🦊 Ryan Curpen", "🦊 Amaury Dormoy", "🦊 Samuel Giles", "🦊 Clara Poncet",
  "🦊 Nicolas Hay", "🦊 Célia Lambertod",
  // SEA - Smarties 🌈
  "🌈 Louis Bonjour", "🌈 Manon Lamarre", "🌈 Éléa Decostaire", "🌈 Elodie Soldo",
  "🌈 Lenny Lesne", "🌈 Marie-Emmanuelle",
  // SEA - Spicies 🌶️
  "🌶️ Olivia Troehler", "🌶️ Jane Bonneville", "🌶️ Solène Perroy",
  "🌶️ Erwan Tanguy", "🌶️ Emilie Deleigue", "🌶️ Estelle Durivault", "🌶️ Alicia Kremer",
  // Studio (créa) 🎨
  "🎨 Charlotte Cohen", "🎨 Nathaniel Benhamou", "🎨 Amina Tahri", "🎨 Elsa Elmalem",
  "🎨 Kevin Épée", "🎨 Yanis Daubié", "🎨 Arthur Privat", "🎨 Marlène Adjovi",
  // CRM 💌
  "💌 Morgane Chabagny", "💌 Liam Laribi", "💌 Lou Verplancke", "💌 Mathilde Chabert",
  // Sales 🤝
  "🤝 Vincent Coupat", "🤝 Lilian Scarpino", "🤝 Emma Bonneville", "🤝 Sacha Cardine",
  "🤝 Tom Cayer-Barrioz", "🤝 Félix Horréard",
  // Tracking 📊
  "📊 Julian Gillot",
  // Quality & Dev 🛠️
  "🛠️ Clara Magnin", "🛠️ Sami Hadj-Chaouch",
  // Admin & RH 📋
  "📋 Marion Péan", "📋 Théodore Fresnais", "📋 Audrey Ortega",
  // Direction 👑
  "👑 Rémy Bendayan", "👑 Anthony Chelly"
];
