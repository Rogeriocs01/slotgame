# pygame_interface.py
# Slot machine com rolagem real e parada em 4s / 7s / 10s

import os
import sys
import random
import pygame

# =========================
# PATHS
# =========================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SYMBOLS_DIR = os.path.join(ASSETS_DIR, "symbols")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
BG_PATH = os.path.join(ASSETS_DIR, "bg.png")

# =========================
# CONFIG
# =========================
SCREEN_W, SCREEN_H = 900, 600
FPS = 60

COLS = 3
ROWS_VISIBLE = 3

SYMBOL_SIZE = 120
REEL_GAP = 20

TOP_MARGIN = 150
LEFT_MARGIN = (SCREEN_W - (COLS * SYMBOL_SIZE + (COLS - 1) * REEL_GAP)) // 2

SPIN_SPEED = 40
STOP_TIMES = [4 * FPS, 7 * FPS, 10 * FPS]  # frames

# =========================
# HELPERS
# =========================
def load_symbols():
    symbols = []
    for f in os.listdir(SYMBOLS_DIR):
        if f.lower().endswith(".png"):
            img = pygame.image.load(os.path.join(SYMBOLS_DIR, f)).convert_alpha()
            img = pygame.transform.smoothscale(img, (SYMBOL_SIZE, SYMBOL_SIZE))
            symbols.append((os.path.splitext(f)[0], img))
    if not symbols:
        raise RuntimeError("Nenhum símbolo encontrado em assets/symbols")
    return symbols

# =========================
# SLOT LOGIC
# =========================
class SlotMachine:
    def calcular_ganho(self, grid):
        middle = [col[1] for col in grid]
        if middle.count(middle[0]) == len(middle):
            return 100
        return 0

# =========================
# REEL
# =========================
class Reel:
    def __init__(self, x, symbols):
        self.x = x
        self.symbols = symbols
        self.queue = []
        self.reset_queue()
        self.offset = 0
        self.speed = SPIN_SPEED
        self.spinning = False
        self.frame_count = 0
        self.target = None

    def reset_queue(self):
        self.queue = [random.choice(self.symbols) for _ in range(15)]

    def start(self):
        self.spinning = True
        self.frame_count = 0
        self.offset = 0

    def stop_exact(self, target_names):
        for i in range(3):
            self.queue[i + 1] = next(s for s in self.symbols if s[0] == target_names[i])
        self.offset = 0
        self.spinning = False

    def update(self):
        if not self.spinning:
            return

        self.frame_count += 1
        self.offset += self.speed

        while self.offset >= SYMBOL_SIZE:
            self.offset -= SYMBOL_SIZE
            self.queue.pop(0)
            self.queue.append(random.choice(self.symbols))

    def draw(self, screen):
        clip_rect = pygame.Rect(
            self.x,
            TOP_MARGIN,
            SYMBOL_SIZE,
            SYMBOL_SIZE * ROWS_VISIBLE
        )
        screen.set_clip(clip_rect)

        y0 = TOP_MARGIN - self.offset
        for i in range(4):
            name, img = self.queue[i]
            screen.blit(img, (self.x, y0 + i * SYMBOL_SIZE))

        screen.set_clip(None)

    def visible_names(self):
        return [self.queue[i][0] for i in range(1, 4)]

# =========================
# UI
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
        self.machine = SlotMachine()

        self.reels = []
        for i in range(COLS):
            x = LEFT_MARGIN + i * (SYMBOL_SIZE + REEL_GAP)
            self.reels.append(Reel(x, self.symbols))

        self.font = pygame.font.SysFont(None, 32)
        self.last_win = 0


        self.ultimo_ganho = 0
        self.spinning = False
        self.global_frame = 0

        self.final_grid = []

        self.sounds = {
            "spin": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "spin1.wav")),
            "win": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "win1.wav")),
            "lose": pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "lose1.mp3")),
        }

    def start_spin(self):
        if self.spinning:
            return

        self.spinning = True
        self.global_frame = 0
        self.ultimo_ganho = 0

        self.final_grid = [
            [random.choice(self.symbols)[0] for _ in range(ROWS_VISIBLE)]
            for _ in range(COLS)
        ]

        self.sounds["spin"].play()

        for r in self.reels:
            r.start()

    def update(self):
        if self.spinning:
            self.global_frame += 1

            for i, r in enumerate(self.reels):
                if r.spinning and self.global_frame >= STOP_TIMES[i]:
                    r.stop_exact(self.final_grid[i])

            if all(not r.spinning for r in self.reels):
                self.spinning = False
                grid = [r.visible_names() for r in self.reels]
                self.ultimo_ganho = self.machine.calcular_ganho(grid)

                if self.ultimo_ganho > 0:
                    self.sounds["win"].play()
                else:
                    self.sounds["lose"].play()

        for r in self.reels:
            r.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for r in self.reels:
            r.draw(self.screen)

        # =========================
# LINHA VENCEDORA (linha do meio)
# =========================
        if self.last_win > 0:
            overlay = pygame.Surface(
        (COLS * SYMBOL_SIZE + (COLS - 1) * REEL_GAP, SYMBOL_SIZE),
        pygame.SRCALPHA
    )

    # cor dourada translúcida
        overlay.fill((255, 215, 0, 90))

    # posição da linha do meio
        line_x = LEFT_MARGIN
        line_y = TOP_MARGIN + SYMBOL_SIZE  # linha do meio

        self.screen.blit(overlay, (line_x, line_y))


        texto = self.font.render(f"Ganho: {self.ultimo_ganho}", True, (255, 255, 255))
        self.screen.blit(texto, (20, 20))

        instrucao = self.font.render("SPACE = GIRAR", True, (255, 255, 0))
        self.screen.blit(instrucao, (SCREEN_W - 220, 20))

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

# =========================
# START
# =========================
if __name__ == "__main__":
    SlotGameUI().run()
