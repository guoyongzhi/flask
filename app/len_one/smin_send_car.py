import requests
import time
import random
import logger
from app.Common_max import car_num

sun = error = fail = 0
num = 1


def open_send_car(host, count, camera_list):
    global sun, error, fail, num
    openSendCar = logger.logs('openSendCar')
    for i in range(1, count + 1):
        car = car_num()
        for cl in camera_list:
            try:
                openSendCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, cl, car,
                                                        str(round((num / (count * len(camera_list)) * 100), 2)) + '%'))
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


def pay_send_car(host, count):
    global sun, error, fail, num
    count_list = []
    paySendCar = logger.logs('paySendCar')
    for i in range(count):
        car = car_num()
        count_list.append(car)
        try:
            paySendCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, '192.168.11.226', car,
                                                              str(round((num / count * 100), 2)) + '%'))
            res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                                params={'ip': '192.168.11.226', 'platenumber': car}, timeout=3)
            if res.status_code == 200:
                sun += 1
            else:
                fail += 1
        except Exception as e:
            print(e)
            error += 1
        num += 1
        time.sleep(5)
    int_list = count_list.copy()
    out_list = []
    num = 1
    while len(out_list) != len(int_list):
        index = random.randint(0, len(int_list) - 1)
        # print(index, int_list, out_list)
        cl = int_list[index]
        if cl in out_list:
            continue
        input("当前编号{}当前车牌号:".format(num) + cl)
        try:
            print('正在调用网关为{0}-摄像头为{1}-车牌为{2}-当前进度为{3}'.format(host, '192.168.11.233', cl,
                                                              str(round((num / count * 100), 2)) + '%'))
            res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                                params={'ip': '192.168.11.233', 'platenumber': cl}, timeout=3)
            out_list.append(cl)
            if res.status_code == 200:
                sun += 1
            else:
                fail += 1
        except Exception as e:
            print(e)
            error += 1
        num += 1
            
    return sun, error, fail


if __name__ == '__main__':
    Camera_list = ['192.168.11.237', '192.168.11.229']
    result = open_send_car('192.168.11.153', 200, camera_list=Camera_list)
    print(result)
    # pay_send_car('192.168.11.158', 10)
