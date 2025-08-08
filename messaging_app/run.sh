#!/bin/bash

# Build the Docker image
docker build -t messaging-app .

# Run the container with port mapping
docker run -p 8000:8000 --name messaging-app-container messaging-app