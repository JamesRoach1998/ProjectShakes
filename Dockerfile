# 1) Use a slim Python image
FROM python:3.10-slim

# 2) Set working directory
WORKDIR /app

# 3) Copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of your app code
COPY . .

# 5) Collect static files
RUN python manage.py collectstatic --noinput

# 6) Expose port 8000 (Railway maps $PORT → 8000)
EXPOSE 8000

# 7) Start the app with Gunicorn
CMD ["gunicorn","shakes.wsgi","--bind","0.0.0.0:8000"]
