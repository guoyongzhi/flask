# import random
#
# lis = ['11', '22', '33']
# pl = len(lis)
# count = 30
# card_list = []
# try:
#     for i in range(0, int(count)):
#         r = random.randint(0, pl - 1)
#         card_list.append(lis[r])
# except Exception as e:
#     print(e)
# pcl = len(card_list)
# print(pcl)
# lis = ['11', '22', '33']
# for i in range(10):
#     r = random.randint(0, len(lis))
#     print(r)
import sys


class aname():
    def __init__(self):
        self.a = 2
        self.b = 3


class bname(aname):
    def __init__(self):
        self.c = 4
        self.d = 5
        super(bname, self).__init__()
        

class name(bname):
    # def __init__(self):
    #     self.c = 1
    #     self.d = 2
        
    def get_class_name(self):
        print(sys._getframe().f_code.co_name)
        return self.__class__.__name__
    
    def get_Num(self):
        print(self.a)
        print(self.b)
        print(self.c)
        print(self.d)
    
    
name = name()
print('' + name.get_class_name())
name.get_Num()
