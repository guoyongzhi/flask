# # -*- coding:utf8 -*-
#
# import threading
# import hashlib
# import socket
# import base64
#
# global clients
# clients = {}
#
#
# # 通知客户端
# def notify(message):
#     for connection in clients.values():
#         connection.send('%c%c%s' % (0x81, len(message), message))
#
#
# # 客户端处理线程
# class websocket_thread(threading.Thread):
#     def __init__(self, connection, username):
#         super(websocket_thread, self).__init__()
#         self.connection = connection
#         self.username = username
#
#     def run(self):
#         print('new websocket client joined!')
#         data = self.connection.recv(1024)
#         headers = self.parse_headers(data)
#         token = self.generate_token(headers['Sec-WebSocket-Key'])
#         tttt= '\
# HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
# Upgrade: WebSocket\r\n\
# Connection: Upgrade\r\n\
# Sec-WebSocket-Accept: %s\r\n\r\n' % (token.decode())
#         self.connection.send(tttt.encode("utf-8"))
#         while True:
#             try:
#                 data = self.connection.recv(1024)
#             except Exception as e:
#                 print("unexpected error: ", e)
#                 clients.pop(self.username)
#                 break
#             data = self.parse_data(data)
#             if len(data) == 0:
#                 continue
#             message = self.username + ": " + data
#             notify(message)
#
#     def parse_data(self, msg):
#         for i in zip(str(msg[1])):
#             v = ord(str(i[0])) & 0x7f
#             if v == 0x7e:
#                 p = 4
#             elif v == 0x7f:
#                 p = 10
#             else:
#                 p = 2
#             mask = msg[p:p + 4]
#             data = msg[p + 4:]
#         return ''
#
#     def parse_headers(self, msg):
#         headers = {}
#         header, data = msg.decode().split('\r\n\r\n', 1)
#         for line in header.split('\r\n')[1:]:
#             key, value = line.split(': ', 1)
#             headers[key] = value
#         headers['data'] = data
#         return headers
#
#     def generate_token(self, msg):
#         key = msg + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
#         ser_key = hashlib.sha1(key.encode('utf8')).digest()
#         return base64.b64encode(ser_key)
#
#
# # 服务端
# class websocket_server(threading.Thread):
#     def __init__(self, port):
#         super(websocket_server, self).__init__()
#         self.port = port
#
#     def run(self):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         sock.bind(('127.0.0.1', self.port))
#         sock.listen(5)
#         print('websocket server started!')
#         while True:
#             connection, address = sock.accept()
#             try:
#                 username = "ID" + str(address[1])
#                 thread = websocket_thread(connection, username)
#                 thread.start()
#                 clients[username] = connection
#             except socket.timeout:
#                 print('websocket connection timeout!')
#
#
# if __name__ == '__main__':
#     server = websocket_server(9000)
#     server.start()

from flask import Flask, request, render_template
from geventwebsocket.websocket import WebSocket, WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

import json

app = Flask(__name__)


@app.route('/index/')
def index():
    return render_template('websocket.html')


# user_socket_list = []
user_socket_dict = {}


@app.route('/ws/<username>')
def ws(username):
    user_socket = request.environ.get("wsgi.websocket")
    if not user_socket:
        return "请以WEBSOCKET方式连接"

    user_socket_dict[username] = user_socket
    print(user_socket_dict)

    while True:
        try:
            user_msg = user_socket.receive()
            for user_name, u_socket in user_socket_dict.items():

                who_send_msg = {
                    "send_user": username,
                    "send_msg": user_msg
                }

                if user_socket == u_socket:
                    continue
                u_socket.send(json.dumps(who_send_msg))

        except WebSocketError as e:
            user_socket_dict.pop(username)
            print(user_socket_dict)
            print(e)


if __name__ == '__main__':
    app.debug = True
    http_serve = WSGIServer(("127.0.0.1", 5000), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()
