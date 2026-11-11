from cliente import Cliente


class Cliente2(Cliente):
    def __init__(self):
        super().__init__("CLIENTE 2")


if __name__ == "__main__":
    Cliente2().iniciar()
