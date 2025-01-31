# pip install aiopyston

from pyston import PystonClient,File
import asyncio

async def main():

    with open('test.py') as f:
        file = File(f)

    client = PystonClient()
    output = await client.execute(
        "python",
        [file]
    )

    print(output)

asyncio.get_event_loop().run_until_complete(main())