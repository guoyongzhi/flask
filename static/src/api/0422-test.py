# import requests
# import re
# from bs4 import BeautifulSoup
#
#
# res = requests.get('http://192.168.11.153:8301/api/v1/help/index')
# res.encoding = res.apparent_encoding
# result = res.text
# # print(result)
# soup = BeautifulSoup(result, 'html.parser')
#
# ul = soup.find_all(name='li')
# # print(ul, len(ul))
# # li_list = ul.find_all(name='li')
#
# for i in zip(ul):
#     p = re.compile('\W')
#     li = re.findall(p, i)
#     print(li)
import datetime
import time

import itchat

from static.src.api.chengyujielong import chengyujielong

# 登录
# itchat.login()
import requests

itchat.auto_login()
# # 发送消息
# itchat.send(u'你好', 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)
# print(friends)
# groups = itchat.search_chatrooms(name='珠峰优惠会员群VIP10元1群')
# print(groups)
# print(groups[0]['UserName'])
# itchat.send(u' ', groups[0]['UserName'])
# print(friends)
# my_friend = itchat.search_friends(name=r'M96黄敏~电商')
# print(my_friend)
# my_friends = itchat.search_friends(name=r'M')
# print(my_friends)
# my_friendx = itchat.search_friends(name=r'心语过往')
# print(my_friendx)
# itchat.send(u'你好', my_friendx[0]['UserName'])
# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0

# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
# 1表示男性，2女性
for i in friends[1:]:
    # print(i)
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1

# 总数算上，好计算比例啊～
total = len(friends[1:])

# 好了，打印结果
print(u"男性好友：%.2f%%" % (float(male) / total * 100))
print(u"女性好友：%.2f%%" % (float(female) / total * 100))
print(u"其他：%.2f%%" % (float(other) / total * 100))
roomslist = itchat.get_chatrooms()
for i in roomslist:
    print(i)


user_list = []
userchengyu_list = []
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # msg = "努力上班中，晚点回复！"
    ss = ''
    # global ss
    talk = msg.text
    print(msg['User']['NickName'], msg['User']['RemarkName'], talk)
    name = msg['User']['RemarkName']
    if not name:  # 当没有备注时取微信名称
        name = msg['User']['NickName']
    if name == '心语过往':
        try:
            tot = talk.split()[0]
            ty = tot[:1]
            who = tot[1:]
            talk = talk.split()[1]
            if ty == '@':
                hetalk = itchat.search_friends(name=who)
            else:
                hetalk = itchat.search_chatrooms(name=who)
            itchat.send(talk, hetalk[0]['UserName'])
        except Exception as e:
            print(e)
        return '发送成功'
    else:
        if talk == '开始聊天' or talk == '开启聊天':
            if user_list:
                for i in user_list:
                    if i == name:
                        ss = i
                        return '已经开始聊天咯~'
            else:
                user_list.append(name)
                return '你好呀！我的小可爱'
            if not ss:
                user_list.append(name)
                return '你好呀！我的小可爱'
        if talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了':
            try:
                user_list.remove(name)
                return '拜拜~'
            except Exception as e:
                print(e, '该值不存在')
        if talk == '成语接龙' or talk == '打开成语接龙':
            talk = ''
            if userchengyu_list:
                for i in userchengyu_list:
                    if i == msg['User']['NickName']:
                        ss = i
                        return '已经开始成语接龙咯~'
            else:
                userchengyu_list.append(str(msg['User']['NickName']))
                return chengyujielong(talk, name)
            if not ss:
                userchengyu_list.append(str(msg['User']['NickName']))
                return chengyujielong(talk, name)
        elif talk == '不玩了' or talk == '关闭成语接龙' or talk == '退出':
            talk = '退出'
            try:
                userchengyu_list.remove(str(msg['User']['NickName']))
                return chengyujielong(talk, name)
            except Exception as e:
                print(e, '该值不存在')
        if userchengyu_list:
            for n in userchengyu_list:
                if name == n:
                    return chengyujielong(talk, name)
            else:
                talk = ''
                return chengyujielong(talk, name)
        if user_list:
            for n in user_list:
                if n == name:
                    res = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                    res = res.json()["content"]
                    print(n, "--私聊：{}  ({})".format(res, datetime.datetime.now()))
                    return res


qun_list = []
chengyu_list = []
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    nn = ''
    talk = msg['Content']
    this = msg['User']['Self']['DisplayName']
    qname = msg['User']['NickName']
    whotalk = msg['ActualNickName']
    if not this:  # 当没有备注时取微信名称
        this = msg['User']['Self']['NickName']
    print(msg['User']['NickName'], msg['User']['Self']['DisplayName'], '--', msg['ActualNickName'], ':', talk)
    if talk[:1] == '@':
        try:
            new = talk.split()[0]
            who = new[1:]
            talk = talk.split()[1]
            if who == this:
                if talk == '菜单' or talk == '帮助' or talk == 'help':
                    with open('help.txt', encoding='utf-8') as f:
                        aa = f.readlines()
                    f.close()
                    return "自己看吧，是不是多到眼花\n机器人聊天    成语接龙\n其他功能正在努力开发中"
                elif talk == '成语接龙' or talk == '打开成语接龙':
                    talk = ''
                    if chengyu_list:
                        for i in chengyu_list:
                            if i == qname:
                                nn = i
                                return '@' + whotalk + ' ' + '已经开始成语接龙咯~'
                    else:
                        chengyu_list.append(qname)
                        return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                    if not nn:
                        chengyu_list.append(qname)
                        return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                elif talk == '不玩了' or talk == '关闭成语接龙' or talk == '退出':
                    talk = '退出'
                    try:
                        chengyu_list.remove(qname)
                        return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                    except Exception as e:
                        print(e, '该值不存在')
                if chengyu_list:
                    if not talk:
                        return '@' + whotalk + ' 艾特本喵有何事！'
                    for n in chengyu_list:
                        if qname == n:
                            return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                    else:
                        chengyu_list.append(qname)
                        return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                else:
                    # if talk:
                    #     return '@' + whotalk + ' 成语接龙未开启'
                    if not talk:
                        return '@' + whotalk + ' 艾特本喵有何事！'
                    else:
                        res = chengyujielong(talk, qname)
                        if res == talk + ' 这不是一个成语哦':
                             return res
                        else:
                            chengyu_list.append(qname)
                            return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                
        except Exception as e:
            print(e)
    # print(msg['User']['NickName'], msg['User']['Self']['DisplayName'], '--', msg['ActualNickName'], ':', talk)
    if talk == '开始聊天' or talk == '开启聊天' or talk == '机器人聊天':
        if qun_list:
            for i in qun_list:
                if i == msg['User']['NickName']:
                    nn = i
                    return '已经开始聊天咯~'
        else:
            qun_list.append(qname)
            return '你们好呀！我的小可爱们'
        if not nn:
            qun_list.append(qname)
            return '你们好呀！我的小可爱们'
    elif talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了':
        try:
            qun_list.remove(qname)
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif qun_list:
        if talk[:1] == '@':
            new = talk.split()[0]
            who = new[1:]
            talk = talk.split()[1]
            if who == this:
                for n in qun_list:
                    if qname == n:
                        ress = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                        re = ress.json()["content"]
                        print(n, "--群聊：{}  ({})".format(re, datetime.datetime.now()))
                        return '@' + whotalk + ' ' + re
        else:
            if talk[:1] == '@':
                new = talk.split()[0]
                who = new[1:]
                talk = talk.split()[1]
                if who != this:
                    for n in qun_list:
                        if qname == n:
                            ress = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                            re = ress.json()["content"]
                            print(n, "--群聊：{}  ({})".format(re, datetime.datetime.now()))
                            return re


itchat.run()
