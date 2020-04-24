# coding:utf-8
import socketio
from flask import *
import time
import requests as req
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
# from flask_socketio import SocketIO, emit
# from Main import comm_send_msg

apnew = Blueprint('apnew', __name__)


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


@apnew.route('/tt', methods=['GET', 'POST'])
def tt():
    aa = stratr()
    if aa == 'OK':
        return "test"
    else:
        return "ERROR"


@apnew.route('/th', methods=['GET', 'POST'])
def th():
    aa = request.values.get('id')
    create_thread(aa)
    return "11"


# apnew.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(apnew)


@apnew.route('/tth', methods=['GET', 'POST'])
def thh():
    aa = request.values.get('id')
    msg = dict(result=aa)
    date = dict(evenType=2, msg=msg)
    # socketio.emit('response', {'data': date}, namespace='/conn', broadcast=True)
    re = dict(code=200, msg='OK', result='null')
    # comm_send_msg(a=2, b=date)
    # res = req.get(url='http://192.168.11.103:5000/send', params=json.dumps(date))
    # print(res.text)
    return json.dumps(re)


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