# Dockerfile

FROM python:3.10-slim

# Install espeak for phoneme generation
RUN apt-get update && apt-get install -y espeak && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django project
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Start Gunicorn
CMD python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:8000
