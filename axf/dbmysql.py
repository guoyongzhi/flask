#!/usr/bin/Python-3.6.2
def my_db(sql, db):
    import pymysql
    coon = pymysql.connect(
        host='129.204.252.175', user='root', passwd='UjuW5;Ue964!',
        port=3306, db=db, charset='utf8')
    cur = coon.cursor()  # 建立游标
    cur.execute(sql)  # 执行sql
    if sql.strip()[:6].upper() == 'SELECT':
        res = cur.fetchall()
    else:
        coon.commit()
        res = 'ok'
    cur.close()
    coon.close()
    return res


def my_db_select(sql, db):
    import pymysql
    coon = pymysql.connect(
        host='129.204.252.175', user='root', passwd='UjuW5;Ue964!',
        port=3306, db=db, charset='utf8')
    cur = coon.cursor()  # 建立游标
    cur.execute(sql)  # 执行sql
    res = cur.fetchall()
    cur.close()
    coon.close()
    return res


def my_si_db(sql, db):
    import pymysql
    coon = pymysql.connect(host='192.168.11.153', user='root', passwd='iEntrance123456+-*/', port=3306, db=db, charset='utf8')
    cur = coon.cursor()  # 建立游标
    cur.execute(sql)  # 执行sql
    if sql.strip()[:6].upper() == 'SELECT':
        res = cur.fetchall()
    else:
        coon.commit()
        res = 'ok'
    cur.close()
    coon.close()
    return res
# sql = 'select * from passport_city;'
# x = my_db_select(sql, 'passport')
# print(x)
# for i in x:
#     lis = dict(id=i[0], pow=i[1])
#     print(lis, type(lis))
#     # list.append(lis)
# print(dict)
# import numpy as np
# a = np.arange(6).reshape(2, 3)
# print(a)

