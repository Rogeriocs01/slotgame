import random

class SlotMachine:
    def __init__(self):
        # Nomes dos símbolos devem bater com assets_config.py
        self.simbolos = [
            "cereja",
            "limao",
            "uva",
            "morango",
            "7"
        ]

    def girar(self):
        resultado = [
            random.choice(self.simbolos),
            random.choice(self.simbolos),
            random.choice(self.simbolos)
        ]
        ganho = self.calcular_ganho(resultado)
        return resultado, ganho

    def calcular_ganho(self, resultado):
        a, b, c = resultado

        # Três iguais
        if a == b == c:
            return 200

        # Dois iguais
        if a == b or b == c or a == c:
            return 100

        return 0
