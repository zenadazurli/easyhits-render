FROM python:3.11-slim

# 1. Imposta la directory di lavoro
WORKDIR /app

# 2. Installa Chrome e le dipendenze (chiave GPG aggiornata)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. Installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia lo script
COPY cookie_refresh.py .

# 5. Comando di avvio
CMD ["python", "cookie_refresh.py"]
