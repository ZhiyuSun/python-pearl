# 元类的等价定义
class Base:
    pass


class Child:
    pass


# 等价定义 注意Base后要加上逗号否则就不是tuple了
SameChild = type('Child', (Base,), {})

# 加上方法
class ChildWithMethod(Base):
    bar = True

    def hello(self):
        print("hello")

def hello(self):
    print("hello")


# 等价定义
SameChildWithMethod = type("ChildWithMethod", (Base,), {"bar": True, "hello": hello})
SameChildWithMethod().hello()

# 自定义元类
# 继承type
class LowercaseMeta(type):
    '''
    修改类的属性名称为小写的元类
    '''

    # __new__ 类的实列的创建，#__init__类的初始化

    # 方法一：
    # def __new__(mcs, name, bases, attrs):
    #     lower_attrs = {}
    #     for k, v in attrs.items():
    #         if not k.startswith('__'):  # 排除魔术方法
    #             lower_attrs[k.lower()] = v
    #         else:
    #             lower_attrs[k] = v
    #     return type.__new__(mcs, name, bases, lower_attrs)

    # 方法二：
    def __new__(cls, *args, **kwargs):
        # 将要替换args
        new_args = []
        for arg in args:
            if isinstance(arg, dict):
                low_attrs = {}
                for k, v in arg.items():
                    if str(k).startswith('__'):
                        low_attrs[k] = v
                    else:
                        low_attrs[str(k).lower()] = v
                new_args.append(low_attrs)
            else:
                new_args.append(arg)
        return type.__new__(cls, *new_args, **kwargs)


# 类
class LowercaseClass(metaclass=LowercaseMeta):
    BAR = True

    def HELLO(self):
        print('hello')


# 此时BAT,HELLO   都变为小写
print(dir(LowercaseClass))
LowercaseClass().hello()
