FROM python:3.9-slim

WORKDIR /app

COPY . .

# Create data directory for file storage
RUN mkdir -p data/backups

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]