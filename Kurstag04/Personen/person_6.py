import datetime


class Person:
    def __init__(self, name="Chrigu", birthdate=datetime.datetime(1991, 3, 13)):
        self.name = name
        self.birthdate = birthdate

    def get_age(self):
        return datetime.datetime.now().year - self.birthdate.year


p6 = Person("Timon", datetime.datetime(2019, 1, 29))
print(p6.name)
print(p6.get_age())
