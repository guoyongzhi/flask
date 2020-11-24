import json
import threading
from datetime import datetime
from datetime import timedelta
import os
import random
import time
from functools import lru_cache
import numpy as np

import itchat
import logger
import traceback

from static.src.api.chengyujielong import chengyujielong
from static.src.api.count.read_name_all_info import read_name_all_info
from static.src.api.config.get_game_config import Config
from axf.dbredis import db_redis
from static.src.api.data.game_views import execute_sql_lite

import requests

user_list = []
user_idiom_list = []
ana_list = []
ret_dict = dict()
At_who = '机器人_菲菲'


@itchat.msg_register(itchat.content.TEXT)  # 私发消息
def text_reply(msg):  # 处理私人消息
    # msg = "努力上班中，晚点回复！"
    global user_list, user_idiom_list, ana_list, ret_dict, At_who
    # print(msg)
    talk = msg.text
    fromUserName = msg['FromUserName']
    try:
        name = msg['User']['RemarkName']
        if not name:
            name = msg['User']['NickName']
    except Exception:
        name = msg['RecommendInfo']['UserName']
        # print(name, fromUserName)
        if not name:  # 当没有备注时取微信名称
            name = msg['RecommendInfo']['NickName']
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
        itchat.auto_login(hotReload=True, enableCmdQR=True)
        return 'OK'
    elif name in user_idiom_list:
        return chengyujielong(talk, name)
    elif name in user_list:
        # if "小白" in talk:
        #     talk = talk.replace('小白', '菲菲')
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        # if '菲菲' in re:
        #     re = re.replace('菲菲', '小白')
        print(name, "--私聊：{}  ({})".format(re, datetime.now()))
        return re
    elif name in ana_list:
        a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
        return a.split()[0]
    else:
        talk_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        he_talk = itchat.search_friends(name=At_who)
        if not he_talk:
            return
        if name in ret_dict:
            last_time = ret_dict[name]
            lo_time = datetime.strptime(talk_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(last_time,
                                                                                            '%Y-%m-%d %H:%M:%S')
            inner_time = int(timedelta.total_seconds(lo_time) / 60)
            if inner_time > 180:
                itchat.send(name + ':' + talk, he_talk[0]['UserName'])
                ret_dict[name] = talk_time
                # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'
            else:
                itchat.send(name + ':' + talk, he_talk[0]['UserName'])
                ret_dict[name] = talk_time
                return
        else:
            ret_dict[name] = talk_time
            itchat.send(name + ':' + talk, he_talk[0]['UserName'])
            # return '信息已收到，本人暂时离开，急事请致电，谢谢配合！'


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


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)  # 群消息（群游戏）
def text_reply(msg):  # 处理群消息
    global game_dict, qun_list, idiom_list, red_packet_list, Num_bomb_dict, sign_in_list, esl,\
         robNum, rewardPoint, rewardGold
    try:
        # print(msg)
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
        ActualUserName = msg['ActualUserName']  # 用户名称（腾讯用内置）
        talk = msg['Content']
        this = msg['User']['Self']['DisplayName']
        # thisUserName = msg['User']['Self']['UserName']
        qname = msg['User']['NickName']
        qun_user_name = msg['FromUserName']
        who = ''
        if not this:  # 当没有备注时取微信名称
            this = msg['User']['Self']['NickName']
        # 转存群名称，群ID  sqlite
        qun_keys_list = db_redis(15).get_db_keys()
        if qname == '':
            qname = qun_user_name
        else:
            if qun_user_name in qun_keys_list:
                qun_dict = json.loads(db_redis(15).get_owner(qun_user_name))
                qun_dict['qname'] = qname
                result = esl.update_delete_sql("update GroupChat set name=? where id=?", qname, qun_dict['qun_id'])
                if result == 'ok':
                    db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
                    db_redis(15).delete(qun_user_name)
                else:
                    print("修改表名称失败")
        if qname in qun_keys_list:
            qun_dict = json.loads(db_redis(15).get_owner(qname))
            qun_id = qun_dict['qun_id']
        else:  # redis + sqlite 存储
            esl.insert_sql(table_name='GroupChat', sql=[qname, qun_user_name])
            time.sleep(0.05)
            qun_list = esl.select_run("select id from GroupChat where name=?", qname)
            qun_id = 0
            if qun_list:
                for r in qun_list:
                    qun_id = r[0]
            db_redis(15).set_value(name=qname,
                                   value=json.dumps({"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0,
                                                     "robot_type": 0, "red_packet": False}, ensure_ascii=False))
            qun_dict = {"qname": qname, "qun_id": qun_id, "pai": 0, "this_num": 0, "robot_type": 0, "red_packet": False}
        who_talk = msg['ActualNickName']
        if not who_talk:
            return
        users_key_list = db_redis(14).get_db_keys()
        if str(qun_dict['qun_id']) + '_' + who_talk in users_key_list:
            game_users_who_talk = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who_talk)
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
                        print(who_talk, qun_dict['qun_id'], who_talk_id, '为none', who_talk_list)
                        return
                    if who_talk_id == 0:
                        print("当前用户id为0")
                        return
                    if db_redis(14).r.exists(str(qun_dict['qun_id']) + '_' + who_talk):
                        print("已找到用户")
                        game_users_who_talk = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who_talk)
                    else:
                        db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk, value=json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "RobCount": "0-0-0"}, ensure_ascii=False))
                        game_users_who_talk = json.dumps(
                            {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum,
                             "RobCount": "0-0-0"}, ensure_ascii=False)
            else:
                game_users_who_talk = ''
        # print(who_talk_id)
        aa = qname.split('/')
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
    if '@' in talk:
        # 拆分语言
        now_talk = talk.split('@')
        if now_talk[0] == '':
            del now_talk[0]
        # if len(now_talk) == 1:
        #     return ""  # 没有说话直接返回
        whoUserName = ''
        if talk[:1] == '@':  # 艾特一人（首位）
            try:
                new = talk.split()
                Users_list = msg['User']['MemberList']
                who = new[0]
                who = who[1:]
                if who == '所有人':
                    # return '@' + who_talk + ' 收到~'
                    return
            except Exception as e:
                print('报错了', e)
                return
            dd = 0
            ss = 0
            try:
                if Users_list:
                    while ss <= len(new):
                        for i in Users_list:
                            t_name = i['DisplayName']
                            if t_name == '':
                                t_name = i['NickName']
                            if t_name == who:
                                whoUserName = i['UserName']
                                dd = 1
                                break
                        if dd == 1:
                            break
                        else:
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
                talk = ''
            # print(ss, '----')
        elif len(now_talk) > 3:  # 处理艾特多人（先不处理）
            return
        else:  # 艾特一人（话语在首位）
            try:
                Users_list = msg['User']['MemberList']
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
            dd = 0
            ss = 0
            try:
                if Users_list:
                    while ss <= len(now_talk):
                        for i in Users_list:
                            t_name = i['DisplayName']
                            if t_name == '':
                                t_name = i['NickName']
                            if t_name == who:
                                whoUserName = i['UserName']
                                dd = 1
                                break
                        if dd == 1:
                            break
                        else:
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
                talk = b_talk + talk  # print(talk)
            except Exception as ec:
                print(ec, msg)
                talk = ''
    if msg['isAt']:
        if who == this:
            if '点歌' == talk[:2] or '播放' == talk[:2]:
                name = talk.split()
                if talk[2:] == '':
                    return '亲点歌格式不对哦~ 点歌请艾特我回复点歌 【歌名】'
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
            elif '课程表' == talk:
                week_dict = dict(i1='星期一', i2='星期二', i3='星期三', i4='星期四', i5='星期五', i6='星期六', i7='星期日')
                dayOfWeek = datetime.now().isoweekday()  # 返回数字1-7代表周一到周日
                return '唉，本喵今天要上的网课就是这些啦：————' + week_dict[
                    'i' + str(dayOfWeek)] + '. |\n语文课：【成语接龙】\n课间 ' '|\n玩小游戏：【打劫】 \n下午| \n音乐课：【点歌】' \
                                            '\n数学课： 【踩雷】'
            elif '抢劫' == talk or '打劫' == talk:  # 打劫机器人
                values_dict_who_talk = json.loads(game_users_who_talk)
                if qun_dict['this_num'] == 0:
                    return "@ " + who_talk + " 抢劫失败，机器人资产不足，可回复《兑换》消耗1积分。兑换机器人1000金币~"
                to = random.randint(1, qun_dict['this_num'])
                winner = random.randint(0, 1)
                qun_dict['this_num'] -= to
                if winner == 1:
                    to *= 2
                # if who_talk not in game_dict:
                #     getpai = 0
                #     getjifen = 0
                #     getjinbi = to
                # else:
                #     nowinfo = game_dict[who_talk]
                #     getpai = nowinfo[0]
                #     getjifen = nowinfo[1]
                #     getjinbi = nowinfo[2]
                getjinbi = values_dict_who_talk['gold']
                getjinbi += to
                try:
                    RobCount = values_dict_who_talk['RobCount']
                    if RobCount:
                        rob_count_list = RobCount.splik('-')
                    else:
                        rob_count_list = ['0', '0', '0']
                except Exception:
                    rob_count_list = ['0', '0', '0']
                rob_count_list = [str(int(rob_count_list[0]) + 1), str(int(rob_count_list[1]) + 1), rob_count_list[2]]
                values_dict_who_talk['RobCount'] = '-'.join(rob_count_list)
                values_dict_who_talk['gold'] = getjinbi
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                       value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                esl.update_delete_sql("update users set gold=? where id=?", getjinbi, who_talk_id)
                db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
                if winner:
                    return '😂恭喜[' + who_talk + '] 抢劫 [' + this + '] 成功，人品大爆发奖励双倍，抢走了对方' + str(
                        to) + '金币！\n⚠您还可以抢劫' + str(values_dict_who_talk['robNum']) + '次(打劫机器人不消耗次数)！'
                return '😂[' + who_talk + '] 抢劫 [' + this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫' + str(
                    values_dict_who_talk['robNum']) + '次(打劫机器人不消耗次数)！'
            elif '兑换抢劫次数' == talk or '兑换打劫次数' == talk:
                values_dict_who_talk = json.loads(game_users_who_talk)
                if values_dict_who_talk['point'] == 0:
                    return "兑换失败，你的积分为零！"
                values_dict_who_talk['point'] -= 1
                values_dict_who_talk['robNum'] += 5
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                       value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                esl.update_delete_sql("update users set point=?  where id=?",
                                      values_dict_who_talk['point'], who_talk_id)
                return "兑换成功，祝你天天开心！（当日有效）"
            elif not talk:
                # itchat.search_chatrooms(msg='消息', toUserName=ActualUserName)
                # print(12)
                # '@' + who_talk + '\u2005艾特本喵有何事！'
                return
            if qname in idiom_list:
                return '@' + who_talk + '\u2005成语接龙-：' + chengyujielong(talk, qname)
        else:
            print("进来非艾特了")
            pass
    else:  # 同志们之间艾特
        # 先处理艾特谁入库
        if who != '':
            print(who_talk + '----' + who + '---' + talk)
        # if who and '所有人' not in who and who != '':
        #     if str(qun_dict['qun_id']) + '_' + who in users_key_list:
        #         game_users_who = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who)
        #         who_id = json.loads(game_users_who)['user_id']
        #     else:  # redis + sqlite 存储
        #         sql = "select max(id) from users where name=? and GroupChat_ID=?"
        #         who_list = esl.select_run(sql, who, qun_dict['qun_id'])
        #         if not who_list:
        #             result = esl.insert_sql(table_name='users',
        #                                     sql=[qun_dict['qun_id'], who, '', whoUserName, 0, 0, 0, 0, 0, 0, nowTime])
        #             if result == 'ok':
        #                 who_list = esl.select_run("select max(id) from users where name=? and GroupChat_ID=?",
        #                                           who, qun_dict['qun_id'])
        #                 if who_list:
        #                     who_id = who_list[0][0]
        #                     if who_id == 0:
        #                         print("当前用户id仍为0")
        #                         return
        #                     db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who, value=json.dumps(
        #                         {"user_id": who_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum},
        #                         ensure_ascii=False))
        #                     game_users_who = json.dumps(
        #                         {"user_id": who_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum},
        #                         ensure_ascii=False)
        #                 else:
        #                     return
        #             else:
        #                 print("插入语句失败", result)
        #                 return
        #         else:
        #             who_id = who_list[0][0]
        #             if who_id == 0:
        #                 print("当前用户id仍为0")
        #                 return
        #             if db_redis(14).r.exists(str(qun_dict['qun_id']) + '_' + who):
        #                 print("已存在该用户")
        #                 game_users_who = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who)
        #             else:
        #                 db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who, value=json.dumps(
        #                     {"user_id": who_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum}))
        #                 game_users_who = json.dumps(
        #                     {"user_id": who_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": robNum})
        game_users_who = ''
        who_id = 0
        if str(qun_dict['qun_id']) + '_' + who in users_key_list:
            game_users_who = db_redis(14).get_owner(str(qun_dict['qun_id']) + '_' + who)
            who_id = json.loads(game_users_who)['user_id']
        if '抢劫' == talk or '打劫' == talk:  # 玩家间打劫
            try:
                if not game_users_who_talk:
                    return
                values_dict_who_talk = json.loads(game_users_who_talk)
                if values_dict_who_talk['robNum'] == 0:
                    return "很抱歉您今日打劫次数已用尽（积分可购买打劫次数）"
                if not game_users_who:
                    print(game_users_who, talk)
                    return '打劫失败，对方账号未开通'
                values_dict = json.loads(game_users_who)
                # print(values_dict_who_talk, '---', values_dict)
                if values_dict['gold'] <= 50:
                    return '打劫失败，对方无资产或资产过低！'
                else:
                    win_rate_p = np.array([0.8, 0.2])  # 设置成功失败比例（70%成功，30%被反）
                    fzhuan = np.random.choice([0, 1], p=win_rate_p.ravel())
                    winner = random.randint(0, 1)
                    setjinbi = values_dict['gold']
                    getjinbi = values_dict_who_talk['gold']
                    try:
                        RobCount = values_dict_who_talk['RobCount']
                        if RobCount:
                            rob_count_list = RobCount.split('-')
                        else:
                            rob_count_list = ['0', '0', '0']
                    except Exception:
                        rob_count_list = ['0', '0', '0']
                    print(rob_count_list)
                    if fzhuan == 0:
                        gold = int(setjinbi * 0.4)
                        if gold > 5000:
                            gold = 5000
                        to = random.randint(1, gold)
                        setjinbi = setjinbi - to
                        if winner == 1:
                            to *= 2
                        getjinbi = getjinbi + to
                        values_dict_who_talk['robNum'] -= 1
                        winern = '😂恭喜['
                        win = '成功'
                        winfo = '抢走了对方'
                        ci = '次！'
                        rob_count_list = [str(int(rob_count_list[0]) + 1), str(int(rob_count_list[1]) + 1),
                                          rob_count_list[2]]
                    else:
                        if getjinbi == 1:
                            getjinbi = 2
                        gold = int(getjinbi * 0.2)
                        if gold > 3000:
                            gold = 3000
                        to = random.randint(1, gold)
                        if winner == 1:
                            to *= 2
                        setjinbi += to
                        getjinbi -= to
                        winern = '😂很遗憾['
                        win = '失败'
                        winfo = '反被对方抢走'
                        ci = '次(抢劫失败不消耗次数)！'
                        rob_count_list = [str(int(rob_count_list[0]) + 1), rob_count_list[1],
                                          str(int(rob_count_list[2]) + 1)]
                    values_dict_who_talk['RobCount'] = '-'.join(rob_count_list)
                    values_dict_who_talk['gold'] = getjinbi
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                    esl.update_delete_sql("update users set gold=? and RobCount=? where id=?", getjinbi,
                                          '-'.join(rob_count_list), who_talk_id)
                    values_dict['gold'] = setjinbi
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who,
                                           value=json.dumps(values_dict, ensure_ascii=False))
                    esl.update_delete_sql("update users set gold=? where id=?", setjinbi, who_id)
                    rob_str = '\n打劫统计：总次数' + rob_count_list[0] + '-成功次数' + rob_count_list[1] + '-失败次数' \
                              + rob_count_list[2]
                    if winner == 1:
                        return winern + who_talk + '] 抢劫 [' + who + '] ' + win + '，人品大爆发奖励双倍，' + winfo + str(
                            to) + '金币！\n⚠您还可以抢劫' + str(values_dict_who_talk['robNum']) + ci + rob_str
                    return winern + who_talk + '] 抢劫 [' + who + '] ' + win + '，' + winfo + str(
                        to) + '金币！\n⚠您还可以抢劫' + str(values_dict_who_talk['robNum']) + ci + rob_str
            except Exception as e:
                print('报错了' + str(e))
                return "打劫失败"
        elif '赠送' == talk[:2] or '转赠' == talk[:2]:
            try:
                if not game_users_who_talk:
                    return
                if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
                    return '赠送失败，当前您未开户！'
                if not game_users_who:
                    return '赠送失败，对方未开户！'
                values_dict_who_talk = json.loads(game_users_who_talk)
                if values_dict_who_talk['gold']:
                    values_dict = json.loads(game_users_who)
                    try:
                        to = int(talk[2:])
                    except Exception:
                        return "请输入正确的金币数量"
                    if to > values_dict_who_talk['gold']:
                        return "您的金币不足" + str(to)
                    if to <= 0:
                        return "请输入正确的金币数量"
                    values_dict['gold'] += to
                    values_dict_who_talk['gold'] -= to
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                    esl.update_delete_sql(
                        "update users set gold=? where id=?", values_dict_who_talk['gold'], who_talk_id)
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who,
                                           value=json.dumps(values_dict, ensure_ascii=False))
                    esl.update_delete_sql(
                        "update users set gold=? where id=?", values_dict['gold'], who_id)
                    return '😂[' + who_talk + '] 赠送 [' + who + '] ' + str(to) + '金币成功'
                else:
                    return '赠送失败，当前您金币不足！'
            except Exception as e:
                return '报错了' + str(e)
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
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            qun_dict['pai'] += 1
            if qun_dict['pai'] <= 10:
                result = db_redis(13).get_owner(owner=str(qun_dict['qun_id']))
                if result:
                    sign_list = result[1:-1].replace("'", '').split(', ')
                    sign_in_list = sign_list
                sign_in_list.append(who_talk)
                db_redis(13).set_value(name=str(qun_dict['qun_id']), value=str(sign_in_list))
                sign_in_list.clear()
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            values_dict = json.loads(game_users_who_talk)
            values_dict['sign_toList'] = qun_dict['pai']
            values_dict['point'] = rewardPoint
            values_dict['gold'] = rewardGold
            values_dict['signTime'] = nowTime
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(values_dict, ensure_ascii=False))
            esl.update_delete_sql("update users set sign_toList=?, point=?, gold=?, signTime=? where id=?",
                                  pai, rewardPoint, rewardGold, str(nowTime), who_talk_id)
            now = time.strftime("%H:%M:%S")
            return "👻[" + who_talk + ']签到成功\n👻签到排名：第' + str(pai) + '名\n👻奖励：' + str(rewardPoint) + '积分 ' +\
                   str(rewardGold) + '金币\n👻现有资产：' + str(values_dict['point']) + '积分 ' + \
                   str(values_dict['gold']) + '金币\n👻头衔：新手上路\n👻时间：' + str(now)
        else:
            values_dict = json.loads(game_users_who_talk)
            if values_dict['sign_toList'] == 0:
                qun_dict['pai'] += 1
                if qun_dict['pai'] <= 10:
                    result = db_redis(13).get_owner(owner=str(qun_dict['qun_id']))
                    if result:
                        sign_list = result[1:-1].replace("'", '').split(', ')
                        sign_in_list = sign_list
                    sign_in_list.append(who_talk)
                    db_redis(13).set_value(name=str(qun_dict['qun_id']), value=str(sign_in_list))
                    sign_in_list.clear()
                values_dict['sign_toList'] = qun_dict['pai']
                values_dict['point'] += rewardPoint
                values_dict['gold'] += rewardGold
                jinbi = values_dict['gold']
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
                qun_dict['pai'] = pai
                db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
                values_dict['signTime'] = nowTime
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                       value=json.dumps(values_dict, ensure_ascii=False))
                esl.update_delete_sql(
                    "update users set sign_toList=?, point=?, gold=?, signTime=? where id=?", pai, values_dict['point'],
                    jinbi, str(nowTime), who_talk_id)
                return "👻[" + who_talk + ']签到成功\n👻签到排名：第' + str(pai) + '名\n👻奖励：' + str(rewardPoint) + '积分 ' + str(
                    rewardGold) + '金币\n👻现有资产：' + str(values_dict['point']) + '积分 ' + str(
                    jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
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
        result = esl.select_run('select name, gold from users where GroupChat_ID=%d group by id gold desc limit 0,10'
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
    elif '查询' == talk or '积分查询' == talk or '金币查询' == talk:  # 已废弃game_redis_dict
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            return "对不起，您无资产"
        values_dict = json.loads(game_users_who_talk)
        t_pai = values_dict['sign_toList']
        jifen = values_dict['point']
        jinbi = values_dict['gold']
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
            return "👻[" + who_talk + ']查询成功\n👻签到排名：第' + str(t_pai) + '名\n👻资产：' + str(jifen) + '积分 ' + str(
                jinbi) + '金币\n👻头衔：' + ty + '\n👻时间：' + str(now)
    elif '兑换' == talk:  # 兑换机器人金币
        if str(qun_dict['qun_id']) + '_' + who_talk not in users_key_list:
            return '很抱歉，您的账户无资产~'
        else:
            # redis
            result_dict = json.loads(game_users_who_talk)
            if result_dict['point'] == 0:
                return '很抱歉，您的账户积分不足~'
            result_dict['point'] -= 1
            qun_dict['this_num'] += 1000
            db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                   value=json.dumps(result_dict, ensure_ascii=False))
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            # 本地存储
            game_dict[who_talk] = result_dict['sign_toList'], result_dict['point'], result_dict['gold'], nowTime
            return "@" + who_talk + " 兑换成功，祝您游戏愉快~"
    elif '讲个笑话' == talk or '笑话' == talk or '讲笑话' == talk:
        result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        re = result.json()["content"]
        if '{br}' in re:
            re = re.replace('{br}', '\n')
        return re
    elif '讲个故事' == talk or '故事' == talk or '讲故事' == talk:
        return '很抱歉~该功能尚未实现！ 回复“帮助”查看已完成功能~'
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
                result_dict = json.loads(game_users_who_talk)
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
                    result_dict['gold'] -= 5
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(result_dict, ensure_ascii=False))
                    return '@' + who_talk + " 踩雷了 - 5金币，本轮已结束。继续请继续输入数字。"
                elif Num < a1:
                    c = Num
                    Num_bomb_dict[qname] = a1, c, d
                    monkey_Num += 1
                    result_dict['gold'] += 1
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(result_dict, ensure_ascii=False))
                    return '@' + who_talk + " 恭喜您未中雷 + 1金币，请继续：" + str(c) + " 到" + str(d) + "的数字"
                elif Num > a1:
                    d = Num
                    Num_bomb_dict[qname] = a1, c, d
                    monkey_Num += 1
                    result_dict['gold'] += 1
                    game_dict[who_talk] = cai_lei_info[0], cai_lei_info[1], monkey_Num, cai_lei_info[3]
                    db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + who_talk,
                                           value=json.dumps(result_dict, ensure_ascii=False))
                    return '@' + who_talk + " 恭喜您未中雷 + 1金币，请继续：" + str(c) + " 到" + str(d) + "的数字"
                else:
                    Num_bomb_dict[qname] = a1, c, d
                    return '@' + who_talk + " 输入错误，请输入：" + str(c) + "到" + str(d) + "的数字"
            except Exception as e:
                print("处理踩雷异常了", e)
    elif qname in qun_list:
        try:
            robot_type = qun_dict['robot_type']
        except Exception:
            robot_type = 0
        if robot_type == 0:
            dn = ''
            if talk == '菲菲':
                qun_dict['robot_type'] = 1
            elif talk == '图灵':
                qun_dict['robot_type'] = 2
            elif talk == '小思':
                qun_dict['robot_type'] = 3
            else:
                qun_dict['robot_type'] = 3
                dn = '未选择已默认小思-'
            db_redis(15).set_value(name=qname, value=json.dumps(qun_dict, ensure_ascii=False))
            return dn + welcome
        else:
            # 聊天机器人菲菲
            if robot_type == 1:
                result = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
                re = result.json()["content"]
                if '{br}' in re:
                    re = re.replace('{br}', '\n')
                if '未获取到相关信息' in re:
                    re = '好尴尬呀，我不懂你在说什么呀~'
            elif robot_type == 2:
                # 图灵
                headers = {
                    "Cookie": "UM_distinctid=172b59426052c6-0ae0ede1b1ab8c-34564a7c-1fa400-172b594260624f; "
                              "CNZZDATA1000214860=157799959-1592178930-null%7C1592178930; "
                              "gr_user_id=2dd58613-bba9-44cc-9505-b778900b4b6f; "
                              "JSESSIONID=0198F61914835FC183DD233109693DAF; "
                              "gr_session_id_22222-22222-22222-22222=16a60451-d9e5-4b29-a9ca-19b15b7777f6; "
                              "CNZZDATA1274031688=771303685-1604714880-null%7C1604714880; "
                              "gr_session_id_22222-22222-22222-22222_16a60451-d9e5-4b29-a9ca-19b15b7777f6=true; "
                              "login-token=BfVxWx-DeYRLEsCOVF8U1UJaq3LOgWlOuBOj9y01mPpyN42z5d"
                              "-gdzxzl4ve6Uj1_JXmqDUuGSXRy7lO14_-uSJcYSLFfqW3x49yr6auSTqW4W0UjNC"
                              "-LcYK_u46UjYt777Vnao9TJ1TV0v4hdI7qf4SECBnBlFG8lWPEnM52znVLd8OEgFTBNaZPdxvqjufpmLZ"
                              "-JoEfknIIG "
                              "-EUoVJRliIzeCuw8VI0UiO_YbhC0tXG1lJfwyAS_fextXuHk"
                              "-twmueDAONjxgEWWy0rppCuXpDpy6duiPeHzVRK4ivO5fjYoBrsTmZmrEKJZnpSwZDNhJpcuXsNk"
                              "-YTzVOmDQ7xdBC2vOcrXkc1GZzQ-Hdm7U1tMbZtkTtBB7ax0Inlmu31KFoxmHuPB_StoT2OWwY_m_ZOI-i; "
                              "Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1604717321; "
                              "Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1604718789",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"}
                url = "http://www.tuling123.com/robot-chat/robot/chat/708871/WrA7?geetest_challenge=&geetest_validate" \
                      "=&geetest_seccode= "
                data = {"perception": {"inputText": {"text": str(talk)}}, "userInfo": {"userId": "demo"}}
                res = requests.post(url, json.dumps(data), headers=headers)
                result = json.loads(res.text)
                if result['type'] == 'success':
                    re = result['data']['results'][0]['values']['text']
                else:
                    re = '好尴尬呀，我不懂你在说什么呀~'
                    print(result)
            else:  # 小思
                url = 'https://api.ownthink.com/bot'
                headers = {"Content-Type": "application/json",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                                         "(KHTML, like Gecko)Chrome/70.0.3538.25 "
                                         "Safari/537.36Core/1.70.3741.400 QQBrowser/10.5.3863.400"}
                data = {"appid": "1ac9c3cf079bbf0c5f795625bd159fbe", "Secret": "b49389fda4894414b122bbf024f6259e",
                        "spoken": talk, "userid": qun_dict['qun_id']}
                res = requests.post(url, data, headers=headers)
                result = json.loads(res.text)
                if result['message'] == 'success':
                    re = result['data']['info']['text']
                else:
                    re = '好尴尬呀，我不懂你在说什么呀~'
                    print(result)
            print(qname, "--群聊：{}  ({})".format(re, datetime.now()))
            return re
    elif qname in ana_list:
        a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
        return a.split()[0]
    else:
        if len(talk) == 4:  # 输入成语直接开始成语接龙
            res = chengyujielong(talk, qname)
            if res:
                idiom_list.append(qname)
                return '@' + who_talk + " 成语接龙开始咯：" + res
                # else:
                #     return '@' + who_talk + '\u2005本喵正专心上网课呢，不跟你聊天哦~不如@我说“课程表”，看看我的日程？'
        if who == this:
            # return "抱歉~ 暂时不明白您说什么呢"
            return


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
    try:
        this = msg['User']['Self']['DisplayName']
        if not this:
            this = msg['User']['Self']['NickName']
    except Exception as e:
        print(e)
        this = ''
    if '收到红包，请在手机上查看' == msg['Content']:
        if t_name in red_packet_list:
            itchat.send(talk, qname)
        return
    elif '加入了群聊' in msg['Content']:
        new = msg['Content'].split()
        s = new[0].split('"')
        if len(s) >= 4:
            if s[4] == '加入了群聊':
                if t_name in '三门峡2.5云车场调试':
                    return
                itchat.send(msg['Content'], qname)
                if '珠峰' in t_name:
                    itchat.send('欢迎"' + s[3] +
                                '"新朋友，出来报道，请爆照.积极发言，发红包,多参加活动 分享过去的活动图片！'
                                '不可以发与珠峰群无关的广告，链接和小程序！否则请出！谢谢配合！', qname)
                elif '粤宋堂' in t_name:
                    itchat.send('欢迎"' + s[3] + '"新朋友，新人进群改备注（注意备注格式），发红包！', qname)
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


@itchat.msg_register(itchat.content.RECORDING)  # 录音类
def RECORDING_rep(msg):
    if os.path.exists(RECORDING_dir) and os.path.isdir(RECORDING_dir):
        pass
    else:
        os.mkdir(RECORDING_dir)
    msg.download(RECORDING_dir + '\\' + msg.fileName)  # print('私发发录音了', msg)


@itchat.msg_register(itchat.content.RECORDING, isGroupChat=True)  # 群录音类
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
    status = itchat.check_login()
    print("当前状态：", status)
    if status != '200' and status != '400':
        # itchat.logout()
        print("离线了", status)
        itchat.auto_login(hotReload=True)
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
    itchat.logout()
    return


if __name__ == '__main__':
    try:
        run()  # 初始化
        itchat.auto_login(hotReload=True)  # 登
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
        # for g in itchat.get_chatrooms(update=True)[0:]:
        #     print(g)
        itchat.run(blockThread=False)
    except Exception:
        with open('chat/error.log', 'a') as f:
            f.write('*' * 100 + "\n")
            print("外部捕获到异常")
            f.write(traceback.format_exc())  # 使用 traceback.format_exc() 获取异常详细信息
            f.write('*' * 100 + "\n")
