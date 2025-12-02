# Backend Dockerfile - Production Ready
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Create directories for data persistence
RUN mkdir -p /app/chroma_db /app/sample_data

# Expose port (will be overridden by $PORT on cloud platforms)
EXPOSE 8000

# Run startup script (seeds DB and starts server)
CMD ["bash", "start.sh"]