import sqlite3
import setting
from static.src.api.gime_table import *
import numpy as np
from static.src.api.config.get_game_config import *
from django.db import connection


def open_db(db):
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
        database = 'games.db'
        if os.path.exists(database):
            self.db = database
        else:
            database_dir = os.path.join(setting.APP_ROOT + r'static\src\api')
            self.db = os.path.join(database_dir + database_dir)
        if not os.path.exists(self.db):
            print("sqlite数据文件未找到")
    
    # def __new__(cls, *args, **kwargs):
    #
    #     return
    
    def select_run(self, sql, *args, **kwargs):
        # if not os.access(self.db, os.R_OK):
        #     return None
        coon = sqlite3.connect(self.db)
        c = coon.cursor()
        try:
            if args:
                c.execute(sql, args)
            else:
                c.execute(sql)
            res_list = []
            for r in c.fetchall():
                res_list.append(r)
            coon.close()
            return res_list
        except Exception as e:
            coon.close()
            print(sql, args, "sql执行异常", e)
            return None
    
    def run_commit(self, sql, *args):
        coon = sqlite3.connect(self.db)
        c = coon.cursor()
        try:
            if args:
                c.execute(sql, tuple(args[0]))
            else:
                c.execute(sql)
            coon.commit()
            result = 'ok'
        except Exception as e:
            if args:
                print(sql, tuple(args[0]))
            else:
                print(sql)
            print("sql执行异常", e)
            result = str(e)
        coon.close()
        return result
    
    def new_table(self, tables_name):
        dd = tables_name + '_table_sql'
        sql = ''
        for key, value in globals().items():
            if dd == key:
                sql = value
        if not sql:
            return
        return self.run_commit(sql)
    
    def insert_sql(self, table_name, sql, *args):
        if table_name == 'users':
            if not sql[1]:
                if not sql[2]:
                    return
        insert_table = send_sql(table_name)
        sql_l = 'insert into {}'.format(insert_table) + ' values('
        if sql:
            for i in range(len(sql)):
                if i == len(sql) - 1:
                    sql_l += '?)'
                else:
                    sql_l += '?,'
            return self.run_commit(sql_l, sql)
        else:
            return None
    
    def update_delete_sql(self, sql, *args):
        return self.run_commit(sql, args)
    
    def select_sql(self, sql, *args):
        return self.select_run(sql, args)


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
    import json
    from axf.dbredis import db_redis
    esl = execute_sql_lite()
    # users_key_list = db_redis(14).get_db_keys()
    # error_list = []
    # sum_list = []
    # no_list = []
    # dd_list = []
    # for u in users_key_list:
    #     qun_id = u[:2]
    #     try:
    #         qun_id = int(qun_id)
    #     except Exception as e:
    #         print(e)
    #         continue
    #     if qun_id != 19:
    #         continue
    #     users = json.loads(db_redis(14).get_owner(u))
    #     res = esl.update_delete_sql("update users set point=?, gold=? where id=? and GroupChat_ID=?",
    #                                 users['point'], users['gold'], users['user_id'], qun_id)
    #     # res = esl.select_run('select name from users where id=? and GroupChat_ID=?', users['user_id'], qun_id)
    #     if res:
    #         if res[0][0] is None:
    #             error_list.append(u)
    #         elif res[0][0]:
    #             if res[0][0] == 'ok':
    #                 sum_list.append(u)
    #             else:
    #                 dd_list.append(u)
    #         else:
    #             dd_list.append(u)
    #     else:
    #         no_list.append(u)
    # # print(sum_list)
    # print(error_list)
    # print(no_list)
    # print(dd_list)
    
    # ree = esl.select_run('select * from (select count(name) sum, name from users group by name,
    # GroupChat_ID) a where a.sum>1')
    # print(ree)
    # for t in table_list:
    #     esl.new_table(tables_name=t)
    # res = esl.select_run("select id from GroupChat GC where name='诗和远方｜户外'")
    # res = esl.insert_sql(table_name='users', sql=[1, 23, '', 123, 0, 0, 0, 0, 0, 0, 123])
    res = esl.select_run('select name, gold from users where GroupChat_ID=19 group by id order by gold desc limit 0,10')
    # res = esl.select_run("select * from users where GroupChat_ID = 19 and name=%s" % "J'adore")
    print(res)
    # who_talk_list = esl.select_run('''select max(id) from users where name=?''', "Mr. Black")
    # print(who_talk_list)
    # if who_talk_list:
    #     print(who_talk_list[0][0])
    #     print(11)
    # else:
    #     print(22)
    # print(res)
    # Boss_challenge(10000, 1, 278)
    # execute_sql_lite().insert_sql('GroupChat', ['sddf', 'fffffff'])
    # execute_sql_lite()
