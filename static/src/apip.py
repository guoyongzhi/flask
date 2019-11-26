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
