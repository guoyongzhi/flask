import requests, json


def main():
    # 参数
    farmat = 1
    cityname = input("请输入你想查询的城市天气：")
    key = '621043608cb9e7f7f485461ef9e5adef'
    get_weather(farmat, cityname, key)


def get_weather(format, cityname, key):
    url = 'http://v.juhe.cn/weather/index'
    params = 'format={}&cityname={}&key={}'.format(format, cityname, key)
    city_weather = requests.get(url, params)
    # print(city_weather)
    result = json.loads(city_weather.text)
    # print(result)
    if result:
        if result['error_code'] == 0:
            print("请求成功！")
        else:
            print(result['reason'])
    else:
        print('请求接口失败！！')


if __name__ == "__main__":
    # main()
    # aa = '@A乐雅家具厂13066278897 下个月我们在一起去'
    # dict = dict()
    # if 'a' not in dict:
    #     print(11)
    # else:
    #     print(22)
    # print(len("下个月我"))
    # aaa = dict(username='宋Pro DM～你身边的保险小能手')
    # talk = '@宋Pro DM～你身边的保险小能手 修车的时候我要在那里看着他修吗'
    # new = talk.split()[0]
    # who = new[1:]
    # print(talk.split())
    # ss = 0
    # changdu = talk.split()
    # dd = 1
    # while ss < 3:
    #     if 'username' in aaa:
    #         awho = aaa['username']
    #         print(who, type(who), awho, type(awho))
    #         if who == awho:
    #             print('相等了')
    #             break
    #         else:
    #             print(who)
    #             ss += 1
    #             who = who + ' ' + changdu[ss]
    # print(who, new[1:])
    # nnn = '宋Pro DM～你身边的保险小能手'
    # bbb = changdu[0] + ' ' + changdu[1]
    # bbb = bbb[1:]
    # print(type(nnn), type(bbb))
    # if nnn == bbb:
    #     print('OK')
    # dd = 0
    # sn = 2
    # list = [2, 3, 4, 5, 6]
    # if dd == 0:
    #     while sn < 3:
    #         for i in list:
    #             print(i)
    #             if sn == i:
    #                 print('nnnnnnnnnn')
    #                 dd = 1
    #                 break
    #         if dd == 1:
    #             break
    #         else:
    #             # print(who)
    #             sn += 1
                # who = who + ' ' + changdu[ss]
    talk = '@机器人longer [呲牙]'
    print(len(talk), talk)
    new = talk.split()
    # ss = talk.split('@')
    # print(new, ss)
    # url = "http://open.iciba.com/dsapi"
    # req = requests.get(url)
    # # "content":"Interests are anchors, and I believe they will bring peace and even happiness in the end."
    # contents = req.json()['content']
    # print(contents)
    # trans = req.json(contents)['translation']
    # print(trans)
    print(new, len(new))
    who = new[0]
    who = who[1:]
    a = 1
    ss = 0
    users_list = ['机器人longer']
    dd = 0
    while ss <= len(new):
        for i in users_list:
            print(1111, i, who)
            if i == who:
                dd = 1
                break
        if dd == 1:
            break
        else:
            ss += 1
            if ss >= len(new):
                break
            print('ss', ss)
            insp = who + ' ' + new[ss]
            a = 1
            print(2222, insp, who)
            while True:
                ll = len(insp) + 1
                print(talk[:ll], insp)
                if talk[:ll] == '@' + insp:
                    who = insp
                    break
                else:
                    nn = ' '
                    for i in range(0, a):
                        nn += ' '
                    insp = who + nn + new[ss]
                    a += 1
                    print(333, insp, who)
    try:
        print(ss)
        if ss + 1 < len(new):
            if ss + 1 != len(new):
                talk = ''
                for i in range(ss + 1, len(new)):
                    if talk == '':
                        talk = talk + new[i]
                    else:
                        talk = talk + ' ' + new[i]
            else:
                talk = new[ss + 1]
        else:
            talk = ''
    except:
        talk = ''
    print(who, talk)
    
    alist = []
    print(type(alist))
    if type(alist) is list:
        print('是list')
    blist = dict()
    print(type(blist))
    if type(blist) is dict:
        print('是dict')
    
    # new = aa.split()[0]
    # te = aa.split()[1]
    # print(new[1:])
    # print(new[:1])
    # print(te)
