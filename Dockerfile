FROM python:3.11-slim

# Installa Node.js e dipendenze di sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    xvfb \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    libxkbcommon0 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Installa cloakbrowser via npm (il binario stealth)
RUN npm install -g cloakbrowser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY cookie_refresh.py .

# Assicuriamoci che il binario di cloakbrowser sia nel PATH
ENV PATH="/usr/local/bin:${PATH}"

CMD ["python", "cookie_refresh.py"]
