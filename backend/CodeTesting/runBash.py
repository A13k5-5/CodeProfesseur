import subprocess


def exec_bash():
    try:
        result = subprocess.run(
            ["bash", "./run_tests.sh"],
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
    output = exec_bash()
    print(output)
