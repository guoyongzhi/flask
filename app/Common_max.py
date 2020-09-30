

# 随机生成一个车牌号码
import random


def car_num():
    char0 = ["京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "苏", "浙", "赣", "鄂", "桂", "甘", "晋", "蒙",
             "陕", "吉", "闽", "赣", "粤", "青", "藏", "川", "宁", "琼"]  # 省份简称
    char1 = """ABCDEFGH"""  # 车牌号中没有I和O
    char2 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    
    id_1 = random.choice(char0)  # 车牌号第一位     省份简称
    id_2 = ''.join(random.sample(char1, 1))  # 车牌号第二位
    cc = 0
    car_id = ''
    while cc < 10:
        cc += 1
        id_3 = ''.join(random.sample(char2, 5))
        v = id_3.isalpha()  # 所有字符都是字母时返回 true
        if v is True:
            continue
        else:
            car_id = id_1 + id_2 + id_3
            break
    return car_id


# print(car_num())
