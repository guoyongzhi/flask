#!/usr/bin/env python3
# coding=utf-8
# Author: yannanxiu

import os
from flask import Flask, render_template, request, current_app
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
from urllib import parse

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


@app.route('/', methods=["GET", "POST"])
def rsa():
    public_key = None
    if "GET" == request.method:
        with open(public_key_file) as file:
            public_key = file.read()
    elif request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("passwd")
        current_app.logger.debug("username:" + username + "\n" + "password:" + password)
        print("username:" + username + "\n" + "password:" + password)

        # decrypt
        username_ret = decrypt_data(username)
        password_ret = decrypt_data(password)
        if username_ret and password_ret:
            current_app.logger.debug(username_ret.decode() + " " + password_ret.decode())
            print(username_ret.decode() + " " + password_ret.decode())
            return 'OK'

    return render_template("rsa_view.html", public_key=public_key)


@app.route('/js_rsa_test', methods=["GET", "POST"])
def js_rsa_test():
    return render_template("js_rsa_test.html")


@app.route('/templates/ase.js')
def get_ase():
    return render_template('ase.js')


@app.route('/templates/crypto-js.js')
def get_js():
    return render_template('crypto-js.js')
if __name__ == '__main__':
    app.debug = True
    app.run()

