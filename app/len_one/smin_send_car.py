import requests
import time
import random
import logger
import threading
from app.Common_max import car_num

sun = error = fail = 0
num = 1


def open_send_car(host, count, camera_list):
    global sun, error, fail, num
    sun = error = fail = 0
    num = 1
    openSendCar = logger.logs('openSendCar')
    for i in range(1, count + 1):
        car = car_num()
        for cl in camera_list:
            try:
                openSendCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, cl, car, str(round((
                        num / (count * len(camera_list)) * 100), 2)) + '%'))
                res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                                    params={'ip': cl, 'platenumber': car}, timeout=3)
                if res.status_code == 200:
                    sun += 1
                else:
                    fail += 1
            except Exception as e:
                print(e)
                error += 1
            time.sleep(6)
            num += 1
    return sun, error, fail


def pay_send_car(host, count, date_time):
    global sun, error, fail, num
    sun = error = fail = 0
    num = 1
    count_list = []
    paySendIntCar = logger.logs('paySendIntCar' + date_time)
    if host == '192.168.11.158':
        inIP = '192.168.11.226'
        outIP = '192.168.11.233'
    elif host == '192.168.11.153':
        inIP = '192.168.111.237'
        outIP = '192.168.111.229'
    else:
        return "未找到配置的网关/摄像机"
    for i in range(count):
        car = car_num()
        count_list.append(car)
        try:
            Num = str(round((num / count * 100), 2))
            paySendIntCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, inIP, car, Num + '%'))
            res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                                params={'ip': inIP, 'platenumber': car}, timeout=300)
            if res.status_code == 200:
                sun += 1
            else:
                fail += 1
        except Exception as e:
            print(e)
            error += 1
        num += 1
        time.sleep(random.randint(6, 12))
    int_list = count_list.copy()
    out_list = []
    num = 1
    paySendOutCar = logger.logs('paySendOutCar' + date_time)
    while len(out_list) != len(int_list):
        index = random.randint(0, len(int_list) - 1)
        cl = int_list[index]
        if cl in out_list:
            continue
        input("当前编号{}当前车牌号:".format(num) + cl)
        try:
            Num = str(round((num / count * 100), 2))
            paySendOutCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, outIP, cl, Num + '%'))
            res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                                params={'ip': outIP, 'platenumber': cl}, timeout=300)
            out_list.append(cl)
            if res.status_code == 200:
                sun += 1
            else:
                fail += 1
        except Exception as e:
            print(e)
            error += 1
        num += 1
        time.sleep(random.randint(6, 12))
    return sun, error, fail


def run(count=1, host='192.168.11.158'):
    a = 1
    while a <= count:
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("当前时间{0}进入第{1}轮测试".format(nowTime, a))
        datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print(pay_send_car(host, 100, date_time=datetime))
        sleep_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("当前休眠开始时间：", sleep_Time)
        if a <= count:
            time.sleep(120)
        a += 1


if __name__ == '__main__':
    Camera_list = ['192.168.11.226', '192.168.11.233']
    result = pay_send_car('192.168.11.158', 5, date_time='2020-11-18')
    print(result)
    # threading_list = []
    # a1 = threading.Thread(target=run, args=(101, '192.168.11.158',))
    # a2 = threading.Thread(target=run, args=(101, '192.168.11.153',))
    # a1.start()
    # a2.start()
    # threading_list.append(a1)
    # threading_list.append(a2)
    # print(a1, a2, '已启动')
