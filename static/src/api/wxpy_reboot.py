import json
import threading
from datetime import datetime
from datetime import timedelta
import os
import random
import time
from functools import lru_cache
import numpy as np
import logger
import traceback

from static.src.api.chengyujielong import chengyujielong, idiom_dict, users_list
from static.src.api.count.read_name_all_info import read_name_all_info
from static.src.api.config.get_game_config import Config
from axf.dbredis import db_redis
from static.src.api.game_views import execute_sql_lite
from static.src.api.search import main
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
    print(msg.text, type(msg))
    # msg = "努力上班中，晚点回复！"
    global user_list, user_idiom_list, ana_list, ret_dict, At_who
    # print(msg)
    talk = msg.text
    try:
        name = msg.sender.name
        if not name:
            name = msg.member.name
    except Exception:
        name = msg.sender.name
        # print(name, fromUserName)
        if not name:  # 当没有备注时取微信名称
            name = msg.member.name
    # print(name, talk)
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
                                he_talk = bot.friends.search(name=i)
                                msg.forward(talk_info, chat=he_talk[0]['UserName'])
                    else:
                        for i in to_list:
                            if i != '':
                                q_talk = bot.groups.search(name=i)
                                msg.forward(talk_info, chat=q_talk[0]['UserName'])
                return who + ':发送成功'
            except Exception as e:
                print(e)
                return '发送失败'
    if talk == '开始聊天' or talk == '开启聊天':
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
            r = db_redis(db=3).delete(name)
            if r:
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
    elif '清除签到记录' in talk:
        func(keep_on=False)
        return "ok"
    elif '设置转发' == talk[:4]:
        At_who = talk[4:]
    elif '重载' in talk:
        # itchat.logout()
        # itchat.auto_login(hotReload=True, enableCmdQR=True)
        return 'OK'
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
        he_talk = bot.friends.search(name=At_who)
        if not he_talk:
            return
        if name in ret_dict:
            last_time = ret_dict[name]
            lo_time = datetime.strptime(talk_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(last_time,
                                                                                            '%Y-%m-%d %H:%M:%S')
            inner_time = int(timedelta.total_seconds(lo_time) / 60)
            if inner_time > 180:
                msg.forward(name + ':' + talk, chat=he_talk[0]['UserName'])
                ret_dict[name] = talk_time  # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
            else:
                msg.forward(name + ':' + talk, chat=he_talk[0]['UserName'])
                ret_dict[name] = talk_time
                return
        else:
            ret_dict[name] = talk_time
            msg.forward(name + ':' + talk, chat=he_talk[0]['UserName'])  # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
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
rewardPoint: int = 0
rewardGold: int = 0


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


@bot.register(Group)
def Group_reply(msg):
    global pai, this_num, game_dict, qun_list, idiom_list, red_packet_list, Num_bomb_dict, sign_in_list, esl, robNum,\
        rewardPoint, rewardGold
    # print(msg.text, msg.sender.name, msg.member.name, msg.receiver.name, msg.type)
    try:
        # print(msg)
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
        ActualUserName = msg.raw.get('FromUserName')  # 用户名称（腾讯用内置）
        talk = msg.text
        if talk is None:
            talk = ''
        group = bot.groups().search(msg.sender.name)[0]
        this = group.self.name
        qname = msg.sender.name
        qun_user_name = ActualUserName
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
            qun_id = qun_dict['qun_id']
            pai = qun_dict['pai']
            this_num = qun_dict['this_num']
        else:  # redis + sqlite 存储
            esl.insert_sql(table_name='GroupChat', sql=[qname, qun_user_name])
            time.sleep(0.05)
            qun_list = esl.select_run("select id from GroupChat where name=?", qname)
            qun_id = 0
            if qun_list:
                for r in qun_list:
                    qun_id = r[0]
            db_redis(15).set_value(name=qname, value=json.dumps(
                {"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0, "robot_type": 0, "red_packet": False},
                ensure_ascii=False))
            qun_dict = {"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0, "robot_type": 0, "red_packet": False}
        who_talk = msg.member.name
        if not who_talk:
            return
        users_key_list = db_redis(14).get_db_keys()
        if str(qun_id) + '_' + who_talk in users_key_list:
            game_users_who_talk = db_redis(14).get_owner(str(qun_id) + '_' + who_talk)
            who_talk_id = json.loads(game_users_who_talk)['user_id']
            esl.update_delete_sql("update users set point=?, gold=? where id=?",
                                  json.loads(game_users_who_talk)['point'], json.loads(game_users_who_talk)['gold'],
                                  who_talk_id)
        else:  # redis + sqlite 存储
            if who_talk:
                sql = "select max(id) from users where name=? and GroupChat_ID=?"
                who_talk_list = esl.select_run(sql, who_talk, qun_id)
                if not who_talk_list[0][0]:
                    result = esl.insert_sql(table_name='users',
                                            sql=[qun_id, who_talk, '', ActualUserName, 0, 0, 0, 0, 0, 0, nowTime,
                                                 '0-0-0'])
                    time.sleep(0.05)
                    if result == 'ok':
                        sql = "select max(id) from users where name=? and GroupChat_ID=?"
                        who_talk_list = esl.select_run(sql, who_talk, qun_id)
                        if who_talk_list:
                            who_talk_id = who_talk_list[0][0]
                            if who_talk_id == 0:
                                print("当前用户id为0")
                                return
                            if not who_talk_id:
                                return
                            db_redis(14).set_value(name=str(qun_id) + '_' + who_talk, value=json.dumps(
                                {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                                 "RobCount": "0-0-0"}, ensure_ascii=False))
                            game_users_who_talk = json.dumps(
                                {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                                 "RobCount": "0-0-0"}, ensure_ascii=False)
                        else:
                            return
                    else:
                        print("插入语句失败", result)
                        return
                else:
                    who_talk_id = who_talk_list[0][0]
                    if not who_talk_id:
                        print(who_talk, qun_id, who_talk_id, '为none', who_talk_list)
                        return
                    if who_talk_id == 0:
                        print("当前用户id为0")
                        return
                    if db_redis(14).r.exists(str(qun_id) + '_' + who_talk):
                        print("已找到用户")
                        game_users_who_talk = db_redis(14).get_owner(str(qun_id) + '_' + who_talk)
                    else:
                        db_redis(14).set_value(name=str(qun_id) + '_' + who_talk, value=json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "RobCount": "0-0-0"}, ensure_ascii=False))
                        game_users_who_talk = json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "RobCount": "0-0-0"}, ensure_ascii=False)
            else:
                game_users_who_talk = ''
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
                if who == '所有人':
                    # return '@' + who_talk + ' 收到~'
                    return
            except Exception as e:
                print('报错了', e)
                return
            ss = 0
            try:
                if Users_list:
                    while ss <= len(new):
                        isOK = group.search(who)
                        if not isOK:
                            isOK = bot.groups().search(keywords=msg.sender.name, nick_name=who)[0]
                            print(isOK)
                        if len(isOK) > 1:
                            p_list = []
                            for i in isOK:
                                if who == i.nick_name:
                                    p_list.append(i.nick_name)
                                    pass
                            if len(p_list) == 1:
                                who = p_list[0].name
                                break
                        elif len(isOK) == 1:
                            who = isOK[0].name
                            break
                        ss += 1
                        if ss >= len(new) + 3:
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
                                    nn = ' '
                                    for i in range(0, a):
                                        nn += ' '
                                    joint_name = who + nn + new[ss]
                                    a += 1
                                    ao += 1
                else:
                    who = ''
                    print('找不到用户', 111)
            except Exception as eb:
                who = ''
                print('处理用户抱错了', eb, 213)
            try:
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
        elif len(now_talk) > 3:  # 处理艾特多人（先不处理）
            return
        else:  # 艾特一人（话语在首位）
            try:
                a_talk = now_talk
                b_talk = a_talk[0]
                who = a_talk[1]
                if '' in who:
                    now_talk = who.split()
                    who = now_talk[0]
                if who == '所有人':
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
                        if len(isOK) > 1:
                            p_list = []
                            for i in isOK:
                                if who == i.name:
                                    p_list.append(i.name)
                            if len(p_list) == 1:
                                who = p_list[0].name
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
                                    nn = ' '
                                    for i in range(0, a):
                                        nn += ' '
                                    joint_name = who + nn + now_talk[ss]
                                    a += 1
                                    ao += 1
                else:
                    who = ''
                    print('找不到用户', msg)
            except Exception as eb:
                who = ''
                print('处理用户抱错了', eb, msg)
            try:
                if '' in who:
                    ss += 1
                if ss < len(now_talk):
                    if ss != len(now_talk):
                        if ss == 0:
                            ss += 1
                        talk = ''
                        for i in range(ss, len(now_talk)):
                            if talk == '':
                                talk = talk + now_talk[i]
                            else:
                                talk = talk + ' ' + now_talk[i]
                    else:
                        talk = now_talk[ss]
                else:
                    talk = ''
                talk = b_talk + talk
            except Exception as ec:
                print(ec, msg, 502)
                talk = ''
    if msg.is_at:
        that = Group.search(msg.sender, msg.text.split()[0][1:])
        print(that[0].name)
    else:
        if who != '':
            print(who_talk + '----' + who + '---' + talk)
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
    with open('config.txt', 'r', encoding='utf-8') as file:
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
            pai = len(keys_list)
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
    pai = 0
    # sign_in_list.clear()
    # if game_dict:
    #     for i in game_dict.keys():
    #         game_dict[i] = pai, game_dict[i][1], game_dict[i][2], game_dict[i][3]
    print("开始删除redis签到记录")
    # 清除用户签到排名
    keys_list = db_redis(14).r.keys()
    if keys_list:
        for kl in keys_list:
            res_qun_dict = db_redis(14).get_owner(owner=kl)
            result_dict = json.loads(res_qun_dict)
            if result_dict['sign_toList'] == 0 and result_dict['robNum'] == robNum:
                continue
            result_dict['sign_toList'] = 0
            result_dict['robNum'] = robNum
            if 'RobCount' not in result_dict:
                result_dict['RobCount'] = '0-0-0'
            db_redis(14).set_value(name=kl, value=json.dumps(result_dict, ensure_ascii=False))
    # 清除群签到排名数据
    keys_list = db_redis(15).r.keys()
    if keys_list:
        for kl in keys_list:
            res_qun_dict = db_redis(15).get_owner(owner=kl)
            result_dict = json.loads(res_qun_dict)
            if result_dict['pai'] != 0:
                result_dict['pai'] = 0
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
        print("离线了", status)
        # bot = Bot(cache_path=True)
    timing_check_login = threading.Timer(10, func_check_login)
    timing_check_login.start()


def set_common_return_info():
    global welcome, goodbye, robNum, rewardPoint, rewardGold
    welcome = Config().get_pu('basics', 'welcome')
    goodbye = Config().get_pu('basics', 'goodbye')
    robNum = int(Config().get_pu('basics', 'robNum'))
    rewardPoint = int(Config().get_pu('basics', 'rewardPoint'))
    rewardGold = int(Config().get_pu('basics', 'rewardGold'))
    if welcome and goodbye and robNum and rewardPoint and rewardGold:
        return True
    else:
        return False


# 初始化函数（读配置文件、更新缓存）
def run():
    print("先初始化再启动")
    import setting
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
    # print(timer_start_time)
    # 54186.75975
    
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
