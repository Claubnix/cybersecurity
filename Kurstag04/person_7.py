import datetime

import custom_lib


p7 = custom_lib.Person("Timon", datetime.datetime(2019, 1, 29))
print(p7.name)
print(p7.get_age())
