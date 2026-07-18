# syntax=docker/dockerfile:1

# Use the official Python image matching the local Python version.
FROM python:3.14.6-slim-trixie

# Improve Python behavior inside the container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# All following commands will run from /app inside the container.
WORKDIR /app

# Copy requirements first so Docker can cache the dependency layer.
COPY requirements.txt ./requirements.txt

# Install the Python dependencies.
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy the backend, frontend templates, static files, and tests.
COPY app ./app
COPY tests ./tests

# Document the port used by FastAPI.
EXPOSE 8000

# Start one FastAPI/Uvicorn process inside the container.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]