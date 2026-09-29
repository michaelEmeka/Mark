FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev
RUN chown -R appuser:appuser /app/.venv

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

RUN chmod +x /app/entrypoint.prod.sh