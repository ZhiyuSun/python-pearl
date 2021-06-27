开设了新专栏[《Python开发》](https://juejin.cn/column/6977390824208203789)，将分享一些我在Python使用上的使用经验。

Python是一门动态语言，设计模式用的不如Java丰富，很多设计模式语言本身已经支持了，比如装饰器模式，迭代器模式。但学习设计模式，以及它在Python中的运用，可以让我们代码变得更加优雅。

设计模式主要分为创建型、结构性和行为型，分这三类进行介绍。

以下所有涉及的代码都存放在我的github该[目录](https://github.com/ZhiyuSun/python-pearl/tree/main/design-pattern)下。

## 创建型

常见创建型设计模式：
- 工厂模式(Factory)：解决对象创建问题
- 构造模式(Builder)：控制复杂对象的创建
- 原型模式(Prototype)：通过原型的克隆创建新的实例
- 单例模式(Singleton)：一个类只能创建同一个对象
- 对象池模式(Pool)：预先分配同一类型的一组实例
- 惰性计算模式(Lazy Evaluation)：延迟计算(python的property)

### 工厂模式

- 解决对象创建问题
- 解耦对象的创建和使用
- 包括工厂方法和抽象工厂

``` python
class Dog:
    def speak(self):
        print("wang wang")

class Cat:
    def speak(self):
        print("miao miao")

def animal_factory(name):
    if name == 'dog':
        return Dog()
    elif name == 'cat':
        return Cat()
```

### 构造模式

- 用于控制复杂对象的构造
- 创建和表示分离。比如你要买电脑，工厂模式直接给你需要的电脑，但是构造模式允许你自己定义电脑的配置，组装完成后给你。

我这里模拟一个王者荣耀创建新英雄的例子。

``` python
class Hero:
    def __init__(self, name):
        self.name = name
        self.blood = None
        self.attack = None
        self.job = None

    def __str__(self):
        info = ("Name {}".format(self.name), "blood: {}".format(self.blood),
                "attack: {}".format(self.attack), "job: {}".format(self.job))
        return '\n'.join(info)


class HeroBuilder:
    def __init__(self):
        self.hero = Hero("Monki")

    def configure_blood(self, amount):
        self.hero.blood = amount

    def configure_attack(self, amount):
        self.hero.attack = amount

    def configure_job(self, job):
        self.hero.job = job

class Game:
    def __init__(self):
        self.builder = None

    def construct_hero(self, blood, attack, job):
        self.builder = HeroBuilder()
        self.builder.configure_blood(blood)
        self.builder.configure_attack(attack),
        self.builder.configure_job(job)

    @property
    def hero(self):
        return self.builder.hero

game = Game()
game.construct_hero(5000, 200, "warrior")
hero = game.hero
print(hero)
```

### 原型模式

- 通过克隆原型来创建新的实例
- 可以使用相同的原型，通过修改部分属性来创建新的示例
- 用途：对于一些创建实例开销比较高的地方可以用原型模式

### 单例模式

- 单例模式：一个类创建出来的对象都是同一个
- ptyhon的模块其实就是单例的，只会导入一次
- 使用共享同一个实例的方法来创建单例模式

``` python
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
```

上面的方法中，New 是真正创建实例对象的方法，所以重写基类的new 方法，以此保证创建对象的时候只生成一个实例。

单例模式是面试中的常考题，除了上面这种实现，还有很多其他方法，再举几例：

使用装饰器

``` python
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
```

使用元类，元类是用于创建类对象的类，类对象创建实例对象时一定要调用call方法，因此在调用call时候保证始终只创建一个实例即可，type是python的元类。

``` python

class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class Foo(metaclass=Singleton):
    pass

foo1 = Foo()
foo2 = Foo()
print(foo1 is foo2)  # True
```

## 结构型

常见结构型设计模式
- 装饰器模式（Decorator）:无需子类化扩展对象功能
- 代理模式（Proxy）:把一个对象的操作代理到另一个对象
- 适配器模式（Adapter）：通过一个间接层适配统一接口
- 外观模式（Facade）:简化复杂对象的访问问题
- 享元模式（Flyweight）:通过对象复用（池）改善资源利用，比如连接池
- Model-View-Controller(MVC)：解耦展示逻辑和业务逻辑

### 装饰器模式

Python语言本身支持装饰器。

- python中一切皆对象，函数也可以当做参数传递
- 装饰器是接受函数作为参数，添加功能后返回一个新函数的函数（类）
- python中通过@使用装饰器，语法糖

例子：编写一个记录函数耗时的装饰器：

``` python
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
```

也可以用类做装饰器

``` python
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
```

还可以给类装饰器加上参数

``` python
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
```

### 代理模式

- 把一个对象的操作代理到另一个对象
- 通常使用has a 组合关系

``` python
from typing import Union


class Subject:
    def do_the_job(self, user: str) -> None:
        raise NotImplementedError()


class RealSubject(Subject):
    def do_the_job(self, user: str) -> None:
        print(f"I am doing the job for {user}")


class Proxy(Subject):
    def __init__(self) -> None:
        self._real_subject = RealSubject()

    def do_the_job(self, user: str) -> None:
        print(f"[log] Doing the job for {user} is requested.")
        if user == "admin":
            self._real_subject.do_the_job(user)
        else:
            print("[log] I can do the job just for `admins`.")


def client(job_doer: Union[RealSubject, Proxy], user: str) -> None:
    job_doer.do_the_job(user)


proxy = Proxy()
real_subject = RealSubject()
client(proxy, 'admin')
client(proxy, 'anonymous')
# [log] Doing the job for admin is requested.
# I am doing the job for admin
# [log] Doing the job for anonymous is requested.
# [log] I can do the job just for `admins`.
client(real_subject, 'admin')
client(real_subject, 'anonymous')
# I am doing the job for admin
# I am doing the job for anonymous
```

### 适配器模式

- 把不同对象的接口适配到同一个接口
- 想象一个多功能充电头，可以给不同的电器充电，充当了适配器
- 当我们需要给不同的对象统一接口的时候可以使用适配器模式

``` python
class Dog:
    def __init__(self):
        self.name = "Dog"

    def bark(self):
        return "woof!"

class Cat:
    def __init__(self):
        self.name = "Cat"

    def meow(self):
        return "meow!"

class Adapter:
    def __init__(self, obj, **adapted_methods):
        """适配器类接收适配器方法"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, item):
        return getattr(self.obj, item)

objects = []
dog = Dog()
objects.append(Adapter(dog, make_noise=dog.bark))
cat = Cat()
objects.append(Adapter(cat, make_noise=cat.meow))
for obj in objects:
    print("a {} goes {}".format(obj.name, obj.make_noise()))

```

## 行为型

常见行为型设计模式：
- 迭代器模式（Iterator）：通过统一的接口迭代对象
- 观察者模式（Observer）：对象发生改变时，观察者执行相应动作
- 策略模式（Strategy）：针对不同规模输入使用不同的策略

### 迭代器模式

- python内置对迭代器模式的支持
- 比如我们可以用for遍历各种Interable的数据类型
- python里可以实现__next__和__iter__实现迭代器

``` python
class NumberWords:
    """Counts by word numbers, up to a maximum of five"""

    _WORD_MAP = (
        "one",
        "two",
        "three",
        "four",
        "five",
    )

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):  # this makes the class an Iterable
        return self

    def __next__(self):  # this makes the class an Iterator
        if self.start > self.stop or self.start > len(self._WORD_MAP):
            raise StopIteration
        current = self.start
        self.start += 1
        return self._WORD_MAP[current - 1]


for number in NumberWords(start=1, stop=2):
    print(number)
```


### 观察者模式

- 发布订阅是一种罪常用的实现方式
- 发布订阅用于解耦逻辑
- 可以通过回调等方式实现，当发生事件时，调用相应的回调函数

``` python
class Publisher: # 发布者
    def __init__(self):
        self.observers = [] # 观察者

    def add(self, observer): # 加入观察者
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print("Failed to add: {}".format(observer))

    def remove(self, observer): # 移除观察者
        try:
            self.observers.remove(observer)
        except ValueError:
            print("Failed to remove: {} ".format(observer))

    def notify(self): # 调用观察者的回调
        [o.notify_by(self) for o in self.observers]

class Formatter(Publisher):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_value):
        self._data = int(new_value)
        self.notify() # data在被合法赋值以后会执行notify

class BinaryFormatter: # 订阅者
    def notify_by(self, publisher):
        print("{}: {} has new bin data={}".format(type(self).__name__, publisher.name, bin(publisher.data)))

df = Formatter('formatter')  # 发布者
bf1 = BinaryFormatter()  # 订阅者
bf2 = BinaryFormatter()  # 订阅者
df.add(bf1) # 添加订阅者
df.add(bf2) # 添加订阅者
df.data = 3 # 设置的时候调用订阅者的notify_by
```

### 策略模式

- 根据不同的输入采取不同的策略
- 比如买东西超过10个打八折，超过20个打7折
- 对外暴露统一的接口，内部采用不同的策略计算

``` python
class Order:
    def __init__(self, price, discount_strategy=None):
        self.price = price
        self.discount_strategy = discount_strategy

    def price_after_discount(self):
        if self.discount_strategy:
            discount = self.discount_strategy(self)
        else:
            discount = 0
        return self.price - discount

    def __repr__(self):
        return "Price: {}, price after discount: {}".format(self.price, self.price_after_discount())

def ten_percent_discount(order):
    return order.price * 0.10


def on_sale_discount(order):
    return order.price * 0.25 + 20


order0 = Order(100)
order1 = Order(100, discount_strategy=ten_percent_discount)
order2 = Order(1000, discount_strategy=on_sale_discount)
print(order0)
print(order1)
print(order2)
```

## 参考资料

https://github.com/faif/python-patterns