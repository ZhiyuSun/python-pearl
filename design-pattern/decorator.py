import time

def log_time(func):  # 接受一个函数作为参数
    def _log(*args, **kwargs):
        beg = time.time()
        res = func(*args, **kwargs)
        print('use time: {}'.format(time.time() - beg))
        return res

    return _log

@log_time  # 装饰器语法糖
def mysleep():
    time.sleep(1)

mysleep()

# 另一种写法，和上面的调用方式等价
def mysleep2():
    time.sleep(1)

newsleep = log_time(mysleep2)
newsleep()