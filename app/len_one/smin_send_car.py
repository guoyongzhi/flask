import requests
import time
import random
import logger
import threading
import numpy as np
from queue import Queue
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


def open_gae(host, cl, car, openSendCar):
    result = False
    try:
        openSendCar.info('正在调用网关为{0}-摄像头为{1}-车牌为{2}'.format(host, cl, car))
        res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
                            params={'ip': cl, 'platenumber': car}, timeout=3)
        if res.status_code == 200:
            result = True
    except Exception as e:
        print(e)
        result = False
    return result


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
            # time.sleep(10)
            # res = requests.post('http://' + host + ':8019/api/v1/WebCommon/TestPlateResult',
            #                     params={'ip': inIP, 'platenumber': car}, timeout=300)
            # if res.status_code == 200:
            #     sun += 1
            # else:
            #     fail += 1
        except Exception as e:
            print(e)
            error += 1
        num += 1
        time.sleep(random.randint(10, 18))
    int_list = count_list.copy()
    time.sleep(30)
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
        time.sleep(random.randint(10, 18))
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


# 生产消费模型
q = Queue(maxsize=600)
count_list = []
product_is_alive = False


def product(host, cl):  # 生产者(进)
    global count_list, product_is_alive
    count = 1
    product_is_alive = True
    while count < 1000:
        car = car_num()
        d = 0
        while car in count_list:
            car = car_num()
            if d > 20:
                car = None
                break
            d += 1
        if car is None:
            time.sleep(1 * 20)
        res = open_gae(host=host, cl=cl, car=car, openSendCar=logger.logs('product'))
        if res is True:
            count_list.append(car)
            q.put(car)
            # print('生产车牌{}'.format(car))
            count += 1
            time.sleep(random.randint(15, 70))
    product_is_alive = False


def consumer(host, cl):  # 消费者（出）
    # np.random.seed(0)
    global count_list, product_is_alive
    while True:
        if len(count_list) == 0 and product_is_alive is False:
            print("退出")
            break
        if q.empty():
            time.sleep(3)
            continue
        car = q.get(timeout=1)
        time.sleep(random.randint(30, 80))
        if car is None:
            time.sleep(6)
        res = open_gae(host=host, cl=cl, car=car, openSendCar=logger.logs('consumer'))
        if res:
            count_list.remove(car)
            q.task_done()
        else:
            q.put(car)
            print("车牌调用失败失败", car)


def run_product_consumer():
    threading_list = []
    # 部队线程
    p = threading.Thread(target=product, args=('192.168.11.153', '192.168.111.237',))
    s = threading.Thread(target=consumer, args=('192.168.11.153', '192.168.11.228',))
    threading_list.append(p)
    threading_list.append(s)
    p.start()
    time.sleep(5 * 60)
    s.start()
    print("等待结束")
    p.join()
    s.join()
        

if __name__ == '__main__':
    Camera_list = ['192.168.11.226', '192.168.11.233']
    result = pay_send_car('192.168.11.158', 1, date_time='2020-12-11')
    print(result)
    # run_product_consumer()
    # threading_list = []
    # a1 = threading.Thread(target=run, args=(101, '192.168.11.158',))
    # a2 = threading.Thread(target=run, args=(101, '192.168.11.153',))
    # a1.start()
    # a2.start()
    # threading_list.append(a1)
    # threading_list.append(a2)
    # print(a1, a2, '已启动')
