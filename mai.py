import flask
import time
from flask import request
from app.src.openpyxl_excel import openpyxl_excel

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


@app.route('/', methods=['Get', 'POST'])
def index():
    return "ok"


if __name__ == '__main__':
    app.debug = True
    app.run('192.168.11.103', 9999)

