from test import get_sum

if __name__ == "__main__":
    with open("tests.txt", "r") as tests_file:
        test_cases = [line.strip() for line in tests_file.readlines()]
    with open("expectedOutput.txt", "r") as test_output_files:
        expected_outputs = [line.strip() for line in test_output_files.readlines()]
    for i, test in enumerate(test_cases):
        output = get_sum(test)
        assert (
            output == expected_outputs[i]
        ), f"Incorrect for input: {test}, received: {output}, expected: {expected_outputs[i]}"
