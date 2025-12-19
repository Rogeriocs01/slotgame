import pygame
import os
from game.engine import Jogo

pygame.init()
pygame.mixer.init()

LARGURA = 900
ALTURA = 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tigrinho Recreativo")

jogo = Jogo()
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arialblack", 30)
fonte_menor = pygame.font.SysFont("arial", 20)

CAMINHO = os.path.join("..", "..", "assets")
SIMBOLOS = os.path.join(CAMINHO, "simbolos")

bg = pygame.image.load(os.path.join(CAMINHO, "bg.png"))
bg = pygame.transform.scale(bg, (LARGURA, ALTURA))

imagens = {}
for s in ["A","B","C","D","7"]:
    img = pygame.image.load(os.path.join(SIMBOLOS, f"{s}.png"))
    imagens[s] = pygame.transform.scale(img, (120, 120))

slots = ["A", "B", "C"]

btn_rect = pygame.Rect(350, 400, 200, 60)

rodando = True
while rodando:
    tela.blit(bg, (0,0))

    titulo = fonte.render("TIGRINHO RECREATIVO", True, (0,255,0))
    tela.blit(titulo, (230, 10))

    saldo_txt = fonte_menor.render(f"Saldo: {jogo.saldo}", True, (255,255,255))
    tela.blit(saldo_txt, (20, 70))

    for i, simb in enumerate(slots):
        tela.blit(imagens[simb], (240 + i*150, 180))

    pygame.draw.rect(tela, (0,200,0), btn_rect, border_radius=10)
    girar_txt = fonte.render("GIRAR", True, (255,255,255))
    tela.blit(girar_txt, (btn_rect.x+40, btn_rect.y+10))

    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(evento.pos):
                if jogo.saldo >= jogo.aposta:
                    jogo.saldo -= jogo.aposta
                    resultado, ganho = jogo.maquina.girar()
                    slots = resultado
                    jogo.saldo += ganho

    clock.tick(60)

pygame.quit()
