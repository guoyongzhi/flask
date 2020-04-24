

import random
a1 = random.randint(85, 99)
print(a1, type(a1))  # 产生 1 到 10 的一个整数型随机数
a2 = random.random()
print(a2, type(a2), float('%.1f' % a2), round(a2, 1))  # 产生 0 到 1 之间的随机浮点数
a3 = random.uniform(1.1, 5.4)
print(a3, type(a3))  # 产生  1.1 到 5.4 之间的随机浮点数，区间可以不是整数
a4 = random.choice('tomorrow')
print(a4, type(a4))  # 从序列中随机选取一个元素
a5 = random.randrange(1, 100, 2)
print(a5, type(a5))  # 生成从1到100的间隔为2的随机整数
a6 = random.sample([1, 3, 5, 6, 7], 3)
print(a6, type(a6))  # 从list中随机获取3个元素，作为一个片断返回

list = [1, 3, 5, 6, 7]  # 将序列中的元素顺序打乱
random.shuffle(list)

print(list)

a = float(1+0.1)
print(a)

print(random.randint(0, 10))
