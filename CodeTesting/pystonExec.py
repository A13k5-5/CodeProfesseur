from pyston import PystonClient, File
import asyncio
import re


async def main():
    with open("tests.txt", "r") as tests_file:
        test_cases = [line.strip() for line in tests_file.readlines()]

    with open("test.py", "r") as f:
        test_code = f.read()

    client = PystonClient()

    for test in test_cases:
        print(f"Running with input: {test}")

        # Create a wrapper script that safely imports just the function
        wrapper_code = """
# Create a temporary module file
with open("temp_module.py", "w") as f:
    f.write('''
{}
''')

# Import only the function from the module
from temp_module import get_sum

# Run get_sum with test input
result = get_sum({})
print(result)
""".format(
            test_code, test
        )

        # Create a File object with the wrapper code
        wrapper_file = File("wrapper.py", wrapper_code)

        # Execute the wrapper script
        output = await client.execute("python", [wrapper_file])
        print(f"Output: {output}")
        print("-" * 30)


# Use the recommended asyncio pattern
asyncio.run(main())
