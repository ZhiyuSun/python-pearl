def flist(l):
    l.append(0)
    print(id(l))    # 每次打印的id相同
    print(l)


ll = []
print(id(ll))
flist(ll)   # [0]
flist(ll)   # [0,0]

print("=" * 10)


def fstr(s):
    print(id(s)) # 和入参ss的id相同
    s += "a"
    print(id(s))  # 和入参ss的id不同，每次打印结果不相同
    print(s)


ss = "sun" # 我这里没有用空字符串，如果是空字符串，函数+"a"那里由于缓存机制，会永远为"a"的地址，读者可自己做测试
print(id("a"))
print(id(ss))
fstr(ss)    # a
fstr(ss)    # a

print("=" * 10)


def clear_list(l):
    l = []

l2 = [1,2,3]
clear_list(l2)
print(l2) # [1,2,3]

print("=" * 10)

# 2
def fl(l=[1]):
    l.append(1)
    print(l)
fl()
fl()
# 记住：默认参数只计算一次

print("=" * 10)

# 3
a = 1
def fun(a):
    print("func_in",id(a))
    a = 2
    print("re-point",id(a), id(2))
print("func_out",id(a), id(1))

fun(a)

print("=" * 10)

# 什么是 args?
def print_multiple_args(*args):
    print(type(args), args)
    for idx, val in enumerate(args):  # enumerate()枚举函数
        print(idx, val)


print_multiple_args('a', 'b', 'c')
# 通过将列表前加*打包成关键字参数，指明了接收值参数必须是*args
print_multiple_args(*['a', 'b', 'c'])


# 什么是 kwargs?
def print_kwargs(**kwargs):
    print(type(kwargs), kwargs)
    for k, v in kwargs.items():
        print('{}: {}'.format(k, v))


print_kwargs(a=1, b=2)
# 给字典前加**打包成关键字参数,指明接收值的参数必须是**kwargs
print_kwargs(**dict(a=1, b=2))


def print_all(a, *args, **kwargs):
    print(a)
    if args:
        print(args)
    if kwargs:
        print(kwargs)


print_all('hello', 'world', name='monki')