# FILE: /docker-test-runner/docker-test-runner/src/test_wrapper.py
# This file can never be run on its own, as it is running test.py implicitly by importing it.
# Therefore this file can be executed either by Piston API or in an isolated docker container

import importlib

def code_tester(module_name, func_name):

    try:
        module = importlib.import_module(module_name)
        target_function = getattr(module, func_name)
    except (ImportError, AttributeError) as e:
        print("Stupid")


    def test():
        with open("tests.txt", "r") as tests_file:
            test_cases = [int(line.strip()) for line in tests_file.readlines()]
        with open("expectedOutput.txt", "r") as test_output_files:
            expected_outputs = [int(line.strip()) for line in test_output_files.readlines()]
        for i, test in enumerate(test_cases):
            output = target_function(test)
            if output != expected_outputs[i]:
                print(
                    f"Incorrect for input: {test}, received: {output}, expected: {expected_outputs[i]}"
                )
                return
        print("All tests passed")
    
    test()


if __name__ == "__main__":
    # test()
    code_tester("test", "get_sum")
