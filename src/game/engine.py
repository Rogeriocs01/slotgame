from .slots import SlotMachine

class Jogo:
    def __init__(self):
        self.saldo = 9999
        self.aposta = 50
        self.maquina = SlotMachine()

    def iniciar(self):
        print("=== JOGO RECREATIVO ===")
        print("Moeda virtual • Sem dinheiro real\n")

        while True:
            print(f"Saldo atual: {self.saldo}")
            print(f"Aposta por rodada: {self.aposta}")
            cmd = input("ENTER = girar | Q = sair\n").lower()

            if cmd == "q":
                print("Obrigado por jogar!")
                break

            if self.saldo < self.aposta:
                print("Sem saldo para jogar. Fim de jogo.")
                break

            self.saldo -= self.aposta

            resultado, ganho = self.maquina.girar()

            print("Resultado:", resultado)

            if ganho > 0:
                print("Você ganhou:", ganho)
                self.saldo += ganho
            else:
                print("Não foi dessa vez 😅")

            print("="*30)
