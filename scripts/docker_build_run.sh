#!/bin/bash
# Build and run Docker container

IMAGE_NAME="browser-automation-python"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Running security verification..."
docker run --rm $IMAGE_NAME

echo "Running JSON verification..."
docker run --rm $IMAGE_NAME check_cred_json

echo "Install pytest in the image..."
docker run pip install pytest

echo "Run tests inside the container..."
docker run --rm browser-automation-python pytest