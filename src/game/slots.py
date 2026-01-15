import random

class SlotMachine:
    def __init__(self):
        self.simbolos = ["cereja", "limao", "uva", "morango", "7"]

    def girar(self):
        resultado = [
            random.choice(self.simbolos),
            random.choice(self.simbolos),
            random.choice(self.simbolos),
        ]
        ganho = self.calcular_ganho(resultado)
        return resultado, ganho

    def calcular_ganho(self, linha):
        a, b, c = linha

         # JACKPOT
        if a == b == c == "7":
             return 1000

         # TRÊS IGUAIS
        if a == b == c:
            tabela = {
            "morango": 300,
            "uva": 200,
            "limao": 150,
            "cereja": 100,
        }
            return tabela.get(a, 0)

    # DOIS IGUAIS
        if a == b or b == c or a == c:
            return 50

        return 0
