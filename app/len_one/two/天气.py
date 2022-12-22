#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
# *_* coding:utf-8 *_*

# 开发团队:中国软件开发团队
# 开发人员:Administrator
# 开发时间:2019/3/23 5:16
# 文件名称:weatherSpider
# 开发工具:PyCharm


import tkinter

import tkinter.messagebox

from tkinter import ttk

import requests

# from PIL import ImageTk as itk

from selenium import webdriver

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.options import Options

import re

'''
 获取本地所在城市名称
 '''


def get_local_city():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 更换头部
    # chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)
    # AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    driver.get("http://www.weather.com.cn")
    text = driver.page_source
    result = re.findall('<span class="city_name"><em>(.*?)</em></span>', text, re.S)
    driver.close()
    return result[0]


class MyFrame(tkinter.Frame):
    def __init__(self, default_city):
        self.root = tkinter.Tk()
        self.root.title("天气查询")
        self.root.geometry('1200x700+400+220')
        # 修改默认应用程序图标
        # self.root.iconbitmap('camero.ico')
        bg = tkinter.Canvas(self.root, width=1200, height=600, bg='white')
        # self.img = itk.PhotoImage(file="bg.jpg")
        bg.place(x=100, y=40)
        # bg.create_image(0, 0, anchor=tkinter.NW, image=self.img)
        self.city = tkinter.Entry(self.root, width=16, font=("仿宋", 18, "normal"))
        self.city.place(x=200, y=60)
        self.city.insert(0, default_city)
        citylabel = tkinter.Label(self.root, text='查询城市', font=("仿宋", 18, "normal"))
        citylabel.place(x=80, y=60)
        # 查询按钮
        chaxun = tkinter.Button(self.root, width=10, height=3, text="查询", bg='#00CCFF', bd=5, font="bold",
                                command=self.search)
        chaxun.place(x=800, y=50)
        # 清除按钮
        clearbtn = tkinter.Button(self.root, width=10, height=3, text="清除", bg='#00CCFF', bd=5, font="bold",
                                  command=self.clear)
        clearbtn.place(x=950, y=50)
        poslabel = tkinter.Label(self.root, text='选择位置', font=("仿宋", 18, "normal"))
        poslabel.place(x=80, y=100)
        comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = ttk.Combobox(self.root, width=30, height=18, font=("仿宋", 18, "normal"),
                                       textvariable=comvalue)  # 初始化
        self.comboxlist["values"] = ("1", "2", "3")
        self.comboxlist.current(0)  # 选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>", self.choose)  # 绑定事件,(下拉列表框被选中时，绑定choose()函数)
        self.comboxlist.place(x=200, y=100)
        self.result = tkinter.Listbox(self.root, heigh=18, width=65, font=("仿宋", 20, "normal"))  # 显示天气框
        self.result.place(x=125, y=150)
        self.citys = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36',
            'Cookie': '__guid=182823328.3322839646442213000.1543932524694.901; '
                      'vjuids=1858d43b6.167798cbdb7.0.8c4d7463d5c5d; vjlast=1543932526.1543932526.30; '
                      'userNewsPort0=1; f_city=%E5%B9%B3%E9%A1%B6%E5%B1%B1%7C101180501%7C; '
                      'Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1543932526,1543932551,1543932579; '
                      'Wa_lvt_1=1547464114,1547464115,1547880054,1547983123; defaultCty=101181001; '
                      'defaultCtyName=%u5546%u4E18; monitor_count=6; Wa_lpvt_1=1547983809'}
        # 开启本地天气查询
        if (default_city != ''):
            self.tianqiforecast(default_city)
    
    def tianqiforecast(self, searchcity):
        city = searchcity
        url = 'http://toy1.weather.com.cn/search?cityname=' + city + '&callback=success_jsonpCallback&_=1548048506469'
        response = requests.get(url, headers=self.headers)
        html1 = response.content.decode('utf-8')
        self.citys = re.findall('"ref":"(.*?)~.*?~(.*?)~.*?~(.*?)~.*?~.*?~.*?~.*?~(.*?)"', html1, re.S)
        if (len(self.citys) == 0):
            a = "出错了,未查找到该城市"
            self.result.insert(tkinter.END, a)
            return  # 显示当前城市常用查询点
        plist = []
        print(self.citys)
        for i in range(0, len(self.citys)):
            # print(i + 1, ':%14s ' % "".join(citys[i]))
            plist.append(self.citys[i][1])
            pos = tuple(plist)
            self.comboxlist["values"] = pos
            self.comboxlist.current(0)
            if len(self.citys) != 0:
                self.query(0)
    
    def search(self):
        mycity = self.city.get()
        if (mycity != ''):
            self.clear()
        self.tianqiforecast(mycity)
    
    def query(self, choose):
        if (len(self.citys[choose][0]) == 9):
            if (self.citys[choose][0][0] != '1' or self.citys[choose][0][1] != '0' or self.citys[choose][0][2] != '1'):
                # 查询国外天气
                print("国外")
                url2 = 'http://www.weather.com.cn/weathern/' + self.citys[choose][0] + '.shtml'
                responseweather = requests.get(url2, headers=self.headers)
                html2 = responseweather.content.decode('utf-8')
                weather = re.findall('<li class="date-.*?".*?".*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
                temp_weather = re.findall(
                    '<p class="weather-info">(.*?)</p>.*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">(.*?)</p>',
                    html2, re.S)
                if len(temp_weather) < 7:
                    # 当天
                    today1 = re.findall('<li class="blue-item active".*?>(.*?)<div class="item-active"></div>\\n</li>',
                        html2, re.S)
                    
                    today = re.findall('<p class="weather-info">(.*?)</p>.*?<p class="wind-info">(.*?)</p>', today1[0],
                                       re.S)
                    print(today)  # 后6天
                    weather.append(temp_weather)
                else:
                    weather.append(temp_weather)
                Hightempture = re.findall(
                    '<script>var eventDay =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
                Lowtempture = re.findall('var eventNight =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];',
                                         html2, re.S)
                # print(Hightempture,Lowtempture)
                b = '查询城市为：' + str(self.citys[choose][3]) + '    ' + str(self.citys[choose][1])
                self.result.insert(tkinter.END, b)
                if len(temp_weather) < 7:  # 如日本
                    if len(weather) <= 0 or len(Lowtempture) <= 0 or len(Hightempture) <= 0 or len(
                            Lowtempture[0]) != 7 or len(Hightempture[0]) != 7:
                        a = '系统出错，数据不完整:'
                        self.result.insert(tkinter.END, a)
                        self.result.insert(tkinter.END, url2)
                        print(url2)
                    else:
                        for i in range(0, 7):
                            if i < 1:
                                a = "".join(weather[i]) + '    ' + Lowtempture[0][i] + '℃  ~  ' + Hightempture[0][
                                    i] + '℃   ' + str(today[0][0]) + ' 风：' + str(today[0][1])
                                self.result.insert(tkinter.END, a)
                            else:
                                a = "".join(weather[i]) + '    ' + Lowtempture[0][i] + '℃  ~  ' + Hightempture[0][
                                    i] + '℃   ' + "".join(weather[7][i - 1])
                                self.result.insert(tkinter.END, a)
                else:  # 如美国
                    if len(temp_weather) <= 0 or len(Lowtempture) <= 0 or len(Hightempture) <= 0 or len(
                            Lowtempture[0]) != 7 or len(Hightempture[0]) != 7:
                        a = '系统出错，数据不完整:'
                        self.result.insert(tkinter.END, a)
                        self.result.insert(tkinter.END, url2)
                        print(url2)
                    else:
                        for i in range(0, 7):
                            a = "".join(weather[i]) + '    ' + Lowtempture[0][i] + '℃  ~  ' + Hightempture[0][
                                i] + '℃   ' + "".join(weather[7][i])
                        self.result.insert(tkinter.END, a)
            else:  # 国内天气查询
                print("国内")
                url2 = 'http://www.weather.com.cn/weathern/' + self.citys[choose][0] + '.shtml'
                responseweather = requests.get(url2, headers=self.headers)
                html2 = responseweather.content.decode('utf-8')
                weather = re.findall('<li class="date-.*?".*?".*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
                weather.append(re.findall(
                    '<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">(.*?)</p>',
                    html2, re.S))
                Hightempture = re.findall(
                    '<script>var eventDay =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2,
                    re.S)
                Lowtempture = re.findall(
                    'var eventNight =\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
                b = '查询城市为：' + str(self.citys[choose][3]) + '    ' + str(self.citys[choose][1])
                self.result.insert(tkinter.END, b)
                if len(weather) <= 0 or len(Lowtempture) <= 0 or len(Hightempture) <= 0 or len(
                        Lowtempture[0]) != 8 or len(Hightempture[0]) != 8:
                    a = '系统出错，数据不完整:'
                    self.result.insert(tkinter.END, a)
                    self.result.insert(tkinter.END, url2)
                    print(url2)
                else:
                    for i in range(0, 8):
                        a = "".join(weather[i]) + '    ' + Lowtempture[0][i] + '℃  ~  ' + Hightempture[0][
                            i] + '℃   ' + "".join(weather[8][i])
                        self.result.insert(tkinter.END, a)
            if (len(self.citys[choose][0]) == 12):  # 查询搜索相关结果的下一个城市天气预报
                print("其他")
                url2 = 'http://forecast.weather.com.cn/town/weathern/' + self.citys[choose][0] + '.shtml'
                responseweather = requests.get(url2, headers=self.headers)
                html2 = responseweather.content.decode('utf-8')
                weather = re.findall('<li class="date-.*?".*?"da.*?">(.*?)</.*?"date-i.*?">(.*?)<.*?', html2, re.S)
                html2 = re.sub('lt;', '<', html2)
                weather.append(re.findall(
                    '<p class="weather-in.*?" title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?<p class="wind-i.*?">\\r\\n(.*?)\\r\\n',
                    html2, re.S))
                Hightempture = re.findall(
                    'var eventDay = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2, re.S)
                Lowtempture = re.findall(
                    'var eventNight = \["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\];', html2,
                    re.S)
                # print(Hightempture,Lowtempture)
                b = '查询城市为：' + str(self.citys[choose][3]) + '   ' + str(self.citys[choose][2]) + '    ' + str(
                    self.citys[choose][1])
                self.result.insert(tkinter.END, b)
                if len(weather) <= 0 or len(Lowtempture) <= 0 or len(Hightempture) <= 0 or len(
                        Lowtempture[0]) != 8 or len(Hightempture[0]) != 8:
                    a = '系统出错，数据不完整:'
                    self.result.insert(tkinter.END, a)
                    self.result.insert(tkinter.END, url2)
                    print(url2)
                else:
                    for i in range(0, 8):
                        a = "".join(weather[i]) + '    ' + Lowtempture[0][i] + '℃  ~  ' + Hightempture[0][
                            i] + '℃   ' + "".join(weather[8][i])
                    # print(a)
                    self.result.insert(tkinter.END, a)
    
    '''
         选择搜索城市相关的下一个城市名称，并进行天气查询
         '''
    
    def choose(self, event):
        print(11111)
        c = self.comboxlist.get()
        choose = -1
        for i in range(0, len(self.citys)):
            if c == self.citys[i][1]:
                choose = i
                break
        if choose != -1:
            self.query(choose)
    
    '''
         清除天气查询结果
         '''
    
    def clear(self):
        print("dddddd")
        self.result.delete(0, tkinter.END)


# self.city.delete(0, tkinter.END)
# tkinter.messagebox.showerror('showerror', 'hello')


if __name__ == '__main__':
    # 获取当前城市
    # default_city = get_local_city()
    default_city = '广州'
    myframe = MyFrame(default_city)
    myframe.root.mainloop()