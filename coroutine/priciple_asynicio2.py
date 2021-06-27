import time
import asyncio

async def worker_1():
    print('worker_1 start')
    await asyncio.sleep(1)
    print('worker_1 done')
    return 1

async def worker_2():
    print('worker_2 start')
    await asyncio.sleep(2)
    print('worker_2 done')
    return 2 / 0

async def worker_3():
    print('worker_3 start')
    await asyncio.sleep(1)  # 如果这句话已经过了，那么主函数里的canceled就不生效了
    print('worker_3 done')
    # while True:
    #     print("worker_3 is running")
    #     time.sleep(0.5)
    return 3

async def main():
    task_1 = asyncio.create_task(worker_1())
    task_2 = asyncio.create_task(worker_2())
    task_3 = asyncio.create_task(worker_3())
    print("sleep 2 first")
    await asyncio.sleep(5)
    task_3.cancel() # 若3已经执行完，则无效
    print("task 3 is canceled")
    print("sleep 2 again")
    await asyncio.sleep(2)
    print("sleep 2 again again")
    await asyncio.sleep(2)
    res = await asyncio.gather(task_1, task_2, task_3, return_exceptions=True)
    print(res)


begin_time = time.time()
asyncio.run(main())
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))
