FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear usuario no-root (seguridad)
RUN useradd -m -r appuser && chown -R appuser /app
USER appuser

# Puerto (Render asigna uno automáticamente)
EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando para Render - usa $PORT que Render proporciona automáticamente
CMD gunicorn marketcampus.wsgi:application --bind 0.0.0.0:$PORT --workers 3