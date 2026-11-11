import socket  # Abre la conexión TCP y envía los mensajes
import threading  # Permite recibir mensajes mientras usamos el teclado
from contextlib import suppress  # Ignora errores concretos al cerrar la conexión


class Cliente2:
    def __init__(self, host="127.0.0.1", puerto=5050):
        # Guardamos el nombre que verá el chat y la dirección que Docker publica en el equipo
        self.nombre = "CLIENTE 2"
        self.direccion = (host, puerto)

    def iniciar(self):
        # Al conectarnos, mandamos nuestro nombre y esperamos que el servidor lo acepte
        try:
            with socket.create_connection(self.direccion) as conexion:
                # makefile nos deja leer el socket como texto, una línea a la vez.
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
        # Mientras un hilo lee el teclado, el otro recibe mensajes
        # Event es la señal que ambos consultan para saber si toca salir
        cerrar = threading.Event()

        receptor = threading.Thread(target=self.recibir, args=(entrada, cerrar))
        receptor.start()
        try:
            while not cerrar.is_set():
                mensaje = input().strip()
                if cerrar.is_set() or mensaje == "/salir":
                    break
                if mensaje:
                    # Enviamos bytes para marcar el final del mensaje
                    conexion.sendall((mensaje + "\n").encode("utf-8"))
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            cerrar.set()
            # Cerramos el envío y la recepción para desbloquear la lectura del receptor
            # Si el socket ya se desconectó, podemos seguir aunque shutdown dé error
            with suppress(OSError):
                conexion.shutdown(socket.SHUT_RDWR)
            # join espera a que el receptor termine antes de salir
            receptor.join()

    def recibir(self, entrada, cerrar):
        # Mostramos los mensajes con el nombre que puso el servidor, si la conexión
        # se corta, avisamos al otro hilo para que termine cuando se pulse Enter
        try:
            for linea in entrada:
                print(linea.rstrip("\n"))
        except OSError:
            pass
        finally:
            if not cerrar.is_set():
                cerrar.set()
                print("\nSe cerró la conexión con el servidor, presiona Enter para salir.")


# Iniciamos este cliente cuando ejecutamos su archivo desde la terminal
if __name__ == "__main__":
    Cliente2().iniciar()
