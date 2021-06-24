class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            _instance = super().__new__(cls, *args, **kwargs)
            cls._instance = _instance
        return cls._instance


class MyClass(Singleton):
    pass

c1 = MyClass()
c2 = MyClass()
print(c1 is c2) # true


def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class Foo:
    pass
foo1 = Foo()
foo2 = Foo()
print(foo1 is foo2)  # True

#
# class Singleton(type):
#     def __call__(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instance
#
#
# class Foo(metaclass=Singleton):
#     pass
#
# foo1 = Foo()
# foo2 = Foo()
# print(foo1 is foo2)  # True