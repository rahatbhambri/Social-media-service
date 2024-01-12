import asyncio, random
from time import sleep

async def run_tasks():
    await asyncio.gather(waited_sum(13, 2), waited_sq(5), waited_mul(23, 6)) 

async def waited_sum(a, b):
    d = random.randint(5, 15)
    await asyncio.sleep(d)
    print(a+b, "Async result1")

async def waited_mul(a, b):
    d = random.randint(5, 15)
    await asyncio.sleep(d)
    print(a*b, "Async result2")

async def waited_sq(a):
    d = random.randint(5, 15)
    await asyncio.sleep(d)
    print(a**2, "Async result2")
