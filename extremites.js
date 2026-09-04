"use strict";

// version web d'Extrémités, mon jeu de cartes fait en Python (Tkinter) à la base.
// même logique, même IA (assez simple, cf botPlay plus bas), portée en JS.

const screens = {
  mode: document.getElementById("screen-mode"),
  setup: document.getElementById("screen-setup"),
  game: document.getElementById("screen-game"),
  result: document.getElementById("screen-result"),
};

const themeBtn = document.getElementById("theme-btn");
const modeLabel = document.getElementById("mode-label");
const stepValue = document.getElementById("step-value");
const stepDec = document.getElementById("step-dec");
const stepInc = document.getElementById("step-inc");
const hdrTitle = document.getElementById("hdr-title");
const remainingLabel = document.getElementById("remaining-label");
const p1Name = document.getElementById("p1-name");
const p2Name = document.getElementById("p2-name");
const p1Score = document.getElementById("p1-score");
const p2Score = document.getElementById("p2-score");
const turnIndicator = document.getElementById("turn-indicator");
const cardsTrack = document.getElementById("cards-track");
const takeLeftBtn = document.getElementById("take-left");
const takeRightBtn = document.getElementById("take-right");
const statusLine = document.getElementById("status-line");
const resultMsg = document.getElementById("result-msg");
const resultP1 = document.getElementById("result-p1");
const resultP2 = document.getElementById("result-p2");

let isDark = true;
let mode = null;
let nbCardsVal = 10;
let state = null;

function showScreen(name) {
  Object.values(screens).forEach((s) => s.classList.remove("is-active"));
  screens[name].classList.add("is-active");
}

// le thème jour/nuit du jeu est indépendant de celui du reste du portfolio,
// je le garde en mémoire (isDark) plutôt qu'en localStorage, pas besoin qu'il
// soit persistant ici — à chaque partie on repart du thème sombre
function applyTheme() {
  if (isDark) {
    document.documentElement.removeAttribute("data-theme");
    themeBtn.textContent = "☼ Mode Jour";
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    themeBtn.textContent = "☾ Mode Nocturne";
  }
}

themeBtn.addEventListener("click", () => {
  isDark = !isDark;
  applyTheme();
});

document.querySelectorAll("[data-mode]").forEach((b) =>
  b.addEventListener("click", () => {
    mode = b.dataset.mode;
    modeLabel.textContent =
      mode === "pvp" ? "Mode : Joueur contre Joueur" : "Mode : Joueur contre Ordinateur";
    stepValue.textContent = String(nbCardsVal);
    showScreen("setup");
  })
);

stepDec.addEventListener("click", () => {
  if (nbCardsVal > 2) {
    nbCardsVal -= 1;
    stepValue.textContent = String(nbCardsVal);
  }
});

stepInc.addEventListener("click", () => {
  if (nbCardsVal < 20) {
    nbCardsVal += 1;
    stepValue.textContent = String(nbCardsVal);
  }
});

document.getElementById("setup-back-btn").addEventListener("click", () => showScreen("mode"));
document.getElementById("start-game-btn").addEventListener("click", startGame);
document.getElementById("replay-same-btn").addEventListener("click", startGame);
document.getElementById("replay-count-btn").addEventListener("click", () => {
  stepValue.textContent = String(nbCardsVal);
  showScreen("setup");
});
document.getElementById("replay-home-btn").addEventListener("click", () => showScreen("mode"));

takeLeftBtn.addEventListener("click", () => take("G"));
takeRightBtn.addEventListener("click", () => take("D"));

function startGame() {
  // valeurs 1 à 13 comme un jeu de cartes classique (as à roi, sans les figures
  // de couleur — juste le chiffre compte pour le score)
  const cards = [];
  for (let i = 0; i < nbCardsVal; i++) cards.push(1 + Math.floor(Math.random() * 13));

  state = {
    cards,
    scoreJ1: 0,
    scoreJ2: 0,
    curPlayer: 1,
    // tirage au sort pour savoir qui commence contre le bot, sinon le joueur
    // aurait toujours la main en premier ce qui l'avantage un peu
    botTurn: mode === "bot" ? Math.random() < 0.5 : false,
  };

  hdrTitle.textContent = mode === "pvp" ? "Joueur 1  ─  Joueur 2" : "Joueur  ─  Ordinateur";
  p1Name.textContent = mode === "pvp" ? "Joueur 1" : "Joueur";
  p2Name.textContent = mode === "pvp" ? "Joueur 2" : "Ordinateur";
  p1Score.textContent = "0";
  p2Score.textContent = "0";
  statusLine.textContent = "";

  updateRemaining();
  updateTurnIndicator();
  renderCards();
  enableTakeButtons();

  showScreen("game");

  if (mode === "bot" && state.botTurn) {
    disableTakeButtons();
    setTimeout(botPlay, 900);
  }
}

function updateRemaining() {
  remainingLabel.textContent = `Cartes restantes : ${state.cards.length}`;
}

function updateTurnIndicator() {
  if (mode === "pvp") {
    turnIndicator.textContent = `─── Tour du Joueur ${state.curPlayer} ───`;
  } else if (state.botTurn) {
    turnIndicator.textContent = "─── Tour de l'Ordinateur ───";
  } else {
    turnIndicator.textContent = "─── Votre tour ───";
  }
}

// redessine toute la rangée de cartes — plus simple de tout vider et
// reconstruire à chaque coup que d'essayer de retirer juste une carte du DOM
function renderCards() {
  cardsTrack.innerHTML = "";
  const n = state.cards.length;
  state.cards.forEach((value, i) => {
    const el = document.createElement("div");
    // seules les cartes aux deux bouts sont prenables, donc seules elles
    // sont mises en avant (couleur + flèche) pour que ce soit clair au joueur
    const edge = i === 0 || i === n - 1;
    el.className = "card" + (edge ? " is-edge" : "");
    el.textContent = String(value);
    if (edge) {
      const arrow = document.createElement("span");
      arrow.className = "arrow";
      arrow.textContent = i === 0 ? "❮" : "❯";
      el.appendChild(arrow);
    }
    cardsTrack.appendChild(el);
  });
}

function disableTakeButtons() {
  takeLeftBtn.disabled = true;
  takeRightBtn.disabled = true;
}

function enableTakeButtons() {
  takeLeftBtn.disabled = false;
  takeRightBtn.disabled = false;
}

function take(side) {
  if (!state.cards.length) return;
  const val = side === "G" ? state.cards.shift() : state.cards.pop();
  const sf = side === "G" ? "première" : "dernière";

  if (mode === "pvp") {
    if (state.curPlayer === 1) {
      state.scoreJ1 += val;
      p1Score.textContent = String(state.scoreJ1);
      statusLine.textContent = `Joueur 1 prend la ${sf} carte  ·  +${val} pt`;
    } else {
      state.scoreJ2 += val;
      p2Score.textContent = String(state.scoreJ2);
      statusLine.textContent = `Joueur 2 prend la ${sf} carte  ·  +${val} pt`;
    }
    state.curPlayer = state.curPlayer === 1 ? 2 : 1;
  } else {
    state.scoreJ1 += val;
    p1Score.textContent = String(state.scoreJ1);
    statusLine.textContent = `Vous prenez la ${sf} carte  ·  +${val} pt`;
    state.botTurn = true;
    disableTakeButtons();
  }

  updateRemaining();
  renderCards();

  if (!state.cards.length) {
    setTimeout(showResult, 900);
    return;
  }

  updateTurnIndicator();
  if (mode === "bot") {
    setTimeout(botPlay, 1000);
  }
}

// IA volontairement simple : le bot regarde juste les deux cartes visibles
// (première/dernière) et prend celle qui vaut le plus. Pas de calcul plus loin
// que ça, donc un joueur qui réfléchit un peu à l'avance peut le battre
function botPlay() {
  if (!state.cards.length) return;

  const side = state.cards[0] > state.cards[state.cards.length - 1] ? "G" : "D";
  const val = side === "G" ? state.cards.shift() : state.cards.pop();
  const sf = side === "G" ? "première" : "dernière";

  state.scoreJ2 += val;
  p2Score.textContent = String(state.scoreJ2);
  statusLine.textContent = `L'Ordinateur prend la ${sf} carte  ·  +${val} pt`;
  state.botTurn = false;

  updateRemaining();
  renderCards();

  if (!state.cards.length) {
    setTimeout(showResult, 900);
    return;
  }

  updateTurnIndicator();
  enableTakeButtons();
}

function showResult() {
  let msg;
  if (mode === "pvp") {
    if (state.scoreJ1 > state.scoreJ2) msg = "Le Joueur 1 remporte la victoire !";
    else if (state.scoreJ2 > state.scoreJ1) msg = "Le Joueur 2 remporte la victoire !";
    else msg = "Égalité parfaite !";
  } else {
    if (state.scoreJ1 > state.scoreJ2) msg = "Victoire !  Vous l'emportez !";
    else if (state.scoreJ2 > state.scoreJ1) msg = "L'Ordinateur l'emporte.  Bien essayé.";
    else msg = "Égalité !";
  }

  resultMsg.textContent = msg;
  const p1n = mode === "pvp" ? "Joueur 1" : "Joueur";
  const p2n = mode === "pvp" ? "Joueur 2" : "Ordinateur";
  resultP1.textContent = `${p1n}  :  ${state.scoreJ1} pts`;
  resultP2.textContent = `${p2n}  :  ${state.scoreJ2} pts`;

  showScreen("result");
}

applyTheme();
