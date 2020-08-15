import json
import requests
import re
import os
import time
from lxml import etree
from aip import AipSpeech
from selenium import webdriver

url = 'http://finance.sina.com.cn/stock/usstock/sector.shtml'
jsurl = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['fa8Vo3U4TzVRdsLs']/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id="

html = requests.get(jsurl)
xml = html.text
aa = xml.split("/*<script>location.href='//sina.com';</script>*/")[1]
bb = aa.split("IO.XSRV2.CallbackList['fa8Vo3U4TzVRdsLs']")[1]
cc = bb[1:]
dd = cc[:-2]
# print(dd)
json_data = json.loads(dd)
date = json_data['data']
for d in date:
    print(d, type(d))
# dr = webdriver.Firefox()
# dr.get(url)
# time.sleep(3)
# xml = etree.HTML(html.text)
with open('1.html', mode='a', encoding='utf-8') as f:
    f.write(html.text)
    f.close()
# print(xml.xpath('/html/body/div[6]/div[2]'))
# dr.quit()
