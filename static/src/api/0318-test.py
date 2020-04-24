import random

lis = ['11', '22', '33']
pl = len(lis)
count = 30
card_list = []
try:
    for i in range(0, int(count)):
        r = random.randint(0, pl - 1)
        card_list.append(lis[r])
except Exception as e:
    print(e)
pcl = len(card_list)
print(pcl)
# lis = ['11', '22', '33']
# for i in range(10):
#     r = random.randint(0, len(lis))
#     print(r)
