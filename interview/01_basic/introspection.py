l = [1,2,3]
d = dict(a=1)

print(type(l))
print(type(d))

print(isinstance(l, list))
print(isinstance(d, dict))

def add(a, b):
    if isinstance(a, int):
        return a+b
    elif isinstance(a, str):
        return a.upper() + b

print(add(1, 2))
print(add('monkey', 'king'))

# 返回变量中的内存地址
print(id(l))
print(id(d))

print(l is d)
print(l is l)

# is用来比较是不是同一个对象，而==用来比较对象是否相等
l1 = [1,2,3]
l2 = [1,2,3]
print(l1 == l2)
print(l1 is l2)

