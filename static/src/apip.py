# coding:utf-8
from flask import *
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def gg_th(id=5):
    while True:
        print("线程正在启动" + str(id))
        time.sleep(int(id))


def stratr():
    tb = Thread(target=gg_th, args=(1,))
    tb.start()
    return "OK"


def create_thread(aa):
    pool = ThreadPoolExecutor(5)
    return pool


def ap_new(app):
    @app.route('/tt', methods=['GET', 'POST'])
    def tt():
        aa = stratr()
        if aa == 'OK':
            return "test"
        else:
            return "ERROR"
    
    @app.route('/th', methods=['GET', 'POST'])
    def th():
        aa = request.values.get('id')
        create_thread(aa)
        return "11"


executor = ThreadPoolExecutor(2)


def ss():
    for i in range(10):
        time.sleep(5)
        print(i)
    return 'OK'


def show():
    executor.submit(ss)
    time.sleep(1)
    print("程序已启动")


# def show():
#     print(list(show_str()))
#     print('*****')


if __name__ == '__main__':
    show()
    print('main')
