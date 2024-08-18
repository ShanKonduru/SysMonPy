@echo off
poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi
docker-compose up --build
