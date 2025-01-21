# Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-opencv \
    libopencv-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /backend

# Install dependencies
COPY requirements.txt /backend/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Make the entry point script executable
RUN chmod +x docker-entrypoint.sh

# Entry point
ENTRYPOINT [ "sh", "./docker-entrypoint.sh" ]

# Expose port
EXPOSE 8000