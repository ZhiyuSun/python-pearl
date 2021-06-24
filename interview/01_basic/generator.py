
# 生成器
def simple_gen():
    yield 'hello'
    yield 'world'

gen = simple_gen()
print(type(gen))  # <class 'generator'>
print(next(gen))
print(next(gen))
# print(next(gen))


# 基于生成器的协程
def coro():
    hello = yield 'hello' # yield关键字在=右边作为表达式，可以被send值
    yield hello

c = coro()
print(next(c)) # 输出"hello"，这里调用next产出第一个值"hello"，之后函数暂停
print(c.send('world')) # 再次调用send发送值，此时hello变量赋值为'world'，然后yield产出hello变量的值'world'
# 之后协程结束，后续再send值会抛异常StopIteration
# c.send(None) # 抛出异常
next(c)
