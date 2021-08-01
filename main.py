#!/usr/bin/env python3
# coding=utf-8

import os
from flask import *
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
from static.src.apip import *
import base64
from urllib import parse
from axf.dbmysql import my_db
# from flask_cache import Cache
from flask_caching import Cache
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from werkzeug.contrib.cache import MemcachedCache
# from extensions import cache
# from setting import Config

# app.config.from_object(Config)
# from flask_socketio import SocketIO, emit
from threading import Lock
import random

async_mode = None

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))
private_key_file = os.path.join(curr_dir, "my_private_rsa_key.bin")
public_key_file = os.path.join(curr_dir, "my_rsa_public.pem")

app = Flask(__name__)
cache = Cache()
# cache.config = 'simple'
# ap_new(app)
app.register_blueprint(apnew)
cache.init_app(app=app, config={"CACHE_TYPE": "simple"})


def decrypt_data(inputdata, code="123456"):
    # URLDecode
    data = parse.unquote(inputdata)
    
    # base64decode
    data = base64.b64decode(data)
    
    private_key = RSA.import_key(open(curr_dir + "/my_private_rsa_key.bin").read(), passphrase=code)
    # 使用 PKCS1_v1_5，不要用 PKCS1_OAEP
    # 使用 PKCS1_OAEP 的话，前端 jsencrypt.js 加密的数据解密不了
    cipher_rsa = PKCS1_v1_5.new(private_key)
    
    # 当解密失败，会返回 sentinel
    sentinel = None
    ret = cipher_rsa.decrypt(data, sentinel)
    
    return ret


@app.before_request
def before_action():
    a = request.path
    # if request.path.find('.ico')==-1:
    u = a.split('/')
    if len(u) >= 3:
        uu = request.path.split('/')
        if uu[2] == 'admin':
            if not 'username' in session:
                session['newurl'] = request.path
                return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    date_dict = request.values.to_dict()
    print(date_dict.keys(), date_dict.items(), date_dict.values(), len(date_dict))
    # c = CombinedMultiDict(['GET', 'POST'])
    # print(c['username'])
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            session['username'] = request.form['username']
            if 'newurl' in session:
                newurl = session['newurl']
                session.pop('newurl', None)
                return redirect(newurl)
            else:
                return redirect('/home')
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/test')
@cache.memoize(timeout=10, )
def test():
    print("是否走缓存了！")
    IP = request.values.ip
    # cache = MemcachedCache(['127.0.0.1:5000'])
    return 'test' + IP


# cached_test = test()


@app.route('/biaoge')
def biaoge():
    return render_template('biaoge.html')


@app.route('/passport', methods=['GET', 'POST'])
def get_user():
    id = request.values.get('user_id')
    if id:
        sql = 'select id,show_name,default_name,phone_number,sex from passport_20180612 where id=%d' % int(id)
    else:
        sql = 'select id,show_name,default_name,phone_number,sex from passport_20180612'
    res = my_db(sql, 'passport')
    list = []
    for i in res:
        lis = dict(id=i[0], name=i[1], default_name=i[2], phone_number=i[3], sex=i[4])
        list.append(lis)
    re = dict(msg='请求成功', code=200, data=list, tot=len(res), sEcho=1, iTotalRecords=1, iTotalDisplayRecords=1)
    return json.dumps(re, ensure_ascii=False)


@app.route('/test-conn')
def get_test_conn():
    return render_template('testconn.html')


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
# thread = None
# thread_lock = Lock()
#
#
# @socketio.on('connect', namespace='/conn')
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(target=background_thread)
#
#
# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message)
#
#
# def background_thread():
#     while True:
#         socketio.sleep(10)  # 心跳五秒一次
#         # t = random.randint(1, 100)
#         date = dict(evenType=0, msg={"result": 'null'})
#         print(date)
#         socketio.emit('response', {'data': date}, namespace='/conn')
#
#
# @app.route('/send')
# def send_msg():
#     evenType = request.values.get('evenType')
#     msg = request.values.get('msg')
#     date = dict(evenType=evenType, msg={"result": msg})
#     socketio.emit('response', {'data': date}, namespace='/conn', broadcast=True)
#     re = dict(code=200, msg='OK', result='null')
#     return json.dumps(re, ensure_ascii=False)
#
#
# def comm_send_msg(a=0, b=None):
#     date = dict(evenType=a, msg={"result": b})
#     socketio.emit('response', {'data': date}, namespace='/conn', broadcast=True)
#     return 'OK'


if __name__ == '__main__':
    app.debug = True
    app.threaded = True
    app.run(host='192.168.1.100', port=80)  
    # socketio.run(app, host='192.168.11.103', port=5000, debug=True)