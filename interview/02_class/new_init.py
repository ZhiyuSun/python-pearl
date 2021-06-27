class Person:
    def __new__(cls, *args, **kwargs):
        print("in __new__")
        instance = super().__new__(cls)
        # return instance

    def __init__(self, name, age):
        print("in __init__")
        self._name = name
        self._age = age

p = Person("zhiyu", 26)
print("p:", p)
