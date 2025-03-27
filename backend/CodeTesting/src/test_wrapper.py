import json
import importlib
import os


def get_json_data():
    with open("sample.json", "r") as file:
        sample_json = json.loads(file.read())
    inputs = sample_json["input"]
    expected_outputs = sample_json["output"]
    func_name = sample_json["func_name"]
    submission_path = sample_json["submission_path"]
    submission_fileName = os.path.basename(submission_path)
    module_name = os.path.splitext(submission_fileName)[0]

    return inputs, expected_outputs, func_name, module_name


def run_tests():
    # Read the json
    inputs, expected_outputs, func_name, module_name = get_json_data()

    # Import the funtion dynamically
    solution_module = importlib.import_module(module_name)
    solution_function = getattr(solution_module, func_name)

    # Run the function and compare expected outputs with actual outputs
    for i in range(len(inputs)):
        actual_output = solution_function(*(inputs[i]))
        if actual_output != expected_outputs[i]:
            print(
                f"Incorrect for input: {inputs[i]}, received: {actual_output}, expected: {expected_outputs[i]}"
            )
            return
    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
