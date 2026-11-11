import socket
import threading
from contextlib import suppress


class Cliente1:
    def __init__(self, host="127.0.0.1", puerto=5050):
        # Guardamos el nombre que verá el chat y la dirección que Docker publica en el equipo.
        self.nombre = "CLIENTE 1"
        self.direccion = (host, puerto)

    def iniciar(self):
        # Al conectarnos, mandamos nuestro nombre y esperamos que el servidor lo acepte.
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
        # El hilo principal lee el teclado y envía lo que escribimos, y el receptor
        # muestra lo que llega mientras escribimos y los dos comparten una señal de cierre.
        cerrar = threading.Event()

        receptor = threading.Thread(target=self.recibir, args=(entrada, cerrar))
        receptor.start()
        try:
            while not cerrar.is_set():
                mensaje = input().strip()
                if cerrar.is_set() or mensaje == "/salir":
                    break
                if mensaje:
                    # El salto de línea le indica al servidor dónde termina el mensaje.
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
        # Mostramos los mensajes con el nombre que puso el servidor, si la conexión
        # se corta, avisamos al otro hilo para que termine cuando se pulse Enter.
        try:
            for linea in entrada:
                print(linea.rstrip("\n"))
        except OSError:
            pass
        finally:
            if not cerrar.is_set():
                cerrar.set()
                print("\nSe cerró la conexión con el servidor, presiona Enter para salir.")


# Iniciamos este cliente cuando ejecutamos su archivo desde la terminal.
if __name__ == "__main__":
    Cliente1().iniciar()
