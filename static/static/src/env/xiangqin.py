import os
import time
from aip import AipSpeech
from axf.dbmysql import my_db


# APP_ID = '16007067'
# API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
# SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'
#
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class mubot(object):
    def __init__(self):
        self.path = r"93-97女生.txt"
    
    def get_zhang(self):
        with open("93-97女生删改.txt", 'r', encoding='utf-8') as f:
            aaa = f.readlines()
            f.close()
        i = 0
        a = 2
        list = []
        dis = dict(Num='', Sex='', rdata='', SingleTime='', Location1='', Location2='', Education='', Height='',
                   Weight='', rwork='', other='')
        for m, aa in zip(range(0, len(aaa)), aaa):
            vaule = ''
            fielname = aa.split()[0]
            # print(fielname)
            if fielname == '——照片在上，资料在下——':
                i += 1
                a = 0
            else:
                try:
                    name = str(fielname.split('：')[0])
                    vaule = fielname.split('：')[1]
                    if name == "编号":
                        dis['Num'] = vaule
                    elif name == "性别":
                        dis['Sex'] = vaule
                    elif name == "出生年月":
                        dis['rdata'] = vaule
                    elif name == "单身时间":
                        dis['SingleTime'] = vaule
                    elif name == "籍贯/成长地":
                        dis['Location1'] = vaule
                    elif name == "目前所在地":
                        dis['Location2'] = vaule
                    elif name == "学历":
                        dis['Education'] = vaule
                    elif name == "工作单位及岗位":
                        dis['rwork'] = vaule
                    elif name == "身高":
                        dis['Height'] = vaule
                    elif name == "体重":
                        dis['Weight'] = vaule
                    else:
                        dis['other'] += vaule + ','
                except Exception as e:
                    if name == "编号":
                        dis['Num'] = vaule
                    elif name == "性别":
                        dis['Sex'] = vaule
                    elif name == "出生年月":
                        dis['rdata'] = vaule
                    elif name == "单身时间":
                        dis['SingleTime'] = vaule
                    elif name == "籍贯/成长地":
                        dis['Location1'] = vaule
                    elif name == "目前所在地":
                        dis['Location2'] = vaule
                    elif name == "学历":
                        dis['Education'] = vaule
                    elif name == "工作单位及岗位":
                        dis['rwork'] = vaule
                    elif name == "身高":
                        dis['Height'] = vaule
                    elif name == "体重":
                        dis['Weight'] = vaule
                    vaule += fielname  # print(e)
            list.append(vaule)
            if i > 1:
                if a == 0:
                    try:
                        ot = dis['other'].split('"')[0]
                        ot += dis['other'].split('"')[1]
                        ot += dis['other'].split('"')[2]
                        ot += dis['other'].split('"')[3]
                        ot += dis['other'].split('"')[4]
                        ot += dis['other'].split('"')[5]
                    except Exception as e:
                        # print(e)
                        dis['other'] = ot
                    list = []
                    sql = 'INSERT INTO xq(Num, Sex, rdata, SingleTime, Location1, Location2, Education, Height, Weight, rwork, other) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (
                    dis['Num'], dis['Sex'], dis['rdata'], dis['SingleTime'], dis['Location1'], dis['Location2'],
                    dis['Education'], dis['Height'], dis['Weight'], dis['rwork'], str(dis['other']))
                    # print(sql)
                    res = my_db(sql, 'passport')
                    if res == 'ok':
                        print(dis['Num'], "成功")
                        dis['other'] = ''
                        a = 1
                    else:
                        print("失败", sql)
    
    def delbialline(self):
        infp = open(self.path, 'r', encoding='utf-8')
        outfp = open('93-97女生删改.txt', 'w', encoding='utf-8')
        lines = infp.readlines()
        for li in lines:
            if li.split():
                outfp.writelines(li)
        infp.close()
        outfp.close()


mubot().get_zhang()
# mubot().delbialline()
# mubot().get_len("最佳赘婿", "第902章")