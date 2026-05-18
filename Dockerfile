# Usiamo un'immagine base Python, sufficientemente leggera
FROM python:3.11-slim

# 1. Aggiorniamo il sistema e installiamo le dipendenze necessarie per CloakBrowser
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Impostiamo la directory di lavoro
WORKDIR /app

# 3. Copiamo e installiamo le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamo lo script Python
COPY cookie_refresh.py .

# 5. Comando per avviare lo script (Render lo eseguirà)
CMD ["python", "cookie_refresh.py"]
