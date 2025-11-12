class Person:
    name = "Chrigu"
    age = 34

    def __init__(self, name, age):
        self.name = name
        self.age = age


# p2 = Person() --> funktioniert nicht!
p2 = Person("Timon", 6)
print(p2.name)
print(p2.age)
