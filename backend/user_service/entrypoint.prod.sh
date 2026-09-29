#!/usr/bin/env bash

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput
uv run gunicorn base.wsgi:application --bind 0.0.0.0:8000 --workers 3