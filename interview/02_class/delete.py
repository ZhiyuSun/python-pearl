import time
class People:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __del__(self): # 在对象被删除的条件下，自动执行
        print('__del__')

obj = People("zhiyu", 26)
# del obj
time.sleep(5)