from threading import Thread
from time import sleep
from queue import Queue

class Producer(Thread):
    def __init__(self, worker, queue):
        super().__init__()
        self._worker = worker
        self._queue = queue

    def run(self):
        while True:
            if 0 <= self._queue.qsize() <= 10:
                queue.put('baozi')
                print('{} 生产了1个包子, 一共{}个包子'.format(self._worker,
                                                   self._queue.qsize()))
                sleep(0.5)
            elif 10 < self._queue.qsize() <= 20:
                queue.put('baozi')
                print('{} 生产了1个包子, 一共{}个包子'.format(self._worker, self._queue.qsize()))
                sleep(1)
            else:
                print('仓库较多，生产者休息3秒钟。')
                sleep(3)

# content of queue_test.py
class Consumer(Thread):
    def __init__(self, client, queue):
        super().__init__()
        self._client = client
        self._queue = queue

    def run(self):
        while True:
            if self._queue.empty():
                print('仓库没有包子了。。。')
                sleep(0.5)
            else:
                result = self._queue.get()
                print('{} 消费了1个包子, 还剩{}个包子'.format(self._client, self._queue.qsize()))
                sleep(0.5)

queue = Queue(maxsize=20)

for item in ['LiBao', 'YangBao']:
    temp = Producer(item, queue)
    temp.start()

for item in ['ChengBaoConsumer', 'TianBaoConsumer']:
    temp = Consumer(item, queue)
    temp.start()