FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install "poetry==$POETRY_VERSION" && \
    rm -rf /root/.cache/pip

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка только продакшен-зависимостей
RUN poetry install --no-dev --no-interaction --no-ansi && \
    rm -rf /root/.cache/pypoetry

# Копирование приложения
COPY . .

# Создание не-root пользователя
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

# Проверка работоспособности
RUN poetry run python -c "from app.core.config import settings; print('✅ Config loaded:', settings.postgres_host)"

EXPOSE 8000

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]