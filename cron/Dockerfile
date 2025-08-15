FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 5004
CMD ["gunicorn", "--bind", "0.0.0.0:5004", "app:app", "--workers", "1"]