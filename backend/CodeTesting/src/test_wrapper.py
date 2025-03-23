# FILE: /docker-test-runner/docker-test-runner/src/test_wrapper.py
# This file can never be run on its own, as it is running test.py implicitly by importing it.
# Therefore this file can be executed either by Piston API or in an isolated docker container

import importlib
import sys
import json

sys.path.append("../..")  # Add parent directory to path
# from database import dbmanager


def code_tester(module_name: str, func_name: str, qid: int):
    try:
        module = importlib.import_module(module_name)
        target_function = getattr(module, func_name)
    except (ImportError, AttributeError) as e:
        print("Module or function not found")

    def test():
        # db = dbmanager("../../professeur.db")
        # test_cases = db.get_question(qid)["input"]
        # expected_outputs = db.get_question(qid)["output"]
        # print(test_cases, expected_outputs)
        with open("sample.json") as jsonData:
            data = json.load(jsonData)
            test_cases = data["input"]
            expected_outputs = data["output"]
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
    code_tester("forSampleJson", "returnTwo", "1")
