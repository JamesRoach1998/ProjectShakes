# Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# (static collection disabled for now)
# RUN python manage.py collectstatic --noinput

# … everything up to EXPOSE 8000 stays the same …

EXPOSE 8000

# Bind to 8000 inside the container—Railway will route external traffic here.
CMD python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:8000
