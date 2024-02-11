# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install curl for health checks and clean up after to reduce image size
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install the Python dependencies defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Set an environment variable to ensure Python scripts look in the correct directory
ENV PYTHONPATH=/app

# Define the health check for the container to check the app's health status
# This will perform a curl command to the app's health endpoint
# If the command fails, the container is considered unhealthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Command to run the app using Gunicorn, a Python WSGI HTTP Server for UNIX
# Binds Gunicorn to all network interfaces on port 8000 and runs the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]