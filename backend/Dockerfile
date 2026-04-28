# ── Backend — Flask API ───────────────────────────────────────────────────────
# Build multi-stage: dipendenze separate dal codice per layer caching ottimale.

# Stage 1: installa le dipendenze
FROM python:3.12-slim AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: immagine finale
FROM python:3.12-slim AS final
WORKDIR /app

# Copia le dipendenze già installate dallo stage precedente
COPY --from=deps /usr/local/lib/python3.12/site-packages \
                 /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copia il codice sorgente
COPY . .

# Variabili d'ambiente Flask
ENV FLASK_APP=todo.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Usa flask run invece di python run.py: più controllabile in container
CMD ["flask", "run"]
