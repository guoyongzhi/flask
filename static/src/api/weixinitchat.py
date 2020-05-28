import json
import threading
import itchat
from itchat.content import *



# 登录
# itchat.login()
import requests

itchat.auto_login()
# # 发送消息
# itchat.send(u'你好', 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)
# print(friends)
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
# roomslist = itchat.get_chatrooms()
# for i in roomslist:
#     print(i)
# who = '郭,心语过往'
# list = who.split(',')
# if not list:
#     list = who.split('，')
# print(list)
# for i in list:
#     hetalk = itchat.search_friends(name=i)
#     print(hetalk[0]['UserName'])


@itchat.msg_register([TEXT, NOTE, MAP, CARD, SHARING, PICTURE, RECORDING, VOICE, ATTACHMENT, VIDEO], isGroupChat=True)  # 通知类
def note_reply(msg):
    qname = msg['User']['UserName']
    talk = msg['Content']
    if msg['IsAt']:
        itchat.send('@' + msg['ActualNickName'] + '\u2005send', toUserName=msg['FromUserName'], mediaId=msg['MsgId'])
        itchat.send_msg('@' + msg['ActualNickName'] + '\u2005send_msg', toUserName=msg['FromUserName'])
        itchat.send_raw_msg(msgType=msg['Type'], content='@' + msg['ActualNickName'] + '\u2005send_raw_msg', toUserName=
        msg['FromUserName'])
    elif '加入了群聊' in msg['Content']:
        new = msg['Text'].split()
        s = new[0].split('"')
        if len(s) >= 4:
            if s[4] == '加入了群聊':
                itchat.send('欢迎"' + s[3] + '"加入群聊', qname)
                itchat.send('欢迎"' + s[3] + '"新朋友，出来报道，请爆照.积极发言，发红包,多参加活动 分享过去的活动图片！不可以发与珠峰群无关的广告，链接和小程序！否则请出！谢谢配合！',
                            qname)
    elif '点歌' in talk or '播放' in talk:
        name = talk.split()
        if len(name) > 1:
            songname = name[1]
        else:
            name = talk.split('-')
            if len(name) == 1:
                return '亲点歌格式不对哦~ 点歌请艾特我回复点歌 【歌名】'
            songname = name[1]
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1' \
              '&remoteplace=txt.yqq.song&searchid=55989056282747366&t=0&aggr=1&cr=1&catZhida=1&lossless=0' \
              '&flag_qc=0&p=1&n=10&w=' + songname + '&g_tk_new_20200303=1945000638&g_tk=654347293&loginUin=1983496818&hostUin=0&format=json' \
                                                    '&inCharset=utf8&outCharset=utf-8&notice=0&platfin talk orm=yqq.json&needNewCode=0 '
        res = requests.get(url=url)
        jm = json.loads(res.text)
        psid = jm['data']['song']['list'][0]['id']
        songer = jm['data']['song']['list'][0]['singer'][0]['name']
        songname = jm['data']['song']['list'][0]['title']
        test = 'https://i.y.qq.com/v8/playsong.html?songid={}&source=yqq#wechat_redirect'.format(psid)
        return '非常好听的《' + songname + '-' + str(songer) + '》来咯~ 点击链接欣赏:\n' + test
    print(msg)


@itchat.msg_register([TEXT, NOTE, MAP, CARD, SHARING, PICTURE, RECORDING, VOICE, ATTACHMENT, VIDEO],
                     isGroupChat=False)  # 通知类
def note_reply(msg):
    if msg['Type'] == 'Picture':
        itchat.send_image('200430-152225.gif', toUserName=msg['FromUserName'])
    print(msg)


itchat.run()
