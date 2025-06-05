# Dockerfile

# 1. Base image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /usr/src/app

# Install system dependencies (including curl)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      curl && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY app ./app

# 6. Expose port 5000
EXPOSE 5000

# 7. Set environment variables
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 8. Start the Flask app
CMD ["flask", "run"]
