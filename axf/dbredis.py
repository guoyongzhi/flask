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
# pool = redis.ConnectionPool(host='129.28.151.153', password='tengo153yz')  # 实现一个连接池

# r = redis.Redis(connection_pool=pool)


class db_redis(object):
    def __init__(self, db=0):
        pool = redis.ConnectionPool(host='129.28.151.153', password='tengo153yz', max_connections=15)
        if db != 0:
            self.r = redis.Redis(connection_pool=pool, db=db)
        else:
            self.r = redis.Redis(connection_pool=pool)
    
    def set_value(self, name, value, ex=0, px=0):
        if ex and px:
            self.r.set(name=name, value=value, ex=ex, px=px)
        elif px:
            self.r.set(name=name, value=value, px=px)
        elif ex:
            self.r.set(name=name, value=value, ex=ex)
        else:
            self.r.set(name=name, value=value)
        return True
    
    def get_owner(self, owner):
        return self.r.get(name=owner)
    
    def delete(self, name):
        self.r.delete(name)
        return True


# user_info = dict(id=1, name='小明', age=18)
user_info = dict(pai=1, jifen=20, jinbi=201)
db_redis().set_value(name='85197', value=json.dumps(user_info), ex=30 * 60)
# print(r.keys())
# print(r.info())
# print(r)
owner = db_redis().get_owner('85197')
if not owner:
    print(owner)
else:
    print(json.loads(owner.decode('utf8')))
# # print(r.get('redisutil').decode('utf8'))
# # db_redis().delete(name='1')
# nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# t_now = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 00:00:00'
# return_time = '2020-10-10 18:00:00'
# if t_now > return_time:
#     print(11111)

# new_time = time.strptime(nowTime, '%Y-%m-%d %H:%M:%S')
# old_time = time.strptime(return_time, '%Y-%m-%d %H:%M:%S')
# print(nowTime, return_time)
# loop_time = time.gmtime(time.mktime(new_time) - time.mktime(old_time))
# print(loop_time)

