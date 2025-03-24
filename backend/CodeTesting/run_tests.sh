# Build the Docker image
docker build -q -t test-runner .

# Run the Docker container
docker run --rm -q test-runner