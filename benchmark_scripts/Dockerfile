# Use a lightweight Python base image
FROM python:3.11-slim

# Set environment variables
ENV VIRTUAL_ENV=/home/myenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate the virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Install Jupyter Notebook
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir notebook

# Set working directory
WORKDIR /home/myenv

# Expose port for Jupyter Notebook
EXPOSE 8888
