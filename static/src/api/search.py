
class search(list):
    def __init__(self, chat_list=None, source=None):
        if chat_list:
            super(search, self).__init__(chat_list)
        self.source = source
        
    @classmethod
    def __a(cls):
        print("私有函数__a")
    
    def b(self):
        self.__a()
        
    @classmethod
    def _c(cls):
        print("私有函数_c")


class search_dict(dict):
    def __init__(self, date_dict=None, source=None):
        if date_dict:
            super(search_dict, self).__init__(date_dict)
        self.source = source


# date = search_dict(dict(a=1, b=2, c=3))
# print(date, type(date))
# print(date.items())
# print(date.keys())
# # print(date.has_key('a'))
# if 'a' and 'b' and 'c' in date:
#     print("存在")


def what_talk(talk='', keyword=[]):
    """
    判断话语是否是关键字
    :param talk: 话语
    :type talk: str
    :param keyword: 关键字
    :type keyword: list
    :return: 是否存在
    :rtype: bool
    """
    for key in keyword:
        if talk == key:
            return True
    return False


# talk = '等等就来了'
# if what_talk(talk, ['等等', '就', '我']):
#     print("存在")
#
# if ('等等' or '就' or '我') in talk:
#     print("存在12")
# a = 'e19d5cd5af0378da05f63f891c7467af'
# print(a.upper())
# print(len(a))
# case_index = '1'
# file = r'I:\work\TestUI\data\identityface\login_case.xlsx'
# if case_index and case_index != file:
#     print("重置")

import re

# pattern = re.compile(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$')
# str = u'16042819960701121X'
# print(pattern.search(str))
# d = dict(a=1, b=2, c=3)
# import json
# json.dumps()

# ases = ['timestamp', 'nonce', 'EventType', 'InfoCode']
# print(sorted(ases))
# ases.remove('timestamp')
# print(ases)
# search = search(chat_list=[1, 2, 3], source=1)
# print(search, type(search))
import time
import datetime
now = datetime.datetime.now()
nowdate = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
print(now)
res = now - nowdate
print(res, type(res))
print(int(res.total_seconds()))

import requests

while True:
    res = requests.get("")
