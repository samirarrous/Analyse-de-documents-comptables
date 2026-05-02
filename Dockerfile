FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# default command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]