import socket
import threading
from contextlib import suppress


class Cliente2:
    def __init__(self, host="127.0.0.1", puerto=5050):
        self.nombre = "CLIENTE 2"
        self.direccion = (host, puerto)

    def iniciar(self):
        try:
            with socket.create_connection(self.direccion) as conexion:
                with conexion.makefile("r", encoding="utf-8") as entrada:
                    conexion.sendall((self.nombre + "\n").encode("utf-8"))
                    respuesta = entrada.readline().rstrip("\n")
                    if respuesta != "OK":
                        print(respuesta or "El servidor cerró la conexión.")
                        return

                    print(f"Conectado como {self.nombre}. Escribe /salir para cerrar el chat.")
                    self.conversar(conexion, entrada)
        except OSError as error:
            print(f"No se pudo comunicar con el servidor: {error}")

    def conversar(self, conexion, entrada):
        cerrar = threading.Event()

        # Mientras la terminal espera lo que escribimos, este hilo sigue mostrando el chat.
        receptor = threading.Thread(target=self.recibir, args=(entrada, cerrar))
        receptor.start()
        try:
            while not cerrar.is_set():
                mensaje = input().strip()
                if cerrar.is_set() or mensaje == "/salir":
                    break
                if mensaje:
                    conexion.sendall((mensaje + "\n").encode("utf-8"))
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            cerrar.set()
            # Despertamos al receptor si todavía está esperando una línea del servidor.
            with suppress(OSError):
                conexion.shutdown(socket.SHUT_RDWR)
            receptor.join()

    def recibir(self, entrada, cerrar):
        try:
            for linea in entrada:
                print(linea.rstrip("\n"))
        except OSError:
            pass
        finally:
            if not cerrar.is_set():
                cerrar.set()
                print("\nSe cerró la conexión con el servidor. Presiona Enter para salir.")


if __name__ == "__main__":
    Cliente2().iniciar()
