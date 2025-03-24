cd CodeTesting

# Build the Docker image
docker build -q -t test-runner . > /dev/null

# Run the Docker container
docker run --rm -q test-runner