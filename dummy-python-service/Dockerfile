# Use the official Python image as base
FROM python:3.11-slim

# Set non-root user and create directories with correct ownership
RUN groupadd -g 999 python && useradd -r -u 999 -g python python

# Create app root
RUN mkdir -p /app

# Copy Python service
COPY ./service app/service

# Set work dir
WORKDIR /app

# Install Python packages
#COPY ./dummy-python-service/requirements.txt /service/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/service/requirements.txt

# Env & build args
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy Python application
#COPY ./dummy-python-service /service

# WSGI + ASGI
ENTRYPOINT python /app/service/gunicorn_runner.py
