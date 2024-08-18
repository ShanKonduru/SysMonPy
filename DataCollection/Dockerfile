# DataCollector/Dockerfile
FROM python:3.11-alpine

# Install build dependencies
RUN apk add --no-cache gcc python3-dev musl-dev linux-headers

# Set up poetry
RUN pip install poetry
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Run the data collector
CMD ["poetry", "run", "python", "collector.py"]
