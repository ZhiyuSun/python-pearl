import threading
from time import time

def loop_add(n):
    i = 0
    while i < n:
        i += 1


if __name__ == '__main__':
    begin_time = time()

    # loop_add(100000000)
    #
    t1 = threading.Thread(target=loop_add, args=(50000000,))
    t2 = threading.Thread(target=loop_add, args=(50000000,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))
