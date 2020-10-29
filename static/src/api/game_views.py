import sqlite3
from static.src.api.gime_table import *
import numpy as np
from static.src.api.config.get_game_config import *


def open_db():
    db = 'games.db'
    coon = sqlite3.connect(db)
    c = coon.cursor()
    return coon, c


def close_db(coon, c):
    coon.commit()
    coon.close()


class Users:
    __table_name__ = 'users'
    
    def __init__(self, parameter):
        self.GroupChat_ID = parameter.get('GroupChat_ID', 0)
        self.name = parameter.get('name', '')
        self.nickname = parameter.get('nickname', '')
        self.username = parameter.get('username', '')
        self.sign_toList = parameter.get('sign_toList', 0)
        self.point = parameter.get('point', 0)
        self.gold = parameter.get('gold', 0)
        self.signTime = parameter.get('signTime', '')
        self.fightingCombat = parameter.get('fightingCombat', 0)
        self.hiddenScore = parameter.get('hiddenScore', 0)
        self.addTime = parameter.get('sign_toList', '')
    
    @classmethod
    def add(cls, users):
        coon, c = open_db()
        sql_inset = """"""
        coon.execute(sql_inset)
        close_db(coon, c)


class execute_sql_lite(object):
    def __init__(self):
        self.db = r'I:\work\flask\static\src\api\games.db'
    
    # def __new__(cls, *args, **kwargs):
    #
    #     return
    
    def select_run(self, sql):
        try:
            coon = sqlite3.connect(self.db)
            c = coon.cursor()
            c.execute(sql)
            res_list = []
            for r in c.fetchall():
                res_list.append(r)
            coon.close()
            return res_list
        except Exception as e:
            print(e)
            return None
    
    def run_commit(self, sql):
        coon = sqlite3.connect(self.db)
        c = coon.cursor()
        try:
            c.execute(sql)
            coon.commit()
            res = 'ok'
        except Exception as e:
            res = str(e)
        coon.close()
        return res
    
    def new_table(self, tables_name):
        dd = tables_name + '_table_sql'
        sql = ''
        for key, value in globals().items():
            if dd == key:
                sql = value
        if not sql:
            return
        return self.run_commit(sql)
    
    def insert_sql(self, table_name, sql):
        if table_name == 'users':
            if not sql[1]:
                if not sql[2]:
                    return
        insert_table = send_sql(table_name)
        dd = ''
        for i in sql:
            if isinstance(i, (str, float)):
                if dd:
                    dd += ",'" + i + "'"
                else:
                    dd = "'" + i + "'"
            elif isinstance(i, int):
                if dd:
                    dd += ',' + str(i)
                else:
                    dd = str(i)
        sql = 'insert into %s values (%s)' % (insert_table, dd)
        print(sql)
        return self.run_commit(sql)
    
    def update_delete_sql(self, sql):
        return self.run_commit(sql)
    
    def select_sql(self, sql):
        return self.select_run(sql)


def Boss_challenge(Boss_blood, number, total_force):
    cut_result = total_force * (number + 8)
    print(cut_result)
    if cut_result > Boss_blood:
        win_rate = 1
    else:
        print(cut_result / Boss_blood)
        if cut_result / Boss_blood <= 0.5:
            win_rate = 0.39
        elif cut_result / Boss_blood <= 0.6:
            win_rate = 0.59
        elif cut_result / Boss_blood <= 0.7:
            win_rate = 0.69
        elif cut_result / Boss_blood <= 0.8:
            win_rate = 0.79
        elif cut_result / Boss_blood <= 0.9:
            win_rate = 0.89
        else:
            win_rate = 0.95
    win_rate_p = np.array([1 - win_rate, win_rate])
    result_index = np.random.choice([0, 1], p=win_rate_p.ravel())
    print(result_index)
    return result_index


def Boss_prop_drop(Boss_name, number, total_prop):
    drop_a = Config().get_PU('Boss-Probability', Boss_name)
    return drop_a


if __name__ == '__main__':
    #  初始化
    # table_list = ['GroupChat', 'users', 'Backpack', 'shop', 'monster', 'prop']
    esl = execute_sql_lite()
    # for t in table_list:
    #     esl.new_table(tables_name=t)
    # res = esl.select_run("select id from GroupChat GC where name='诗和远方｜户外'")
    # esl.insert_sql(table_name='users', sql=[1, 23, '', 123, 0, 0, 0, 0, 0, 0, 123])
    who_talk_list = esl.select_run(sql="select max(id) from users where name='%s'" % "Mr. Black")
    print(who_talk_list)
    if who_talk_list:
        print(who_talk_list[0][0])
        print(11)
    else:
        print(22)
    # print(res)
    # Boss_challenge(10000, 1, 278)
    # execute_sql_lite().insert_sql('GroupChat', ['sddf', 'fffffff'])
    # execute_sql_lite()
