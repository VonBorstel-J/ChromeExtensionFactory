# /backend/Dockerfile

# Stage 1: Build the backend dependencies
FROM python:3.10-slim as builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Run the backend with Gunicorn and Gevent
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port for the Flask application
EXPOSE 5000

# Start Gunicorn with Gevent workers
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "4", "--worker-class", "gevent", "--timeout", "120"]
