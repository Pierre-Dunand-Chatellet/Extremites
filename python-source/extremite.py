import tkinter as tk
import random
import os
import sys

def resource_path(relative_path):
    """Retourne le chemin correct en développement ET dans le .exe PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


class CardGame(tk.Tk):
    """
    Jeu de Cartes — Interface graphique Tkinter
    Avec bascule Mode Nocturne / Mode Jour
    """

    FONT = "Segoe UI"

    # ── Palettes de couleurs ─────────────────────────────────────
    THEMES = {
        "dark": {
            "BG": "#1E1E2E",       # Bleu nuit profond
            "PANEL": "#2A2A3C",    # Bleu-gris désaturé
            "ACCENT": "#89B4FA",   # Bleu pastel
            "GOLD": "#E5C890",     # Or sable doux
            "WHITE": "#CDD6F4",    # Blanc cassé
            "MUTED": "#7F849C",    # Gris bleuté
            "BTN_HOVER": "#74C7EC",# Cyan doux
            "GREEN": "#A6E3A1",    # Vert tendre
            "SCORE_J1": "#89B4FA",
            "SCORE_J2": "#F9E2AF",
            "SHADOW": "#000000"
        },
        "light": {
            "BG": "#FAFAF9",
            "PANEL": "#F5F5F4",
            "ACCENT": "#7C9CF5",
            "GOLD": "#C9A66B",
            "WHITE": "#44403C",
            "MUTED": "#78716C",
            "BTN_HOVER": "#6D8AE8",
            "GREEN": "#7BAE7F",
            "SCORE_J1": "#7C9CF5",
            "SCORE_J2": "#C9A66B",
            "SHADOW": "#E7E5E4"
        }
    }

    def __init__(self):
        super().__init__()
        try:
            self.iconbitmap(resource_path("extremite.ico"))
        except Exception as e:
            print("Erreur icône :", e)

        self.title("Extrémités")
        self.geometry("900x720")
        self.resizable(False, False)

        # ─ État du thème ──────────────────────────────────
        self.is_dark = True
        self.colors = self.THEMES["dark"]
        self.configure(bg=self.colors["BG"])

        # ─ État de la partie ──────────────────────────────
        self.mode         = None    # "pvp" | "bot"
        self.cards        = []
        self.nb_cards_val = 10      # nombre de cartes courant
        self.score_j1     = 0
        self.score_j2     = 0
        self.cur_player   = 1       # PvP uniquement
        self.bot_turn     = False   # Mode bot uniquement
        self.nb_var       = None    

        self.container = tk.Frame(self, bg=self.colors["BG"])
        self.container.pack(fill="both", expand=True)

        self.show_mode_selection()

    # ══════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════

    def clear(self):
        """Supprime tous les widgets de l'écran courant."""
        for w in self.container.winfo_children():
            w.destroy()

    def make_btn(self, parent, text, cmd,
                 color=None, hover=None, width=28,
                 font_size=12, padx_=20, pady_=10):
        """Crée un bouton stylisé avec effet de survol."""
        c  = color or self.colors["ACCENT"]
        hv = hover or self.colors["BTN_HOVER"]
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=c, fg=self.THEMES["dark"]["BG"] if self.is_dark else "#FFFFFF",
            font=(self.FONT, font_size, "bold"),
            relief="flat", bd=0,
            padx=padx_, pady=pady_, width=width,
            cursor="hand2",
            activebackground=hv, activeforeground=self.colors["BG"],
        )
        b.bind("<Enter>", lambda e: b.config(bg=hv) if b["state"] == "normal" else None)
        b.bind("<Leave>", lambda e: b.config(bg=c)  if b["state"] == "normal" else None)
        return b

    def toggle_theme(self):
        """Alterne entre le mode Jour et le mode Nocturne."""
        self.is_dark = not self.is_dark
        self.colors = self.THEMES["dark"] if self.is_dark else self.THEMES["light"]
        self.configure(bg=self.colors["BG"])
        self.container.config(bg=self.colors["BG"])
        self.show_mode_selection()

    # ══════════════════════════════════════════════════════
    # ÉCRAN 1 — Sélection du mode de jeu
    # ══════════════════════════════════════════════════════

    def show_mode_selection(self):
        self.clear()

        # — Barre supérieure avec bouton de thème —
        top_bar = tk.Frame(self.container, bg=self.colors["BG"])
        top_bar.pack(fill="x", padx=20, pady=(15, 0))

        btn_text = "☼  Mode Jour" if self.is_dark else "☾  Mode Nocturne"
        theme_btn = tk.Button(top_bar, text=btn_text, font=(self.FONT, 10, "bold"),
                              bg=self.colors["PANEL"], fg=self.colors["MUTED"],
                              relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
                              command=self.toggle_theme)
        theme_btn.pack(side="right")

        tk.Label(self.container,
                 text="─── Extrémités ───",
                 font=(self.FONT, 30, "bold"),
                 bg=self.colors["BG"], fg=self.colors["ACCENT"]).pack(pady=(15, 6))

        tk.Label(self.container,
                 text="Prenez les meilleures cartes  ·  Accumulez le plus de points",
                 font=(self.FONT, 11, "italic"),
                 bg=self.colors["BG"], fg=self.colors["MUTED"]).pack(pady=(0, 36))

        # Encadré des règles
        rules_panel = tk.Frame(self.container, bg=self.colors["PANEL"])
        rules_panel.pack(padx=90, fill="x")

        tk.Label(rules_panel, text="Règles du jeu",
                 font=(self.FONT, 13, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["WHITE"]).pack(pady=(18, 6))

        tk.Label(rules_panel,
                 text=("À chaque tour, choisissez de prendre la première carte\n"
                       "ou la dernière carte de la séquence.\n"
                       "Le joueur qui totalise le plus de points remporte la partie."),
                 font=(self.FONT, 11),
                 bg=self.colors["PANEL"], fg=self.colors["MUTED"],
                 justify="center").pack(pady=(0, 18))

        # Boutons de sélection de mode
        btn_area = tk.Frame(self.container, bg=self.colors["BG"])
        btn_area.pack(pady=40)

        tk.Label(btn_area, text="Sélectionnez un mode de jeu",
                 font=(self.FONT, 13),
                 bg=self.colors["BG"], fg=self.colors["WHITE"]).pack(pady=(0, 20))

        self.make_btn(btn_area, "❯  Joueur contre Joueur",
                      cmd=lambda: self.set_mode("pvp"), width=32).pack(pady=8)

        self.make_btn(btn_area, "❯  Contre l'Ordinateur",
                      cmd=lambda: self.set_mode("bot"),
                      color=self.colors["GOLD"], width=32).pack(pady=8)

    def set_mode(self, m):
        self.mode = m
        self.show_card_count()

    # ══════════════════════════════════════════════════════
    # ÉCRAN 2 — Choix du nombre de cartes
    # ══════════════════════════════════════════════════════

    def show_card_count(self):
        self.clear()

        tk.Label(self.container, text="─── Préparation ───",
                 font=(self.FONT, 24, "bold"),
                 bg=self.colors["BG"], fg=self.colors["ACCENT"]).pack(pady=(58, 8))

        mode_label = ("Joueur contre Joueur"
                      if self.mode == "pvp" else "Joueur contre Ordinateur")
        tk.Label(self.container, text=f"Mode : {mode_label}",
                 font=(self.FONT, 12, "italic"),
                 bg=self.colors["BG"], fg=self.colors["MUTED"]).pack(pady=(0, 42))

        # Panneau de saisie
        panel = tk.Frame(self.container, bg=self.colors["PANEL"])
        panel.pack(padx=120, fill="x")

        tk.Label(panel, text="Nombre de cartes dans la partie",
                 font=(self.FONT, 13, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["WHITE"]).pack(pady=(22, 12))

        self.nb_var = tk.IntVar(value=self.nb_cards_val)
        stepper_row = tk.Frame(panel, bg=self.colors["PANEL"])
        stepper_row.pack()

        def _make_step_btn(parent, text, cmd):
            sb = tk.Button(parent, text=text,
                           font=(self.FONT, 20, "bold"),
                           bg=self.colors["ACCENT"], fg=self.THEMES["dark"]["BG"] if self.is_dark else "#FFFFFF",
                           relief="flat", bd=0,
                           padx=18, pady=5, cursor="hand2",
                           command=cmd,
                           activebackground=self.colors["BTN_HOVER"],
                           activeforeground=self.colors["BG"])
            sb.bind("<Enter>", lambda e: sb.config(bg=self.colors["BTN_HOVER"]))
            sb.bind("<Leave>", lambda e: sb.config(bg=self.colors["ACCENT"]))
            return sb

        _make_step_btn(stepper_row, "−", self._dec).pack(side="left", padx=10)
        tk.Label(stepper_row, textvariable=self.nb_var,
                 font=(self.FONT, 32, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["WHITE"], width=3).pack(side="left")
        _make_step_btn(stepper_row, "+", self._inc).pack(side="left", padx=10)

        # On limite de nouveau à 20 cartes max pour forcer 2 lignes de 10
        tk.Label(panel, text="Min : 2  ·  Max : 20",
                 font=(self.FONT, 10, "italic"),
                 bg=self.colors["PANEL"], fg=self.colors["MUTED"]).pack(pady=(8, 22))

        # Boutons d'action
        btn_area = tk.Frame(self.container, bg=self.colors["BG"])
        btn_area.pack(pady=36)

        self.make_btn(btn_area, "❯  Commencer la Partie",
                      cmd=self.start_game, width=32).pack(pady=8)
        self.make_btn(btn_area, "❮  Retour",
                      cmd=self.show_mode_selection,
                      color=self.colors["MUTED"], width=32).pack(pady=8)

    def _dec(self):
        if self.nb_cards_val > 2:
            self.nb_cards_val -= 1
            self.nb_var.set(self.nb_cards_val)

    def _inc(self):
        if self.nb_cards_val < 20:
            self.nb_cards_val += 1
            self.nb_var.set(self.nb_cards_val)

    def start_game(self):
        self.cards      = [random.randint(1, 13) for _ in range(self.nb_cards_val)]
        self.score_j1   = 0
        self.score_j2   = 0
        self.cur_player = 1
        self.bot_turn   = False
        if self.mode == "bot":
            self.bot_turn = random.choice([True, False])
        self.show_game()

    # ══════════════════════════════════════════════════════
    # ÉCRAN 3 — Plateau de jeu
    # ══════════════════════════════════════════════════════

    def show_game(self):
        self.clear()

        # — Barre de titre —
        hdr = tk.Frame(self.container, bg=self.colors["PANEL"], height=55)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        hdr_title = ("Joueur 1  ─  Joueur 2"
                     if self.mode == "pvp" else "Joueur  ─  Ordinateur")
        tk.Label(hdr, text=hdr_title,
                 font=(self.FONT, 15, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["ACCENT"]).pack(side="left", padx=25, pady=14)

        self.rl = tk.Label(hdr, text=f"Cartes restantes : {len(self.cards)}",
                           font=(self.FONT, 11),
                           bg=self.colors["PANEL"], fg=self.colors["MUTED"])
        self.rl.pack(side="right", padx=25)

        # — Scores —
        sf = tk.Frame(self.container, bg=self.colors["BG"])
        sf.pack(fill="x", padx=50, pady=(15, 0))

        p1f = tk.Frame(sf, bg=self.colors["BG"])
        p1f.pack(side="left", expand=True)
        p1_name = "Joueur 1" if self.mode == "pvp" else "Joueur"
        tk.Label(p1f, text=p1_name,
                 font=(self.FONT, 12, "bold"),
                 bg=self.colors["BG"], fg=self.colors["SCORE_J1"]).pack()
        self.sv1 = tk.StringVar(value="0")
        tk.Label(p1f, textvariable=self.sv1,
                 font=(self.FONT, 32, "bold"),
                 bg=self.colors["BG"], fg=self.colors["SCORE_J1"]).pack()

        tk.Label(sf, text="─── vs ───",
                 font=(self.FONT, 14, "italic"),
                 bg=self.colors["BG"], fg=self.colors["MUTED"]).pack(side="left", expand=True)

        p2f = tk.Frame(sf, bg=self.colors["BG"])
        p2f.pack(side="left", expand=True)
        p2_name = "Joueur 2" if self.mode == "pvp" else "Ordinateur"
        tk.Label(p2f, text=p2_name,
                 font=(self.FONT, 12, "bold"),
                 bg=self.colors["BG"], fg=self.colors["SCORE_J2"]).pack()
        self.sv2 = tk.StringVar(value="0")
        tk.Label(p2f, textvariable=self.sv2,
                 font=(self.FONT, 32, "bold"),
                 bg=self.colors["BG"], fg=self.colors["SCORE_J2"]).pack()

        # — Séparateur —
        tk.Frame(self.container, bg=self.colors["PANEL"], height=1).pack(fill="x", padx=40, pady=10)

        # — Indicateur de tour —
        self.tv = tk.StringVar()
        self._upd_turn()
        tk.Label(self.container, textvariable=self.tv,
                 font=(self.FONT, 12, "italic"),
                 bg=self.colors["BG"], fg=self.colors["MUTED"]).pack(pady=(0, 6))

        # — Canvas des cartes —
        self.cc = tk.Canvas(self.container, bg=self.colors["BG"],
                            highlightthickness=0, height=220)
        self.cc.pack(fill="x", padx=20)
        self.cc.bind("<Configure>", lambda e: self._redraw())
        self.after(60, self._redraw)

        # — Boutons —
        bf = tk.Frame(self.container, bg=self.colors["BG"])
        bf.pack(pady=10)

        self.lbtn = self.make_btn(bf, "❮  Première Carte",
                                  cmd=lambda: self.take("G"), width=22)
        self.lbtn.pack(side="left", padx=20)

        self.rbtn = self.make_btn(bf, "Dernière Carte  ❯",
                                  cmd=lambda: self.take("D"), width=22)
        self.rbtn.pack(side="left", padx=20)

        self.stv = tk.StringVar(value="")
        tk.Label(self.container, textvariable=self.stv,
                 font=(self.FONT, 11, "italic"),
                 bg=self.colors["BG"], fg=self.colors["GREEN"]).pack(pady=4)

        if self.mode == "bot" and self.bot_turn:
            self._dis()
            self.after(900, self._bot)

    # ── Rendu dynamique contraint (Max 10/ligne) ──────────

    def _redraw(self):
        cc = self.cc
        cw = cc.winfo_width()
        if cw <= 1:
            self.after(60, self._redraw)
            return
        cc.delete("all")
        n = len(self.cards)
        if not n:
            return

        ch  = cc.winfo_height()
        GAP = 8
        caw = 64
        cah = 96
        
        # On force la grille à un maximum de 10 cartes par ligne
        cols = min(10, n) if n > 0 else 1
        rows = (n + cols - 1) // cols 

        tot_h = rows * cah + (rows - 1) * GAP
        y0 = (ch - tot_h) / 2

        shadow_color = self.colors["SHADOW"]

        for i, v in enumerate(self.cards):
            r = i // cols
            c = i % cols
            
            # Recalcul pour centrer la ligne actuelle
            cards_in_this_row = min(cols, n - r * cols)
            tot_w = cards_in_this_row * caw + (cards_in_this_row - 1) * GAP
            x0 = (cw - tot_w) / 2
            
            bx = x0 + c * (caw + GAP)
            by = y0 + r * (cah + GAP)
            cx = bx + caw / 2
            cy = by + cah / 2
            
            edge = (i == 0 or i == n - 1)
            fill = self.colors["ACCENT"] if edge else self.colors["PANEL"]
            tfg  = self.colors["BG"] if edge else self.colors["WHITE"]

            # Ombre portée
            cc.create_rectangle(bx + 3, by + 4, bx + caw + 3, by + cah + 4, 
                                fill=shadow_color, outline="", stipple="gray50")
            
            # Carte
            cc.create_rectangle(bx, by, bx + caw, by + cah, 
                                fill=fill, outline=self.colors["GOLD"], width=2 if edge else 1)
            
            # Valeur
            cc.create_text(cx, cy, text=str(v), font=(self.FONT, 20, "bold"), fill=tfg)
            
            # Flèches
            if edge:
                arr = "❮" if i == 0 else "❯"
                cc.create_text(cx, cy + cah/2 - 12, text=arr, 
                               font=(self.FONT, 10), fill=self.colors["GOLD"])

    # ── Logique de jeu ─────────────────────────────────────

    def _upd_turn(self):
        if self.mode == "pvp":
            self.tv.set(f"─── Tour du Joueur {self.cur_player} ───")
        elif self.bot_turn:
            self.tv.set("─── Tour de l'Ordinateur ───")
        else:
            self.tv.set("─── Votre tour ───")

    def _dis(self):
        for b in (self.lbtn, self.rbtn):
            b.config(state="disabled", bg=self.colors["MUTED"], cursor="")

    def _ena(self):
        for b in (self.lbtn, self.rbtn):
            b.config(state="normal", bg=self.colors["ACCENT"], cursor="hand2")

    def take(self, side):
        if not self.cards: return
        val = self.cards.pop(0) if side == "G" else self.cards.pop()
        sf  = "première" if side == "G" else "dernière"

        if self.mode == "pvp":
            if self.cur_player == 1:
                self.score_j1 += val
                self.sv1.set(str(self.score_j1))
                self.stv.set(f"Joueur 1 prend la {sf} carte  ·  +{val} pt")
            else:
                self.score_j2 += val
                self.sv2.set(str(self.score_j2))
                self.stv.set(f"Joueur 2 prend la {sf} carte  ·  +{val} pt")
            self.cur_player = 2 if self.cur_player == 1 else 1
        else:
            self.score_j1 += val
            self.sv1.set(str(self.score_j1))
            self.stv.set(f"Vous prenez la {sf} carte  ·  +{val} pt")
            self.bot_turn = True
            self._dis()

        self.rl.config(text=f"Cartes restantes : {len(self.cards)}")
        self._redraw()

        if not self.cards:
            self.after(900, self.show_result)
            return

        self._upd_turn()
        if self.mode == "bot":
            self.after(1000, self._bot)

    def _bot(self):
        if not self.cards: return

        side = "G" if self.cards[0] > self.cards[-1] else "D"
        val  = self.cards.pop(0) if side == "G" else self.cards.pop()
        sf   = "première" if side == "G" else "dernière"

        self.score_j2 += val
        self.sv2.set(str(self.score_j2))
        self.stv.set(f"L'Ordinateur prend la {sf} carte  ·  +{val} pt")
        self.bot_turn = False

        self.rl.config(text=f"Cartes restantes : {len(self.cards)}")
        self._redraw()

        if not self.cards:
            self.after(900, self.show_result)
            return

        self._upd_turn()
        self._ena()

    # ══════════════════════════════════════════════════════
    # ÉCRAN 4 — Résultat de la partie
    # ══════════════════════════════════════════════════════

    def show_result(self):
        self.clear()

        if self.mode == "pvp":
            if self.score_j1 > self.score_j2:
                msg, mc = "Le Joueur 1 remporte la victoire !", self.colors["SCORE_J1"]
            elif self.score_j2 > self.score_j1:
                msg, mc = "Le Joueur 2 remporte la victoire !", self.colors["SCORE_J2"]
            else:
                msg, mc = "Égalité parfaite !", self.colors["MUTED"]
        else:
            if self.score_j1 > self.score_j2:
                msg, mc = "Victoire !  Vous l'emportez !", self.colors["GREEN"]
            elif self.score_j2 > self.score_j1:
                msg, mc = "L'Ordinateur l'emporte.  Bien essayé.", self.colors["ACCENT"]
            else:
                msg, mc = "Égalité !", self.colors["MUTED"]

        tk.Label(self.container, text="─── Fin de la Partie ───",
                 font=(self.FONT, 24, "bold"),
                 bg=self.colors["BG"], fg=self.colors["ACCENT"]).pack(pady=(72, 18))

        tk.Label(self.container, text=msg,
                 font=(self.FONT, 20, "bold"),
                 bg=self.colors["BG"], fg=mc).pack(pady=(0, 36))

        rec = tk.Frame(self.container, bg=self.colors["PANEL"])
        rec.pack(padx=120, fill="x")

        tk.Label(rec, text="─  Score final  ─",
                 font=(self.FONT, 13, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["WHITE"]).pack(pady=(18, 12))

        row = tk.Frame(rec, bg=self.colors["PANEL"])
        row.pack(pady=(0, 18))

        p1n = "Joueur 1" if self.mode == "pvp" else "Joueur"
        p2n = "Joueur 2" if self.mode == "pvp" else "Ordinateur"

        tk.Label(row, text=f"{p1n}  :  {self.score_j1} pts",
                 font=(self.FONT, 16, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["SCORE_J1"]).pack(side="left", padx=50)
        tk.Label(row, text=f"{p2n}  :  {self.score_j2} pts",
                 font=(self.FONT, 16, "bold"),
                 bg=self.colors["PANEL"], fg=self.colors["SCORE_J2"]).pack(side="left", padx=50)

        opts = tk.Frame(self.container, bg=self.colors["BG"])
        opts.pack(pady=36)

        tk.Label(opts, text="Que souhaitez-vous faire ?",
                 font=(self.FONT, 12),
                 bg=self.colors["BG"], fg=self.colors["WHITE"]).pack(pady=(0, 18))

        self.make_btn(opts, "❯  Rejouer (mêmes paramètres)",
                      cmd=self.start_game, width=36).pack(pady=7)

        self.make_btn(opts, "❯  Changer le nombre de cartes",
                      cmd=self.show_card_count,
                      color=self.colors["GOLD"], width=36).pack(pady=7)

        self.make_btn(opts, "❯  Retourner à l'accueil",
                      cmd=self.show_mode_selection,
                      color=self.colors["MUTED"], width=36).pack(pady=7)

if __name__ == "__main__":
    app = CardGame()
    app.mainloop()