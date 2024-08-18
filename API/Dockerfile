# API/Dockerfile
FROM python:3.11-alpine

# Install build dependencies
RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

# Set up poetry
RUN pip install poetry
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

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000
EXPOSE 5000

# Start the Flask app
CMD ["poetry", "run", "flask", "run"]
    