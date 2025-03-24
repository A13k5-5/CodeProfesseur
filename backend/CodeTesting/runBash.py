import subprocess
import json


def exec_bash(input_json, output_json, path):
    input_data = json.loads(input_json)
    output_data = json.loads(output_json)

    combined_data = {"input": input_data, "output": output_data}

    with open(path, "w") as file:
        json.dump(combined_data, file)
    try:
        result = subprocess.run(
            ["bash", "run_tests.sh"],
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
    path = "./run_tests.sh"
    # output = exec_bash()
    # print(output)
