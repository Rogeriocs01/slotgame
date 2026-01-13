# pygame_interface.py
# Implementa animação REAL de rolagem com desaceleração e parada por coluna

import os
import sys
import random
import pygame

# =========================
# Paths
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SYMBOLS_DIR = os.path.join(ASSETS_DIR, "symbols")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
BG_PATH = os.path.join(ASSETS_DIR, "bg.png")

# =========================
# Config
# =========================
SCREEN_W, SCREEN_H = 900, 600
FPS = 60
COLS = 3
ROWS_VISIBLE = 3
SYMBOL_SIZE = 120
REEL_GAP = 20
TOP_MARGIN = 120
LEFT_MARGIN = (SCREEN_W - (COLS * SYMBOL_SIZE + (COLS - 1) * REEL_GAP)) // 2

SPIN_SPEED_START = 35
SPIN_DECEL = 0.6
MIN_SPEED = 2
STOP_DELAY_FRAMES = 18  # atraso entre paradas das colunas

# =========================
# Helpers
# =========================

def load_symbols():
    symbols = []
    for f in os.listdir(SYMBOLS_DIR):
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            img = pygame.image.load(os.path.join(SYMBOLS_DIR, f)).convert_alpha()
            img = pygame.transform.smoothscale(img, (SYMBOL_SIZE, SYMBOL_SIZE))
            symbols.append((os.path.splitext(f)[0], img))
    if not symbols:
        raise RuntimeError("Nenhum símbolo encontrado em assets/symbols")
    return symbols

# =========================
# Slot Machine (lógica simples)
# =========================
class SlotMachine:
    def __init__(self, symbols):
        self.symbol_names = [s[0] for s in symbols]

    def calcular_ganho(self, grid):
        # grid: lista de colunas, cada coluna com 3 nomes visíveis
        # regra simples: linha do meio igual
        middle = [col[1] for col in grid]
        if middle.count(middle[0]) == len(middle):
            return 100
        return 0

# =========================
# Reel (coluna com rolagem real)
# =========================
class Reel:
    def __init__(self, x, symbols):
        self.x = x
        self.symbols = symbols[:]  # lista (name, surface)
        self.queue = []
        self.reset_queue()
        self.offset = 0
        self.speed = 0
        self.spinning = False
        self.stopping = False
        self.target_names = None

    def reset_queue(self):
        # fila grande para simular infinito
        self.queue = [random.choice(self.symbols) for _ in range(12)]

    def start(self):
        self.speed = SPIN_SPEED_START
        self.spinning = True
        self.stopping = False
        self.target_names = None

    def request_stop(self, target_names):
        # target_names: 3 nomes finais (top, mid, bot)
        self.stopping = True
        self.target_names = target_names

    def update(self):
        if not self.spinning:
            return

        self.offset += self.speed

        # passou um símbolo inteiro
        while self.offset >= SYMBOL_SIZE:
            self.offset -= SYMBOL_SIZE
            self.queue.pop(0)
            self.queue.append(random.choice(self.symbols))

        if self.stopping:
            self.speed = max(self.speed - SPIN_DECEL, MIN_SPEED)

            # condição de parada suave
            if self.speed <= MIN_SPEED + 0.01:
                # alinhar para o alvo
                names = [self.queue[i][0] for i in range(1, 4)]
                if names == self.target_names and self.offset < 2:
                    self.speed = 0
                    self.offset = 0
                    self.spinning = False
                    self.stopping = False

    def draw(self, screen):
        y0 = TOP_MARGIN - self.offset
        for i in range(5):  # desenha extra para rolagem
            name, img = self.queue[i]
            screen.blit(img, (self.x, y0 + i * SYMBOL_SIZE))

    def visible_names(self):
        # retorna 3 visíveis (top, mid, bot)
        return [self.queue[i][0] for i in range(1, 4)]

# =========================
# UI Principal
# =========================
class SlotGameUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Slot Game")
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load(BG_PATH).convert()
        self.bg = pygame.transform.smoothscale(self.bg, (SCREEN_W, SCREEN_H))

        self.symbols = load_symbols()
        self.machine = SlotMachine(self.symbols)

        self.reels = []
        for i in range(COLS):
            x = LEFT_MARGIN + i * (SYMBOL_SIZE + REEL_GAP)
            self.reels.append(Reel(x, self.symbols))

        self.font = pygame.font.SysFont(None, 36)
        self.last_win = 0
        self.spinning = False
        self.stop_index = 0
        self.stop_timer = 0

        sSOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

        self.sounds = {
            "click": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "click.mp3")),
            "spin": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "spin1.wav")),
            "win": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "win1.mp3")),
            "lose": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "lose1.mp3")),
}


    def start_spin(self):
        if self.spinning:
            return
        self.last_win = 0
        self.spinning = True
        self.stop_index = 0
        self.stop_timer = 0
        self.sounds["spin"].play()
        for r in self.reels:
            r.start()

        # define resultado final agora (justo)
        self.final_grid = []
        for _ in range(COLS):
            col = [random.choice(self.symbols)[0] for _ in range(ROWS_VISIBLE)]
            self.final_grid.append(col)

    def update(self):
        if self.spinning:
            self.stop_timer += 1
            if self.stop_index < COLS and self.stop_timer >= STOP_DELAY_FRAMES:
                self.stop_timer = 0
                target = self.final_grid[self.stop_index]
                self.reels[self.stop_index].request_stop(target)
                self.stop_index += 1

            if all(not r.spinning for r in self.reels):
                self.spinning = False
                grid = [r.visible_names() for r in self.reels]
                self.last_win = self.machine.calcular_ganho(grid)
                if self.last_win > 0:
                    self.sounds["win"].play()
                else:
                    self.sounds["lose"].play()

        for r in self.reels:
            r.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for r in self.reels:
            r.draw(self.screen)

        txt = self.font.render(f"Ganho: {self.last_win}", True, (255, 255, 255))
        self.screen.blit(txt, (20, 20))

        btn = self.font.render("SPACE = SPIN", True, (255, 255, 0))
        self.screen.blit(btn, (SCREEN_W - 220, 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.start_spin()

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SlotGameUI().run()
