import json
import threading
from datetime import datetime
from datetime import timedelta
import os
import random
import time
from functools import lru_cache
import logger

from static.src.api.chengyujielong import *
from static.src.api.count.read_name_all_info import read_name_all_info
from static.src.api.config.get_game_config import Config
from static.src.api.base.top_search import main as search
from axf.dbredis import db_redis
from static.src.api.data.game_views import execute_sql_lite
from static.src.api.base.robot_chat import robot_chat
from static.src.api.base.rob import Rob
from static.src.api.base.find_music import find_music
from static.src.api.base.common import get_nickname, is_talk_keyword
from static.src.api.base.probability import probability
from wxpy import *

import requests

user_list = []
user_idiom_list = []
ana_list = []
ret_dict = dict()
At_who = '机器人_菲菲'

bot = Bot(cache_path=True)
# 账号自身
myself = bot.self


@bot.register(Friend)
def Chat_reply(msg):
    global user_list, user_idiom_list, ana_list, ret_dict, At_who
    talk = msg.text
    if not talk:
        talk = ''
    try:
        name = msg.sender.name
        if not name:
            name = msg.member.name
    except Exception:
        name = msg.sender.name
        if not name:  # 当没有备注时取微信名称
            name = msg.member.name
    if name == At_who:
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
                                he_talk = bot.friends().search(i)
                                he_talk[0].send_msg(msg=talk_info)
                    else:
                        for i in to_list:
                            if i != '':
                                q_talk = bot.groups().search(name=i)
                                q_talk[0].send_msg(msg=talk_info)
                return who + ':发送成功'
            except Exception as e:
                print(e)
                return '发送失败'
    if is_talk_keyword(talk, ['开始聊天', '开启聊天']):
        # talk_list = db_redis(db=3).get_owner(owner=fromUserName)
        # print(talk_list)
        if name in user_list:
            return '已经开始聊天咯~'
        user_list.append(str(name))
        db_redis(db=3).set_value(name=name, value=str(user_list))
        return '你好呀！我的小可爱'
    elif talk == '结束聊天' or talk == '关闭聊天' or talk == '不聊了' or talk == '闭嘴':
        try:
            talk_list = db_redis(db=3).r.keys()
            # print(talk_list)
            user_list.remove(str(name))
            d_name = db_redis(db=3).delete(name)
            if d_name:
                print("删除成功")
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
    elif '名言名句' == talk:
        if name in ana_list:
            return '已经开始发送名言名句咯~'
        ana_list.append(str(name))
        return '你好呀！我的小可爱'
    elif '存档' == talk:
        res = set_info()
        return res
    elif '读档' == talk:
        res = get_info()
        return res
    elif '清除签到记录' == talk:
        func(keep_on=False)
        return "ok"
    elif '设置转发' == talk[:4]:
        At_who = talk[4:]
    elif '重载' in talk:
        # itchat.logout()
        # itchat.auto_login(hotReload=True, enableCmdQR=True)
        return 'OK'
    elif '获取群信息' in talk:
        try:
            bot.groups(update=True)
            group_fzr = bot.groups().search(u'白云山')[0]
            print(group_fzr)
            members_list = []
            for fzr in group_fzr.members:
                print(fzr.name, fzr.is_friend, fzr.name, fzr.nick_name, fzr.display_name)
                members_list.append(fzr)  # print fzr.is_friend, fzr.name, fzr.nick_name
            print(len(members_list))
            members_set = set(members_list)
            # print(len(members_set))
            # for mem in members_set:
            #     print(mem.name, mem.is_friend, mem.name, mem.nick_name, mem.display_name)
        except Exception as e:
            print(e)
    elif '退出' == talk:
        stop()
    elif name in user_idiom_list:
        return chengyujielong(talk, name)
    elif name in user_list:
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        print(name, "--私聊：{}  ({})".format(re, datetime.now()))
        return re
    elif name in ana_list:
        a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
        return a.split()[0]
    else:
        talk_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        he_talk = bot.friends().search(name=At_who)
        if not he_talk:
            return
        if name in ret_dict:
            last_time = ret_dict[name]
            lo_time = datetime.strptime(talk_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(last_time,
                                                                                            '%Y-%m-%d %H:%M:%S')
            inner_time = int(timedelta.total_seconds(lo_time) / 60)
            if inner_time > 180:
                msg.forward(chat=he_talk[0], prefix=name)
                ret_dict[name] = talk_time  # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
            else:
                msg.forward(chat=he_talk[0], prefix=name)
                ret_dict[name] = talk_time
                return
        else:
            ret_dict[name] = talk_time
            msg.forward(chat=he_talk[0], prefix=name)  # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
    if msg.is_at:
        print(msg)
    return


game_dict = dict()
pai: int = 0
this_num = 0
qun_list = []
idiom_list = []
red_packet_list = []
Num_bomb_dict = dict()
sign_in_list = []
welcome = goodbye = ''
esl: object = None
robNum: int = 0
minRewardPoint: int = 0
rewardPoint: int = 0
minRewardGold: int = 0
rewardGold: int = 0
luck_draw: int = 0


# sqlite 重载
@lru_cache(maxsize=10, typed=False)
def refresh_sqlite():
    global esl
    a = 0
    while a < 3:
        try:
            if not esl:
                esl = execute_sql_lite()
                if esl:
                    break
        except Exception:
            a += 1
    return esl


spam_dict = dict()


@bot.register(Group)
def Group_reply(msg):
    global game_dict, qun_list, idiom_list, red_packet_list, Num_bomb_dict, sign_in_list, esl, robNum,\
        rewardPoint, rewardGold
    # print(msg.text, msg.sender.name, msg.member.name, msg.receiver.name, msg.type)
    if msg.type in ['Sharing']:
        return
    if msg.type in ['Video', 'Picture', 'Attachment', 'Recording']:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'file')
        path = os.path.join(path, str(msg.type.upper()))
        if os.path.exists(path) and os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        msg.get_file(path + '\\' + msg.file_name)
        return
    try:
        # print(msg)
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
        ActualUserName = msg.raw.get('FromUserName')  # 用户名称（腾讯用内置）
        talk = msg.text
        if talk is None:
            talk = ''
        if '- - - - - - - - - - - - - - -' in talk:
            talk = talk.split('\n- - - - - - - - - - - - - - -\n')[1]
        group = bot.groups().search(msg.sender.name)[0]
        this = group.self.name
        qname = msg.sender.name
        qun_user_name = ActualUserName
        if talk:
            if qname not in spam_dict:
                spam_dict[qname] = round(time.time(), 3), talk, 0
            else:
                last_time, last_talk, count = spam_dict[qname]
                now_time = round(time.time(), 3)
                if float(now_time - last_time) < 1 and last_talk == talk:
                    count += 1
                    spam_dict[qname] = now_time, talk, count
                    if count == 3:
                        return "别刷屏"
                    else:
                        return
                else:
                    count = 0
                spam_dict[qname] = now_time, talk, count
        who = ''
        # 转存群名称，群ID  sqlite
        qun_keys_list = db_redis(15).get_db_keys()
        if qname == '':
            qname = qun_user_name
        else:
            if qun_user_name in qun_keys_list:
                qun_dict = json.loads(db_redis(15).get_owner(qun_user_name))
                qun_id = qun_dict['qun_id']
                qun_dict['qname'] = qname
                result = esl.update_delete_sql("update GroupChat set name=? where id=?", qname, qun_id)
                if result == 'ok':
                    db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
                    db_redis(15).delete(qun_user_name)
                else:
                    print("修改表名称失败")
        if qname in qun_keys_list:
            qun_dict = json.loads(db_redis(15).get_owner(qname))
        else:  # redis + sqlite 存储
            esl.insert_sql(table_name='GroupChat', sql=[qname, qun_user_name])
            time.sleep(0.05)
            qun_list = esl.select_run("select id from GroupChat where name=?", qname)
            qun_id = 0
            if qun_list:
                for rq in qun_list:
                    qun_id = rq[0]
            db_redis(15).set_value(name=qname, value=json.dumps(
                {"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0, "robot_type": 0, "red_packet": False},
                ensure_ascii=False))
            qun_dict = {"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0, "robot_type": 0, "red_packet": False}
        if msg.type == 'Note':
            try:
                t_name = qname
            except Exception as e:
                t_name = ''
                print(e)
                print(msg)
            now = time.strftime("%H:%M:%S")
            time_local = msg.create_time
            # print(time_local, type(time_local))
            # 转换成新的时间格式(2016-05-05 20:28:54)
            # dt = time.strftime("%H:%M:%S", time_local)
            # if now > dt:
            #     print(t_name + dt + "now" + now)
            #     now = dt
            talk = '发红包了 时间：' + now
            if '收到红包，请在手机上查看' == msg.text:
                if 'red_packet' in qun_dict:
                    if qun_dict['red_packet']:
                        return talk
                return
            elif '加入了群聊' in msg.text:
                new = msg.text.split()
                s = new[0].split('"')
                if len(s) >= 4:
                    if s[4] == '加入了群聊':
                        if '车场' in t_name:
                            return
                        elif '广州富豪名媛群' not in t_name:
                            group.send_msg(msg.text)
                        if '珠峰' in t_name:
                            group.send_msg('欢迎"' + s[
                                3] + '"新朋友，出来报道，请爆照.积极发言，发红包,多参加活动' + ' ' + '分享过去 的活动图片！'
                                           + '不可以发与珠峰群无关的广告，链接和小程序！否则请出！谢谢配合！')
                        elif '粤宋堂' in t_name:
                            group.send_msg('欢迎"' + s[3] + '"新朋友，新人进群改备注（注意备注格式），发红包！')
                        elif '广州富豪名媛群' in t_name:
                            group.send_msg('欢迎"' + s[3] + '"新朋友，新人进群请详阅公告，改备注（注意备注格式），爆照发红包！')
                        else:
                            group.send_msg('欢迎"' + s[3] + '"新朋友')
                        return
            elif '拍了拍' in msg.text:
                new = msg.text.split()
                s = new[0].split('"')
                if '车场' in t_name:
                    return
            elif msg.text == '"' + msg.member.name + '" 撤回了一条消息':
                print(msg.member.name, '撤回了一条消息')
            else:
                print("什么也没有" + now, msg)
            return
        who_talk = msg.member.name
        if not who_talk:
            return
        users_key_list = db_redis(14).get_db_keys()
        if str(qun_dict['qun_id']) + '_' + who_talk in users_key_list:
            values_dict_who_talk = json.loads(db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who_talk))
            who_talk_id = values_dict_who_talk['user_id']
            result = esl.update_delete_sql("update users set point=?, gold=? where id=? and GroupChat_ID=?",
                                           values_dict_who_talk['point'], values_dict_who_talk['gold'], who_talk_id,
                                           qun_dict['qun_id'])
            if result != 'ok':
                print("同步失败" + result)
        else:  # redis + sqlite 存储
            if who_talk:
                sql = "select max(id) from users where name=? and GroupChat_ID=?"
                who_talk_list = esl.select_run(sql, who_talk, qun_dict['qun_id'])
                if not who_talk_list[0][0]:
                    result = esl.insert_sql(table_name='users',
                                            sql=[qun_dict['qun_id'], who_talk, '', ActualUserName, 0, 0, 0, 0, 0, 0,
                                                 nowTime, '0-0-0'])
                    time.sleep(0.05)
                    if result == 'ok':
                        sql = "select max(id) from users where name=? and GroupChat_ID=?"
                        who_talk_list = esl.select_run(sql, who_talk, qun_dict['qun_id'])
                        if who_talk_list:
                            who_talk_id = who_talk_list[0][0]
                            if who_talk_id == 0:
                                print("当前用户id为0")
                                return
                            if not who_talk_id:
                                return
                            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk, value=json.dumps(
                                {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                                 "luck_draw": 0, "RobCount": "0-0-0"}, ensure_ascii=False))
                            values_dict_who_talk = {"user_id": who_talk_id, "sign_toList": 0, "point": 0,
                                                    "gold": 0, "robNum": robNum, "luck_draw": 0, "RobCount": "0-0-0"}
                        else:
                            return
                    else:
                        print("插入语句失败", result)
                        return
                else:
                    who_talk_id = who_talk_list[0][0]
                    if not who_talk_id:
                        print(who_talk, qun_dict['qun_id'], who_talk_id, '为none', who_talk_list)
                        return
                    if who_talk_id == 0:
                        print("当前用户id为0")
                        return
                    if db_redis(14).r.exists(str(qun_dict['qun_id']) + '_' + who_talk):
                        print("已找到用户")
                        values_dict_who_talk = json.loads(db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' +
                                                                                 who_talk))
                    else:
                        db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk, value=json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "RobCount": "0-0-0"}, ensure_ascii=False))
                        values_dict_who_talk = json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "luck_draw": 0, "RobCount": "0-0-0"}, ensure_ascii=False)
            else:
                values_dict_who_talk = {}
        aa = qname.split('/')
        an = ''
        for i in aa:
            an += i
        x = logger.logs(an)
        try:
            x.info(who_talk + "：" + talk)
        except Exception as ex:
            print(ex, who_talk + "：" + talk)
    except Exception as ea:
        print(ea)
        return
    if '@' in talk:
        # 拆分语言
        now_talk = talk.split('@')
        Users_list = group
        if now_talk[0] == '':
            del now_talk[0]
        if talk[:1] == '@':  # 艾特一人（首位）
            try:
                new = talk.split()
                who = new[0]
                who = who[1:]
                if '所有人' in who:
                    # return '@' + who_talk + ' 收到~'
                    return
            except Exception as e:
                print('报错了', e)
                return
            ss = 0
            ns = 0
            try:
                if Users_list:
                    while ss <= len(new):
                        ns += 1
                        if ns > 20:
                            who = ''
                            break
                        isOK = group.search(who.replace('🌼', '🌻'))
                        # print(isOK)
                        if not isOK:
                            print("isOK 为空", isOK)
                            two_OK = group.search(who[:1])
                            if not two_OK:
                                who = ''
                                break
                            else:
                                if len(two_OK) == 1:
                                    who = two_OK[0].name
                                    break
                                isOK = two_OK
                        if len(isOK) > 1:
                            p_list = []
                            for i in isOK:
                                name = i.name
                                if not name:
                                    name = i.nick_name
                                if talk[1:len(name) + 1] == name:
                                    p_list.append(name)
                            if len(p_list) == 1:
                                try:
                                    who = p_list[0]
                                except Exception as e:
                                    print(e, 436)
                                break
                        elif len(isOK) == 1:
                            try:
                                who = isOK[0].name
                            except Exception as e:
                                print(e, 442)
                            break
                        ss += 1
                        if ss >= len(new) + 3:
                            who = ''
                            break
                        joint_name = who + ' '
                        a = 1
                        ao = 0
                        d = 0
                        while ao <= 10:
                            ll = len(joint_name) + 1
                            if talk[:ll] == '@' + joint_name:
                                who = joint_name
                                break
                            else:
                                if d == 0:
                                    ss -= 1
                                    joint_name = who + new[ss - 1]
                                    d += 1
                                else:
                                    ns = ' '
                                    for i in range(0, a):
                                        ns += ' '
                                    joint_name = who + ns + new[ss]
                                    a += 1
                            ao += 1
                else:
                    who = ''
                    print('找不到用户', 470)
            except Exception as eb:
                who = ''
                print('处理用户抱错了', eb, 473)
            try:
                # print("talk---" + talk[(len(who) + 1):].replace(' ', ''))
                if '' in who:
                    ss += 1
                if ss < len(new):
                    if ss != len(new):
                        if ss == 0:
                            ss += 1
                        talk = ''
                        for i in range(ss, len(new)):
                            if talk == '':
                                talk = talk + new[i]
                            else:
                                talk = talk + ' ' + new[i]
                    else:
                        talk = new[ss]
                else:
                    talk = ''
            except Exception as ec:
                print(ec, msg)
                talk = ''  # print(ss, '----')
        elif len(now_talk) > 2:  # 处理艾特多人（先不处理）
            return
        else:  # 艾特一人（话语在首位）
            try:
                a_talk = now_talk
                b_talk = a_talk[0]
                who = a_talk[1]
                if '' in who:
                    now_talk = who.split()
                    who = now_talk[0]
                if '所有人' in who:
                    # '@' + who_talk + ' 收到~'
                    return
            except Exception as e:
                print('报错了', e)
                return
            ss = 0
            try:
                if Users_list:
                    while ss <= len(now_talk):
                        isOK = group.search(who)
                        # print(isOK)
                        if not isOK:
                            break
                        if len(isOK) > 1:
                            p_list = []
                            for i in isOK:
                                name = i.name
                                if not name:
                                    name = i.nick_name
                                if talk[(1 + len(b_talk)):len(name + b_talk) + 1] == name:
                                    p_list.append(name)
                            if len(p_list) == 1:
                                who = p_list[0]
                                break
                        elif len(isOK) == 1:
                            who = isOK[0].name
                            break
                        ss += 1
                        if ss >= len(now_talk) + 3:
                            break
                        joint_name = who + ' '
                        a = 1
                        ao = 0
                        d = 0
                        while ao <= 10:
                            ll = len(joint_name) + len(b_talk) + 1
                            if talk[:ll] == b_talk + '@' + joint_name:
                                who = joint_name
                                break
                            else:
                                if d == 0:
                                    ss -= 1
                                    joint_name = who + now_talk[ss - 1]
                                    d += 1
                                else:
                                    nb = ' '
                                    for i in range(0, a):
                                        nb += ' '
                                    joint_name = who + nb + now_talk[ss]
                                    a += 1
                                    ao += 1
                else:
                    who = ''
                    print('找不到用户', msg)
            except Exception as eb:
                who = ''
                print('处理用户抱错了', eb, msg)
            talk = b_talk + talk[(len(b_talk) + 1 + len(who)):].replace(' ', '')
        if ' ' in who:
            test_who = who.split(' ')
            for i in test_who:
                if i in talk:
                    talk = talk.replace(i, '')
            print(622, who, test_who, talk)
        talk = talk.replace(' ', '')
    if msg.is_at:
        if '点歌' == talk[:2] or '播放' == talk[:2]:
            return find_music(talk)
        elif '课程表' == talk:
            week_dict = dict(i1='星期一', i2='星期二', i3='星期三', i4='星期四', i5='星期五', i6='星期六', i7='星期日')
            dayOfWeek = datetime.now().isoweekday()  # 返回数字1-7代表周一到周日
            return '唉，本喵今天要上的网课就是这些啦：————' + week_dict[
                'i' + str(dayOfWeek)] + '. |\n语文课：【成语接龙】\n课间 ' '|\n玩小游戏：【打劫】 \n下午| \n音乐课：【点歌】' \
                                        '\n数学课： 【踩雷】'
        elif '抢劫' == talk or '打劫' == talk:  # 打劫机器人
            return Rob(who, who_talk, this, esl).rob_robot(values_dict_who_talk, qun_dict)
        elif '兑换抢劫次数' == talk or '兑换打劫次数' == talk:
            if values_dict_who_talk['point'] < 5:
                return "兑换失败，你的积分已经见底了！"
            values_dict_who_talk['point'] -= 5
            values_dict_who_talk['robNum'] += 5
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict_who_talk, ensure_ascii=False))
            esl.update_delete_sql("update users set point=?  where id=?", values_dict_who_talk['point'],
                                  values_dict_who_talk['user_id'])
            return "兑换成功，祝你天天开心！（当日有效）"
        elif '兑换抽奖次数' == talk or '兑换大转盘次数' == talk:
            if values_dict_who_talk['point'] < 5:
                return "兑换失败，你的积分已经见底了！"
            values_dict_who_talk['point'] -= 5
            values_dict_who_talk['luck_draw'] += 1
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict_who_talk, ensure_ascii=False))
            esl.update_delete_sql("update users set point=?  where id=?", values_dict_who_talk['point'],
                                  values_dict_who_talk['user_id'])
            return "兑换成功，祝你天天开心！（当日有效）"
        elif '抽奖' == talk or '大转盘' == talk:
            if 'luck_draw' not in values_dict_who_talk:
                return "很抱歉你没有参加活动"
            if values_dict_who_talk['luck_draw'] == 0:
                return "很抱歉你的抽奖次数已用尽"
            values_dict_who_talk['luck_draw'] -= 1
            info, reversal, cb = probability().probability_luck_draw()
            if "恭喜" in info:
                if cb == 1:
                    values_dict_who_talk['point'] += reversal
                elif cb == 2:
                    values_dict_who_talk['robNum'] += reversal
                else:
                    values_dict_who_talk['gold'] += reversal
                
                esl.update_delete_sql("update users set point=?  where id=?", values_dict_who_talk['point'],
                                      values_dict_who_talk['user_id'])
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict_who_talk, ensure_ascii=False))
            return "@" + who_talk + ' ' + info + "\n剩余抽奖次数：" + str(values_dict_who_talk['luck_draw'])
        elif not talk:
            # itchat.search_chatrooms(msg='消息', toUserName=ActualUserName)
            # print(12)
            # '@' + who_talk + '\u2005艾特本喵有何事！'
            return
        if qname in idiom_list:
            return '@' + who_talk + '\u2005成语接龙-：' + chengyujielong(talk, qname)
    else:
        if str(qun_dict['qun_id']) + '_' + who in users_key_list:
            game_users_who = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who)
            if '抢劫' == talk or '打劫' == talk:  # 玩家间打劫
                return Rob(who, who_talk, this, esl).rob_user(values_dict_who_talk, game_users_who, qun_dict)
            elif '赠送' == talk[:2] or '转赠' == talk[:2]:
                return Rob(who, who_talk, this, esl).presenter_user(values_dict_who_talk, game_users_who, qun_dict,
                                                                    talk, users_key_list)
    # 以下为不需要艾特可触发内容
    if '开始聊天' == talk or '开启聊天' == talk or '机器人聊天' == talk:
        if qname in qun_list:
            return '已经开始聊天咯~请选择机器人型号《菲菲》《图灵》《小思》'
        qun_list.append(qname)
        return "请选择机器人类型：《菲菲》《图灵》《小思》 默认小思"
    elif '结束聊天' == talk or '关闭聊天' == talk or '不聊了' == talk or talk == '闭嘴':
        try:
            qun_list.remove(qname)
            qun_dict['robot_type'] = 0
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            return goodbye
        except Exception as e:
            print(e, '该值不存在')
    elif '开启红包提醒' == talk or '开启红包预警' == talk or '红包提示' == talk:
        if qname in red_packet_list:
            return '已经开启红包提醒咯~'
        qun_dict['red_packet'] = True
        red_packet_list.append(qname)
        db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
        return '红包提醒已打开'
    elif '关闭红包提醒' == talk or '关闭红包预警' == talk:
        try:
            red_packet_list.remove(qname)
            qun_dict['red_packet'] = False
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            return '红包提醒已关闭~'
        except Exception as e:
            print(e, '该值不存在')
    elif talk == '取消名言名句' or talk == '关闭名言名句' or talk == '退出名言名句':
        try:
            ana_list.remove(str(qname))
            return goodbye
        except Exception as e:
            print(e, '该值不存在')
    elif '名言名句' == talk:
        if qname in ana_list:
            return '已经开始发送名言名句咯~'
        ana_list.append(str(qname))
        return welcome
    elif '签到' == talk:
        users_key_list = db_redis(14).r.keys()
        if minRewardPoint == rewardPoint:
            Point = rewardPoint
        else:
            Point = random.randint(minRewardPoint, rewardPoint)
        if minRewardGold == rewardGold:
            Gold = rewardGold
        else:
            Gold = random.randint(minRewardGold, rewardGold)
        qun_dict['pai'] += 1
        if qun_dict['pai'] <= 10:
            result = db_redis(13).get_owner(owner=str(qun_dict['qun_id']))
            if result:
                sign_list = result[1:-1].replace("'", '').split(', ')
                sign_in_list = sign_list
            sign_in_list.append(who_talk)
            db_redis(13).set_value(name=str(qun_dict['qun_id']), value=str(sign_in_list))
            sign_in_list.clear()
        now = time.strftime("%H:%M:%S")
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            values_dict_who_talk['sign_toList'] = qun_dict['pai']
            values_dict_who_talk['point'] = Point
            values_dict_who_talk['gold'] = Gold
            values_dict_who_talk['signTime'] = nowTime
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict_who_talk, ensure_ascii=False))
            esl.update_delete_sql("update users set sign_toList=?, point=?, gold=?, signTime=? where id=?",
                                  qun_dict['pai'], Point, Gold, str(nowTime), values_dict_who_talk['user_id'])
            return "👻[" + who_talk + ']签到成功\n👻签到排名：第' + str(qun_dict['pai']) + '名\n👻奖励：' + \
                   str(Point) + '积分 ' + str(Gold) + '金币\n👻现有资产：' + str(values_dict_who_talk['point']) + '积分 ' + str(
                values_dict_who_talk['gold']) + '金币\n👻头衔：新手上路\n👻时间：' + str(now)
        else:
            if values_dict_who_talk['sign_toList'] == 0:
                luck_draw_info = ''
                if 'luck_draw' in values_dict_who_talk:
                    if values_dict_who_talk['luck_draw'] > 0:
                        luck_draw_info = str(values_dict_who_talk['luck_draw']) + '抽奖次数'
                values_dict_who_talk['sign_toList'] = qun_dict['pai']
                values_dict_who_talk['point'] += Point
                values_dict_who_talk['gold'] += Gold
                db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
                values_dict_who_talk['signTime'] = nowTime
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                       value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                esl.update_delete_sql("update users set sign_toList=?, point=?, gold=?, signTime=? where id=?",
                                      qun_dict['pai'], values_dict_who_talk['point'], values_dict_who_talk['gold'],
                                      str(nowTime), values_dict_who_talk['user_id'])
                return "👻[" + who_talk + ']签到成功\n👻签到排名：第' + str(qun_dict['pai']) + '名\n👻奖励：' + \
                       str(Point) + '积分 ' + str(Gold) + '金币' + luck_draw_info + '\n👻现有资产：' + \
                       str(values_dict_who_talk['point']) +\
                       '积分 ' + str(values_dict_who_talk['gold']) + '金币\n👻头衔：' + \
                       get_nickname(values_dict_who_talk['gold']) + '\n👻时间：' + str(now)
            else:
                return '亲您已签到过了，请勿重复签到'
    elif '签到排行榜' == talk or '签到排行' == talk:
        result = db_redis(13).get_owner(owner=str(qun_dict['qun_id']))
        if result:
            sign_list = result[1:-1].replace("'", '').split(',')
            sign_in_list = sign_list
        if sign_in_list:
            info = '今日当前签到前十排行榜\n'
            sign_in_list_len = 1
            for i in sign_in_list:
                if len(sign_in_list) == sign_in_list_len:
                    info += '第' + str(sign_in_list_len) + '名：' + i
                else:
                    info += '第' + str(sign_in_list_len) + '名：' + i + '\n'
                sign_in_list_len += 1
        else:
            info = '当前签到排行榜\n无人签到'
        return info
    elif '金币排行榜' == talk or '金币排行' == talk:
        result = esl.select_run(
            'select name, gold from users where GroupChat_ID=%d group by id order by gold desc limit 0,10'
            % qun_dict['qun_id'])
        if result:
            info = '今日当前金币前十排行榜\n'
            sign_in_list_len = 1
            for i in result:
                if len(result) == sign_in_list_len:
                    info += '第' + str(sign_in_list_len) + '名：' + i[0] + '-金币：' + str(i[1])
                else:
                    info += '第' + str(sign_in_list_len) + '名：' + i[0] + '-金币：' + str(i[1]) + '\n'
                sign_in_list_len += 1
            return info
        else:
            return "查询失败请稍后再试！"
    elif '积分排行榜' == talk or '积分排行' == talk:
        result = esl.select_run(
            'select name, point from users where GroupChat_ID=%d group by id order by point desc limit 0,10' % qun_dict[
                'qun_id'])
        if result:
            info = '今日当前积分前十排行榜\n'
            sign_in_list_len = 1
            for i in result:
                if len(result) == sign_in_list_len:
                    info += '第' + str(sign_in_list_len) + '名：' + i[0] + '-积分：' + str(i[1])
                else:
                    info += '第' + str(sign_in_list_len) + '名：' + i[0] + '-积分：' + str(i[1]) + '\n'
                sign_in_list_len += 1
            return info
        else:
            return "查询失败请稍后再试！"
    elif '查询' == talk or '积分查询' == talk or '金币查询' == talk:  # 已废弃game_redis_dict
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            return "对不起，您无资产"
        now = time.strftime("%H:%M:%S")
        luck_draw_info = ''
        if 'luck_draw' in values_dict_who_talk:
            if values_dict_who_talk['luck_draw'] > 0:
                luck_draw_info = '\n👻剩余抽奖次数' + str(values_dict_who_talk['luck_draw'])
        if values_dict_who_talk['sign_toList'] == 0:
            return "👻[" + who_talk + ']查询成功\n👻签到排名：未签到\n👻资产：' + str(values_dict_who_talk['point']) +\
                   '积分 ' + str(values_dict_who_talk['gold']) + '金币\n👻头衔：' + \
                   get_nickname(values_dict_who_talk['gold']) + luck_draw_info + '\n👻时间：' + str(now)
        else:
            return "👻[" + who_talk + ']查询成功\n👻签到排名：第' + str(values_dict_who_talk['sign_toList']) + \
                   '名\n👻资产：' + str(values_dict_who_talk['point']) + '积分 ' + str(values_dict_who_talk['gold']) +\
                   '金币\n👻头衔：' + get_nickname(values_dict_who_talk['gold']) + luck_draw_info + '\n👻时间：' + str(now)
    elif '兑换' == talk:  # 兑换机器人金币
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            return '很抱歉，您的账户无资产~'
        else:
            if values_dict_who_talk['point'] == 0:
                return '很抱歉，您的账户积分不足~'
            values_dict_who_talk['point'] -= 1
            qun_dict['this_num'] += 1000
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict_who_talk, ensure_ascii=False))
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            return "@" + who_talk + "兑换成功，祝您游戏愉快~"
    elif '抽奖池' == talk:
        return "奖池抽奖可得金币2000,4000,6000,8000,10000档次，积分5,10,15,20档次，打劫次数5，10档次"
    elif '讲个笑话' == talk or '笑话' == talk or '讲笑话' == talk:
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        return re
    elif '讲个故事' == talk or '故事' == talk or '讲故事' == talk:
        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
    elif '热搜' in talk:
        return '当前时间' + nowTime + '热搜前十\n' + search()
    elif '菜单' == talk or '帮助' == talk or 'help' == talk:
        return "自己看看吧，是不是多到眼花\n机器人聊天    成语接龙\n群签到    打劫游戏\n点歌    踩雷游戏\n笑话  " \
               "谁是魔王（开发中）\n辅助功能： 名言名句    红包提醒\n其他功能正在努力开发中"
    elif '聊天菜单' == talk or '聊天帮助' == talk or '聊天help' == talk:
        return "@" + who_talk + ': 艾特我回复：' + '开始聊天  或  开启聊天  或  机器人聊天\n结束回复：结束聊天  或  关闭聊天  或  不聊了。'
    elif '成语接龙菜单' == talk or '成语接龙帮助' == talk or '成语接龙help' == talk:
        return "@" + who_talk + ': 艾特我回复：' + '成语接龙  或  打开成语接龙  或  直接说成语\n结束回复：不玩了  或  关闭成语接龙  或  退出。'
    elif '签到菜单' == talk or '签到帮助' == talk or '签到help' == talk:
        return "@" + who_talk + ': 艾特我回复：签到 '
    elif '抢劫菜单' == talk or '抢劫帮助' == talk or '抢劫help' == talk:
        return "@" + who_talk + ': 艾特我或他（她）回复：打劫 或 抢劫'
    elif '成语接龙' == talk or '打开成语接龙' == talk:
        talk = ''
        if qname in idiom_list:
            return '@' + who_talk + ' ' + '已经开始成语接龙咯~'
        idiom_list.append(qname)
        return '@' + who_talk + ' 成语接龙：' + chengyujielong(talk, qname)
    elif '不玩了' == talk or '关闭成语接龙' == talk or '退出' == talk:
        talk = '退出'
        try:
            idiom_list.remove(qname)
            return '@' + who_talk + ' 成语接龙：' + chengyujielong(talk, qname)
        except Exception as e:
            print(e, '该值不存在')
    elif '踩雷' == talk or '数字炸弹' == talk:
        if qname in Num_bomb_dict:
            a1, c, d = Num_bomb_dict[qname]
            return '踩雷游戏已开启，当前 ' + c + ' 到 ' + d + " 呢!"
        Num_bomb_dict[qname] = random.randint(0, 100), 0, 100
        return welcome + " 踩雷开始咯 当前 0 到 100 呢"
    elif talk == '取消踩雷' or talk == '关闭踩雷' or talk == '退出踩雷':
        try:
            del Num_bomb_dict[str(qname)]
            return goodbye
        except Exception as e:
            print(e, '该值不存在')
    elif qname in Num_bomb_dict:  # 踩雷游戏
        Num = -1
        try:
            Num = int(talk)
        except Exception:
            pass
        if Num != -1:
            try:
                a1, c, d = Num_bomb_dict[qname]
                cai_lei_info = game_dict[who_talk]
                monkey_Num = cai_lei_info[2]
                if a1 == -1:
                    a1 = random.randint(0, 100)
                    c = 0
                    d = 100
                if Num <= c or Num >= d:
                    return '@' + who_talk + " 输入错误，请输入：" + str(c) + " 到" + str(d) + "的数字"
                elif Num == a1:
                    a1 = -1
                    Num_bomb_dict[qname] = a1, c, d
                    monkey_Num -= 5
                    values_dict_who_talk['gold'] -= 5
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                    return '@' + who_talk + " 踩雷了 - 5金币，本轮已结束。继续请继续输入数字。"
                elif Num < a1:
                    c = Num
                    Num_bomb_dict[qname] = a1, c, d
                    monkey_Num += 1
                    values_dict_who_talk['gold'] += 1
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                    return '@' + who_talk + " 恭喜您未中雷 + 1金币，请继续：" + str(c) + " 到" + str(d) + "的数字"
                elif Num > a1:
                    d = Num
                    Num_bomb_dict[qname] = a1, c, d
                    monkey_Num += 1
                    values_dict_who_talk['gold'] += 1
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                    return '@' + who_talk + " 恭喜您未中雷 + 1金币，请继续：" + str(c) + " 到" + str(d) + "的数字"
                else:
                    Num_bomb_dict[qname] = a1, c, d
                    return '@' + who_talk + " 输入错误，请输入：" + str(c) + "到" + str(d) + "的数字"
            except Exception as e:
                print("处理踩雷异常了", e)
    elif qname in qun_list:
        return robot_chat(talk, qun_dict, welcome)
    elif qname in ana_list:
        a = read_name_all_info(r'count').run()
        return a.split()[0]
    else:
        if len(talk) == 4:  # 输入成语直接开始成语接龙
            res = chengyujielong(talk, qname)
            if res:
                idiom_list.append(qname)
                return '@' + who_talk + " 成语接龙开始咯：" + res
                # else:
                #     return '@' + who_talk + '\u2005本喵正专心上网课呢，不跟你聊天哦~不如@我说“课程表”，看看我的日程？'
    return


@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    #  接受好友请求
    new_friends = msg.card.accept()
    # 向新好友发送消息
    new_friends.send('哈哈，我自动接受了你的好友请求！')
    return


def set_info():
    with open('config.txt', 'w', encoding='utf-8') as file:
        file.write('.'.join(qun_list))
        file.write('---\n')
        file.write('.'.join(user_list))
        file.write('---\n')
        file.write(json.dumps(game_dict, ensure_ascii=False))
        file.write('---\n')
        file.write('.'.join(user_idiom_list))
        file.write('---\n')
        file.write('.'.join(red_packet_list))
        file.write('---\n')
        file.write('.'.join(idiom_list))
        file.write('---\n')
        file.write(str(this_num))
        file.write('---\n')
        file.write('.'.join(ana_list))
        file.write('---\n')
        file.write('.'.join(sign_in_list))
        file.write('---\n')
        file.write(json.dumps(idiom_dict, ensure_ascii=False))
        file.write('---\n')
        file.write('.'.join(users_list))
        file.write('---\n')
        file.close()
    return "存档成功"


def get_info():
    global qun_list, user_list, game_dict, user_idiom_list, red_packet_list, idiom_list, this_num, ana_list,\
        sign_in_list, pai, idiom_dict, users_list
    with open(r'G:\Python\flask\static\src\api\config.txt', 'r', encoding='utf-8') as file:
        a_list = []
        aa = file.readlines()
        for a in aa:
            a_list.append(a[:-4])
        if len(a_list) == 11:
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
            sign_in_list = a_list[8].split('.')
            try:
                sign_in_list.remove('')
            except Exception:
                pass
            keys_list = db_redis(0).r.keys()
            idiom_dict = json.loads(a_list[9])
            users_list = a_list[10].split('.')
            try:
                users_list.remove('')
            except Exception:
                pass
            res = "读档成功"
        else:
            res = "读档失败"
        file.close()
    return res


# 每日0时清数据定时器
def func(keep_on=True):
    global pai, game_dict, sign_in_list
    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("开始删除redis签到记录")
    # 清除用户签到排名&每日抽奖次数
    keys_list = db_redis(14).r.keys()
    if keys_list:
        for kl in keys_list:
            res_qun_dict = db_redis(14).get_owner(owner=kl)
            result_dict = json.loads(res_qun_dict)
            if result_dict['sign_toList'] == 0 and result_dict['robNum'] == robNum:
                continue
            result_dict['sign_toList'] = 0
            result_dict['robNum'] = robNum
            result_dict['luck_draw'] = luck_draw
            if 'RobCount' not in result_dict:
                result_dict['RobCount'] = '0-0-0'
            db_redis(14).set_value(name=kl, value=json.dumps(result_dict, ensure_ascii=False))
    # 清除群签到排名、机器人金币数据
    keys_list = db_redis(15).r.keys()
    if keys_list:
        for kl in keys_list:
            res_qun_dict = db_redis(15).get_owner(owner=kl)
            result_dict = json.loads(res_qun_dict)
            result_dict['pai'] = 0
            result_dict['this_num'] = 5000
            db_redis(15).set_value(name=kl, value=json.dumps(result_dict, ensure_ascii=False))
    keys_list = db_redis(13).r.keys()
    # 清除签到排行榜库
    if keys_list:
        for kl in keys_list:
            db_redis(13).delete(name=kl)
    print("0点定时存档", set_info())
    print("执行时间", new_time)
    # 如果需要循环调用，就要添加以下方法
    if keep_on:
        timing = threading.Timer(86400, func)
        timing.start()


# 每隔10秒检测登陆状态
def func_check_login():
    global bot
    status = bot.alive()
    print("当前状态：", status)
    if status != '200' and status != '400':
        # itchat.logout()
        print("离线了", status)  # bot = Bot(cache_path=True)
    timing_check_login = threading.Timer(10, func_check_login)
    timing_check_login.start()


def set_common_return_info():
    global welcome, goodbye, robNum, minRewardPoint, rewardPoint, minRewardGold, rewardGold, luck_draw
    welcome = Config().get_pu('basics', 'welcome')
    goodbye = Config().get_pu('basics', 'goodbye')
    robNum = int(Config().get_pu('basics', 'robNum'))
    luck_draw = int(Config().get_pu('basics', 'luck_draw'))
    minRewardPoint = int(Config().get_pu('basics', 'minRewardPoint'))
    rewardPoint = int(Config().get_pu('basics', 'rewardPoint'))
    minRewardGold = int(Config().get_pu('basics', 'minRewardGold'))
    rewardGold = int(Config().get_pu('basics', 'rewardGold'))
    if welcome and goodbye and robNum and rewardPoint and rewardGold:
        return True
    else:
        return False


# 初始化函数（读配置文件、更新缓存）
def run():
    print("先初始化再启动")
    # config_dir = os.path.join(setting.APP_ROOT, r"static\src\api\config")
    # config_path = os.path.join(config_dir, 'game_config.ini')
    # print(config_path)
    print(get_info())
    result_set_info = set_common_return_info()
    if result_set_info:
        print("配置文件初始化完成")
    else:
        print("配置文件初始化失败")
    #  初始化table
    refresh_sqlite()
    # table_list = ['GroupChat', 'users', 'Backpack', 'shop', 'monster', 'prop']
    # for t in table_list:
    #     esl.new_table(t)
    print("初始化完成")
    now_time = datetime.now()
    # 获取明天年月日
    next_time = now_time + timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天0点时间
    next_time = datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")
    print("明天时间", next_time)
    # # 获取昨天时间
    # last_time = now_time + datetime.timedelta(days=-1)
    
    # 获取距离明天0点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)
    timer.start()
    # timer_check_login = threading.Timer(10, func_check_login)
    # timer_check_login.start()
    return True


# 手动退出（建议使用，先保存数据再退出）
def stop():
    set_info()
    bot.logout()
    return


if __name__ == '__main__':
    run()
    embed()
    bot.start()
