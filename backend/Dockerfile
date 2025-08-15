FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV HOST=0.0.0.0

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "4"]