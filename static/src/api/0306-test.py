from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# 遍历Month所有成员
for member in Month:
    print(member.name, member.value)

# 直接使用枚举
print(Month.Jan)  # Month.Jan
print(Month.Jan.name)  # Jan
print(Month.Jan.value)  # 1

# 通过枚举变量名或枚举值来访问指定枚举对象
print(Month['Jan'])  # Month.Jan
print(Month(1))  # Month.Jan

# 遍历Month枚举的所有成员
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

