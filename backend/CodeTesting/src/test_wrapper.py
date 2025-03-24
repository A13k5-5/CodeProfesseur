# This file can never be run on its own, as it is running test.py implicitly by importing it.
# Therefore this file should be run using the Docker environment built in runBash.py

import importlib
import sys
import json
import os


def get_json_data():
    with open("sample.json") as jsonData:
        data = json.load(jsonData)
        test_cases = data["input"]
        expected_outputs = data["output"]
        submission_path = data["submission_path"]
        func_name = data["func_name"]
    submission_fileName = os.path.basename(submission_path)
    module_name = os.path.splitext(submission_fileName)[0]
    return test_cases, expected_outputs, module_name, func_name


def code_tester():
    test_cases, expected_outputs, module_name, func_name = get_json_data()
    try:
        module = importlib.import_module(module_name)
        target_function = getattr(module, func_name)
    except (ImportError, AttributeError) as e:
        print("Module or function not found")

    def test():
        for i, test in enumerate(test_cases):
            output = target_function(*test)
            if output != expected_outputs[i]:
                print(
                    f"Incorrect for input: {test}, received: {output}, expected: {expected_outputs[i]}"
                )
                return
        print("All tests passed!")

    test()


if __name__ == "__main__":
    code_tester()
