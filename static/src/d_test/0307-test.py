from enum import Enum, unique

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))


@unique
class Weekday(Enum):
    Sun = 0  # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


for member in Month:
    print(member.name, member.value)

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

print(Weekday.Tue)  # Weekday.Tue
print(Weekday['Tue'])  # Weekday.Tue
print(Weekday.Tue.value)  # 2
print(Weekday(1))  # Weekday.Mon


