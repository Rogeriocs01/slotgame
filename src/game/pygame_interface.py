# src/game/pygame_interface.py

import pygame
import sys

from assets_config import BACKGROUND, SYMBOLS, MASCOT

# =========================
# CONFIGURAÇÕES BÁSICAS
# =========================

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

SYMBOL_SIZE = 120
SYMBOL_Y = 260
SYMBOL_X_POSITIONS = [360, 500, 640]

# =========================
# CLASSE PRINCIPAL DA TELA
# =========================

class SlotGameUI:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Slot Game Recreativo")

        self.clock = pygame.time.Clock()

        # Carregar imagens
        self.background = pygame.image.load(BACKGROUND).convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.mascote_idle = pygame.image.load(
            MASCOT["idle"]
        ).convert_alpha()

        self.symbol_images = {}
        for name, path in SYMBOLS.items():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(
                img, (SYMBOL_SIZE, SYMBOL_SIZE)
            )
            self.symbol_images[name] = img

        # Símbolos iniciais (fixos)
        self.current_symbols = ["cereja", "limao", "uva"]

    # =========================
    # LOOP PRINCIPAL
    # =========================

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # =========================
    # DESENHO DA TELA
    # =========================

    def draw(self):
        # Fundo
        self.screen.blit(self.background, (0, 0))

        # Símbolos
        for i, symbol in enumerate(self.current_symbols):
            img = self.symbol_images[symbol]
            x = SYMBOL_X_POSITIONS[i]
            self.screen.blit(img, (x, SYMBOL_Y))

        # Mascote (canto inferior esquerdo)
        self.screen.blit(self.mascote_idle, (40, 350))


# =========================
# EXECUÇÃO DIRETA
# =========================

if __name__ == "__main__":
    game = SlotGameUI()
    game.run()
