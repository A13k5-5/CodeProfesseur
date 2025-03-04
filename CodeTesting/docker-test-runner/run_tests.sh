#!/bin/bash

# Build the Docker image
docker build -t test-runner .

# Run the Docker container
docker run --rm test-runner

# The --rm flag automatically removes the container after it exits.