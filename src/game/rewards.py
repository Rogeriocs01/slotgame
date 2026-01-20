# rewards.py
import random

class SlotMachine:
    def __init__(self, win_chance=0.25, force_win=False):
        """
        win_chance: chance de ganhar (0.25 = 25%)
        force_win: modo debug (sempre ganha)
        """
        self.win_chance = win_chance
        self.force_win = force_win

    def spin_is_winner(self):
        if self.force_win:
            return True
        return random.random() < self.win_chance

    def calcular_ganho(self, linha):
        """
        Recebe a linha central do slot
        Retorna o valor do ganho
        """

        # PRIORIDADE MÁXIMA
        if linha == ["7", "7", "7"]:
            return 500

        # TRÊS IGUAIS
        if linha[0] == linha[1] == linha[2]:
            simbolo = linha[0]
            tabela = {
                "cereja": 100,
                "uva": 80,
                "morango": 60,
                "limao": 40,
            }
            return tabela.get(simbolo, 30)

        # DOIS CEREJAS
        if linha.count("cereja") == 2:
            return 20

        return 0
