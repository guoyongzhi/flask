import urllib.request
import requests
import json
from bs4 import BeautifulSoup
# from selenium import webdriver
#
# diver = webdriver.Firefox()
# dr = diver.get("https://book.qidian.com/info/1004608738#Catalog")
# html = dr.page_source
# print(html)
#
# dr.close()
te = requests.get("https://book.qidian.com/info/1004608738#Catalog")
date = te.text
soup = BeautifulSoup(date, 'lxml')
print(soup.prettify())
print(soup.t)
# print(soup)
# for div in soup.find(attrs={'class': "cf"}):
#     print(div)
    # print(div)
    # if div.get('class'):
        # print(div)
        # print(div.get('class'))
#         if div.get('class')[0] == 'book-detail-wrap':
#             print(div)
            # print(div.find_all(name='div', attrs={'class': 'catalog-content-wrap'}))
            # for ul in div.find_all(name='div'):
            #     print(ul)
#     aa = div.get("href")



class GetQiDian(object):
    def __init__(self):
        pass

    def get_url(self, url):
        te = urllib.request.urlopen(url)
        return te.read()

    def get_html(self, date):
        soup = BeautifulSoup(date, 'lxml')
        for div in soup.find_all('div'):
            if div.get("class")[0] == "all-book-list":
                for li in div.find_all('h4'):
                    for a in li.find_all('a'):
                        aa = a.get("href")
                        print("结果utl是：https%s \n 标题是：%s" % (aa, a.text))

    def run(self, url):
        date = self.get_url(url)
        self.get_html(date)

# if __name__ == "__main__":
#     url = 'https://www.qidian.com/all'
#     GetQiDian().run(url)
