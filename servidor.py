import socket
import threading


class Servidor:
    NOMBRES = ("CLIENTE 1", "CLIENTE 2")

    def __init__(self, host="0.0.0.0", puerto=5000):
        # Guardamos las conexiones por nombre. El bloqueo coordina a los hilos
        # cuando registran clientes, los quitan o les mandan mensajes.
        self.direccion = (host, puerto)
        self.clientes = {}
        self.bloqueo = threading.Lock()

    def iniciar(self):
        # Abrimos el puerto TCP dentro del contenedor. Por cada conexión que
        # aceptamos, arrancamos un hilo y seguimos esperando al siguiente cliente.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as escucha:
            escucha.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            escucha.bind(self.direccion)
            escucha.listen()
            print(f"Servidor escuchando en el puerto {escucha.getsockname()[1]}.")
            print("Escribe un mensaje y presiona Enter para enviarlo a los clientes.")

            # La consola tiene su propio hilo para poder escribir mientras llegan conexiones.
            threading.Thread(target=self.leer_consola, daemon=True).start()
            while True:
                conexion, _ = escucha.accept()
                threading.Thread(target=self.atender, args=(conexion,), daemon=True).start()

    def atender(self, conexion):
        # Este método se ejecuta en el hilo de un cliente durante toda su conexión.
        nombre = None
        registrado = False
        try:
            # El cliente manda su nombre primero. Después, cada línea es un mensaje del chat.
            with conexion, conexion.makefile("r", encoding="utf-8") as entrada:
                nombre = entrada.readline().rstrip("\n")
                with self.bloqueo:
                    # Confirmamos que el nombre sea válido y que nadie lo esté usando.
                    if nombre not in self.NOMBRES or nombre in self.clientes:
                        conexion.sendall("Ese nombre no está disponible.\n".encode("utf-8"))
                        return
                    conexion.sendall(b"OK\n")
                    self.clientes[nombre] = conexion
                    registrado = True
                    print(f"{nombre} se conectó.")

                for linea in entrada:
                    mensaje = linea.strip()
                    if mensaje:
                        self.difundir(nombre, mensaje)
        except (OSError, UnicodeError):
            pass
        finally:
            # Al salir, liberamos el nombre para que ese cliente se pueda conectar de nuevo.
            if registrado:
                with self.bloqueo:
                    del self.clientes[nombre]
                    print(f"{nombre} se desconectó.")

    def leer_consola(self):
        # Lo que escribimos en la consola del contenedor también entra al chat.
        while True:
            try:
                mensaje = input().strip()
            except EOFError:
                return
            if mensaje:
                self.difundir("SERVIDOR", mensaje)

    def difundir(self, autor, mensaje):
        # Le ponemos el nombre del autor y enviamos la misma línea a todos.
        # Cada cliente recibe también una copia de sus propios mensajes.
        linea = f"[{autor}]: {mensaje}"
        datos = (linea + "\n").encode("utf-8")

        # Si llegan dos mensajes al mismo tiempo, los repartimos de a uno.
        # Así los dos clientes reciben líneas completas y en el mismo orden.
        with self.bloqueo:
            print(linea)
            for conexion in self.clientes.values():
                try:
                    conexion.sendall(datos)
                except OSError:
                    # El hilo de esa conexión se encarga de sacarla del chat.
                    pass


# Arrancamos el servidor al ejecutar este archivo.
if __name__ == "__main__":
    try:
        Servidor().iniciar()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
