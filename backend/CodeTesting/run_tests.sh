#!/bin/bash

# Build the Docker image
docker build -q -t test-runner .

# Run the Docker container
docker run --rm -q test-runner

# The --rm flag automatically removes the container after it exits.