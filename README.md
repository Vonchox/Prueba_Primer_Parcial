# Chat en tiempo real con Python

El chat tiene tres participantes: `SERVIDOR`, `CLIENTE 1` y `CLIENTE 2`. Se comunican por TCP y cada participante puede escribir mientras recibe mensajes, en este caso docker solo ejecuta el servidor y los clientes se ejecutan con Python desde dos terminales de VS Code.

## Requisitos

- Python 3 instalado en tu computadora.
- Docker Desktop abierto con Docker Compose disponible.
- VS Code con la carpeta del repositorio abierta.

Los comandos se ejecutan desde la raíz del repositorio, donde está `compose.yaml`.

## 1. Levantar el servidor

En la primera terminal, construye y arranca el servidor, luego abre su consola para poder escribir en el chat.

```sh
docker compose up --build -d
docker compose attach servidor
```

Deja abierta esa terminal. El servidor escucha en el puerto `5000` dentro del contenedor. Docker lo publica en `127.0.0.1:5050`, que es la dirección que usan los clientes.

## 2. Conectar los dos clientes

En una segunda terminal de VS Code, inicia Cliente 1.

```sh
python cliente1.py
```

En una tercera terminal, inicia Cliente 2.

```sh
python cliente2.py
```

Si en Windows usas el lanzador de Python, puedes escribir `py cliente1.py` y `py cliente2.py`.


## Cerrar el chat

Escribe `/salir` en cada cliente. Para salir de la consola del servidor, presiona `Ctrl+P` y luego `Ctrl+Q`. Después, detén el servidor con este comando desde cualquier terminal libre del repositorio.

```sh
docker compose down
```

## Cómo se reparte el trabajo

- `servidor.py` contiene la clase `Servidor`, en este abre un hilo para atender a cada cliente y otro para leer la consola, los mensajes se reparten a todos los clientes conectados, incluido quien escribió.
- `cliente.py` contiene la clase `Cliente` con la conexión, el envío y un hilo para mostrar los mensajes entrantes.
- `cliente1.py` y `cliente2.py` tienen una clase y un punto de inicio por participante. Cada clase le pasa su nombre al cliente común.
