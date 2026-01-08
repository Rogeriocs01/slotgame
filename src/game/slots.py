class SlotMachine:
    def __init__(self):
        self.paytable = {
            "cereja": 2,
            "limao": 2,
            "uva": 3,
            "morango": 4,
            "7": 10,
        }

    def calculate_win(self, symbols):
        a, b, c = symbols

        # Três iguais
        if a == b == c:
            multiplier = self.paytable.get(a, 0)
            return multiplier * 10

        # Dois iguais
        if a == b or b == c or a == c:
            return 5

        return 0
