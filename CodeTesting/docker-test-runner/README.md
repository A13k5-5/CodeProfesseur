# docker-test-runner/docker-test-runner/README.md

# Docker Test Runner

This project provides a simple way to run Python tests in a Docker container. It includes a test wrapper that imports a function from another module, executes tests based on input from files, and verifies the results against expected outputs.

## Project Structure

- `src/test_wrapper.py`: Contains the test wrapper that imports the `get_sum` function and runs tests.
- `src/test.py`: Defines the `get_sum` function that is tested.
- `src/tests.txt`: Input test cases for the `get_sum` function.
- `src/expectedOutput.txt`: Expected outputs corresponding to the test cases.
- `Dockerfile`: Instructions to build the Docker image for running the tests.
- `run_tests.sh`: Script to build the Docker image and run the tests in a container.

## Getting Started

To run the tests in a Docker container, follow these steps:

1. **Build the Docker Image**:
   Open a terminal and navigate to the project directory. Run the following command to build the Docker image:

   ```
   docker build -t test-runner .
   ```

2. **Run the Tests**:
   After the image is built, you can run the tests using the provided script:

   ```
   ./run_tests.sh
   ```

   This script will create a Docker container, execute the tests, and then remove the container after execution.

## Requirements

- Docker must be installed on your machine.
- Ensure that the necessary permissions are set to execute the `run_tests.sh` script.

## Conclusion

This project allows you to easily run Python tests in an isolated environment using Docker, ensuring that your tests are executed consistently across different setups.