# Dockerfile

# 1) Use a minimal Python image
FROM python:3.10-slim

# 2) Set working directory
WORKDIR /app

# 3) Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the entire Django project code
COPY . .

# 5) (Optional) Collect static. Disabled now until everything else works:
# RUN python manage.py collectstatic --noinput

# 6) Expose the port your app will listen on
EXPOSE 8000

# 7) Launch Gunicorn via shell so $PORT is expanded at runtime
ENTRYPOINT /bin/sh -c "exec python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:\$PORT"

