#!/bin/bash

echo "Applying migrations"
poetry run python manage.py makemigrations
poetry run python manage.py makemigrations django_app
poetry run python manage.py migrate
poetry run python manage.py initadmin
  poetry run python manage.py collectstatic --noinput


echo "Running server..."

poetry run uvicorn core.asgi:fastapi_app --reload --host 0.0.0.0 --port 8000 &
poetry run uvicorn core.asgi:django_app --reload --host 0.0.0.0 --port 8001
