import pygame
import random
import sys
import os
from slots import SlotMachine


# =========================
# CAMINHOS
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SYMBOLS_DIR = os.path.join(ASSETS_DIR, "simbolos")

# =========================
# CONFIGURAÇÕES VISUAIS
# =========================

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

BACKGROUND_COLOR = (20, 20, 20)
PANEL_COLOR = (55, 55, 55)
SLOT_BG_COLOR = (235, 235, 235)

BUTTON_COLOR = (200, 50, 50)
BUTTON_HOVER = (220, 70, 70)
TEXT_COLOR = (255, 255, 255)

PANEL_WIDTH = 460
PANEL_HEIGHT = 260

SLOT_SIZE = 96
SLOT_GAP = 20

# =========================
# CLASSE PRINCIPAL
# =========================

class SlotGameUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Slot Game Recreativo")

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 28, bold=True)

        # Painel central
        self.panel = pygame.Rect(
            (SCREEN_WIDTH - PANEL_WIDTH) // 2,
            (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 - 40,
            PANEL_WIDTH,
            PANEL_HEIGHT
        )

        # Botão SPIN
        self.button = pygame.Rect(
            SCREEN_WIDTH // 2 - 90,
            self.panel.bottom + 25,
            180,
            55
        )

        # =========================
        # CARREGAR SÍMBOLOS
        # =========================

        self.symbol_images = {
            "cereja": self.load_symbol("cereja.png"),
            "limao": self.load_symbol("limao.png"),
            "uva": self.load_symbol("uva.png"),
            "morango": self.load_symbol("morango.png"),
            "7": self.load_symbol("7.png"),
        }

        self.symbol_keys = list(self.symbol_images.keys())

        # Símbolos iniciais
        self.current = [
            random.choice(self.symbol_keys),
            random.choice(self.symbol_keys),
            random.choice(self.symbol_keys),
        ]

        self.spinning = False
        self.spin_timer = 0

    # =========================
    # FUNÇÕES AUXILIARES
    # =========================

    def load_symbol(self, filename):
        path = os.path.join(SYMBOLS_DIR, filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(
            image, (SLOT_SIZE, SLOT_SIZE)
        )

    # =========================
    # SPIN
    # =========================

    def spin(self):
        self.spinning = True
        self.spin_timer = 20

    # =========================
    # UPDATE
    # =========================

    def update(self):
        if self.spinning:
            self.spin_timer -= 1

            self.current = [
                random.choice(self.symbol_keys),
                random.choice(self.symbol_keys),
                random.choice(self.symbol_keys),
            ]

            if self.spin_timer <= 0:
                self.spinning = False
                self.last_win = self.machine.calculate_win(self.current)

    # =========================
    # DRAW
    # =========================

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # Painel
        pygame.draw.rect(
            self.screen,
            PANEL_COLOR,
            self.panel,
            border_radius=22
        )

        # Slots centralizados
        total_width = (SLOT_SIZE * 3) + (SLOT_GAP * 2)
        start_x = self.panel.centerx - total_width // 2
        slot_y = self.panel.centery - SLOT_SIZE // 2

        for i, key in enumerate(self.current):
            x = start_x + i * (SLOT_SIZE + SLOT_GAP)

            pygame.draw.rect(
                self.screen,
                SLOT_BG_COLOR,
                (x - 6, slot_y - 6, SLOT_SIZE + 12, SLOT_SIZE + 12),
                border_radius=14
            )

            self.screen.blit(
                self.symbol_images[key],
                (x, slot_y)
            )

        # Botão SPIN
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(
            self.screen,
            color,
            self.button,
            border_radius=16
        )

        text = self.font.render("SPIN", True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.button.center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        if not self.spinning:
             if self.last_win > 0:
                msg = f"VOCÊ GANHOU: {self.last_win}"
                color = (50, 220, 50)
        else:
                msg = "TENTE NOVAMENTE"
                color = (220, 60, 60)

        text = self.font.render(msg, True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, self.panel.top - 20))
        self.screen.blit(text, rect)


    # =========================
    # LOOP PRINCIPAL
    # =========================

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos) and not self.spinning:
                        self.spin()

            self.update()
            self.draw()


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    game = SlotGameUI()
    game.run()
