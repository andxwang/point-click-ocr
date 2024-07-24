FROM python:3.12-slim

WORKDIR /ocr_app

# TODO: requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "main.py"]
