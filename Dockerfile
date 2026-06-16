# Python и Poetry идеально сочетаются.
FROM python:3.13 as builder
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
# RUN python -m pip install --upgrade pip && \
#     pip install poetry
# COPY pyproject.toml poetry.lock README.md ./
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
# RUN poetry install --no-root # Установка без зависимостей для разработки


COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] # Укажите основной скрипт вашего приложения

