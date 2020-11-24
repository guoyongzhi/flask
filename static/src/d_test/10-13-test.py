import numpy as np
import random


class a(object):
    def __init__(self, an=1, b=2):
        self.a = an
        self.b = b
        

class bb(a):
    def __init__(self, an=1, b=2):
        super(bb, self).__init__(an, b)
    
    @property
    def x(self):
        print(111)
        return 124


# print(bb(1, 2).x)
# print(len('@ '.replace(' ', '')))
# a = 0
# Num = 3800
# if Num / 100 <= 10:
#     print(Num / 100, 100)
#     count = Num / 100
# elif Num / 1000 <= 10:
#     print(Num / 1000, 1000)
#     count = Num / 1000
# elif Num / 10000 <= 10:
#     print(Num / 10000, 10000)
#     count = Num / 10000
# print(type(count))
# if not isinstance(count, int):
#     count += 1
# print(count)
# sum_dict = dict(a1=0, a2=0, a3=0, a4=0, a5=0)
# double_p = np.array([0.30, 0.30, 0.20, 0.12, 0.08])
# double = np.random.choice([1, 2, 3, 4, 5], p=double_p.ravel())
# if double == 1:
#     stat = 1
#     end = double * 1000
# elif double == 5:
#     stat = (double - 1) * 1000
#     end = Num
# else:
#     stat = double * 1000
#     end = (double + 1) * 1000
# print(random.randint(stat, end))
# print(double, stat, end)


# while a < 10:
    # d_list = ['零', '一', '双', '三', '四', '五']
    # print(d_list[double])
    # sum_dict['a' + str(double)] += 1
    # a += 1
# print(sum_dict)


import time

spam_dict = dict()
talk = '等等'
qname = '123'
while True:
    talk = input("请输入内容")
    if talk:
        if talk == '退出':
            break
        if qname not in spam_dict:
            spam_dict[qname] = round(time.time(), 3), talk, 0
        else:
            last_time, last_talk, count = spam_dict[qname]
            now_time = round(time.time(), 3)
            if float(now_time - last_time) < 3 and last_talk == talk:
                count += 1
                if count in [3, 10, 30]:
                    print("别刷屏")
            else:
                count = 0
            spam_dict[qname] = now_time, talk, count
        
print(spam_dict)


# 2866 2920.61