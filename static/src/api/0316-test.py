import random


red = dict(red1=0, red2=0, red3=0, red4=0, red5=0, red6=0, red7=0, red8=0, red9=0, red10=0, red11=0, red12=0, red13=0,
           red14=0, red15=0, red16=0, red17=0, red18=0, red19=0, red20=0, red21=0, red22=0, red23=0, red24=0, red25=0,
           red26=0, red27=0, red28=0, red29=0, red30=0, red31=0, red32=0, red33=0, red34=0, red35=0)

green = dict(green1=0, green2=0, green3=0, green4=0, green5=0, green6=0, green7=0, green8=0, green9=0, green10=0,
             green11=0, green12=0, green13=0, green14=0, green15=0, green16=0)


def select_green(list_one):
    for lo in list_one:
        for ro in range(1, 17):
            if lo == ro:
                ren = green['green' + str(lo)]
                ren += 1
                green['green' + str(lo)] = ren


def select_red(list_one):
    for ll in list_one:
        for rn in range(1, 36):
            if ll == rn:
                ren = red['red' + str(ll)]
                ren += 1
                red['red' + str(ll)] = ren


def quick_sort(list_1=[], list_2=[]):
    for il in range(len(list_1) - 1):  # 默认从0下标开始
        x = il  # 建立一个信号量
        for j in range(il + 1, len(list_1)):  # 从列表第i+1个元素开始
            if list_1[x] > list_1[j]:  # 一旦匹配到小于下标为i的元素
                x = j
        list_1[il], list_1[x] = list_1[x], list_1[il]  # 将元素赋值给信号量x，依次循环，遇到更小的，继续交换元素
    # if list1 != []:
    if not list_2 == []:
        select_red(list_1)
        select_green(list_2)
    # print(list_1, list_2)


count = int((20200806 - 19960701) / 24)
print(count)
# a1 = a2 = a3 = a4 = a5 = a6 = b = 0
for i in range(count):
    a1 = random.randint(1, 35)
    a2 = random.randint(1, 35)
    while True:
        if a2 == a1:
            a2 = random.randint(1, 35)
        else:
            break
    a3 = random.randint(1, 35)
    while True:
        if a3 == a2 or a3 == a1:
            a3 = random.randint(1, 35)
        else:
            break
    a4 = random.randint(1, 35)
    while True:
        if a4 == a3 or a4 == a2 or a4 == a1:
            a4 = random.randint(1, 35)
        else:
            break
    a5 = random.randint(1, 35)
    while True:
        if a5 == a4 or a5 == a3 or a5 == a2 or a5 == a1:
            a5 = random.randint(1, 35)
        else:
            break
    a6 = random.randint(1, 35)
    while True:
        if a6 == a5 or a6 == a4 or a6 == a3 or a6 == a2 or a6 == a1:
            a6 = random.randint(1, 35)
        else:
            break
    list1 = [a1, a2, a3, a4, a5, a6]
    list2 = [random.randint(1, 16)]
    quick_sort(list1, list2)


# print(red)
# print(green)
red_name_list = list(red)
red_values_list = list(red.values())
bak_red_values_list = red_values_list.copy()
# red_index = bak_red_values_list.index(max(bak_red_values_list))
# print(red_name_list[red_index][3:])
bak_red_values_list.sort(reverse=True)
# print(bak_red_values_list)
new_list = []
for i in range(6):
    new_list.append(bak_red_values_list[i])
# print(new_list)
red_all_list = []
for i in new_list:
    for r in red_values_list:
        if i == r:
            red_all_index = red_values_list.index(i)
            # new_list.remove(i)
            red_all_list.append(int(red_name_list[red_all_index][3:]))
# print(red_all_list)
index = list(green.values()).index(max(list(green.values())))
print(red_all_list, list(green)[index][5:])


# list_red = []
# list_green = []
# for r in red:
#     re = str(round(red[r] * 100 / count, 4)) + '%'
#     list_red.append(red[r])
#     red[r] = re
#
#
# for r in green:
#     re = str(round(green[r] * 100 / count, 4)) + '%'
#     list_green.append(green[r])
#     green[r] = re


# print(red)
# print(green)
# quick_sort(list_red)
# quick_sort(list_green)
# print(list_red)
# print(list_green)

# rer = ''
# for i in range(1, 17):
#     rer += 'green' + str(i) + '=0,'
# print(rer)


def bubble_sort(nums):
    for i in range(len(nums) - 1):
        ex_flag = False  # 改进后的冒泡，设置一个交换标志位
        for j in range(len(nums) - i - 1):
            
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                ex_flag = True
        if not ex_flag:
            return nums  # 这里代表计算机偷懒成功 (〃'▽'〃)
    return nums  # 这里代表计算机没有偷懒成功 o(╥﹏╥)o


import numpy as np


def play_lottery(my_money, play_num, money):
    '''
    随机选择数的中奖率
    result：结果字典
    num：用于统计每个数字出现次数
    my_money：我的余额
    play_num：投注期数
    money：投注额
    flag: 1代表赢钱 0则相反 2表示不输不赢
    
    '''
    flag = 1
    temp = my_money
    result = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    data = np.random.randint(0, 10, (play_num, 1))
    num = np.zeros((10, 1))
    for i in data:
        play = np.random.randint(0, 10, (5, 1))
    if i in play:
        temp = temp + money
    else:
        temp = temp - money
    if result[str(i[0])] == i[0]:
        num[i[0]] = num[i[0]] + 1
    print('我的余额：', temp)
    print('开奖结果统计：\n', num[0][0], num[1][0], num[2][0], num[3][0], num[4][0], num[5][0], num[6][0], num[7][0], num[8][0],
          num[9][0])
    if temp < my_money:
        flag = 0
    elif temp == my_money:
        flag = 2
    return flag


# play_lottery(1000, 100, 10)
