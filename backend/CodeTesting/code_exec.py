import json
import os
import judge0
from judge0 import File, Filesystem


CPU_TIME_LIMIT = 3.0


# This function generates a sample json that contains all the data
# test wrapper uses.
def generate_sample_json(input_json, output_json, submission_path, func_name):
    input_data = json.loads(input_json)
    output_data = json.loads(output_json)

    combined_data = {
        "input": input_data,
        "output": output_data,
        "submission_path": submission_path,
        "func_name": func_name,
    }

    return json.dumps(combined_data)


def evaluate_submission(input_json, output_json, submission_path, func_name):
    sample_json = generate_sample_json(
        input_json, output_json, submission_path, func_name
    )
    submission_fileName = os.path.basename(submission_path)

    with open("./CodeTesting/src/test_wrapper.py", "r") as file:
        wrapper = file.read()

    # Take the submitted file from uploads folder
    with open(f"./CodeTesting/uploads/{submission_fileName}", "r") as file:
        solution = file.read()

    fs = Filesystem(
        content=[
            File(name="sample.json", content=sample_json),
            File(name=submission_fileName, content=solution),
        ]
    )
    result = judge0.run(
        source_code=wrapper, additional_files=fs, cpu_time_limit=CPU_TIME_LIMIT
    )
    return "Time limit exceeded\n" if result.stdout == None else result.stdout
