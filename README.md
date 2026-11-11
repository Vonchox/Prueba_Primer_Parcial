# Chat en tiempo real con Python

## Descripción del ejercicio

El chat tiene tres participantes, el servidor acepta dos conexiones al mismo tiempo, recibe los mensajes de los clientes y los reparte con el nombre de quien escribió, este también puede enviar mensajes desde su propia consola y cada cliente usa un hilo para recibir mensajes mientras escribe en su terminal.

## Estructura del proyecto

| Archivo | Qué hace |
| --- | --- |
| `servidor.py` | Atiende a cada cliente en un hilo y lee la consola del servidor en otro. |
| `cliente1.py` | Conecta, envía y recibe mensajes como `CLIENTE 1`. |
| `cliente2.py` | Conecta, envía y recibe mensajes como `CLIENTE 2`. |
| `Dockerfile` | Construye la imagen que ejecuta el servidor. |
| `compose.yaml` | Define el servicio `servidor`, publica el puerto y habilita su consola. |

## Requisitos

- Python 3 instalado en tu computadora.
- Docker Desktop abierto con Docker Compose disponible.
- VS Code con la carpeta del repositorio abierta.

Los comandos se ejecutan desde la raíz del repositorio, donde está `compose.yaml`.

## Ejecución

Solo el servidor corre en Docker y los clientes se ejecutan con Python en dos terminales independientes de VS Code.

### Terminal 1 · Servidor

Ejecuta los comandos uno por uno. Con `docker compose ps` puedes comprobar que el servicio `servidor` aparece con estado `Up`.

```sh
docker compose up --build -d
docker compose ps
docker compose attach servidor
```

Deja abierta esa terminal. El servidor escucha en el puerto `5000` dentro del contenedor. Docker lo publica en `127.0.0.1:5050`, que es la dirección que usan los clientes.

### Terminal 2 · Cliente 1

En una segunda terminal de VS Code, inicia Cliente 1.

```sh
python cliente1.py
```

### Terminal 3 · Cliente 2

En una tercera terminal, inicia Cliente 2.

```sh
python cliente2.py
```

Si en Windows usas el lanzador de Python, puedes escribir `py cliente1.py` y `py cliente2.py`.

## Prueba de funcionamiento

1. Espera a que cada cliente muestre `Conectado como CLIENTE 1` o `Conectado como CLIENTE 2`.
2. Escribe `Hola a todos` en Cliente 1, `Hola cliente 1` en la consola del servidor y `Buenos días` en Cliente 2 y presiona Enter después de cada mensaje, los dos clientes deben ver las tres líneas con su autor.

   ```text
   [CLIENTE 1]: Hola a todos
   [SERVIDOR]: Hola cliente 1
   [CLIENTE 2]: Buenos días
   ```

3. Para probar que el chat funciona sin turnos, prepara un mensaje distinto en cada cliente y presiona Enter en las dos terminales casi al mismo tiempo, ambos mensajes deben aparecer completos en los dos clientes.

## Cerrar el chat

Escribe `/salir` en cada cliente. Para salir de la consola del servidor, presiona `Ctrl+P` y luego `Ctrl+Q`. Después, detén el servidor con este comando desde cualquier terminal libre del repositorio.

```sh
docker compose down
```
