class Duck:
    def say(self):
        print("嘎嘎")


class Dog:
    def say(self):
        print("汪汪")


def speak(duck):
    duck.say()


duck = Duck()
dog = Dog()
speak(duck)
speak(dog)
print(type(duck))
print(type(dog))
print(isinstance(duck, Duck))
print(isinstance(dog, Dog))