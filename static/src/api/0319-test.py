# import random
#
#
# def split(full_list, shuffle=False, ratio=0.2):
#     n_total = len(full_list)
#     offset = int(n_total * ratio)
#     if n_total == 0 or offset < 1:
#         return [], full_list
#     if shuffle:
#         random.shuffle(full_list)
#     sublist_1 = full_list[:offset]
#     sublist_2 = full_list[offset:]
#     return sublist_1, sublist_2
#
#
# if __name__ == "__main__":
#     li = (1, 2)
#     sublist_1, sublist_2 = split(li, shuffle=False, ratio=0.9)
#
#     print(sublist_1, len(sublist_1))
#     print(sublist_2, len(sublist_2))
# import numpy as np
# # np.random.seed(0)
# p = np.array([0.2, 0.8])
# print(p)
# print(p.ravel())
# for i in range(50):
#     index = np.random.choice([1, 2], p=p.ravel())
#     print(index, i)


# def aa():
#     return 1
#
#
# def bb():
#     for i in range(10):
#         return i
#     return None
#
#
# a = aa()
# print(a)
# b = bb()
# print(b)
import json
from datetime import datetime
import os
import random
import time
import itchat
import logger

from static.src.api.chengyujielong import chengyujielong
from static.src.api.count.read_name_all_info import read_name_all_info

import requests

# 登录
itchat.auto_login()

itchat.auto_login(hotReload=True)  # 热加载

print('检测结果可能会引起不适。')
print('检测结果请在手机上查看，此处仅显示检测信息。')
print('消息被拒收为被拉黑， 需要发送验证信息为被删。')
print('没有结果就是好结果。')
print('检测1000位好友需要34分钟， 以此类推。')
print('为了你的账号安全着想，这个速度刚好。')
print('在程序运行期间请让程序保持运行，网络保持连接。')
print('请不要从手机端手动退出。')
input('按ENTER键继续...')

friends = itchat.get_friends(update=True)
lenght = len(friends)

for i in range(1, lenght):
    # 微信bug，用自己账户给所有好友发送"ॣ ॣ ॣ"消息，当添加自己为好友时，只有自己能收到此信息，如果没添加自己为好友\
    # 没有人能收到此信息，笔者此刻日期为2019/1/6 8:30，到目前为止微信bug还没修复。
    # 所以迭代从除去自己后的第二位好友开始 range(1, lenght)。
    itchat.send("ॣ ॣ ॣ", toUserName=friends[i]['UserName'])
    print(f'检测到第{i}位好友: {str(friends[i]["NickName"]).center(20, " ")}')
    # 发送信息速度过快会被微信检测到异常行为。
    time.sleep(2)

print('已检测完毕，请在手机端查看结果。')

user_list = []
userchengyu_list = []
ana_list = []


@itchat.msg_register(itchat.content.TEXT)  # 私发消息
def text_reply(msg):  # 处理私人消息
    # msg = "努力上班中，晚点回复！"
    ss = ''
    # global user_list, userchengyu_list, ana_list
    talk = msg.text
    print(msg['User']['NickName'], msg['User']['RemarkName'], talk)
    name = msg['User']['RemarkName']
    if not name:  # 当没有备注时取微信名称
        name = msg['User']['NickName']
    if name == '机器人_菲菲':
        if talk[:1] == '@' or talk[:1] == 'T':
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
    if talk == '开始聊天' or talk == '开启聊天':
        if user_list:
            for i in user_list:
                if i == name:
                    ss = i
                    return '已经开始聊天咯~'
            if not ss:
                user_list.append(name)
                return '你好呀！我的小可爱'
        else:
            user_list.append(name)
            return '你好呀！我的小可爱'
    elif talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了':
        try:
            user_list.remove(name)
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '成语接龙' or talk == '打开成语接龙':
        talk = ''
        if userchengyu_list:
            for i in userchengyu_list:
                if i == msg['User']['NickName']:
                    ss = i
                    return '已经开始成语接龙咯~'
        else:
            userchengyu_list.append(name)
            return chengyujielong(talk, name)
        if not ss:
            userchengyu_list.append(name)
            return chengyujielong(talk, name)
    elif talk == '不玩了' or talk == '关闭成语接龙' or talk == '退出':
        talk = '退出'
        try:
            userchengyu_list.remove(name)
            return chengyujielong(talk, name)
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '取消名言名句' or talk == '关闭名言名句' or talk == '退出名言名句':
        try:
            ana_list.remove(name)
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif '名言名句' in talk:
        if not ana_list:
            for i in ana_list:
                if i == name:
                    ss = i
                    return '已经开始聊天咯~'
            if not ss:
                ana_list.append(name)
                return '你好呀！我的小可爱'
        else:
            ana_list.append(name)
            return '你好呀！我的小可爱'
    elif '存档' in talk:
        res = set_info()
        return res
    elif '读档' in talk:
        res = get_info()
        return res
    elif userchengyu_list:
        for n in userchengyu_list:
            if name == n:
                return chengyujielong(talk, name)  # else:  #     talk = ''  #     return chengyujielong(talk, name)
    elif user_list:
        for n in user_list:
            if n == name:
                res = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                res = res.json()["content"]
                if '{br}' in res:
                    res_list = res.split('{br}')
                    res = '\n'.join(res_list)
                print(n, "--私聊：{}  ({})".format(res, datetime.now()))
                return res
    elif ana_list:
        for n in ana_list:
            if n == name:
                a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
                return a.split()[0]
    else:
        hetalk = itchat.search_friends(name='机器人_菲菲')
        itchat.send(name + ':' + talk, hetalk[0]['UserName'])


gamedict = dict()
pai = 0
this_num = 0
qun_list = []
chengyu_list = []
hongbao_list = []


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)  # 群消息（群游戏）
def text_reply(msg):  # 处理群消息
    global pai
    global this_num, gamedict, qun_list, chengyu_list, hongbao_list
    talk = msg['Content']
    this = msg['User']['Self']['DisplayName']
    qname = msg['User']['NickName']
    whotalk = msg['ActualNickName']
    who = ''
    if not this:  # 当没有备注时取微信名称
        this = msg['User']['Self']['NickName']
    if not whotalk:
        whotalk = this
    # print(msg['User']['NickName'], msg['User']['Self']['DisplayName'], '--', msg['ActualNickName'], ':', talk)
    logfilename = msg['User']['NickName']
    aa = logfilename.split('/')
    an = ''
    for i in aa:
        an += i
    x = logger.logs(an)
    try:
        x.info(msg['ActualNickName'] + "：" + talk)
    except Exception as e:
        print(e, msg['ActualNickName'] + "：" + talk)
    if msg['isAt']:
        if talk[:1] == '@':
            try:
                new = talk.split()
                users_list = msg['User']['MemberList']
                who = new[0]
                who = who[1:]
                if who == '所有人':
                    return '@' + whotalk + ' 收到~'
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
                # print(whotalk + '@' + who, talk)
                if who == this:
                    if '菜单' in talk or '帮助' in talk or 'help' in talk:
                        # with open('help.txt', encoding='utf-8') as f:
                        #     aa = f.readlines()
                        # f.close()
                        return "自己看看吧，是不是多到眼花\n机器人聊天    成语接龙\n群签到    打劫游戏\n点歌    \n其他功能正在努力开发中"
                    elif '聊天菜单' in talk or '聊天帮助' in talk or '聊天help' in talk:
                        return "@" + whotalk + ': 开始艾特我回复：' + '开始聊天  或  开启聊天  或  机器人聊天\n结束回复：结束聊天  或  关闭聊天  或  不聊了。'
                    elif '成语接龙菜单' in talk or '成语接龙帮助' in talk or '成语接龙help' in talk:
                        return "@" + whotalk + ': 开始艾特我回复：' + '成语接龙  或  打开成语接龙  或  直接说成语\n结束回复：不玩了  或  关闭成语接龙  或  退出。'
                    elif '签到菜单' in talk or '签到帮助' in talk or '签到help' in talk:
                        return "@" + whotalk + ': 开始艾特我回复：签到 '
                    elif '抢劫菜单' in talk or '抢劫帮助' in talk or '抢劫help' in talk:
                        return "@" + whotalk + ': 开始艾特我或他（她）回复：' + '打劫 或 抢劫'
                    elif '成语接龙' in talk or '打开成语接龙' in talk:
                        talk = ''
                        if chengyu_list:
                            for i in chengyu_list:
                                if i == qname:
                                    nn = i
                                    return '@' + whotalk + ' ' + '已经开始成语接龙咯~'
                            else:
                                chengyu_list.append(qname)
                                return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                    elif '不玩了' in talk or '关闭成语接龙' in talk or '退出' in talk:
                        talk = '退出'
                        try:
                            chengyu_list.remove(qname)
                            return '@' + whotalk + ' 成语接龙：' + chengyujielong(talk, qname)
                        except Exception as e:
                            print(e, '该值不存在')
                    elif '课程表' in talk:
                        week_dict = dict(i1='星期一', i2='星期二', i3='星期三', i4='星期四', i5='星期五', i6='星期六', i7='星期日')
                        dayOfWeek = datetime.now().isoweekday()  # 返回数字1-7代表周一到周日
                        return '唉，本喵今天要上的网课就是这些啦：————' + week_dict['i' + str(dayOfWeek)] + '. |\n语文课：【成语接龙】\n课间 ' \
                                                                                           '|\n玩小游戏：【打劫】 \n下午 \n音乐课：【点歌】'
                    elif '签到' in talk:
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
                                return "👻" + whotalk + '签到成功\n👻排名：第' + str(pai) + '名\n👻奖励：' + str(
                                    jifen) + '积分 ' + str(jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                            else:
                                return '亲您已签到过了，请勿重复签到'
                    elif '查询' in talk:
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
                            return "👻[" + whotalk + ']查询成功\n👻签到排名：第' + str(pai) + '名\n👻资产：' + str(
                                jifen) + '积分 ' + str(jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                    elif '抢劫' in talk or '打劫' in talk:
                        if this_num == 0:
                            return "@ " + whotalk + "抢劫失败，机器人资产不足，可回复《兑换》消耗1积分。兑换机器人1000金币~"
                        if whotalk not in gamedict:
                            getpai = 0
                            getjifen = 0
                            getjinbi = 0
                            to = random.randint(0, this_num)
                            getjinbi += to
                            this_num -= to
                            gamedict[whotalk] = getpai, getjifen, getjinbi
                            return '😂[' + whotalk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                        else:
                            nowinfo = gamedict[whotalk]
                            pai = nowinfo[0]
                            jifen = nowinfo[1]
                            getjinbi = nowinfo[2]
                            to = random.randint(0, this_num)
                            getjinbi += to
                            this_num -= to
                            gamedict[whotalk] = pai, jifen, getjinbi
                            return '😂[' + whotalk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                    elif '兑换' in talk:
                        if whotalk not in gamedict:
                            return '很抱歉，您的账户无资产~'
                        else:
                            nowinfo = gamedict[whotalk]
                            pai = nowinfo[0]
                            jifen = nowinfo[1]
                            getjinbi = nowinfo[2]
                            if jifen == 0:
                                return '很抱歉，您的账户积分不足~'
                            jifen -= 1
                            this_num += 1000
                            gamedict[whotalk] = pai, jifen, getjinbi
                            return "@ " + whotalk + "兑换成功，祝您游戏愉快~"
                    elif '点歌' in talk or '播放' in talk:
                        name = talk.split()
                        if len(name) > 1:
                            songname = name[1]
                        elif len(name) == 1:
                            name = talk.split('-')
                            if len(name) > 1:
                                songname = name[1]
                            else:
                                songname = talk[2:]
                                if not songname:
                                    return '亲点歌格式不对哦~ 点歌请艾特我回复点歌 【歌名】'
                        if '排行榜' == songname:
                            return '亲暂未开通排行榜点歌哦~功能持续更新中，敬请期待 点歌请艾特我回复点歌 【歌名】'
                        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1' \
                              '&remoteplace=txt.yqq.song&searchid=55989056282747366&t=0&aggr=1&cr=1&catZhida=1&lossless=0' \
                              '&flag_qc=0&p=1&n=10&w=' + songname + '&g_tk_new_20200303=1945000638&g_tk=654347293&loginUin=1983496818&hostUin=0&format=json' \
                                                                    '&inCharset=utf8&outCharset=utf-8&notice=0&platfin talk orm=yqq.json&needNewCode=0 '
                        res = requests.get(url=url)
                        jm = json.loads(res.text)
                        try:
                            psid = jm['data']['song']['list'][0]['id']
                            songer = jm['data']['song']['list'][0]['singer'][0]['name']
                            songname = jm['data']['song']['list'][0]['title']
                        except Exception as e:
                            return '点歌失败，找不到该歌曲'
                        test = 'https://i.y.qq.com/v8/playsong.html?songid={}&source=yqq#wechat_redirect'.format(psid)
                        return '非常好听的《' + songname + ' - ' + str(songer) + '》来咯~ 点击链接欣赏:\n' + test
                    elif '讲个笑话' in talk or '笑话' in talk or '讲笑话' in talk:
                        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                    elif '讲个故事' in talk or '故事' in talk or '讲故事' in talk:
                        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                    elif '开始聊天' in talk or '开启聊天' in talk or '机器人聊天' in talk:
                        if qun_list:
                            for i in qun_list:
                                if i == msg['User']['NickName']:
                                    nn = i
                                    return '已经开始聊天咯~'
                        else:
                            qun_list.append(qname)
                            return '你们好呀！我的小可爱们'
                    elif '结束聊天' in talk or '关闭聊天' in talk or '不聊了' in talk:
                        try:
                            qun_list.remove(qname)
                            return '拜拜~'
                        except Exception as e:
                            print(e, '该值不存在')
                    elif not talk:
                        # itchat.send('@' + whotalk + '\u2005艾特本喵有何事！')
                        return '@' + whotalk + '\u2005艾特本喵有何事！'
                    if chengyu_list:
                        for n in chengyu_list:
                            if qname == n:
                                return '@' + whotalk + '\u2005成语接龙-我接：' + chengyujielong(talk, qname)
                        else:
                            chengyu_list.append(qname)
                            return '@' + whotalk + '\u2005成语接龙开始咯：' + chengyujielong(talk, qname)
                    if len(talk) == 4:  # 输入成语直接开始成语接龙
                        res = chengyujielong(talk, qname)
                        if res:
                            chengyu_list.append(qname)
                            return '@' + whotalk + " 成语接龙开始咯：" + res
                        else:
                            return '@' + whotalk + '\u2005本喵正专心上网课呢，不跟你聊天哦~不如@我说“课程表”，看看我的日程？'  # else:  #     return itchat.send('@' + whotalk + '\u2005收到！自动回复~')
                elif '抢劫' in talk or '打劫' in talk:
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
        else:
            talk_list = talk.split('@')
            whotalk = '点歌的人'
            # print(talk_list)
            talk1 = talk_list[0]
            talk2 = talk_list[1]
            new = talk2.split()
            users_list = msg['User']['MemberList']
            who = new[0]
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
                                ll = len(insp)
                                if talk2[:ll] == insp:
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
                    print('找不到用户')
            except Exception as e:
                who = ''
            try:
                if ss + 1 < len(new):
                    if ss + 1 != len(new):
                        talk = talk1
                        for i in range(ss + 1, len(new)):
                            if talk == '':
                                talk = talk + new[i]
                            else:
                                talk = talk + ' ' + new[i]
                    else:
                        talk = new[ss + 1]
                else:
                    talk = talk1
            except Exception as e:
                print(e)
                talk = talk1
            print(whotalk + '@' + who, ':' + talk)
            return
    if '开始聊天' in talk or '开启聊天' in talk or '机器人聊天' in talk:
        if qun_list:
            for i in qun_list:
                if i == msg['User']['NickName']:
                    nn = i
                    return '已经开始聊天咯~'
        else:
            qun_list.append(qname)
            return '你们好呀！我的小可爱们'
    elif '结束聊天' in talk or '关闭聊天' in talk or '不聊了' in talk:
        try:
            qun_list.remove(qname)
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif '开启红包提醒' in talk or '开启红包预警' in talk or '红包提示' in talk:
        if hongbao_list:
            for i in hongbao_list:
                if i == msg['User']['NickName']:
                    nn = i
                    return '已经开始提醒咯~'
        else:
            hongbao_list.append(qname)
            return '红包提醒已打开'
    elif '关闭红包提醒' in talk or '关闭红包预警' in talk:
        try:
            hongbao_list.remove(qname)
            return '红包提醒已关闭~'
        except Exception as e:
            print(e, '该值不存在')
    elif qun_list:
        for n in qun_list:
            if qname == n:
                ress = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                re = ress.json()["content"]
                if '{br}' in re:
                    res_list = re.split('{br}')
                    re = '\n'.join(res_list)
                print(n, "--群聊：{}  ({})".format(re, datetime.now()))
                return re


def set_info():
    with open('config1.txt', 'w', encoding='utf-8') as f:
        f.write('.'.join(qun_list))
        f.write('---')
        f.write('.'.join(user_list))
        f.write('---')
        f.write(json.dumps(gamedict))
        f.write('---')
        f.write('.'.join(userchengyu_list))
        f.write('---')
        f.write('.'.join(hongbao_list))
        f.write('---')
        f.write('.'.join(chengyu_list))
        f.write('---')
        f.write(str(this_num))
        f.write('---')
        f.write('.'.join(ana_list))
        f.close()
    return "存档成功"


def get_info():
    global qun_list, user_list, gamedict, userchengyu_list, hongbao_list, chengyu_list, this_num, ana_list
    with open('config1.txt', 'r', encoding='utf-8') as f:
        aa = f.readlines()
        a_list = aa[0].split('---')
        if len(a_list) == 8:
            qun_list = a_list[0].split('.')
            try:
                qun_list.remove('')
            except:
                pass
            user_list = a_list[1].split('.')
            try:
                user_list.remove('')
            except:
                pass
            gamedict = json.loads(a_list[2])
            userchengyu_list = a_list[3].split('.')
            try:
                userchengyu_list.remove('')
            except :
                pass
            hongbao_list = a_list[4].split('.')
            try:
                hongbao_list.remove('')
            except:
                pass
            chengyu_list = a_list[5].split('.')
            try:
                chengyu_list.remove('')
            except:
                pass
            this_num = int(a_list[6])
            ana_list = a_list[7].split('.')
            try:
                ana_list.remove('')
            except:
                pass
            res = "读档成功"
        else:
            res = "读档失败"
        f.close()
    return res


itchat.run()
