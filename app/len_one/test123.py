import time
import random

import requests

# while 1:
result = requests.post('http://192.168.11.103:8019/simulationSendCar',
                       params=dict(IP='192.168.11.158', count=1, Camera_list='192.168.11.226,192.168.11.233'),
                       timeout=500)
# time.sleep(random.randint(30, 45))
print(result.text)


# import sched
# import time
# from datetime import datetime
#
# # 初始化sched模块的scheduler类
# # 第一个参数是一个可以返回时间戳的函数，第二参数可以在定时未到达之前阻塞
# scheduler = sched.scheduler(time.time, time.sleep)
#
#
# # 被周期性调度触发函数
# def printTime(inc):
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     scheduler.enter(inc, 0, printTime, (inc,))
#
#
# # 默认参数60s
# def main(inc=60):
#     # enter四个参数分别为：间隔事件,优先级（用于同时到达两个事件同时执行的顺序），被调度触发的函数
#     # 给该触发器函数的参数（tuple形式）
#     scheduler.enter(0, 0, printTime, (inc,))
#     scheduler.run()
#
#
# if __name__ == '__main__':
#     # 5秒输出一次
#     # main(60)
#     a = 100
#     b = 0
#     c = 0
#     d = 0
#     for i in range(52):
#         if a < 500:
#             a += 10
#         b += a
#         print('第' + str(i + 1) + '周，存' + str(a) + '元')
#         c += a
#         if (i + 1) % 4 == 0:
#             print('第' + str(d + 1) + '月，存' + str(c) + '元')
#             c = 0
#             d += 1
#     print("一年总共：", b)
#     print(b / 12)
#     print(b / 365)
#
#     am = 7000 - 2556.61 - 900 - 250 - 1000 - 200 - 500
#     ay = am * 12
#     ay = ay - 5000 - 500 * 2
#     print(am, ay)
#
#     ad = 52 * 500
#     print(ad)
#
#     yd = 52 * 7
#     ym = yd / 12
#     print(yd, ym)
