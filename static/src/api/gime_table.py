# 群表(id，群名称，微信群名称)
GroupChat_table_sql = 'create table GroupChat(id integer PRIMARY KEY AUTOINCREMENT not NULL,name text, username text)'
# 用户表（id，群id，用户名称，昵称，微信用户名称，签到排名，积分，金币，签到时间，战斗力，隐藏分，添加时间）
users_table_sql = 'create table users(id integer PRIMARY KEY AUTOINCREMENT not NULL,' \
                  'GroupChat_id int,name text, nickname text, username text,' \
                  ' sign_toList int, integral int, gold int, signTime text, ' \
                  'fightingCombat int, hiddenScore int, addTime text)'
# 背包表（id，用户id，是否装配（0未装配、1装配），道具id，道具数量）
Backpack_table_sql = 'create table Backpack(id integer PRIMARY KEY AUTOINCREMENT not NULL, user_id int, isDress int,' \
                     'prop_id int, propCount int)'
# 商店表（id，商品名称，商品价格，商品介绍，商品属性）
shop_table_sql = 'create table shop(id integer PRIMARY KEY AUTOINCREMENT not NULL, ' \
                 'shopName text, price float, recommend text, property text)'
# 怪物表（id，怪物名称，怪物星级，怪物血量，怪物介绍，怪物属性）
monster_table_sql = 'create table monster(id integer PRIMARY KEY AUTOINCREMENT not NULL,' \
                    ' name text, starLevel int, blood int, recommend text, property text)'
# 道具表（id，道具名称，是否为碎片(0否、1是)，碎片合成数（30），当前数量，道具介绍，道具属性, 可合成道具id（道具为0，碎片为合成后道具id））
prop_table_sql = 'create table prop(id integer PRIMARY KEY AUTOINCREMENT not NULL,' \
                 ' name text, isDebris int, compound int, count int, recommend text, property text, compoundID int)'


def send_sql(table):
    value = ''
    for key, value in globals().items():
        # print(type(key), value)
        if key == table + '_table_sql':
            # print(key, value)
            value = value
            break
    if value:
        sql = str(value)
        a_list = ['create table ', 'id integer PRIMARY KEY AUTOINCREMENT not NULL, ', ' text', ' int', ' AUTOINCREMENT',
                  ' INTEGER', 'integer', 'id,', ' not NULL', ' float']
        for i in a_list:
            sql = sql.replace(i, '')
        return sql


if __name__ == '__main__':
    # print(send_sql('monster'))
    # print(send_sql('shop'))
    import time
    import numpy as np

    # np.random.seed(0)
    sun = error = 0
    a = 1
    while a <= 30:
        p = np.array([0.96, 0.04])
        index = np.random.choice([1, 2], p=p.ravel())

        if index == 1:
            sun += 1
        else:
            error += 1
        a += 1
    print(sun, error)
