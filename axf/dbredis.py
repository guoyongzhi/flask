#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
import time
import redis

'''
这种连接是连接一次就断了，耗资源.端口默认6379，就不用写
r = redis.Redis(host='127.0.0.1',port=6379,password='tianxuroot')
r.set('name','root')

print(r.get('name').decode('utf8'))
'''
'''
连接池：
当程序创建数据源实例时，系统会一次性创建多个数据库连接，并把这些数据库连接保存在连接池中，当程序需要进行数据库访问时，
无需重新新建数据库连接，而是从连接池中取出一个空闲的数据库连接
'''


class db_redis(object):
    def __init__(self, db=0):
        """
        db15 为群 db14 为用户(带群ID) db13为签到排行榜(带群ID)
        :param db:
        :type db:
        """
        if db != 0:
            pool = redis.ConnectionPool(host='129.28.151.153', password='tengo153yz',
                                        decode_responses=True, max_connections=1, db=db)
        else:
            pool = redis.ConnectionPool(host='129.28.151.153', password='tengo153yz',
                                        decode_responses=True, max_connections=1)
        self.r = redis.Redis(connection_pool=pool, decode_responses=True)
    
    def set_value(self, name, value, ex=0, px=0):
        """
        设置缓存
        :param name: 键
        :type name: str
        :param value: 值
        :type value: str
        :param ex:延时过期秒数
        :type ex: int
        :param px:延时过期毫秒数
        :type px:int
        :return:执行结果
        :rtype:bool
        """
        if ex and px:
            self.r.set(name=name, value=value, ex=ex, px=px)
        elif px:
            self.r.set(name=name, value=value, px=px)
        elif ex:
            self.r.set(name=name, value=value, ex=ex)
        else:
            self.r.set(name=name, value=value)
        return True
    
    def batch_set_value(self, parameters=None, **kwargs):
        """
        批量设置
        :param parameters: 参数集合
        :type parameters: dictionary
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return: 成功或失败
        :rtype: bool
        """
        if kwargs:
            if parameters:
                for k in kwargs.keys():
                    parameters[k] = kwargs[k]
                self.r.mset(parameters)
            else:
                self.r.mset(kwargs)
        else:
            if parameters:
                self.r.mset(parameters)
            else:
                return False
        return True
    
    def batch_get_value(self, keys=None):
        """
        批量获取参数
        :param keys: key 按list排列
        :type keys:list
        :return:返回按 keys 顺序排列的值列表
        :rtype:list
        """
        if keys:
            res = self.r.mget(keys)
        else:
            return 'Error'
        return res
    
    def get_set_value(self, key, value):
        """
        设置新值并获取原来的值
        :param key: 键名
        :type key: str
        :param value: 值
        :type value: str
        :return: 旧值
        :rtype: str
        """
        keys = self.r.keys()
        if key in keys:
            res = self.r.getset(key, value)
        else:
            return 'Error'
        return res
    
    def get_owner(self, owner):
        return self.r.get(name=owner)
    
    def delete(self, name):
        keys = self.r.keys()
        if name in keys:
            self.r.delete(name)
        else:
            return False
        return True
    
    def get_db_keys(self):
        return self.r.keys()


if __name__ == '__main__':
    # user_info = dict(id=1, name='小明', age=18)
    # user_info = dict(pai=1, jifen=20, jinbi=201)
    # user_info = [12, 13, 14]
    # print(db_redis().get_set_value('foo', json.dumps(user_info)))
    # print(json.loads(db_redis().get_owner('1')))
    from static.src.api.game_views import execute_sql_lite
    esl = execute_sql_lite()
    # table_list = ['GroupChat', 'users', 'Backpack', 'shop', 'monster', 'prop']
    # for t in table_list:
    #     esl.new_table(tables_name=t)
    qun_id = 16
    who_talk = 'CC'
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
    ActualUserName = ''
    users_key_list = db_redis(14).get_db_keys()
    if str(qun_id) + '_' + who_talk in users_key_list:
        game_users_who_talk = db_redis(14).get_owner(str(qun_id) + '_' + who_talk)
        who_talk_id = json.loads(game_users_who_talk)['user_id']
    else:  # redis + sqlite 存储
        esl.update_delete_sql(sql='delete from users where id=1')
        sql = 'select max(id) from users where name=? and GroupChat_ID=?'
        who_talk_list = esl.select_run(sql, who_talk, qun_id)
        if not who_talk_list[0][0]:
            esl.insert_sql(table_name='users', sql=[qun_id, who_talk, '', ActualUserName, 0, 0, 0, 0, 0, 0, nowTime])
            time.sleep(0.05)
            sql = "select max(id) from users where name=? and GroupChat_ID=?"
            who_talk_list = esl.select_run(sql, who_talk, qun_id)
            if who_talk_list:
                if who_talk_list[0][0]:
                    who_talk_id = who_talk_list[0][0]
                    if who_talk_id == 0:
                        print("当前用户id为0")
                    # db_redis(14).set_value(name=str(qun_id) + '_' + who_talk, value=json.dumps(
                    #     {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": 18}))
                    game_users_who_talk = json.dumps(
                        {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": 18})
            else:
                print(111)
        else:
            who_talk_id = who_talk_list[0][0]
            if who_talk_id == 0:
                print("当前用户id为0")
            if db_redis(14).r.exists(str(qun_id) + '_' + who_talk):
                print("已找到用户")
                game_users_who_talk = db_redis(14).get_owner(str(qun_id) + '_' + who_talk)
            else:
                db_redis(14).set_value(name=str(qun_id) + '_' + who_talk, value=json.dumps(
                    {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": 18}))
                game_users_who_talk = json.dumps(
                    {"user_id": who_talk_id, "sign_toList": 0, "point": 0, "gold": 0, "robNum": 18})
    print(who_talk_id)
    # print(db_redis().batch_get_value(user_info))
    # a = 85197
    # for i in range(10):
    #     db_redis(db=1).set_value(name=str(a), value=json.dumps(user_info))
    #     a += 1
    # # print(r.keys())
    # # print(r.info())
    # # print(r)
    # owner = db_redis().get_owner('85197')
    # if not owner:
    #     print(owner)
    # else:
    #     print(json.loads(owner.decode('utf8')))
    # # print(r.get('redisutil').decode('utf8'))
    # # db_redis().delete(name='1')
    # nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # t_now = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 00:00:00'
    # return_time = '2020-10-10 18:00:00'
    # if t_now > return_time:
    #     print(11111)
