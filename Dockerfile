# Dockerfile (full)

FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional static-collect, disabled until later:
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Shell form CMD so $PORT is expanded at runtime
CMD /bin/sh -c "exec python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:$PORT"
