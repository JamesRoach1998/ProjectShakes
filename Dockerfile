FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python manage.py collectstatic --noinput   <-- comment this out for now

EXPOSE 8000
CMD ["python", "-m", "gunicorn", "shakes.wsgi:application", "--bind", "0.0.0.0:8000"]

