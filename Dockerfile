FROM python:3.13-slim

WORKDIR /app
COPY servidor.py .

CMD ["python", "-u", "servidor.py"]
