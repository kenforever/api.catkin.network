# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONUNBUFFERED=1

# Copy the pyproject.toml files to the container
COPY pyproject.toml /app/

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy the rest of the application code to the container
COPY . /app

RUN poetry install 

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using poetry run
CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
