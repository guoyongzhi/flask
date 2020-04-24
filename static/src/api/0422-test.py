# import requests
# import re
# from bs4 import BeautifulSoup
#
#
# res = requests.get('http://192.168.11.153:8301/api/v1/help/index')
# res.encoding = res.apparent_encoding
# result = res.text
# # print(result)
# soup = BeautifulSoup(result, 'html.parser')
#
# ul = soup.find_all(name='li')
# # print(ul, len(ul))
# # li_list = ul.find_all(name='li')
#
# for i in zip(ul):
#     p = re.compile('\W')
#     li = re.findall(p, i)
#     print(li)
import itchat

# 登录
# itchat.login()
itchat.auto_login()
# # 发送消息
# itchat.send(u'你好', 'filehelper')
# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
# print(friends)

# 初始化计数器，有男有女，当然，有些人是不填的
male = female = other = 0

# 遍历这个列表，列表里第一位是自己，所以从"自己"之后开始计算
# 1表示男性，2女性
for i in friends[1:]:
    # print(i)
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1

# 总数算上，好计算比例啊～
total = len(friends[1:])

# 好了，打印结果
print(u"男性好友：%.2f%%" % (float(male) / total * 100))
print(u"女性好友：%.2f%%" % (float(female) / total * 100))
print(u"其他：%.2f%%" % (float(other) / total * 100))


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    msg = "努力上班中，晚点回复！"
    print(msg)
    return msg


itchat.run()
