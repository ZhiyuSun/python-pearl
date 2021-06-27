本篇是[《线程进程协程》](https://juejin.cn/column/6973554491362639885)专栏的第三篇文章，重点来认识一下Python的GIL锁，并且去深入去理解其对Python多线程的影响。

### 什么是GIL

全局解释器锁 GIL，英文名称为 Global Interpreter Lock，它是解释器中一种线程同步的方式。对于每一个解释器进程都具有一个 GIL ，它的直接作用是限制单个解释器进程中多线程的并行执行，使得即使在多核处理器上对于单个解释器进程来说，在同一时刻运行的线程仅限一个。

对于 Python 来讲，GIL 并不是它语言本身的特性，而是 CPython 解释器的实现特性。Python 代码被编译后的字节码会在解释器中执行，在执行过程中，存在于 CPython 解释器中的 GIL 会致使在同一时刻只有一个线程可以执行字节码。

GIL 的存在引起的最直接的问题便是：在一个解释器进程中通过多线程的方式无法利用多核处理器来实现真正的并行。

因此，Python的多线程是伪多线程，无法利用多核资源，同一个时刻只有一个线程在真正的运行。

### 探讨GIL对Python多线程的影响

#### IO密集型和CPU密集型

接下来，我们通过一些代码实例来模拟GIL对Python多线程的影响。

首先回顾一下计算机密集型和IO密集型。
- 计算密集型（ CPU-bound ）：也称为 CPU 密集型，大部分时间都用于进行计算、逻辑验证等 CPU 处理的程序，比如矩阵计算、视频编解码等，CPU 占用率高。
- IO 密集型（ IO-bound ）：大部分时间都用于等待 IO（比如网络IO，磁盘IO ）处理完成的程序，比如大多数 Web 应用等，CPU 占用率低。

#### CPU密集型代码测试

先对计算密集型进行单线程测试。

``` python
from time import time

def loop_add(n):
    i = 0
    while i < n:
        i += 1


if __name__ == '__main__':
    begin_time = time()

    loop_add(100000000)

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))

```

返回结果为：程序耗时3.2977540493011475s

再对计算密集型进行多线程测试。

``` python
import threading
from time import time

def loop_add(n):
    i = 0
    while i < n:
        i += 1


if __name__ == '__main__':
    begin_time = time()

    t1 = threading.Thread(target=loop_add, args=(50000000,))
    t2 = threading.Thread(target=loop_add, args=(50000000,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))

```

程序耗时3.718836545944214s

#### IO密集型代码测试

再对IO密集型进行测试。

``` python
import requests
from time import *


def loop_request():
    for i in range(50):
        requests.get("http://www.baidu.com")

if __name__ == '__main__':
    begin_time = time()

    loop_request()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))
```
程序耗时3.770847797393799s

改为多线程再进行测试。

``` python
import threading
import requests
from time import *


def loop_request(n):
    for i in range(n):
        requests.get("http://www.baidu.com")


if __name__ == '__main__':
    begin_time = time()

    t1 = threading.Thread(target=loop_request, args=(25,))
    t2 = threading.Thread(target=loop_request, args=(25,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end_time = time()
    run_time = end_time - begin_time
    print("程序耗时{}s".format(run_time))

```

程序耗时1.7753996849060059s

#### 结论

对比结果可以发现，对于CPU密集型程序，多线程并无明显的性能提升，反而延迟增大了，而对于IO密集型程序，执行时间减半了。

为什么CPU密集型的程序的执行时间没有减半呢？这正是GIL 导致的结果，由于在同一时刻，即使在多核 CPU 上，也仅有一个线程在获得该全局锁后才可以执行字节码，其他的线程想要执行字节码就需要等待该全局锁被释放，所以未能实现真正的并行执行，而是一种多线程交替执行的串行执行。因为在多个线程执行过程中也涉及到了全局锁的获取和释放，上下文环境的切换等。并且相较于单核 CPU，这种效率降低的情况在多核 CPU 上在可能会更加显著。

为什么IO密集型的程序执行时间减半了呢？python3.2版本后，GIL锁以固定的时间间隔来进行线程的切换，在其他线程请求获取 GIL 时，当前运行的线程会以 5 毫秒（默认时间）为间隔尝试释放 GIL，另外，GIL 会在遇到 IO操作时被释放并交由其他线程继续执行，比如网络 IO 操作、文件读写等。

### GIL存在的原因

既然GIL对CPU密集型的Python多线程影响这么大，那它为什么存在呢？我们有必要去追溯下原因。

Python 在单核 CPU 时代诞生，所以在最初 CPython 解释器的设计开发中，更多考虑的是适合当时主流的单核 CPU 下的使用场景。

CPython中主要使用引用计数来进行垃圾回收，假如两个线程中引用同一个对象，则有可能导致非线程安全，即一个线程引用计数的更新并未体现在另外一个线程对该引用计数的获取上。所以引入GIL这样粒度大的全局锁后，可以有效的避免 CPython 的内存管理机制在多线程环境中的非线程安全，保证多线程下共享数据的一致性。

GIL锁粒度较大，不需要频繁的获取和释放，相比于其他实现（比如更细粒度的锁），GIL使得Python在单线程下可以保证较高的效率，并且在实现上也相对简单。

随着进入多核CPU时代，Python的多线程无法利用多核CPU也成为了历史遗留问题。

### 有了GIL，还需要关注线程安全吗

我们同样使用一段代码例子来测试

``` python
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
```
我们有两个函数`increase`和`increase_with_lock`，两者的差别是前者没有互斥锁，我们执行`multithread_increase`来对比两个函数的执行结果。

测试结果为
```
6633318
10000000
```

可以看到，在无锁的递增函数中，是非线程安全的，说明在多线程执行过程中，某些线程的修改结果并未体现在其他线程的修改过程中。

原因在于：

GIL 保证的是每一条字节码在执行过程中的独占性，即每一条字节码的执行都是原子性的。GIL 具有释放机制，所以 GIL 并不会保证字节码在执行过程中线程不会进行切换，即在多个字节码之间，线程具有切换的可能性。

我们可以用python的dis模块去查看`a += 1`执行的字节码，发现需要有多个字节码去完成，线程具有切换的可能性，所以它是非线程安全的。

![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/baf13f9bc7ea4593b459f933e8cc4651~tplv-k3u1fbpfcp-watermark.image)

GIL 和线程互斥锁的粒度是不同的，GIL 是 Python 解释器级别的互斥，保证的是解释器级别共享资源的一致性，而线程互斥锁则是代码级（或用户级）的互斥，保证的是 Python 程序级别共享数据的一致性，所以我们仍需要线程互斥锁及其他线程同步方式来保证数据一致。

### 在GIL下如何提升性能

面对GIL的存在，我们有可以有多个方法帮助我们提升性能
- 在 IO 密集型任务下，我们可以使用多线程或者协程来完成。
- 可以选择更换 Jython 等没有 GIL 的解释器，但并不推荐更换解释器，因为会错过众多 C 语言模块中的有用特性。
- 使用多进程来代替多线程。
- 将计算密集型任务转移到 Python 的 C / C++ 扩展模块中完成。

接下来，我们用多进程来改造前面的CPU密集型的代码。

``` python
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

```

结果为：程序耗时1.7649831771850586s

还记得我们前面的结果吗，单线程程序耗时为3.2977540493011475s，多线程程序耗时为3.718836545944214s。现在使用多进程程序，时间缩短了一半。

至此，Python的GIL的知识大致就讲完了，欢迎讨论交流~

这一节所有的代码在我github的该[目录](https://github.com/ZhiyuSun/python-pearl/tree/main/GIL)下。
