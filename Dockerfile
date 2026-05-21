FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# app/main.py calls load_dotenv(), so a .env file in /app or environment
# variables configured by Render are available when Uvicorn imports the app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]   