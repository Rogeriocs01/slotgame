# src/game/assets_config.py
# Arquivo central de configuração de imagens e sons
# Tudo que for visual passa por aqui

import os

# Caminho base do projeto
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# =========================
# IMAGENS
# =========================

BACKGROUND = os.path.join(ASSETS_DIR, "bg.png")

SYMBOLS = {
    "cereja": os.path.join(ASSETS_DIR, "simbolos", "cereja.png"),
    "limao": os.path.join(ASSETS_DIR, "simbolos", "limao.png"),
    "uva": os.path.join(ASSETS_DIR, "simbolos", "uva.png"),
    "morango": os.path.join(ASSETS_DIR, "simbolos", "morango.png"),
    "7": os.path.join(ASSETS_DIR, "simbolos", "7.png"),
}

MASCOT = {
    "idle": os.path.join(ASSETS_DIR, "mascote", "idle.png"),
    "win": os.path.join(ASSETS_DIR, "mascote", "win.png"),
    "lose": os.path.join(ASSETS_DIR, "mascote", "lose.png"),
}

# =========================
# SONS
# =========================

SOUNDS = {
    "click": os.path.join(ASSETS_DIR, "sounds", "click.mp3"),
    "spin": [
        os.path.join(ASSETS_DIR, "sounds", "spin1.wav"),
        os.path.join(ASSETS_DIR, "sounds", "spin2.mp3"),
        os.path.join(ASSETS_DIR, "sounds", "spin3.mp3"),
    ],
    "win": [
        os.path.join(ASSETS_DIR, "sounds", "win1.mp3"),
        os.path.join(ASSETS_DIR, "sounds", "win2.wav"),
        os.path.join(ASSETS_DIR, "sounds", "wincoin1.mp3"),
    ],
    "lose": [
        os.path.join(ASSETS_DIR, "sounds", "lose1.mp3"),
        os.path.join(ASSETS_DIR, "sounds", "lose2.wav"),
    ],
    "theme": os.path.join(ASSETS_DIR, "sounds", "theme1.wav"),
}

