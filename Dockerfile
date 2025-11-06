# Dockerfile for Fly.io deployment
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLY_IO=true

# Expose port for health checks
EXPOSE 8080

# Run the bot
CMD ["python3", "main.py"]

