import json
import random

from .probability import probability
from axf.dbredis import db_redis


class Rob(object):
    def __init__(self, who, who_talk, this, esl):
        """
        打劫赠送相关
        :param who: 对象
        :type who:
        :param who_talk: 主动人（触发者）
        :type who_talk:
        :param this: 本人
        :type this:
        :param esl: 数据库环境
        :type esl:
        """
        self.who = who
        self.who_talk = who_talk
        self.this = this
        self.d_list = ['零', '一', '双', '三', '四', '五']
        self.esl = esl
    
    def rob_robot(self, values_dict_who_talk, qun_dict):
        """
        打劫机器人
        :param values_dict_who_talk: 打劫人字典
        :type values_dict_who_talk: dict
        :param qun_dict: 群字典
        :type qun_dict:
        :return:
        :rtype:
        """
        if qun_dict['this_num'] == 0:
            return "@" + self.who_talk + " 抢劫失败，机器人资产不足，可回复《兑换》消耗1积分。兑换机器人1000金币~"
        if qun_dict['this_num'] <= 500:
            to = qun_dict['this_num']
        else:
            to = random.randint(500, qun_dict['this_num'])
        qun_dict['this_num'] -= to
        double = probability().probability_rob()
        to *= double
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
        db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + self.who_talk,
                               value=json.dumps(values_dict_who_talk, ensure_ascii=False))
        self.esl.update_delete_sql("update users set gold=? where id=?", getjinbi, values_dict_who_talk['user_id'])
        db_redis(15).set_value(name=qun_dict['qname'], value=json.dumps(qun_dict, ensure_ascii=False))
        if double > 1:
            return '😂恭喜[' + self.who_talk + '] 抢劫 [' + self.this + '] 成功，人品大爆发奖励' + self.d_list[
                double] + '倍，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫' + str(
                values_dict_who_talk['robNum']) + '次\n机器人剩余余额' + str(qun_dict['this_num']) + '(打劫机器人不消耗次数)！'
        return '😂[' + self.who_talk + '] 抢劫 [' + self.this + '] 成功，抢走了对方' + str(to) + '金币！\n⚠您还可以抢劫' + str(
            values_dict_who_talk['robNum']) + '次\n机器人剩余余额：' + str(qun_dict['this_num']) + '(打劫机器人不消耗次数)！'
    
    def rob_user(self, values_dict_who_talk, game_users_who, qun_dict):
        """
        用户间打劫
        :param values_dict_who_talk: 打劫人字典
        :type values_dict_who_talk: dict
        :param game_users_who: 被打劫人字典
        :type game_users_who: str
        :param qun_dict: 群
        :type qun_dict: dict
        :return: 结果
        :rtype: str
        """
        try:
            if self.who == self.who_talk:
                return "不要伤害自己哦！"
            if values_dict_who_talk['robNum'] == 0:
                return "很抱歉您今日打劫次数已用尽（积分可购买打劫次数）"
            if values_dict_who_talk['gold'] <= 1000:
                return "自己都是低保户，就不要玩火了！"
            if not game_users_who:
                return '手下留情吧！对方很可怜了！'
            values_dict = json.loads(game_users_who)
            if values_dict['gold'] <= 500:
                return '手下留情吧，' + self.who + '还很弱小呢！'
            else:
                reversal = probability().probability_reversal()
                setjinbi = values_dict['gold']
                getjinbi = values_dict_who_talk['gold']
                double = probability().probability_rob()
                try:
                    RobCount = values_dict_who_talk['RobCount']
                    if RobCount:
                        rob_count_list = RobCount.split('-')
                    else:
                        rob_count_list = ['0', '0', '0']
                except Exception:
                    rob_count_list = ['0', '0', '0']
                if reversal == 0:
                    gold = int(setjinbi * 0.4)
                    if gold > 5000:
                        gold = 5000
                    to = random.randint(500, gold)
                    setjinbi = setjinbi - to
                    to *= int(double)
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
                    to = random.randint(500, gold)
                    getjinbi -= to
                    to *= int(double)
                    setjinbi += to
                    winern = '[流泪]很遗憾['
                    win = '失败'
                    winfo = '反被对方抢走'
                    ci = '次(抢劫失败不消耗次数)！'
                    rob_count_list = [str(int(rob_count_list[0]) + 1), rob_count_list[1],
                                      str(int(rob_count_list[2]) + 1)]
                values_dict_who_talk['RobCount'] = '-'.join(rob_count_list)
                values_dict_who_talk['gold'] = getjinbi
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + self.who_talk,
                                       value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                self.esl.update_delete_sql("update users set gold=? and RobCount=? where id=?", getjinbi,
                                           '-'.join(rob_count_list), values_dict_who_talk['user_id'])
                values_dict['gold'] = setjinbi
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + self.who,
                                       value=json.dumps(values_dict, ensure_ascii=False))
                self.esl.update_delete_sql("update users set gold=? where id=?", setjinbi, values_dict['user_id'])
                rob_str = '\n打劫统计：总次数' + rob_count_list[0] + '-成功次数' + rob_count_list[1] + '-失败次数' + rob_count_list[2]
                if double > 1:
                    return winern + self.who_talk + ']抢劫[' + self.who + ']' + win + '，人品大爆发奖励' + self.d_list[
                        double] + '倍，' + winfo + str(to) + '金币！\n⚠您还可以抢劫' + str(
                        values_dict_who_talk['robNum']) + ci + rob_str
                return winern + self.who_talk + ']抢劫[' + self.who + ']' + win + '，' + winfo + str(
                    to) + '金币！\n⚠您还可以抢劫' + str(values_dict_who_talk['robNum']) + ci + rob_str
        except Exception as e:
            print('报错了' + str(e))
            return "打劫失败"
        
    def presenter_user(self, values_dict_who_talk, game_users_who, qun_dict, talk, users_key_list):
        """
        赠送金币
        :param values_dict_who_talk: 打劫人字典
        :type values_dict_who_talk: dict
        :param game_users_who: 被打劫人字典
        :type game_users_who: str
        :param qun_dict: 群
        :type qun_dict: dict
        :param talk: 话语
        :type talk: str
        :param users_key_list: 用户列表
        :type users_key_list: list
        :return: 结果
        :rtype: str
        """
        try:
            if str(qun_dict['qun_id']) + '_' + self.who_talk not in users_key_list:
                return '赠送失败，当前您一穷二白！'
            if not game_users_who:
                return '赠送失败，对方是个小白！'
            if values_dict_who_talk['gold']:
                values_dict = json.loads(game_users_who)
                try:
                    to = int(talk[2:])
                except Exception:
                    return "请输入正确的金币数量"
                if to > values_dict_who_talk['gold']:
                    return "您已经很穷了，金币不足" + str(to)
                if to <= 0:
                    return "请输入正确的金币数量"
                values_dict['gold'] += to
                values_dict_who_talk['gold'] -= to
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + self.who_talk,
                                       value=json.dumps(values_dict_who_talk, ensure_ascii=False))
                self.esl.update_delete_sql("update users set gold=? where id=?", values_dict_who_talk['gold'],
                                           values_dict_who_talk['user_id'])
                db_redis(14).set_value(name=str(qun_dict['qun_id']) + '_' + self.who,
                                       value=json.dumps(values_dict, ensure_ascii=False))
                self.esl.update_delete_sql("update users set gold=? where id=?", values_dict['gold'],
                                           values_dict['user_id'])
                return '😂[' + self.who_talk + '] 赠送 [' + self.who + '] ' + str(to) + '金币成功'
            else:
                return '穷光蛋就别想着送礼了！'
        except Exception as e:
            return '报错了' + str(e)


if __name__ == '__main__':
    pass
