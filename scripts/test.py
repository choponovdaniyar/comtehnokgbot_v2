import asyncio
import sys
from build import *
from loguru import logger
bl = Builder()


logger.add("test.log", level="DEBUG")

async def run():
    size = 10000

    for x in range(size):
        await bl.build_table()
        print()
    sys.exit()

async def start():
    funcs = [timer(), run()]
    await asyncio.gather(*funcs)

if __name__ == "__main__":
        asyncio.run(start())