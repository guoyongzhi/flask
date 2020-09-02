import json
import os

import flask
import time
from flask import *
import requests
from werkzeug.utils import secure_filename

from app.src.openpyxl_excel import openpyxl_excel
from app.src.common_method import CommonMethod
from setting import APP_ROOT
from bs4 import BeautifulSoup

app = flask.Flask(__name__)


@app.route('/getexcel', methods=['Get', 'POST'])
def get_execl():
    try:
        re = request.values.get('u')  # 标题
        s = re.split(',')
        rs = request.values.get('s')  # 首行数据
        rns = rs.split(',')
        rp = request.values.get('p')  # 循环次数/多条数据
        rn = request.values.get('n')  # 递归数据
        rn = rn.split(',')
    except Exception as e:
        print(e)
        help = 'u:参数标题\n s:首行数据\n p:数据总数\n n:递归参数\n'
        return "参数错误，请检查参数：\n" + help
    fot_i = []
    date = dict()
    date[str(1)] = s
    for i in rn:
        weizhi = 0
        for nn in s:
            if nn == i:
                fot_i.append(weizhi)
            weizhi += 1
    for i in range(1, int(rp) + 1):
        for n in fot_i:
            rns[n] = str(int(rns[n]) + 1)
        date[str(i + 1)] = rns.copy()
    now = int(time.time())
    filename = "I:\\文档\\t\\{}.xlsx".format(str(now))
    res = openpyxl_excel.write_new_file_excel(filename, datadict=date)
    if res != 'OK':
        return "处理Excel错误"
    return flask.send_file(filename, attachment_filename='name.xlsx')
    # return 'OK'


@app.route('/testtest', methods=['Get', 'POST'])
def test_test():
    """
    请求参数
    注：多参数date和headers请使用字典
    :return:
    :rtype:
    """
    date_dict = CommonMethod(request.values).common_all('hostPort', 'urlAddr', 'date', 'headers', 'dateType',
                                                        'methodsType')
    print(date_dict)
    # res = 'error'
    try:
        if 'date' in date_dict['dateType']:
            if 'post' in date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], data=json.loads(date_dict['date']),
                                    headers=json.loads(date_dict['headers']), timeout=3).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], data=json.loads(date_dict['date']),
                                   headers=json.loads(date_dict['headers']), timeout=3).text
        elif 'json' in date_dict['dateType']:
            if 'post' in date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], json=json.loads(date_dict['date']),
                                    headers=json.loads(date_dict['headers'])).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], json=json.loads(date_dict['date']),
                                   headers=json.loads(date_dict['headers']), timeout=3).text
        elif 'params' in date_dict['dateType']:
            if 'post' in date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], params=json.loads(date_dict['date']),
                                    headers=json.loads(date_dict['headers']), timeout=3).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], params=json.loads(date_dict['date']),
                                   headers=json.loads(date_dict['headers']), timeout=3).text
        else:
            res = '未找到对应的请求参数类型'
    except Exception as e:
        res = e
    return res


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                if not filename[-3:] in 'jpgJPGpngPNGmp3mp4warcsvxlsxlsx':
                    return jsonify({'msg': '文件格式不对', 'msg_code': "000011"})
                file.save(os.path.join(APP_ROOT, 'static/uploads', filename))
                return redirect(url_for('upload'))
            else:
                return json_available({'msg_code': "000002", 'msg': "请求参数为空"})
        except Exception as e:
            # api_x.error(e)
            return json.dumps({'msg': '操作失败请联系管理员', 'msg_code': '000010'})
    return render_template('upload.html')


@app.route('/', methods=['Get', 'POST'])
def index():
    return "ok"


if __name__ == '__main__':
    app.debug = True
    app.run('192.168.11.103', 9999)

