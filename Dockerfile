# Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# (static collection disabled for now)
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Shell‐form CMD: this runs via /bin/sh -c, so $PORT will expand
CMD python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:$PORT
