import threading
import requests
from time import *


def loop_request(n):
    for i in range(n):
        requests.get("http://www.baidu.com")


if __name__ == '__main__':
    begin_time = time()
    #
    # loop_request(50)
    #
    t1 = threading.Thread(target=loop_request, args=(25,))
    t2 = threading.Thread(target=loop_request, args=(25,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))
