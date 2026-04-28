FROM python:3.11

WORKDIR /app

# --- dépendances système (IMPORTANT pour ton projet) ---
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# --- dépendances Python ---
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --- copier le code ---
COPY . .

# --- commande par défaut ---
CMD ["python", "src/main.py"]