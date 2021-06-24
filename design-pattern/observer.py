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