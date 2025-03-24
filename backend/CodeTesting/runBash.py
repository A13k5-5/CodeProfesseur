import subprocess
import json


def exec_bash(input_json, output_json, submission_path, func_name):
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
    try:
        result = subprocess.run(
            ["bash", "./CodeTesting/run_tests.sh"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        return e.stderr


if __name__ == "__main__":
    input = "[[1], [2], [3], [4], [5], [6], [7]]"
    output = "[[1, 1], [2, 2], [3, 1], [4, 4], [5, 5], [6, 6], [7, 7]]"
    path = "./run_tests.sh"
    output = exec_bash(input, output, "./src/sample.json")
    print(output)
