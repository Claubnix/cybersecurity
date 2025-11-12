from datetime import date


class Person:
    def __init__(self, name="Chrigu", birthdate=date(1991, 3, 13)):
        self.name = name
        self.birthdate = birthdate

    def get_age(self):
        return date.today().year - self.birthdate.year


p8 = Person("Timon", date(2019, 1, 29))
print(p8.name)
print(p8.get_age())
