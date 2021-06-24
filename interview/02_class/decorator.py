import time


def log_time(func): # 接受一个函数作为参数
    def _log(*args, **kwargs):
        beg = time.time()
        res = func(*args, **kwargs)
        print('use time: {}'.format(time.time()-beg))
        return res
    return _log


@log_time   # 装饰器语法糖
def mysleep():
    time.sleep(1)

mysleep()

# 另一种写法，和上面的调用方式等价

def mysleep2():
    time.sleep(1)

newsleep = log_time(mysleep2)
newsleep()


# 类装饰器
class LogTime:
    def __call__(self, func): # 接受一个函数作为参数
        def _log(*args, **kwargs):
            beg = time.time()
            res = func(*args, **kwargs)
            print('use time: {}'.format(time.time()-beg))
            return res
        return _log

@LogTime()
def mysleep3():
    time.sleep(1)

mysleep3()


# 给类装饰器增加参数，使用类装饰器比较方便实现装饰器参数
class LogTime2:
    def __init__(self, use_int=False):
        self.use_int = use_int

    def __call__(self, func): # 接受一个函数作为参数
        def _log(*args, **kwargs):
            beg = time.time()
            res = func(*args, **kwargs)
            if self.use_int:
                print('use time: {}'.format(int(time.time()-beg)))
            else:
                print('use time: {}'.format(time.time()-beg))
            return res
        return _log

@LogTime2(True)
def mysleep4():
    time.sleep(1)

mysleep4()

@LogTime2(False)
def mysleep5():
    time.sleep(1)

mysleep5()