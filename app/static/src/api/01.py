import xlwt
import re,urllib.request
import selenium
# 1、获取页面源码
def getadte():
    html = urllib.request.urlopen('https://list.tmall.com/search_product.htm?q=%D0%AC%D7%D3&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton').read()
    print(html)
print(getadte())
#print(getadte())
# items = getadte()
# print(items)