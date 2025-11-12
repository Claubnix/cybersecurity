import datetime

import Kurstag04.Personen.custom_lib as custom_lib


p7 = custom_lib.Person("Timon", datetime.datetime(2019, 1, 29))
print(p7.name)
print(p7.get_age())
