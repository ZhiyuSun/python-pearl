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
