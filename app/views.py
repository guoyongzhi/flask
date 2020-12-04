import base64
import hashlib
import json
import os
import struct
# import threading
# import logger
import flask
# import time
# import requests

from flask import *
from werkzeug.utils import secure_filename
from app.src.openpyxl_excel import openpyxl_excel
from app.src.common_method import Parameter
from setting import APP_ROOT
# from app.src import openpyxl_excel
from app import app
from flask import request, render_template, make_response, send_from_directory, jsonify, json_available, url_for
# from app.Common_max import car_num

# from flask.views import MethodView
# from flask_login import login_required, current_user
from app.src import openpyxl_excel
from app.len_one.smin_send_car import *


@app.route('/getExcel', methods=['Get', 'POST'])
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
        return "参数错误，请检查参数：\n" + 'u:参数标题\n s:首行数据\n p:数据总数\n n:递归参数\n'
    fot_i = []
    date = dict()
    date[str(1)] = s
    for n in rn:
        way = 0
        for nn in s:
            if nn == n:
                fot_i.append(way)
            way += 1
    for p in range(1, int(rp) + 1):
        for n in fot_i:
            rns[n] = str(int(rns[n]) + 1)
        date[str(p + 1)] = rns.copy()
    now = int(time.time())
    filename = "I:\\文档\\t\\{}.xlsx".format(str(now))
    res = openpyxl_excel.write_new_file_excel(filename, datadict=date)
    if res != 'OK':
        return "处理Excel错误"
    return flask.send_file(filename, attachment_filename='name.xlsx')  # return 'OK'


@app.route('/testTest', methods=['GET', 'POST'])
def test_test():
    """
    请求参数
    注：多参数date和headers请使用字典
    :return:
    :rtype:
    """
    try:
        User_headers = {'User-Agent': 'Mozilla/5.0'}
        date_dict = request.get_json()
        if date_dict:
            Data = date_dict['date']
            try:
                headers = dict(User_headers, **json.loads(date_dict['headers']))
            except Exception:
                headers = dict(User_headers, **date_dict['headers'])
        else:
            date_dict = Parameter(temp=request.values).common_all('hostPort', 'urlAddr', 'date', 'headers', 'dateType',
                                                                'methodsType')
            Data = json.loads(date_dict['date'])
            try:
                headers = dict(User_headers, **json.loads(date_dict['headers']))
            except Exception:
                headers = dict(User_headers, **date_dict['headers'])
        if not date_dict:
            return "请求无参数或参数不正确"  # print(date_dict, type(date_dict))
    except Exception as e:
        print(e)
        return "请求错误"
    try:
        if 'date' == date_dict['dateType']:
            if 'post' == date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], data=Data, headers=headers,
                                    timeout=3).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], data=Data, headers=headers,
                                   timeout=3).text
        elif 'json' == date_dict['dateType']:
            if 'post' == date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], json=Data, headers=headers).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], json=Data, headers=headers,
                                   timeout=3).text
        elif 'params' == date_dict['dateType']:
            if 'post' == date_dict['methodsType']:
                res = requests.post(date_dict['hostPort'] + date_dict['urlAddr'], params=Data, headers=headers,
                                    timeout=3).text
            else:
                res = requests.get(date_dict['hostPort'] + date_dict['urlAddr'], params=Data, headers=headers,
                                   timeout=3).text
        else:
            res = '未找到对应的请求参数类型'
    except Exception as e:
        print(e)
        res = "请求错误"
    if '\\' in res:
        res = res.replace('\\', '')
    if type(res) is str:
        res = json.loads(res)
    return jsonify(res)


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


@app.route('/Parking/GetInstructCache', methods=['GET', 'POST'])
def get_instruct_cache():
    # print(request.values)
    print(request.get_json())
    # date_dict = Parameter(temp=request.values).common_all('sn', 'index', 'pageSize')
    # print(date_dict)
    result = dict(ID=1, Instruction=1, InstructData="")
    res = {'msg': "1", "result": [result], "code": 1}
    # print(res)
    return jsonify(res)


@app.route('/Parking/GetPermissionList', methods=['GET', 'POST'])
def get_permission_list():
    # print(request.values)
    print(request.get_json())
    # date_dict = Parameter(temp=request.values).common_all('camaraId', 'indx', 'size')
    # print(date_dict)
    result = dict(ip="192.168.11.237", port=8131, plateNumber="粤A6R875", plateState=1, carType="小型车",
                  stat="2020-09-01 00:00:00", end="2080-01-01 00:00:00", matchLevel=1, state=0, _state=1,
                  permissionGroupID=1, userID=1001, isUpdate=False)
    res = {'msg': "1", "result": [result], "code": 1}
    # print(res)
    return jsonify(res)


@app.route('/Parking/GetAddPermissionList', methods=['GET', 'POST'])
def get_add_permission_list():
    date_dict = Parameter(temp=request.values).common_all('carNums')
    print(date_dict)
    result = dict(ip="192.168.11.237", port=8131, plateNumber="粤A6R875", plateState=1, carType="小型车",
                  stat="2020-09-01 00:00:00", end="2080-01-01 00:00:00", matchLevel=1, state=0, _state=1,
                  permissionGroupID=1, userID=1001, isUpdate=False)
    res = {'msg': "1", "result": [result], "code": 1}
    # print(res)
    return jsonify(res)


@app.route('/ThumbReceive.ashx', methods=['GET', 'POST'])
def thumb_receive():
    if request.method == 'POST':
        try:
            file = request.files['file']
            # print(request.get_json())
            date_dict = Parameter(temp=request.values).common_all('Path', "CarNum", "IsReal")
            print(date_dict)
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                if not filename[-3:] in 'jpgJPGpngPNGmp3mp4warcsvxlsxlsx':
                    return jsonify({'msg': '文件格式不对', 'msg_code': "000011"})
                file.save(os.path.join(APP_ROOT, 'static/uploads', filename))
                res = True
                return jsonify(res)
            else:
                return json_available({'msg_code': "000002", 'msg': "请求参数为空"})
        except Exception as e:
            mai_log = logger.logs()
            mai_log.error(e)
            return json.dumps({'msg': '操作失败请联系管理员', 'msg_code': '000010'})
    return render_template('upload.html')


@app.route('/<int:ID>', methods=['Get', 'POST'])
def index(ID):
    return "ok" + str(ID)


@app.route('/', methods=['Get', 'POST'])
def hello():
    return "hello world!"


@app.route('/send/car', methods=['get', 'post'])
def send_car():
    try:
        date_dict = request.get_json()
        if not date_dict:
            date_dict = Parameter(temp=request.values).common_all('count')
    except Exception:
        return jsonify("参数错误或缺失")
    car_list = []
    if not Parameter.common_check_required(date_dict, 'count'):
        return jsonify("参数错误或缺失")
    for car in range(0, int(date_dict['count'])):
        car_list.append(car_num())
    return jsonify(car_list)


@app.route('/send/send_car', methods=['get', 'post'])
def send_send_car():
    try:
        date_dict = request.get_json()
        if not date_dict:
            date_dict = Parameter(temp=request.values).common_all('host', 'ip', 'car')
    except Exception:
        return jsonify("参数错误或缺失")
    car_list = []
    if not Parameter.common_check_required(date_dict, 'host', 'ip', 'car'):
        return jsonify("参数错误或缺失")
    sun = fail = error = 0
    car_nums = date_dict['car']
    re = car_nums.split(',')
    if len(re) == 1:
        res = car_nums.split('，')
        if len(res) > 1:
            re = res
    for c in re:
        if '\n' in c:
            c = c.replace('\n', '')
        if ' ' in c:
            c = c.replace(' ', '')
        if '"' in c:
            c = c.replace('"', '')
        try:
            res = requests.post('http://' + date_dict['host'] + ':8019/api/v1/WebCommon/TestPlateResult',
                                params={'ip': date_dict['ip'], 'platenumber': c}, timeout=3)
            if res.status_code == 200:
                sun += 1
                car_list.append(c)
            else:
                fail += 1
            if len(re) != 1:
                time.sleep(3)
        except Exception as e:
            print(e)
            error += 1
    result_dict = dict(msg=sun, fail=fail, error=error, sun_list=car_list)
    return jsonify(result_dict)


connection_list = {}  # 存放链接客户fd,元组
i = 0
g_code_length = 0
g_header_length = 0  # websocket数据头部长度
PRINT_FLAG = False
return_time = "2020-09-09 00:00:00"
lock = threading.RLock()
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
buffer = ""
buffer_utf8 = b""
length_buffer = 0
"""
经测试发现IE 11浏览器在成功建立websocket连接后，会间隔30s发送空信息给服务器以验证是否处于连接状态，
因此服务区需要对收到的数据进行解码并判断其中载荷内容是否为空，如为空，应不进行广播
"""


# 计算web端提交的数据长度并返回
def get_data_length(message):
    global g_code_length
    global g_header_length
    try:
        g_code_length = message[1] & 127
        if g_code_length == 126:
            g_code_length = struct.unpack('>H', message[2:4])[0]
            g_header_length = 8
        elif g_code_length == 127:
            g_code_length = struct.unpack('>Q', message[2:10])[0]
            g_header_length = 14
        else:
            g_header_length = 6
        g_code_length = int(g_code_length)
    except Exception:
        g_code_length = 0
    return g_code_length


# 解析web端提交的bytes信息，返回str信息（可以解析中文信息）
def parse_data(message):
    """
    :param message: 需要解析的入参消息
    :type message: bytes
    :return: 返回str信息（可以解析中文信息） 失败为空
    :rtype: str
    """
    global g_code_length
    try:
        g_code_length = message[1] & 127
        if g_code_length == 126:
            g_code_length = struct.unpack('>H', message[2:4])[0]
            masks = message[4:8]
            data = message[8:]
        elif g_code_length == 127:
            g_code_length = struct.unpack('>Q', message[2:10])[0]
            masks = message[10:14]
            data = message[14:]
        else:
            masks = message[2:6]
            data = message[6:]
        en_bytes = b""
        cn_bytes = []
        for ai, d in enumerate(data):
            nv = chr(d ^ masks[ai % 4])
            nv_bytes = nv.encode()
            nv_len = len(nv_bytes)
            if nv_len == 1:
                en_bytes += nv_bytes
            else:
                en_bytes += b'%s'
                cn_bytes.append(ord(nv_bytes.decode()))
        if len(cn_bytes) > 2:
            cn_str = ""
            cl_b = len(cn_bytes)
            count = int(cl_b / 3)
            for x in range(count):
                ii = x * 3
                b = bytes([cn_bytes[ii], cn_bytes[ii + 1], cn_bytes[ii + 2]])
                # try:
                cn_str += b.decode()  # except Exception as e:  #     print(e)
            new = en_bytes.replace(b'%s%s%s', b'%s')
            new = new.decode()
            res = (new % tuple(list(cn_str)))
        else:
            res = en_bytes.decode()
    except Exception as e:
        # print("解析消息出错：", message, e)
        # if not res:
        res = ""
    return res


# 调用socket的send方法发送str信息给web端
def sendMessage(message):
    """
    :param message: 消息内容
    :type message: str
    :return: error
    :rtype: None
    """
    global connection_list
    global lock
    result = "OK"
    lock.acquire()
    try:
        send_msg = b""  # 使用bytes格式,避免后面拼接的时候出现异常
        send_msg += b"\x81"
        back_str = []
        back_str.append('\x81')
        data_length = len(message.encode())  # 可能有中文内容传入，因此计算长度的时候需要转为bytes信息
        if PRINT_FLAG:
            print("INFO: send message is %s and len is %d" % (message, len(message.encode('utf-8'))))
        # 数据长度的三种情况
        if data_length <= 125:  # 当消息内容长度小于等于125时，数据帧的第二个字节0xxxxxxx 低7位直接标示消息内容的长度
            send_msg += str.encode(chr(data_length))
        elif data_length <= 65535:  # 当消息内容长度需要两个字节来表示时,此字节低7位取值为126,由后两个字节标示信息内容的长度
            send_msg += struct.pack('b', 126)
            send_msg += struct.pack('>h', data_length)
        elif data_length <= (2 ^ 64 - 1):  # 当消息内容长度需要把个字节来表示时,此字节低7位取值为127,由后8个字节标示信息内容的长度
            send_msg += struct.pack('b', 127)
            send_msg += struct.pack('>q', data_length)
        else:
            print(u'太长了')
        send_message = send_msg + message.encode('utf-8')
        del_list = []
        if connection_list:
            try:
                for connection in connection_list.values():
                    if send_message is not None and len(send_message) > 0:
                        try:
                            connection.send(send_message)
                        except Exception as e:
                            if 'Socket is dead' in str(e):
                                print("找不到连接：准备删除", connection)
                                del_list.append([k for k, v in connection_list.items() if v == connection][0])
            except Exception as e:
                print("严重错误", e)
        if del_list:
            for dl in del_list:
                print("找不到连接：正在删除", dl)
                del connection_list[dl]
    finally:
        # print("释放锁")
        lock.release()
        result = "error"
    return result


def send_receive_message(message):  # 直接回复
    global connection_list
    global lock
    lock.acquire()
    try:
        del_list = []
        if connection_list:
            try:
                for connection in connection_list.values():
                    if message is not None and len(message) > 0:
                        try:
                            connection.send(message)
                        except Exception as e:
                            if 'Socket is dead' in str(e):
                                print("找不到连接：准备删除", connection)
                                del_list.append([k for k, v in connection_list.items() if v == connection][0])
            except Exception as e:
                print("严重错误", e)
        if del_list:
            for dl in del_list:
                print("找不到连接：正在删除", dl)
                del connection_list[dl]
    finally:
        # print("释放锁")
        lock.release()


# 删除连接,从集合中删除连接对象item
def delete_connection(item):
    global connection_list
    print("删除", item)
    del connection_list['connection' + item]


def generate_token(WebSocketKey):
    WebSocketKey = WebSocketKey + GUID
    Ser_WebSocketKey = hashlib.sha1(WebSocketKey.encode(encoding='utf-8')).digest()
    WebSocketToken = base64.b64encode(Ser_WebSocketKey)  # 返回的是一个bytes对象
    return WebSocketToken.decode('utf-8')


@app.route('/ws')
def echo_websocket():
    global i, connection_list, GUID, buffer, buffer_utf8, length_buffer
    global g_code_length
    global g_header_length
    global return_time
    if request.environ.get('wsgi.websocket'):
        user_socket = request.environ['wsgi.websocket']
        if user_socket is None:
            os.abort(404)
        print(request.headers)
        connection_list['connection' + str(i)] = user_socket
        print("新连接", user_socket, 'connection' + str(i))
        while True:
            try:
                if user_socket.closed:
                    break
                mm = b''
                receive_message = ''
                # 每次接收1024字节数据，需要判断是否接收完所有数据，如没有接收完，需要循环接收完再处理
                try:
                    mm = user_socket.receive()
                    if not mm:
                        delete_connection(i)
                        break
                except Exception as e:
                    if 'Socket is dead' in str(e):
                        delete_connection(str(i))
                        user_socket.closed()
                        break
                # 计算接受的长度，判断是否接收完，如未接受完需要继续接收
                if mm is bytes and mm is not None:
                    if g_code_length == 0:
                        get_data_length(mm)  # 调用此函数可以计算并修改全局变量g_code_length和g_header_length的值
                    length_buffer += len(mm)
                    try:
                        buffer_utf8 += mm
                    except Exception:
                        continue
                    if length_buffer - g_header_length < g_code_length:
                        if PRINT_FLAG:
                            print("INFO: 数据未接收完,接续接受")
                        continue
                    else:
                        if PRINT_FLAG:
                            print("g_code_length:", g_code_length)
                            print("INFO Line 204: receive信息 %s,长度为 %d:" % (buffer_utf8, len(buffer_utf8)))
                        if not buffer_utf8:
                            continue
                        receive_message = parse_data(buffer_utf8)  # 接受信息转换
                        if not receive_message:
                            try:
                                send_receive_message(buffer_utf8)
                            except Exception:
                                continue
                            if int(loop_time.tm_sec) >= 30:
                                print("收到心跳并已回复" + nowTime)
                                return_time = nowTime
                else:
                    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    new_time = time.strptime(nowTime, '%Y-%m-%d %H:%M:%S')
                    old_time = time.strptime(return_time, '%Y-%m-%d %H:%M:%S')
                    loop_time = time.gmtime(time.mktime(new_time) - time.mktime(old_time))
                    if not receive_message:
                        receive_message = mm
                    if not receive_message:
                        continue
                    elif receive_message:
                        if receive_message == "quit":
                            print("Socket %s Logout!" % i)
                            nowTime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                            sendMessage(" %s" % nowTime + " Logout")
                            delete_connection(str(i))
                            break
                        else:
                            try:
                                json_str = json.loads(receive_message)
                                if json_str['EventType'] != 0 and json_str['EventType'] != 1:
                                    if json_str['EventType'] == 1005 or json_str['EventType'] == 3006:
                                        receive_log = logger.logs("receive")
                                        receive_log.info(str(receive_message))
                                    else:
                                        print(nowTime, receive_message)
                                else:
                                    if return_time:
                                        sendMessage(receive_message)
                                        if int(loop_time.tm_sec) >= 6:
                                            if json_str['EventType'] == 1:
                                                print("收到并已回复心跳：", nowTime, receive_message)
                                                return_time = nowTime
                                        if json_str['InfoCode'] is not None:
                                            print(nowTime, receive_message)
                            except Exception as e:
                                if 'Socket is dead' in str(e):
                                    delete_connection(str(i))
                                    break
                                else:
                                    try:
                                        # print("解析错误原因是：", e, "错误的消息是：", receive_message)
                                        # send_receive_message(receive_message)
                                        # send_receive_message(receive_message)
                                        send_receive_message(receive_message)
                                    except Exception as e:
                                        if 'Socket is dead' in str(e):
                                            delete_connection(str(i))
                                            break
                                    if int(loop_time.tm_sec) >= 30:
                                        print("收到心跳并已回复" + nowTime)
                                        return_time = nowTime
                                    continue
                g_code_length = 0
                length_buffer = 0
                buffer_utf8 = b""
            except Exception as e:
                print(e)
                break
        i += 1
    return jsonify("再见")


@app.route('/send', methods=['get', 'post'])
def send_msg():
    global connection_list
    try:
        info = request.get_json()
        # print(info)
        if not info:
            msg = request.values.get('msg')
            send_receive_message(msg)
        else:
            msg = info['msg']
            sendMessage(msg)
    except Exception as e:
        print(e)
    return jsonify(list(connection_list.keys()))


@app.route('/simulationSendCar', methods=['get', 'post'])
def simulation_Send_Car():
    try:
        info = request.get_json()
        if info is None:
            info = Parameter(temp=request.values).common_all('IP', 'count', 'Camera_list')
        simulationSendCar_result = open_send_car(info['IP'], int(info['count']), info['Camera_list'].split(','))
    except Exception as e:
        simulationSendCar_result = 'error'
        print(e)
    return jsonify(simulationSendCar_result)


@app.route('/RouteParameter', methods=['get', 'post'])
def RouteParameter():
    try:
        if request.values:
            parameter_dict = Parameter(request.values.items())
        else:
            parameter_dict = Parameter(request.get_json())
        return jsonify(parameter_dict)
    except Exception as e:
        return jsonify(e)
