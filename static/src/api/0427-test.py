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
    main()