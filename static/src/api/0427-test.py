import time

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
    # datadict = dict(t1=['a', 'v', 'b', 'd'], t2=['a', 'v', 'b', 'd', '3'])
    # datadict = dict()
    # if not datadict:
    #     print("空数据")
    # for list in datadict:
    #     print(datadict[list])
    filename = 'D:/a/ens/1023.mp4'
    f = filename[-3:]
    print(f)
    if not filename[-3:] in 'jpgJPGpngPNGmp3mp4war':
        print("文件格式不对")
    print('OK')
    a = [1]
    b = dict()
    print(a, type(a))
    if not type(b) is list:
        print(111)
    else:
        print(222)
