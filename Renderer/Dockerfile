# Renderer/Dockerfile
FROM python:3.11-alpine

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Run the renderer
CMD ["poetry", "run", "python", "renderer.py"]
