#!/usr/bin/Python-3.6.2
from flask import Blueprint, render_template

axf = Blueprint('axf', __name__)


@axf.route('/')
def index():
    return "index"


@axf.route('/regist/')
def regist():
    #注册
    return render_template('regist.html')


@axf.route('/logon/')
def login():
    #登录
    return render_template('login.html')

