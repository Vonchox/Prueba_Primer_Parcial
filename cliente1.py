from cliente import Cliente


class Cliente1(Cliente):
    def __init__(self):
        super().__init__("CLIENTE 1")


if __name__ == "__main__":
    Cliente1().iniciar()
