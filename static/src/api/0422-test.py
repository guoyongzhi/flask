import datetime
import os
import random
import time
import itchat

from static.src.api.chengyujielong import chengyujielong


import requests


# 登录
itchat.auto_login()

# # 发送消息
# itchat.send(u'你好', 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)
# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0

# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算 1表示男性，2女性
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
print(u"男性好友：%.2f%%" % (float(male) / total * 100))
print(u"女性好友：%.2f%%" % (float(female) / total * 100))
print(u"其他：%.2f%%" % (float(other) / total * 100))

user_list = []
userchengyu_list = []


@itchat.msg_register(itchat.content.TEXT)  # 私发消息
def text_reply(msg):  # 处理私人消息
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
            ta_list = talk.split()
            tot = talk.split()[0]
            ty = tot[:1]
            who = tot[1:]
            ss = 0
            talk = ta_list[ss + 1]
            if ss + 1 != len(ta_list):
                talk = ''
                for i in range(ss + 1, len(ta_list)):
                    if talk == '':
                        talk = talk + ta_list[i]
                    else:
                        talk = talk + ' ' + ta_list[i]
            list = who.split(',')
            if not list:
                list = who.split('，')
            if ty == '@':
                for i in list:
                    if i != '':
                        hetalk = itchat.search_friends(name=i)
                        itchat.send(talk, hetalk[0]['UserName'])
            else:
                for i in list:
                    if i != '':
                        hetalk = itchat.search_chatrooms(name=i)
                        itchat.send(talk, hetalk[0]['UserName'])
            return who + '发送成功'
        except Exception as e:
            print(e)
            return '发送失败'
    else:
        if talk == '开始聊天' or talk == '开启聊天':
            if user_list:
                for i in user_list:
                    if i == name:
                        ss = i
                        return '已经开始聊天咯~'
            elif not ss:
                user_list.append(name)
                return '你好呀！我的小可爱'
            else:
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


gamedict = dict()
pai = 0
qun_list = []
chengyu_list = []


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)  # 群消息（群游戏）
def text_reply(msg):  # 处理群消息
    global pai
    nn = ''
    # print(msg['User'])
    # print(len(msg['User']['MemberList']), type(msg['User']['MemberList']))
    # print(msg)
    talk = msg['Content']
    this = msg['User']['Self']['DisplayName']
    qname = msg['User']['NickName']
    whotalk = msg['ActualNickName']
    if not this:  # 当没有备注时取微信名称
        this = msg['User']['Self']['NickName']
    if not whotalk:
        whotalk = this
    print(msg['User']['NickName'], msg['User']['Self']['DisplayName'], '--', msg['ActualNickName'], ':', talk)
    if talk[:1] == '@':
        try:
            new = talk.split()
            users_list = msg['User']['MemberList']
            who = new[0]
            who = who[1:]
            if who == '所有人':
                return '@' + whotalk + ' 收到！机器人回复~'
            dd = 0
            ss = 0
            try:
                if users_list:
                    while ss <= len(new):
                        for i in users_list:
                            tname = i['DisplayName']
                            if tname == '':
                                tname = i['NickName']
                            if tname == who:
                                dd = 1
                                break
                        if dd == 1:
                            break
                        else:
                            ss += 1
                            if ss >= len(new):
                                break
                            insp = who + ' ' + new[ss]
                            a = 1
                            ao = 0
                            while ao <= 10:
                                ll = len(insp) + 1
                                if talk[:ll] == '@' + insp:
                                    who = insp
                                    break
                                else:
                                    nn = ' '
                                    for i in range(0, a):
                                        nn += ' '
                                    insp = who + nn + new[ss]
                                    a += 1
                                    ao += 1
                else:
                    who = ''
                    print('找不到用户', msg)
            except Exception as e:
                who = ''
                print('处理用户抱错了', e, msg)
            try:
                if ss + 1 < len(new):
                    if ss + 1 != len(new):
                        talk = ''
                        for i in range(ss + 1, len(new)):
                            if talk == '':
                                talk = talk + new[i]
                            else:
                                talk = talk + ' ' + new[i]
                    else:
                        talk = new[ss + 1]
                else:
                    talk = ''
            except Exception as e:
                print(e, msg)
                talk = ''
            print(whotalk + '@' + who, talk)
            if who == this:
                if talk == '菜单' or talk == '帮助' or talk == 'help':
                    with open('help.txt', encoding='utf-8') as f:
                        aa = f.readlines()
                    f.close()
                    return "自己看吧，是不是多到眼花\n机器人聊天    成语接龙\n群签到    打劫游戏\n其他功能正在努力开发中"
                elif talk == '聊天菜单' or talk == '聊天帮助' or talk == '聊天help':
                    return "@" + whotalk + ': 开始艾特我回复：' + '开始聊天  或  开启聊天  或  机器人聊天\n结束回复：结束聊天  或  关闭聊天  或  不聊了。'
                elif talk == '成语接龙菜单' or talk == '成语接龙帮助' or talk == '成语接龙help':
                    return "@" + whotalk + ': 开始艾特我回复：' + '成语接龙  或  打开成语接龙  或  直接说成语\n结束回复：不玩了  或  关闭成语接龙  或  退出。'
                elif talk == '签到菜单' or talk == '签到帮助' or talk == '签到help':
                    return "@" + whotalk + ': 开始艾特我回复：签到 '
                elif talk == '抢劫菜单' or talk == '抢劫帮助' or talk == '抢劫help':
                    return "@" + whotalk + ': 开始艾特我或他（她）回复：' + '打劫  或抢劫'
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
                elif talk == '签到':
                    if whotalk not in gamedict:
                        pai += 1
                        qiandaojifen = 10
                        qiandaojinbi = 500
                        gamedict[whotalk] = pai, qiandaojifen, qiandaojinbi
                        now = time.strftime("%H:%M:%S")
                        return "👻[" + whotalk + ']签到成功\n👻排名：第' + str(pai) + '名\n👻奖励：' + str(
                            qiandaojifen) + '积分 ' + str(qiandaojinbi) + '金币\n👻头衔：新手上路\n👻时间：' + str(now)
                    else:
                        nowinfo = gamedict[whotalk]
                        npai = nowinfo[0]
                        jifen = nowinfo[1]
                        jinbi = nowinfo[2]
                        if npai == 0:
                            pai += 1
                            jifen += 10
                            jinbi += 500
                            gamedict[whotalk] = pai, jifen, jinbi
                            if jinbi < 1000:
                                ty = '新手上路'
                            elif jinbi < 5000:
                                ty = '小有成就'
                            elif jinbi < 10000:
                                ty = '小康生活'
                            elif jinbi < 50000:
                                ty = '小老板'
                            elif jinbi < 200000:
                                ty = '大老板'
                            elif jinbi > 200000:
                                ty = '大富翁'
                            now = time.strftime("%H:%M:%S")
                            return "👻" + whotalk + '签到成功\n👻排名：第' + str(pai) + '名\n👻奖励：' + str(jifen) + '积分 ' + str(
                                jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                        else:
                            return '亲您已签到过了，请勿重复签到'
                elif talk == '查询':
                    if whotalk not in gamedict:
                        return '您今天未签到哦~'
                    nowinfo = gamedict[whotalk]
                    pai = nowinfo[0]
                    jifen = nowinfo[1]
                    jinbi = nowinfo[2]
                    if jinbi < 1000:
                        ty = '新手上路'
                    elif jinbi < 5000:
                        ty = '小有成就'
                    elif jinbi < 10000:
                        ty = '小康生活'
                    elif jinbi < 50000:
                        ty = '小老板'
                    elif jinbi < 200000:
                        ty = '大老板'
                    elif jinbi > 200000:
                        ty = '大富翁'
                    now = time.strftime("%H:%M:%S")
                    if pai == 0:
                        return "👻[" + whotalk + ']查询成功\n👻签到排名：未签到\n👻资产：' + str(jifen) + '积分 ' + str(
                            jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                    else:
                        return "👻[" + whotalk + ']查询成功\n👻签到排名：第' + str(pai) + '名\n👻资产：' + str(jifen) + '积分 ' + str(
                            jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                elif talk == '抢劫' or talk == '打劫':
                    if whotalk not in gamedict:
                        getpai = 0
                        getjifen = 0
                        getjinbi = 0
                        to = random.randint(100, 2000)
                        getjinbi += to
                        gamedict[whotalk] = getpai, getjifen, getjinbi
                        return '😂[' + whotalk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                    else:
                        nowinfo = gamedict[whotalk]
                        pai = nowinfo[0]
                        jifen = nowinfo[1]
                        getjinbi = nowinfo[2]
                        to = random.randint(100, 2000)
                        getjinbi += to
                        gamedict[whotalk] = pai, jifen, getjinbi
                        return '😂[' + whotalk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                elif talk == '点歌':
                    return '很抱歉~该功能尚未实现! 回复“帮助”查看已完成功能~'
                elif talk == '讲个笑话' or talk == '笑话' or talk == '讲笑话':
                    return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                elif talk == '讲个故事' or talk == '故事' or talk == '讲故事':
                    return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                # elif talk == '兑换':
                #     if whotalk not in gamedict:
                #         return '很抱歉，您的账户无资产~'
                #     else:
                #         nowinfo = gamedict[whotalk]
                elif talk == '开始聊天' or talk == '开启聊天' or talk == '机器人聊天':
                    if qun_list:
                        for i in qun_list:
                            if i == msg['User']['NickName']:
                                nn = i
                                return '已经开始聊天咯~'
                    else:
                        qun_list.append(qname)
                        return '你们好呀！我的小可爱们'
                elif talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了':
                    try:
                        qun_list.remove(qname)
                        return '拜拜~'
                    except Exception as e:
                        print(e, '该值不存在')
                elif not talk:
                    itchat.send('@' + whotalk + ' 艾特本喵有何事！', toUserName=msg['FromUserName'])
                    return
                if chengyu_list:
                    for n in chengyu_list:
                        if qname == n:
                            return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                    else:
                        chengyu_list.append(qname)
                        return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                elif qun_list:
                    for n in qun_list:
                        if qname == n:
                            ress = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                            re = ress.json()["content"]
                            print(n, "--群聊：{}  ({})".format(re, datetime.datetime.now()))
                            return '@' + whotalk + ' ' + re
                if len(talk) == 4:  # 输入成语直接开始成语接龙
                    res = chengyujielong(talk, qname)
                    if res:
                        chengyu_list.append(qname)
                        return "成语接龙开始咯：" + res
                    else:
                        return itchat.send('@' + whotalk + '\u2005收到！机器人回复~', toUserName=msg['FromUserName'])
                else:
                    return itchat.send('@' + whotalk + '\u2005收到！机器人回复~', toUserName=msg['FromUserName'])
            elif talk == '抢劫' or talk == '打劫':
                try:
                    getpai = 0
                    getjifen = 0
                    getjinbi = 0
                    if whotalk in gamedict:
                        whoget = gamedict[whotalk]
                        getpai = whoget[0]
                        getjifen = whoget[1]
                        getjinbi = whoget[2]
                    if who not in gamedict:
                        return '打劫失败，对方无资产！'
                    whoset = gamedict[who]
                    setpai = whoset[0]
                    setjifen = whoset[1]
                    setjinbi = whoset[2]
                    if setjinbi:
                        fzhuan = random.randint(0, 1)
                        if fzhuan == 0:
                            if setjinbi > 0:
                                to = random.randint(0, setjinbi)
                                setjinbi = setjinbi - to
                                getjinbi = getjinbi + to
                                gamedict[whotalk] = getpai, getjifen, getjinbi
                                gamedict[who] = setpai, setjifen, setjinbi
                                return '😂[' + whotalk + '] 抢劫 [' + who + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                        else:
                            to = random.randint(0, getjinbi)
                            setjinbi += to
                            getjinbi -= to
                            gamedict[whotalk] = getpai, getjifen, getjinbi
                            gamedict[who] = setpai, setjifen, setjinbi
                            return '😂[' + whotalk + '] 抢劫 [' + who + '] 失败，反被对方抢走了' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                    else:
                        return '打劫失败，对方无资产！'
                except Exception as e:
                    return '报错了' + str(e)
        except Exception as e:
            print('报错了', e)
    elif msg['isAt']:
        print(msg)
        # if msg["Text"].find("@" + msg['User']['Self']['NickName']) == 0:
        #     return "@" + msg.actualNickName + " 东你发的信息为：" + msg.text
        itchat.send_raw_msg(msgType='TEXT', content=u'I received: %s' % (msg['Content']), toUserName=msg['FromUserName'])


@itchat.msg_register(itchat.content.NOTE)  # 通知类
def note_rep(msg):
    # print(msg)
    print('发红包了', msg)


@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)  # 通知类
def note_reply(msg):
    # print("通知消息来了", msg)
    qname = msg['User']['UserName']
    now = time.strftime("%H:%M:%S")
    talk = '发红包了 ' + now
    this = msg['User']['Self']['NickName']
    if '收到红包，请在手机上查看' == msg['Content']:
        itchat.send(talk, qname)
        print('note:Content：', msg['Content'])
        print('群里发红包了')
    # elif '红包'in msg['Text']:
    #     itchat.send(talk, qname)
    #     print('note:Text：', msg['Text'])
    #     print('群里发红包了')
    elif msg['ActualNickName'] == this:
        if msg.text == '你撤回了一条消息':
            print('撤回来自己的消息')
    elif msg.text == '"' + msg['ActualNickName'] + '" 撤回了一条消息':
        print(msg['ActualNickName'], '撤回了一条消息')
    else:
        print("什么也没有" + now)


@itchat.msg_register(itchat.content.MAP)  # 地图类
def MAP_rep(msg):
    # print('私发发地图了', msg)
    pass


@itchat.msg_register(itchat.content.MAP, isGroupChat=True)  # 群地图类
def MAP_reply(msg):
    # this = msg['User']['Self']['DisplayName']
    # if not this:  # 当没有备注时取微信名称
    #     this = msg['User']['Self']['NickName']
    # elif '地图' in msg['Text']:
    #     print('note:', msg['Text'])
    #     print('群里地图了')
    # else:
    # print("群地图消息：" + msg)
    pass


@itchat.msg_register(itchat.content.CARD)  # 卡片类
def CARD_rep(msg):
    print('私发发地卡片了', msg)


@itchat.msg_register(itchat.content.CARD, isGroupChat=True)  # 群卡片类
def CARD_reply(msg):
    print('群卡片消息：', msg)


@itchat.msg_register(itchat.content.SHARING)  # 共享类
def SHARING_rep(msg):
    # print(msg)
    print('私发发共享了', msg)


@itchat.msg_register(itchat.content.SHARING, isGroupChat=True)  # 群共享类
def SHARING_reply(msg):
    print('群共享消息：', msg)


PICTURE_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\PICTURE')
@itchat.msg_register(itchat.content.PICTURE)  # 图片类
def PICTURE_rep(msg):
    if os.path.exists(PICTURE_dir) and os.path.isdir(PICTURE_dir):
        pass
    else:
        os.mkdir(PICTURE_dir)
    msg.download(PICTURE_dir + '\\' + msg.fileName)
    # print('私发图片了', msg)


@itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)  # 群图片类
def PICTURE_reply(msg):
    if os.path.exists(PICTURE_dir) and os.path.isdir(PICTURE_dir):
        pass
    else:
        os.mkdir(PICTURE_dir)
    msg.download(PICTURE_dir + '\\' + msg.fileName)
    # print('群发发图片了', msg)


RECORDING_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\RECORDING')
@itchat.msg_register(itchat.content.RECORDING, itchat.content.VOICE)  # 录音类
def RECORDING_rep(msg):
    if os.path.exists(RECORDING_dir) and os.path.isdir(RECORDING_dir):
        pass
    else:
        os.mkdir(RECORDING_dir)
    msg.download(RECORDING_dir + '\\' + msg.fileName)
    # print('私发发录音了', msg)


@itchat.msg_register(itchat.content.RECORDING, itchat.content.VOICE, isGroupChat=True)  # 群录音类
def RECORDING_reply(msg):
    if os.path.exists(RECORDING_dir) and os.path.isdir(RECORDING_dir):
        pass
    else:
        os.mkdir(RECORDING_dir)
    msg.download(RECORDING_dir + '\\' + msg.fileName)
    # print('群录音消息：', msg)


ATTACHMENT_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\ATTACHMENT')
@itchat.msg_register(itchat.content.ATTACHMENT)  # 附件类
def ATTACHMENT_rep(msg):
    if os.path.exists(ATTACHMENT_dir) and os.path.isdir(ATTACHMENT_dir):
        pass
    else:
        os.mkdir(ATTACHMENT_dir)
    msg.download(ATTACHMENT_dir + '\\' + msg.fileName)
    # print('私发附件了', msg)


@itchat.msg_register(itchat.content.ATTACHMENT, isGroupChat=True)  # 群附件类
def ATTACHMENT_reply(msg):
    if os.path.exists(ATTACHMENT_dir) and os.path.isdir(ATTACHMENT_dir):
        pass
    else:
        os.mkdir(ATTACHMENT_dir)
    msg.download(ATTACHMENT_dir + '\\' + msg.fileName)
    # print('群发发附件了', msg)


VIDEO_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\VIDEO')
@itchat.msg_register(itchat.content.VIDEO)  # 视频类
def VIDEO_rep(msg):
    if os.path.exists(VIDEO_dir) and os.path.isdir(VIDEO_dir):
        pass
    else:
        os.mkdir(VIDEO_dir)
    msg.download(VIDEO_dir + '\\' + msg.fileName)


@itchat.msg_register(itchat.content.VIDEO, isGroupChat=True)  # 群视频类
def VIDEO_reply(msg):
    if os.path.exists(VIDEO_dir) and os.path.isdir(VIDEO_dir):
        pass
    else:
        os.mkdir(VIDEO_dir)
    msg.download(VIDEO_dir + '\\' + msg.fileName)


@itchat.msg_register(itchat.content.FRIENDS)  # 朋友类
def FRIENDS_rep(msg):
    # print(msg)
    print('私发朋友了', msg)


@itchat.msg_register(itchat.content.FRIENDS, isGroupChat=True)  # 群朋友类
def FRIENDS_reply(msg):
    print('群发发朋友了', msg)


@itchat.msg_register(itchat.content.SYSTEM)  # 系统自己类
def SYSTEM_rep(msg):
    # print(msg)
    # print('私发系统了', msg)
    pass


@itchat.msg_register(itchat.content.SYSTEM, isGroupChat=True)  # 群系统类
def SYSTEM_reply(msg):
    # print('群发发系统了', msg)
    pass


itchat.run()
