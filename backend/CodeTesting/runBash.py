import subprocess
import json
import os
import judge0
from judge0 import File, Filesystem


CPU_TIME_LIMIT = 3.0


def write_sample_json(input_json, output_json, submission_path, func_name):
    input_data = json.loads(input_json)
    output_data = json.loads(output_json)

    combined_data = {
        "input": input_data,
        "output": output_data,
        "submission_path": submission_path,
        "func_name": func_name,
    }

    with open("./CodeTesting/src/sample.json", "w") as file:
        json.dump(combined_data, file)


def exec_bash(input_json, output_json, submission_path, func_name):
    write_sample_json(input_json, output_json, submission_path, func_name)
    submission_fileName = os.path.basename(submission_path)

    with open("./CodeTesting/src/sample.json", "r") as file:
        sample_json = file.read()

    with open("./CodeTesting/src/test_wrapper.py", "r") as file:
        wrapper = file.read()

    # Take the submitted file from uploades folder
    with open(f"./CodeTesting/uploads/{submission_fileName}", "r") as file:
        solution = file.read()

    fs = Filesystem(
        content=[
            File(name="sample.json", content=sample_json),
            # Renames any solution into solution.py
            File(name=submission_fileName, content=solution),
        ]
    )
    result = judge0.run(
        source_code=wrapper, additional_files=fs, cpu_time_limit=CPU_TIME_LIMIT
    )
    return "Time limit exceeded" if result.stdout == None else result.stdout


if __name__ == "__main__":
    input = "[[1], [2], [3], [4], [5], [6], [7]]"
    output = "[[1, 1], [2, 2], [3, 1], [4, 4], [5, 5], [6, 6], [7, 7]]"
    path = "./run_tests.sh"
    output = exec_bash(input, output, "./src/sample.json")
    print(output)
