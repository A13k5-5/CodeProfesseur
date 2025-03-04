from test import get_sum

if __name__ == "__main__":
    with open("tests.txt", "r") as tests_file:
        test_cases = [line.strip() for line in tests_file.readlines()]
    for test in test_cases:
        get_sum(test)
