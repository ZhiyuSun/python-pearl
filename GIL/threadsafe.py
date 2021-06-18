import threading

a = 0
lock = threading.Lock()


def increase(n):
    global a
    for i in range(n):
        a += 1


def increase_with_lock(n):
    global a
    for i in range(n):
        lock.acquire()
        a += 1
        lock.release()


def multithread_increase(func, n):
    threads = [threading.Thread(target=func, args=(n,)) for i in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(a)


if __name__ == '__main__':
    multithread_increase(increase, 1000000)
    a = 0
    multithread_increase(increase_with_lock, 1000000)
