FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=appuser:appuser . .

RUN uv sync --frozen --no-dev
RUN uv run python manage.py collectstatic --noinput
RUN chown -R appuser:appuser /app/.venv
RUN chown -R appuser:appuser /app/staticfiles

USER appuser

EXPOSE 8000