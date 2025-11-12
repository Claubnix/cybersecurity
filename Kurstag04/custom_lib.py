import datetime


class Person:
    def __init__(self, name="Chrigu", birthdate=datetime.datetime(1991, 3, 13)):
        self.name = name
        self.birthdate = birthdate

    def get_age(self):
        return datetime.datetime.now().year - self.birthdate.year
