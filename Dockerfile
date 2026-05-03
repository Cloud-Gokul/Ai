FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY detect.py .
COPY mask_model.h5 .
COPY templates ./templates

EXPOSE 5000

CMD ["python", "app.py"]
