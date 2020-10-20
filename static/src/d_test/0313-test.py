import time

now = time.strftime("%Y-%m-%d %H:%M:%S")
# 获取当前时间
tss1 = '2020-03-12 00:00:00'  # 固定时间，需要固定时间把now改成当前变量

# 转为时间数组
timeArray = time.strptime(now, "%Y-%m-%d %H:%M:%S")

# 转为时间戳
timeStamp = int(time.mktime(timeArray))
print(now)
print(timeStamp)

