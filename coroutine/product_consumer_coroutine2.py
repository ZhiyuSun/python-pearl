import asyncio
import random
import time


async def consumer(queue, id):
    while True:
        val = await queue.get()
        print('{} get a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def producer(queue, id):
    for i in range(5):
        val = random.randint(1, 10)
        await queue.put(val)
        print('{} put a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def main():
    queue = asyncio.Queue()

    consumer_1 = asyncio.create_task(consumer(queue, 'consumer_1'))
    consumer_2 = asyncio.create_task(consumer(queue, 'consumer_2'))

    producer_1 = asyncio.create_task(producer(queue, 'producer_1'))
    producer_2 = asyncio.create_task(producer(queue, 'producer_2'))

    print("start")
    consumer_1.cancel()
    consumer_2.cancel()
    print("consumer is canceled")
    await asyncio.sleep(10)

    res = await asyncio.gather(consumer_1, consumer_2, producer_1, producer_2, return_exceptions=True)
    print(res)

begin_time = time.time()
asyncio.run(main())
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))


