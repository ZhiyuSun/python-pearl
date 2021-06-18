import multiprocessing
from time import time


def loop_add(n):
    i = 0
    while i < n:
        i += 1


if __name__ == '__main__':
    begin_time = time()

    p1 = multiprocessing.Process(target=loop_add, args=(50000000,))
    p2 = multiprocessing.Process(target=loop_add, args=(50000000,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))
