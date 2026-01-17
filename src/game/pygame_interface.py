# pygame_interface.py
import os
import sys
import random
import pygame

from slots import SlotMachine



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
        self.ultimo_ganho = 0
        self.mensagem = ""
        self.saldo = 1000
        self.aposta = 50
        self.mostrar_linha_vencedora = False
        self.blink_timer = 0
        self.blink_interval = 15  # frames (pisca rápido)
        self.mostrar_linha_vencedora = False



    def start_spin(self):
        if self.spinning:
           return

        if self.saldo < self.aposta:
            self.mensagem = "SALDO INSUFICIENTE"
            return

        self.saldo -= self.aposta
        self.spinning = True
        selfmensagem = ""

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
                reels_visiveis = [r.visible() for r in self.reels]

                resultado = {
    "reels": reels_visiveis,
    "linha_central": [col[1] for col in reels_visiveis]
}

                ganho = self.machine.calcular_ganho(resultado["linha_central"])
                self.ultimo_ganho = ganho
                self.saldo += ganho

                if ganho > 0:
                    self.mensagem = f"GANHOU {ganho}!"
                    self.mostrar_linha_vencedora = True
                    self.sounds["win"].play()
                    self.blink_timer = FPS * 2  # pisca por 2 segundos
                else:
                    self.mensagem = "NÃO FOI DESSA VEZ"
                    self.mostrar_linha_vencedora = False
                    self.sounds["lose"].play()

            if self.mostrar_linha_vencedora:
                self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.mostrar_linha_vencedora = False



        for r in self.reels:
            r.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        if self.mostrar_linha_vencedora and (pygame.time.get_ticks() // self.blink_interval) % 2 == 0:
            overlay = pygame.Surface(
                (COLS * SYMBOL_SIZE + (COLS - 1) * REEL_GAP, SYMBOL_SIZE),
                pygame.SRCALPHA
            )
            overlay.fill((255, 0, 0, 140))  # dourado translúcido

            y = TOP_MARGIN + SYMBOL_SIZE * 1  # linha central
            self.screen.blit(overlay, (LEFT_MARGIN, y))


        for r in self.reels:
            r.draw(self.screen)

        if self.mensagem:
            texto = self.font.render(self.mensagem, True, (255, 255, 0))
            rect = texto.get_rect(center=(SCREEN_W // 2, 50))
            self.screen.blit(texto, rect)
        
        saldo_txt = self.font.render(f"SALDO: {self.saldo}", True, (255, 255, 255))
        aposta_txt = self.font.render(f"APOSTA: {self.aposta}", True, (255, 255, 255))

        self.screen.blit(saldo_txt, (20, 20))
        self.screen.blit(aposta_txt, (20, 60))


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
