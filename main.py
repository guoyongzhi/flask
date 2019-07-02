#!/usr/bin/env python3
# coding=utf-8
# Author: yannanxiu

import os
from flask import *
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
from urllib import parse
from axf.dbmysql import my_db

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))
private_key_file = os.path.join(curr_dir, "my_private_rsa_key.bin")
public_key_file = os.path.join(curr_dir, "my_rsa_public.pem")

app = Flask(__name__)


def decrypt_data(inputdata, code="123456"):
    # URLDecode
    data = parse.unquote(inputdata)

    # base64decode
    data = base64.b64decode(data)

    private_key = RSA.import_key(
        open(curr_dir + "/my_private_rsa_key.bin").read(),
        passphrase=code
    )
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
def test():
    return 'test'


@app.route('/biaoge')
def biaoge():
    return render_template('biaoge.html')


@app.route('/passport', methods=['GET', 'POST'])
def get_user():
    id = request.values.get('user_id')
    if id:
        sql = 'select id,show_name from passport_20180612 where id=%d' % int(id)
    else:
        sql = 'select id,show_name from passport_20180612'
    res = my_db(sql, 'passport')
    list = []
    for i in res:
        lis = dict(id=i[0], name=i[1])
        list.append(lis)
    re = dict(msg='请求成功', code=200, data=list, tot=len(res), sEcho=1, iTotalRecords=1, iTotalDisplayRecords=1)
    return json.dumps(re, ensure_ascii=False)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# @app.route('/', methods=["GET", "POST"])
# def rsa():
#     public_key = None
#     if "GET" == request.method:
#         with open(public_key_file) as file:
#             public_key = file.read()
#     elif request.method == "POST":
#         username = request.values.get("username")
#         password = request.values.get("passwd")
#         current_app.logger.debug("username:" + username + "\n" + "password:" + password)
#         print("username:" + username + "\n" + "password:" + password)
#
#         # decrypt
#         username_ret = decrypt_data(username)
#         password_ret = decrypt_data(password)
#         if username_ret and password_ret:
#             current_app.logger.debug(username_ret.decode() + " " + password_ret.decode())
#             print(username_ret.decode() + " " + password_ret.decode())
#             return 'OK'
#
#     return render_template("rsa_view.html", public_key=public_key)
#
#
# @app.route('/js_rsa_test', methods=["GET", "POST"])
# def js_rsa_test():
#     return render_template("js_rsa_test.html")
#
#
# @app.route('/ase.js')
# def get_ase():
#     return render_template('ase.js')
#
#
# @app.route('/tot')
# def tot():
#     return render_template('tot.html')
#
#
# @app.route('/templates/crypto-js.js')
# def get_js():
#     return render_template('crypto-js.js')
if __name__ == '__main__':
    app.debug = True
    app.run()

