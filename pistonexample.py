from pyston import PystonClient, File
import asyncio


async def main():
    with open("tests.txt", "r") as tests_file:
        test_cases = [line.strip() for line in tests_file.readlines()]

    with open("test.py") as f:
        file = File(f)

    client = PystonClient()

    for test in test_cases:
        print(f"Running with input: {test}")
        output = await client.execute("python", [file], args=[test])
        print(f"Output: {output}")
        print("-" * 30)


asyncio.get_event_loop().run_until_complete(main())
