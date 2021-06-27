线程、进程、协程是日常开发的并发编程中绕不开的内容，而且想要深入掌握这一块知识，也必须对计算机底层知识有一定的掌握，包括组成原理、操作系统、网络等等，所以我写了[《线程进程协程》](https://juejin.cn/column/6973554491362639885)专栏，计划对相关知识做了一下梳理，既是自我的总结，也希望能帮助到读者。

本篇是该专栏的第5篇文章，重点讨论下Python的协程，本节内容的代码存放在github的该[目录](https://github.com/ZhiyuSun/python-pearl/tree/main/coroutine)下。

### 什么是协程

协程，又称微线程，纤程。英文名Coroutine。

子程序，或者称为函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。

所以子程序调用是通过栈实现的，一个线程就是执行一个子程序。

子程序调用总是一个入口，一次返回，调用顺序是明确的。而协程的调用和子程序不同。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

### 协程 VS 多线程

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。

### 基于生成器的协程

一个基于生成器协程的例子如下：

``` python
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)
```

输出结果为：

```
[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 OK
```

注意到consumer函数是一个generator，把一个consumer传入produce后：

首先调用c.send(None)启动生成器；

然后，一旦生产了东西，通过c.send(n)切换到consumer执行；

consumer通过yield拿到消息，处理，又通过yield把结果传回；

produce拿到consumer处理的结果，继续生产下一条消息；

produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。

### 基于asyncio库的协程

使用生成器的协程，是 Python 2 开头的时代实现协程的老方法了，Python 3.7 提供了新的基于 asyncio 和 async / await 的方法。

#### 普通的爬虫程序

``` python
import time

def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    time.sleep(sleep_time)
    print('OK {}'.format(url))


def main(urls):
    for url in urls:
        crawl_page(url)

begin_time = time.time()
main(['url_1', 'url_2', 'url_3', 'url_4'])
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))
```

上面这个程序是模拟的一个简单的爬虫程序，每个url的执行时间就是它们后面的数字，因为是循环执行，4个url一共花去了10s爬取。

#### 协程改造

首先来看 import asyncio，这个库包含了大部分我们实现协程所需的魔法工具。

async 修饰词声明异步函数，于是，这里的 crawl_page 和 main 都变成了异步函数。而调用异步函数，我们便可得到一个协程对象（coroutine object）。

有了协程对象后，便可以通过 asyncio.create_task 来创建任务。任务创建后很快就会被调度执行，这样，我们的代码也不会阻塞在任务这里。所以，我们要等所有任务都结束才行，用for task in tasks: await task 即可。

对于执行tasks，还可以使用gather函数，也可以达到一样的效果。

``` python
import time
import asyncio

async def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))

async def main(urls):
    tasks = [asyncio.create_task(crawl_page(url)) for url in urls]
    for task in tasks:
        await task
    # await asyncio.gather(*tasks)

begin_time = time.time()
asyncio.run(main(['url_1', 'url_2', 'url_3', 'url_4']))
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))
```

这段程序执行完后，耗时为最长的url执行时长，为4s。

#### 深入探索

``` python
import time
import asyncio

async def worker_1():
    print('worker_1 start')
    await asyncio.sleep(1)
    print('worker_1 done')

async def worker_2():
    print('worker_2 start')
    await asyncio.sleep(2)
    print('worker_2 done')

async def main():
    task1 = asyncio.create_task(worker_1())
    task2 = asyncio.create_task(worker_2())
    print('before await')
    await task1
    print('awaited worker_1')
    await task2
    print('awaited worker_2')

begin_time = time.time()
asyncio.run(main())
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))

```

上面这段程序的输出为：

```
before await
worker_1 start
worker_2 start
worker_1 done
awaited worker_1
worker_2 done
awaited worker_2
```

执行过程如下:

1. asyncio.run(main())，程序进入 main() 函数，事件循环开启；
2. task1 和 task2 任务被创建，并进入事件循环等待运行；
3. 运行到 print，输出 'before await'；
4. await task1 执行，用户选择从当前的主任务中切出，事件调度器开始调度 worker_1；
5. worker_1 开始运行，运行 print 输出'worker_1 start'，然后运行到 await asyncio.sleep(1)， 从当前任务切出，事件调度器开始调度 worker_2；
6. worker_2 开始运行，运行 print 输出 'worker_2 start'，然后运行 await asyncio.sleep(2) 从当前任务切出；
7. 以上所有事件的运行时间，都应该在 1ms 到 10ms 之间，甚至可能更短，事件调度器从这个时候开始暂停调度；
8. 一秒钟后，worker_1 的 sleep 完成，事件调度器将控制权重新传给 task_1，输出 'worker_1 done'，task_1 完成任务，从事件循环中退出；
9. await task1 完成，事件调度器将控制器传给主任务，输出 'awaited worker_1'，·然后在 await task2 处继续等待；
10. 两秒钟后，worker_2 的 sleep 完成，事件调度器将控制权重新传给 task_2，输出 'worker_2 done'，task_2 完成任务，从事件循环中退出；
11. 主任务输出 'awaited worker_2'，协程全任务结束，事件循环结束。

读者朋友可以通过调整参数，来模拟协程的过程。

#### 经验分享

开发者要提前知道一个任务的哪个环节会造成I/O阻塞，然后把这个环节的代码异步化处理，并且通过await来标识在任务的该环节中断该任务执行，从而去执行下一个事件循环任务。这样可以充分利用CPU资源，避免CPU等待I/O造成CPU资源白白浪费。当之前任务的那个环节的I/O完成后，线程可以从await获取返回值，然后继续执行没有完成的剩余代码。

协程里面重要的是一个关键字await的理解，async表示其修饰的是协程任务即task，await表示的是当线程执行到这一句，此时该task在此处挂起，然后调度器去执行其他的task，当这个挂起的部分处理完，会调用回掉函数告诉调度器我已经执行完了，那么调度器就返回来处理这个task的余下语句。

### 多线程和asyncio

#### 多线程的局限性

多线程有诸多优点且应用广泛，但也存在一定的局限性：

比如，多线程运行过程容易被打断，因此有可能出现 race condition 的情况；再如，线程切换本身存在一定的损耗，线程数不能无限增加，因此，如果你的 I/O 操作非常 heavy，多线程很有可能满足不了高效率、高质量的需求。

race condition即资源竞争，多个线程在执行的过程中有可能会导致同一个资源/数据被多个线程争夺的情况，这样会导致最后的结果可能会和期望的结果不一致。

#### asyncio的工作原理

Asyncio 和其他 Python 程序一样，是单线程的，它只有一个主线程，但是可以进行多个不同的任务（task），这里的任务，就是特殊的 future 对象。这些不同的任务，被一个叫做 event loop 的对象所控制。你可以把这里的任务，类比成多线程版本里的多个线程。

为了简化讲解这个问题，我们可以假设任务只有两个状态：一是预备状态；二是等待状态。所谓的预备状态，是指任务目前空闲，但随时待命准备运行。而等待状态，是指任务已经运行，但正在等待外部的操作完成，比如 I/O 操作。

在这种情况下，event loop 会维护两个任务列表，分别对应这两种状态；并且选取预备状态的一个任务（具体选取哪个任务，和其等待的时间长短、占用的资源等等相关），使其运行，一直到这个任务把控制权交还给 event loop 为止。

当任务把控制权交还给 event loop 时，event loop 会根据其是否完成，把任务放到预备或等待状态的列表，然后遍历等待状态列表的任务，查看他们是否完成。

- 如果完成，则将其放到预备状态的列表；
- 如果未完成，则继续放在等待状态的列表。

而原先在预备状态列表的任务位置仍旧不变，因为它们还未运行。这样，当所有任务被重新放置在合适的列表后，新一轮的循环又开始了：event loop 继续从预备状态的列表中选取一个任务使其执行…如此周而复始，直到所有任务完成。

值得一提的是，对于 Asyncio 来说，它的任务在运行时不会被外部的一些因素打断，因此 Asyncio 内的操作不会出现 race condition 的情况，这样你就不需要担心线程安全的问题了。

#### asyncio的缺陷

实际工作中，想用好 Asyncio，特别是发挥其强大的功能，很多情况下必须得有相应的 Python 库支持Asyncio 软件库的兼容性问题，在 Python3 的早期一直是个大问题，但是随着技术的发展，这个问题正逐步得到解决。

另外，使用 Asyncio 时，因为你在任务的调度方面有了更大的自主权，写代码时就得更加注意，不然很容易出错。

#### 多线程还是asyncio？

``` python
if io_bound:
    if io_slow:
        print('Use Asyncio')
    else:
        print('Use multi-threading')
else if cpu_bound:
    print('Use multi-processing')
```

可遵循以上原则：

- 如果是 I/O bound，并且 I/O 操作很慢，需要很多任务 / 线程协同实现，那么使用 Asyncio 更合适 
- 如果是 I/O bound，但是 I/O 操作很快，只需要有限数量的任务 / 线程，那么使用多线程就可以了。
- 如果是 CPU bound，则需要使用多进程来提高程序运行效率。

#### 多线程和asyncio协程对比

相同点是都是并发操作，多线程同一时间点只能有一个线程在执行，协程同一时间点只能有一个任务在执行；

对于Python多线程和协程不同点，我做了一张表格


|  |多线程  |asyncio  |
| --- | --- | --- |
| 线程数 | 多线程 |单线程|
| 调度 | 操作系统 |用户控制，更大的自主控制权|
| race condition(资源竞争) | 容易打断，会出现线程安全问题 |不会被打断，不用担心线程安全|
| 切换开销 | 线程切换 |任务切换损耗远小于线程切换损耗|
| 可开启任务数量 | 少 |比线程数量多的多|
| 执行效率 | 如果 IO 操作很快，并不 heavy，那么运用多线程，也能很有效地解决问题 |IO操作heavy的场景下，比多线程运行效率更高|
| 第三方库支持 | 完善 |不完善|


### 参考资料

https://www.liaoxuefeng.com/wiki/1016959663602400/1017968846697824

https://time.geekbang.org/column/article/101855