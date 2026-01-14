# pygame_interface.py
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

SPIN_SPEED = 40
STOP_TIMES = [4 * FPS, 7 * FPS, 10 * FPS]

# =========================
# Helpers
# =========================
def load_symbols():
    symbols = []
    for f in os.listdir(SYMBOLS_DIR):
        if f.lower().endswith(".png"):
            img = pygame.image.load(os.path.join(SYMBOLS_DIR, f)).convert_alpha()
            img = pygame.transform.smoothscale(img, (SYMBOL_SIZE, SYMBOL_SIZE))
            symbols.append((os.path.splitext(f)[0], img))
    return symbols

# =========================
# Slot logic
# =========================
class SlotMachine:
    def calcular_ganho(self, grid):
        middle = [c[1] for c in grid]
        return 100 if middle.count(middle[0]) == 3 else 0

# =========================
# Reel
# =========================
class Reel:
    def __init__(self, x, symbols):
        self.x = x
        self.symbols = symbols
        self.queue = [random.choice(symbols) for _ in range(15)]
        self.offset = 0
        self.spinning = False
        self.frame = 0

    def start(self):
        self.spinning = True
        self.frame = 0

    def stop_exact(self, target):
        for i in range(3):
            self.queue[i + 1] = next(s for s in self.symbols if s[0] == target[i])
        self.offset = 0
        self.spinning = False

    def update(self):
        if not self.spinning:
            return
        self.frame += 1
        self.offset += SPIN_SPEED
        while self.offset >= SYMBOL_SIZE:
            self.offset -= SYMBOL_SIZE
            self.queue.pop(0)
            self.queue.append(random.choice(self.symbols))

    def draw(self, screen):
        y = TOP_MARGIN - self.offset
        for i in range(5):
            screen.blit(self.queue[i][1], (self.x, y + i * SYMBOL_SIZE))

    def visible(self):
        return [self.queue[i][0] for i in range(1, 4)]

# =========================
# UI
# =========================
class SlotGameUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()

        self.bg = pygame.transform.scale(
            pygame.image.load(BG_PATH), (SCREEN_W, SCREEN_H)
        )

        self.symbols = load_symbols()
        self.machine = SlotMachine()

        self.reels = [
            Reel(LEFT_MARGIN + i * (SYMBOL_SIZE + REEL_GAP), self.symbols)
            for i in range(COLS)
        ]

        self.sounds = {
            "spin": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "spin1.wav")),
            "win": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "win1.mp3")),
            "lose": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "lose1.mp3")),
        }

        self.font = pygame.font.SysFont(None, 36)
        self.spinning = False
        self.final_grid = []

    def start_spin(self):
        if self.spinning:
            return
        self.spinning = True
        self.final_grid = [
            [random.choice(self.symbols)[0] for _ in range(ROWS_VISIBLE)]
            for _ in range(COLS)
        ]
        self.sounds["spin"].play()
        for r in self.reels:
            r.start()

    def update(self):
        if self.spinning:
            for i, r in enumerate(self.reels):
                if r.spinning and r.frame >= STOP_TIMES[i]:
                    r.stop_exact(self.final_grid[i])

            if all(not r.spinning for r in self.reels):
                self.spinning = False
                grid = [r.visible() for r in self.reels]
                if self.machine.calcular_ganho(grid):
                    self.sounds["win"].play()
                else:
                    self.sounds["lose"].play()

        for r in self.reels:
            r.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for r in self.reels:
            r.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.start_spin()
            self.update()
            self.draw()

if __name__ == "__main__":
    SlotGameUI().run()
