# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to use it in the combined layer
COPY requirements.txt .

# Install system dependencies and Python dependencies in a single layer to minimize size
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && pip install --no-cache-dir -r requirements.txt \
    # Clean up build dependencies to save space
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Remove Python compiled files and cache
    && find . -type d -name "__pycache__" -exec rm -rf {} + \
    && find . -type f -name "*.pyc" -delete \
    && find . -type f -name "*.pyo" -delete \
    && find . -type f -name "*.pyd" -delete

# Copy the entire project
COPY . .

# Expose the API port (FastAPI default is 8000)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
