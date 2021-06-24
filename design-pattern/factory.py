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

a = animal_factory("dog")
a.speak()
