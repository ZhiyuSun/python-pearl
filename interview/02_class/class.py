class Person:
    Country = 'china'
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_name(self):
        print(self.name)

    @classmethod
    def print_country(cls):
        print(cls.Country)

    @staticmethod
    def join_name(first_name, last_name):
        return print(last_name + first_name)

a = Person("Bruce", "Lee")
a.print_country()
a.print_name()
a.join_name("Bruce", "Lee")
Person.print_country()
Person.print_name(a)
Person.join_name("Bruce", "Lee")
