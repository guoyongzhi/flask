import json
from datetime import datetime
from datetime import timedelta
import os
import random
import time
import itchat
import logger
import traceback

from static.src.api.chengyujielong import chengyujielong
from static.src.api.count.read_name_all_info import read_name_all_info

import requests

user_list = []
user_idiom_list = []
ana_list = []
ret_dict = dict()


@itchat.msg_register(itchat.content.TEXT)  # 私发消息
def text_reply(msg):  # 处理私人消息
    # msg = "努力上班中，晚点回复！"
    global user_list, user_idiom_list, ana_list, ret_dict
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
                talk_info = ta_list[ss + 1]
                if ss + 2 != len(ta_list):
                    for i in range(ss + 2, len(ta_list)):
                        if talk_info == '':
                            talk_info = talk_info + ta_list[i]
                        else:
                            talk_info = talk_info + ' ' + ta_list[i]
                to_list = who.split(',')
                if not to_list:
                    to_list = who.split('，')
                if to_list:
                    if ty == '@':
                        for i in to_list:
                            if i != '':
                                he_talk = itchat.search_friends(name=i)
                                itchat.send(talk_info, he_talk[0]['UserName'])
                    else:
                        for i in to_list:
                            if i != '':
                                q_talk = itchat.search_chatrooms(name=i)
                                itchat.send(talk_info, q_talk[0]['UserName'])
                return who + ':发送成功'
            except Exception as e:
                print(e)
                return '发送失败'
    if talk == '开始聊天' or talk == '开启聊天':
        if name in user_list:
            return '已经开始聊天咯~'
        user_list.append(str(name))
        return '你好呀！我的小可爱'
    elif talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了':
        try:
            user_list.remove(str(name))
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '成语接龙' or talk == '打开成语接龙':
        talk = ''
        if name in user_idiom_list:
            return '已经开始成语接龙咯~'
        user_idiom_list.append(str(name))
        return chengyujielong(talk, name)
    elif talk == '不玩了' or talk == '关闭成语接龙' or talk == '退出':
        talk = '退出'
        try:
            user_idiom_list.remove(str(name))
            return chengyujielong(talk, name)
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '取消名言名句' or talk == '关闭名言名句' or talk == '退出名言名句':
        try:
            ana_list.remove(str(name))
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif '名言名句' in talk:
        if name in ana_list:
            return '已经开始发送名言名句咯~'
        ana_list.append(str(name))
        return '你好呀！我的小可爱'
    elif '存档' in talk:
        res = set_info()
        return res
    elif '读档' in talk:
        res = get_info()
        return res
    elif name in user_idiom_list:
        return chengyujielong(talk, name)
    elif name in user_list:
        if "小白" in talk:
            talk = talk.replace('小白', '菲菲')
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        if '菲菲' in re:
            re = re.replace('菲菲', '小白')
        print(name, "--私聊：{}  ({})".format(re, datetime.now()))
        return re
    elif name in ana_list:
        a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
        return a.split()[0]
    else:
        talk_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        he_talk = itchat.search_friends(name='机器人_菲菲')
        if name in ret_dict:
            last_time = ret_dict[name]
            lo_time = datetime.strptime(talk_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(last_time,
                                                                                            '%Y-%m-%d %H:%M:%S')
            inner_time = int(timedelta.total_seconds(lo_time) / 60)
            if inner_time > 180:
                itchat.send(name + ':' + talk, he_talk[0]['UserName'])
                ret_dict[name] = talk_time
                return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
            else:
                itchat.send(name + ':' + talk, he_talk[0]['UserName'])
                ret_dict[name] = talk_time
                return
        else:
            ret_dict[name] = talk_time
            itchat.send(name + ':' + talk, he_talk[0]['UserName'])
            return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'


game_dict = dict()
pai = 0
this_num = 0
qun_list = []
idiom_list = []
red_packet_list = []
Num_bomb_dict = dict()


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)  # 群消息（群游戏）
def text_reply(msg):  # 处理群消息
    global pai, this_num, game_dict, qun_list, idiom_list, red_packet_list
    try:
        talk = msg['Content']
        this = msg['User']['Self']['DisplayName']
        qname = msg['User']['NickName']
        who_talk = msg['ActualNickName']
        who = ''
        if not this:  # 当没有备注时取微信名称
            this = msg['User']['Self']['NickName']
        if not who_talk:
            who_talk = this
        log_File_Name = msg['User']['NickName']
        aa = log_File_Name.split('/')
        an = ''
        for i in aa:
            an += i
        x = logger.logs(an)
        try:
            x.info(msg['ActualNickName'] + "：" + talk)
        except Exception as ex:
            print(ex, msg['ActualNickName'] + "：" + talk)
    except Exception as ea:
        print(ea)
        return
    if msg['isAt']:
        if talk[:1] == '@':
            try:
                new = talk.split()
                users_list = msg['User']['MemberList']
                who = new[0]
                who = who[1:]
                if who == '所有人':
                    return '@' + who_talk + ' 收到~'
                dd = 0
                ss = 0
                try:
                    if users_list:
                        while ss <= len(new):
                            for i in users_list:
                                t_name = i['DisplayName']
                                if t_name == '':
                                    t_name = i['NickName']
                                if t_name == who:
                                    dd = 1
                                    break
                            if dd == 1:
                                break
                            else:
                                ss += 1
                                if ss >= len(new):
                                    break
                                joint_name = who + ' ' + new[ss]
                                a = 1
                                ao = 0
                                while ao <= 10:
                                    ll = len(joint_name) + 1
                                    if talk[:ll] == '@' + joint_name:
                                        who = joint_name
                                        break
                                    else:
                                        nn = ' '
                                        for i in range(0, a):
                                            nn += ' '
                                        joint_name = who + nn + new[ss]
                                        a += 1
                                        ao += 1
                    else:
                        who = ''
                        print('找不到用户', msg)
                except Exception as eb:
                    who = ''
                    print('处理用户抱错了', eb, msg)
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
                except Exception as ec:
                    print(ec, msg)
                    talk = ''
                if who == this:
                    if '菜单' in talk or '帮助' in talk or 'help' in talk:
                        return "自己看看吧，是不是多到眼花\n机器人聊天    成语接龙\n群签到    打劫游戏\n点歌    踩雷游戏\n其他功能正在努力开发中"
                    elif '聊天菜单' in talk or '聊天帮助' in talk or '聊天help' in talk:
                        return "@" + who_talk + ': 开始艾特我回复：' + '开始聊天  或  开启聊天  或  机器人聊天\n结束回复：结束聊天  或  关闭聊天  或  不聊了。'
                    elif '成语接龙菜单' in talk or '成语接龙帮助' in talk or '成语接龙help' in talk:
                        return "@" + who_talk + ': 开始艾特我回复：' + '成语接龙  或  打开成语接龙  或  直接说成语\n结束回复：不玩了  或  关闭成语接龙  或  退出。'
                    elif '签到菜单' in talk or '签到帮助' in talk or '签到help' in talk:
                        return "@" + who_talk + ': 开始艾特我回复：签到 '
                    elif '抢劫菜单' in talk or '抢劫帮助' in talk or '抢劫help' in talk:
                        return "@" + who_talk + ': 开始艾特我或他（她）回复：' + '打劫 或 抢劫'
                    elif '成语接龙' in talk or '打开成语接龙' in talk:
                        talk = ''
                        if qname in idiom_list:
                            return '@' + who_talk + ' ' + '已经开始成语接龙咯~'
                        idiom_list.append(qname)
                        return '@' + who_talk + ' 成语接龙：' + chengyujielong(talk, qname)
                    elif '不玩了' in talk or '关闭成语接龙' in talk or '退出' in talk:
                        talk = '退出'
                        try:
                            idiom_list.remove(qname)
                            return '@' + who_talk + ' 成语接龙：' + chengyujielong(talk, qname)
                        except Exception as e:
                            print(e, '该值不存在')
                    elif '课程表' in talk:
                        week_dict = dict(i1='星期一', i2='星期二', i3='星期三', i4='星期四', i5='星期五', i6='星期六', i7='星期日')
                        dayOfWeek = datetime.now().isoweekday()  # 返回数字1-7代表周一到周日
                        return '唉，本喵今天要上的网课就是这些啦：————' + week_dict[
                            'i' + str(dayOfWeek)] + '. |\n语文课：【成语接龙】\n课间 ' '|\n玩小游戏：【打劫】 \n下午 \n音乐课：【点歌】'
                    elif '签到' in talk:
                        if who_talk not in game_dict:
                            pai += 1
                            qiandaojifen = 10
                            qiandaojinbi = 500
                            game_dict[who_talk] = pai, qiandaojifen, qiandaojinbi
                            now = time.strftime("%H:%M:%S")
                            return "👻[" + who_talk + ']签到成功\n👻排名：第' + str(pai) + '名\n👻奖励：' + str(
                                qiandaojifen) + '积分 ' + str(qiandaojinbi) + '金币\n👻头衔：新手上路\n👻时间：' + str(now)
                        else:
                            now_info = game_dict[who_talk]
                            d_pai = now_info[0]
                            jifen = now_info[1]
                            jinbi = now_info[2]
                            if pai == 0:
                                d_pai += 1
                                jifen += 10
                                jinbi += 500
                                game_dict[who_talk] = pai, jifen, jinbi
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
                                return "👻" + who_talk + '签到成功\n👻排名：第' + str(pai) + '名\n👻奖励：' + str(
                                    jifen) + '积分 ' + str(jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                            else:
                                return '亲您已签到过了，请勿重复签到'
                    elif '查询' in talk:
                        if who_talk not in game_dict:
                            return '您今天未签到哦~'
                        nowinfo = game_dict[who_talk]
                        t_pai = nowinfo[0]
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
                        if t_pai == 0:
                            return "👻[" + who_talk + ']查询成功\n👻签到排名：未签到\n👻资产：' + str(jifen) + '积分 ' + str(
                                jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                        else:
                            return "👻[" + who_talk + ']查询成功\n👻签到排名：第' + str(t_pai) + '名\n👻资产：' + str(
                                jifen) + '积分 ' + str(jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
                    elif '抢劫' in talk or '打劫' in talk:
                        if this_num == 0:
                            return "@ " + who_talk + " 抢劫失败，机器人资产不足，可回复《兑换》消耗1积分。兑换机器人1000金币~"
                        if who_talk not in game_dict:
                            getpai = 0
                            getjifen = 0
                            getjinbi = 0
                            to = random.randint(0, this_num)
                            getjinbi += to
                            this_num -= to
                            game_dict[who_talk] = getpai, getjifen, getjinbi
                            return '😂[' + who_talk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                        else:
                            nowinfo = game_dict[who_talk]
                            set_pai = nowinfo[0]
                            jifen = nowinfo[1]
                            getjinbi = nowinfo[2]
                            to = random.randint(0, this_num)
                            getjinbi += to
                            this_num -= to
                            game_dict[who_talk] = set_pai, jifen, getjinbi
                            return '😂[' + who_talk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫n次！'
                    elif '兑换' in talk:
                        if who_talk not in game_dict:
                            return '很抱歉，您的账户无资产~'
                        else:
                            nowinfo = game_dict[who_talk]
                            t_pai = nowinfo[0]
                            jifen = nowinfo[1]
                            getjinbi = nowinfo[2]
                            if jifen == 0:
                                return '很抱歉，您的账户积分不足~'
                            jifen -= 1
                            this_num += 1000
                            game_dict[who_talk] = t_pai, jifen, getjinbi
                            return "@ " + who_talk + "兑换成功，祝您游戏愉快~"
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
                              '&remoteplace=txt.yqq.song&searchid=55989056282747366&t=0&aggr=1&cr=1&catZhida=1&' \
                              'lossless=0&flag_qc=0&p=1&n=10&w=' + songname + '&g_tk_new_20200303=1945000638&' \
                                                                              'g_tk=654347293&loginUin=1983496818&' \
                                                                              'hostUin=0&format=json&inCharset=utf8&' \
                                                                              'outCharset=utf-8&notice=0&' \
                                                                              'platfin talk orm=yqq.json&needNewCode=0 '
                        res = requests.get(url=url)
                        jm = json.loads(res.text)
                        try:
                            psid = jm['data']['song']['list'][0]['id']
                            songer = jm['data']['song']['list'][0]['singer'][0]['name']
                            songname = jm['data']['song']['list'][0]['title']
                        except Exception:
                            return '点歌失败，找不到该歌曲'
                        test = "https://i.y.qq.com/v8/playsong.html?songid={}&source=yqq#wechat_redirect".format(psid)
                        return '非常好听的《' + songname + ' - ' + str(songer) + '》来咯~ 点击链接欣赏:\n' + test
                    elif '讲个笑话' in talk or '笑话' in talk or '讲笑话' in talk:
                        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                    elif '讲个故事' in talk or '故事' in talk or '讲故事' in talk:
                        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
                    elif '开始聊天' in talk or '开启聊天' in talk or '机器人聊天' in talk:
                        if qname in qun_list:
                            return '已经开始聊天咯~'
                        qun_list.append(qname)
                        return '你们好呀！我的小可爱们'
                    elif '结束聊天' in talk or '关闭聊天' in talk or '不聊了' in talk:
                        try:
                            qun_list.remove(qname)
                            return '拜拜~'
                        except Exception as e:
                            print(e, '该值不存在')
                    elif not talk:
                        return '@' + who_talk + '\u2005艾特本喵有何事！'
                    elif '踩雷' in talk or '数字炸弹' == talk:
                        if qname in Num_bomb_dict:
                            a1, c, d = Num_bomb_dict[qname]
                            return '踩雷游戏已开启，当前 ' + c + ' 到 ' + d + " 呢!"
                        Num_bomb_dict[qname] = random.randint(0, 100), 0, 100
                        return "你好呀！我的小可爱。踩雷开始咯 当前 0 到 100 呢"
                    elif talk == '取消踩雷' or talk == '关闭踩雷' or talk == '退出踩雷':
                        try:
                            del Num_bomb_dict[str(qname)]
                            return '拜拜~'
                        except Exception as e:
                            print(e, '该值不存在')
                    elif qname in Num_bomb_dict:
                        Num = -1
                        try:
                            Num = int(talk)
                        except Exception as e:
                            print("非踩雷", e)
                        if Num != -1:
                            try:
                                a1, c, d = Num_bomb_dict[qname]
                                if a1 == -1:
                                    a1 = random.randint(0, 100)
                                    c = 0
                                    d = 100
                                if Num <= c or Num >= d:
                                    return '@' + who_talk + " 输入错误，请输入：" + str(c) + " 到" + str(d) + "的数字"
                                elif Num > a1:
                                    d = Num
                                    Num_bomb_dict[qname] = a1, c, d
                                    return '@' + who_talk + " 恭喜您未中雷，请继续：" + str(c) + " 到" + str(d) + "的数字"
                                elif Num < a1:
                                    c = Num
                                    Num_bomb_dict[qname] = a1, c, d
                                    return '@' + who_talk + " 恭喜您未中雷，请继续：" + str(c) + " 到" + str(d) + "的数字"
                                elif Num == a1:
                                    a1 = -1
                                    Num_bomb_dict[qname] = a1, c, d
                                    return '@' + who_talk + " 踩雷了，本轮已结束。继续请继续输入数字。"
                                else:
                                    Num_bomb_dict[qname] = a1, c, d
                                    return '@' + who_talk + " 输入错误，请输入：" + str(c) + "到" + str(d) + "的数字"
                            except Exception as e:
                                print("处理踩雷异常了", e)
                    if qname in idiom_list:
                        return '@' + who_talk + '\u2005成语接龙-我接：' + chengyujielong(talk, qname)
                    if len(talk) == 4:  # 输入成语直接开始成语接龙
                        res = chengyujielong(talk, qname)
                        if res:
                            idiom_list.append(qname)
                            return '@' + who_talk + " 成语接龙开始咯：" + res
                        else:
                            return '@' + who_talk + '\u2005本喵正专心上网课呢，不跟你聊天哦~不如@我说“课程表”，看看我的日程？'
                    else:
                        return '@' + who_talk + '\u2005很抱歉~没明白您的意思呢'
                elif '抢劫' in talk or '打劫' in talk:
                    try:
                        getpai = 0
                        getjifen = 0
                        getjinbi = 0
                        if who_talk in game_dict:
                            whoget = game_dict[who_talk]
                            getpai = whoget[0]
                            getjifen = whoget[1]
                            getjinbi = whoget[2]
                        if who not in game_dict:
                            return '打劫失败，对方无资产！'
                        whoset = game_dict[who]
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
                                    game_dict[who_talk] = getpai, getjifen, getjinbi
                                    game_dict[who] = setpai, setjifen, setjinbi
                                    return '😂[' + who_talk + '] 抢劫 [' + who + '] 成功，抢走了对方' + str(
                                        to) + '金币！\n⚠您还可以抢劫n次！'
                            else:
                                to = random.randint(0, getjinbi)
                                setjinbi += to
                                getjinbi -= to
                                game_dict[who_talk] = getpai, getjifen, getjinbi
                                game_dict[who] = setpai, setjifen, setjinbi
                                return '😂[' + who_talk + '] 抢劫 [' + who + '] 失败，反被对方抢走了' + str(to) +\
                                       '金币！\n⚠您还可以抢劫n次！'
                        else:
                            return '打劫失败，对方无资产！'
                    except Exception as e:
                        return '报错了' + str(e)
            except Exception as e:
                print('报错了',
                      e)
                # else:
                #     talk_list = talk.split('@')
                #     who_talk = '点歌的人'  #
                # print(talk_list)
                #     talk1 = talk_list[0]
                #     talk2 = talk_list[1]
                #     new = talk2.split()
                #     users_list = msg['User']['MemberList']
                #     who = new[0]
                #     dd = 0
                #     ss = 0
                #     try:
                #         if users_list:
                #             while ss <= len(new):
                #                 for i in users_list:
                #                     tname = i['DisplayName']
                #                     if tname == '':
                #                         tname = i['NickName']
                #                     if tname == who:
                #                         dd = 1
                #                         break
                #                 if dd == 1:
                #                     break
                #                 else:
                #                     ss += 1
                #                     if ss >= len(new):
                #                         break
                #                     joint_name = who + ' ' + new[ss]
                #                     a = 1
                #                     ao = 0
                #                     while ao <= 10:
                #                         ll = len(joint_name)
                #                         if talk2[:ll] == joint_name:
                #                             who = joint_name
                #                             break
                #                         else:
                #                             nn = ' '
                #                             for i in range(0, a):
                #                                 nn += ' '
                #                             joint_name = who + nn + new[ss]
                #                             a += 1
                #                             ao += 1
                #         else:
                #             who = ''
                #             print('找不到用户')
                #     except Exception as e:
                #         who = ''
                #     try:
                #         if ss + 1 < len(new):
                #             if ss + 1 != len(new):
                #                 talk = talk1
                #                 for i in range(ss + 1, len(new)):
                #                     if talk == '':
                #                         talk = talk + new[i]
                #                     else:
                #                         talk = talk + ' ' + new[i]
                #             else:
                #                 talk = new[ss + 1]
                #         else:
                #             talk = talk1
                #     except Exception as e:
                #         print(e)
                #         talk = talk1
                #     print(who_talk + '@' + who, ':' + talk)
                #     return
    if '开始聊天' in talk or '开启聊天' in talk or '机器人聊天' in talk:
        if qname in qun_list:
            return '已经开始聊天咯~'
        qun_list.append(qname)
        return '你们好呀！我的小可爱们'
    elif '结束聊天' in talk or '关闭聊天' in talk or '不聊了' in talk:
        try:
            qun_list.remove(qname)
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif '开启红包提醒' in talk or '开启红包预警' in talk or '红包提示' in talk:
        if qname in red_packet_list:
            return '已经开启红包提醒咯~'
        red_packet_list.append(qname)
        return '红包提醒已打开'
    elif '关闭红包提醒' in talk or '关闭红包预警' in talk:
        try:
            red_packet_list.remove(qname)
            return '红包提醒已关闭~'
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '取消名言名句' or talk == '关闭名言名句' or talk == '退出名言名句':
        try:
            ana_list.remove(str(qname))
            return '拜拜~'
        except Exception as e:
            print(e, '该值不存在')
    elif '名言名句' in talk:
        if qname in ana_list:
            return '已经开始发送名言名句咯~'
        ana_list.append(str(qname))
        return '你好呀！我的小可爱'
    elif qname in qun_list:
        if "小白" in talk:
            talk = talk.replace('小白', '菲菲')
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        if '菲菲' in re:
            re = re.replace('菲菲', '小白')
        print(qname, "--群聊：{}  ({})".format(re, datetime.now()))
        return re
    elif qname in ana_list:
        a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
        return a.split()[0]
    else:
        if who == this:
            return "抱歉~ 暂时不明白您说什么呢"


@itchat.msg_register(itchat.content.NOTE)  # 通知类
def note_rep(msg):
    # print(msg)
    print('来通知了', msg)


@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)  # 通知类
def note_reply(msg):
    # print("通知消息来了", msg)
    qname = msg['User']['UserName']
    try:
        t_name = msg['User']['NickName']
    except Exception as e:
        t_name = ''
        print(e)
        print(msg)
    now = time.strftime("%H:%M:%S")
    time_local = time.localtime(msg['CreateTime'])
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%H:%M:%S", time_local)
    if now > dt:
        print(t_name + dt + "now" + now)
        now = dt
    talk = '发红包了 时间：' + now
    this = msg['User']['Self']['NickName']
    if '收到红包，请在手机上查看' == msg['Content']:
        if t_name in red_packet_list:
            itchat.send(talk, qname)
        return
    elif '加入了群聊' in msg['Content']:
        new = msg['Content'].split()
        s = new[0].split('"')
        if len(s) >= 4:
            if s[4] == '加入了群聊':
                itchat.send(msg['Content'], qname)
                if '珠峰' in t_name:
                    itchat.send('欢迎"' + s[3] + '"新朋友，出来报道，请爆照.积极发言，发红包,多参加活动 分享过去的活动图片'\
                                                '！不可以发与珠峰群无关的广告，链接和小程序！否则请出！谢谢配合！', qname)
                else:
                    itchat.send('欢迎"' + s[3] + '"新朋友', qname)
                return
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
    msg.download(PICTURE_dir + '\\' + msg.fileName)  # print('私发图片了', msg)


@itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)  # 群图片类
def PICTURE_reply(msg):
    if os.path.exists(PICTURE_dir) and os.path.isdir(PICTURE_dir):
        pass
    else:
        os.mkdir(PICTURE_dir)
    msg.download(PICTURE_dir + '\\' + msg.fileName)  # print('群发发图片了', msg)


RECORDING_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\RECORDING')


@itchat.msg_register(itchat.content.RECORDING, itchat.content.VOICE)  # 录音类
def RECORDING_rep(msg):
    if os.path.exists(RECORDING_dir) and os.path.isdir(RECORDING_dir):
        pass
    else:
        os.mkdir(RECORDING_dir)
    msg.download(RECORDING_dir + '\\' + msg.fileName)  # print('私发发录音了', msg)


@itchat.msg_register(itchat.content.RECORDING, itchat.content.VOICE, isGroupChat=True)  # 群录音类
def RECORDING_reply(msg):
    if os.path.exists(RECORDING_dir) and os.path.isdir(RECORDING_dir):
        pass
    else:
        os.mkdir(RECORDING_dir)
    msg.download(RECORDING_dir + '\\' + msg.fileName)  # print('群录音消息：', msg)


ATTACHMENT_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file\ATTACHMENT')


@itchat.msg_register(itchat.content.ATTACHMENT)  # 附件类
def ATTACHMENT_rep(msg):
    if os.path.exists(ATTACHMENT_dir) and os.path.isdir(ATTACHMENT_dir):
        pass
    else:
        os.mkdir(ATTACHMENT_dir)
    msg.download(ATTACHMENT_dir + '\\' + msg.fileName)  # print('私发附件了', msg)


@itchat.msg_register(itchat.content.ATTACHMENT, isGroupChat=True)  # 群附件类
def ATTACHMENT_reply(msg):
    if os.path.exists(ATTACHMENT_dir) and os.path.isdir(ATTACHMENT_dir):
        pass
    else:
        os.mkdir(ATTACHMENT_dir)
    msg.download(ATTACHMENT_dir + '\\' + msg.fileName)  # print('群发发附件了', msg)


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


def set_info():
    with open('config.txt', 'w', encoding='utf-8') as file:
        file.write('.'.join(qun_list))
        file.write('---')
        file.write('.'.join(user_list))
        file.write('---')
        file.write(json.dumps(game_dict))
        file.write('---')
        file.write('.'.join(user_idiom_list))
        file.write('---')
        file.write('.'.join(red_packet_list))
        file.write('---')
        file.write('.'.join(idiom_list))
        file.write('---')
        file.write(str(this_num))
        file.write('---')
        file.write('.'.join(ana_list))
        file.close()
    return "存档成功"


def get_info():
    global qun_list, user_list, game_dict, user_idiom_list, red_packet_list, idiom_list, this_num, ana_list
    with open('config.txt', 'r', encoding='utf-8') as file:
        aa = file.readlines()
        a_list = aa[0].split('---')
        if len(a_list) == 8:
            qun_list = a_list[0].split('.')
            try:
                qun_list.remove('')
            except Exception:
                pass
            user_list = a_list[1].split('.')
            try:
                user_list.remove('')
            except Exception:
                pass
            game_dict = json.loads(a_list[2])
            user_idiom_list = a_list[3].split('.')
            try:
                user_idiom_list.remove('')
            except Exception:
                pass
            red_packet_list = a_list[4].split('.')
            try:
                red_packet_list.remove('')
            except Exception:
                pass
            idiom_list = a_list[5].split('.')
            try:
                idiom_list.remove('')
            except Exception:
                pass
            this_num = int(a_list[6])
            ana_list = a_list[7].split('.')
            try:
                ana_list.remove('')
            except Exception:
                pass
            res = "读档成功"
        else:
            res = "读档失败"
        file.close()
    return res


if __name__ == '__main__':
    try:
        # 登录
        itchat.auto_login()
        
        # # 发送消息
        # itchat.send(u'你好', 'filehelper')
        # 获取好友列表
        # friends = itchat.get_friends(update=True)
        # 初始化计数器，有男有女，当然，有些人是不填的
        # male = female = other = 0
        
        # 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算 1表示男性，2女性
        # for i in friends[1:]:
        #     # print(i)
        #     sex = i["Sex"]
        #     if sex == 1:
        #         male += 1
        #     elif sex == 2:
        #         female += 1
        #     else:
        #         other += 1
        
        # 总数算上，好计算比例啊～
        # total = len(friends[1:])
        # print('好友总数', total)
        # print(u"男性好友：%.2f%%" % (float(male) / total * 100))
        # print(u"女性好友：%.2f%%" % (float(female) / total * 100))
        # print(u"其他：%.2f%%" % (float(other) / total * 100))
        itchat.run()
    except Exception:
        with open('chat/error.log', 'a') as f:
            f.write('*' * 100 + "\n")
            f.write(traceback.format_exc())  # 使用 traceback.format_exc() 获取异常详细信息
            f.write('*' * 100 + "\n")
