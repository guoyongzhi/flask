
""" 处理本地数据未同步至redis（已经执行）
import json
from axf.dbredis import db_redis
with open('config.txt', 'r', encoding='utf-8') as file:
    a_list = []
    aa = file.readlines()
    for a in aa:
        a_list.append(a[:-4])
    file.close()
    game_dict = json.loads(a_list[2])
users_keys_list = db_redis(14).r.keys()
del_list = []
# print(game_dict)
for g in game_dict.keys():
    if str('19_') + g in users_keys_list:
        del_list.append(g)
        res = db_redis(14).get_owner(str('19_') + g)
        new = game_dict[g]
        result = json.loads(res)
        result['point'] += new[1]
        result['gold'] += new[2]
        print(res, game_dict[g])
        print(result)
        re = db_redis(14).set_value(name=str('19_') + g, value=json.dumps(result))
for i in del_list:
    del game_dict[i]
print(game_dict.keys())
qun_list = user_list = user_idiom_list = red_packet_list = idiom_list = ana_list = users_list = sign_in_list = []
this_num = 0
idiom_dict = dict()
with open('config.txt', 'w', encoding='utf-8') as file:
    file.write('.'.join(qun_list))
    file.write('---\n')
    file.write('.'.join(user_list))
    file.write('---\n')
    file.write(json.dumps(game_dict))
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
    file.write(json.dumps(idiom_dict))
    file.write('---\n')
    file.write('.'.join(users_list))
    file.write('---\n')
    file.close()
"""
# qun_id = 19
# from axf.dbredis import db_redis
# result = db_redis(13).get_owner(owner=str(qun_id))
# if result:
#     sign_list = result[1:-1].replace("'", '').split(', ')
#     sign_in_list = sign_list
# print(str(sign_in_list))
# sign_list = result[1:-1].replace("'", '').split(',')
# sign_in_list = sign_list
# print(str(sign_in_list))
