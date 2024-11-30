# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies, including MySQL development libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY . .

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
