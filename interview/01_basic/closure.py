def addx(x):
    def adder(y):
        return x + y
    return adder

c = addx(8)
print(type(c))
print(c.__name__)
print(c(10))

print("=" * 10)

from functools import wraps

def cache(func):
    store = {}
    @wraps(func)
    def _(n):
        if n in store:
            return store[n]
        else:
            res = func(n)
            store[n] = res
            return res
    return _

@cache
def f(n):
    if n <= 1:
        return 1
    return f(n-1) + f(n-2)

print(f(10))