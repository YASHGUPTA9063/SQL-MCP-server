# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if required natively by python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the standard port the SDK uses for streamable-http
EXPOSE 5222

# Run the server. It will expect authentication requests from Cohere North by default.
CMD ["python", "server.py", "--transport", "streamable-http"]
