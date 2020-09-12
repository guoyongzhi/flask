# from numpy import *
# print(eye(4))
# import numpy as np
# a = np.array([1,  2,  3,4,5], ndmin =  2)
# print(a)
#
#
# -*- encoding:utf-8 -*-

import sys
from socket import *
import json, time, threading, hashlib
from websocket import create_connection

# reload(sys)
# sys.setdefaultencoding("utf8")

# 输入你的app_key
app_key = "50a9296592f098eb"
# 输入你的app_secret
app_secret = "078c4b4680543536dbfbd8742e1f9a2e"
# 输入你要检测的图片路径
path = ""


# 输入你要使用的api的uri,此处是检测图片人脸个数的uri


def getTimestamp():
    return str(round(time.time()) * 1000)


def GetSign(timestamp):
    hl = hashlib.md5()
    hl.update((timestamp + '#' + app_secret).encode(encoding='utf-8'))
    return hl.hexdigest()


class Client(object):
    def __init__(self):
        self.timestamp = getTimestamp()
        self.sign = GetSign(self.timestamp)
        # 调用create_connection方法，建立一个websocket链接
        # 链接地址请修改成你自己需要的
        self.ws = create_connection(
                "ws://192.168.11.26/websocket/record/" + app_key + '/' + self.timestamp + '/' + self.sign)
        # 建一个线程，监听服务器发送给客户端的数据
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    # 发送方法，聊天输入语句时调用，此处默认为群聊ALL
    def send(self, content):
        # 这里定义的消息体要换成你自己的消息体，变成你需要的。
        msg = {
            "code": 30000,
            "data": {
                "companyId": 1,
                "deviceName": "单元测试",
                "deviceSN": "SKP-4caa7bf8bce3e811feb3a989edb29e46",
                "direction": 1,
                "groupId": 1,
                "groupName": "默认组",
                "id": 6117,
                "originAvatar": "",
                "receptionUserId": 0,
                "receptionUserName": "",
                "signAvatar": "5d0d7dc34b5c570001d3f032",
                "signBgAvatar": "5d0d7dc34b5c570001d3f033",
                "signTime": int(time.time()),
                "userId": int(content),
                "userName": "郭永志",
                "userType": 1,
                "verifyScore": 0.0
            },
            "desc": "",
            "message": "push record"
        }
        msg = json.dumps(msg)
        self.ws.send(msg)
        print("已发送：", content, "消息  ---类型是：", type(content))

    # 接收服务端发送给客户的数据，只要ws处于连接状态，则一直接收数据
    def recv(self):
        try:
            while self.ws.connected:
                result = self.ws.recv(1024)
                print("received msg:" + str(result))
        except Exception as e:
            print(e)
            pass

    # 关闭时，发送QUIT方法，退出ws链接
    def close(self):
        # 具体要知道你自己退出链接的消息体是什么，如果没有，可以不写这个方法
        msg = {
            "type": "QUIT",
            "username": "johanna",
            "content": "byebye,everyone"
        }
        msg = json.dumps(msg)
        self.ws.send(msg)


if __name__ == '__main__':
    c = Client()
    # 当输入非exit时，则持续ws链接状态，如果exit，则关闭链接
    while True:
        content = input("please input(input exit to exit):")
        if content == "exit":
            c.close()
            break
        else:
            c.send(content)
            time.sleep(1)
