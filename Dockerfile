FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Создаем директории для загрузок и логов
RUN mkdir -p /app/uploads /app/logs

# Создаем непривилегированного пользователя
RUN adduser --disabled-password --gecos "" --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Запускаем приложение (Исправлено: src.app.main вместо scr.app.main)
CMD ["sh", "-c", "alembic upgrade head && uvicorn scr.app.main:app --host 0.0.0.0 --port 8000"]

