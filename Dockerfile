# Dockerfile

# 1) Use a minimal Python image
FROM python:3.10-slim

# 2) Set the working directory inside the container
WORKDIR /app

# 3) Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the entire Django project code
COPY . .

# (Optional) 5) Collect your static files into STATIC_ROOT
#    If you have static assets and Whitenoise enabled, re-enable this:
# RUN python manage.py collectstatic --noinput

# 6) Expose the port that your app will listen on
EXPOSE 8000

# 7) Launch Gunicorn via a shell command so Railway’s $PORT can expand
ENTRYPOINT /bin/sh -c "exec python -m gunicorn shakes.wsgi:application --bind 0.0.0.0:\$PORT"
