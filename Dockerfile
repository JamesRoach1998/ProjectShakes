# Dockerfile

FROM python:3.10-slim

# 1) install espeak for phoneme extraction
RUN apt-get update && apt-get install -y espeak && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:8000
