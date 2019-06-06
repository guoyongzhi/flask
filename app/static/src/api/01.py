import requests
import json
import urllib
from lxml import etree


def getSogouImag(category, length, path):
    n = length
    cate = category
    imgs = requests.get(
            'http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category=' + cate + '&tag=%E5%85%A8%E9%83%A8&start=0&len=' + str(
                    n))
    jd = json.loads(imgs.text)
    jd = jd['all_items']
    imgs_url = []
    for j in jd:
        imgs_url.append(j['bthumbUrl'])
    m = 0
    for img_url in imgs_url:
        print('***** ' + str(m) + '.jpg *****' + '   Downloading...')
        urllib.request.urlretrieve(img_url, path + str(m) + '.jpg')
        m = m + 1
    print('Download complete!')


# getSogouImag('壁纸', 2000, 'G:/download/壁纸/')

class GetSouGouImge(object):
    def __init__(self):
        pass

    def open_sougou(self):
        url = "https://pic.sogou.com/pics?query=%C3%C0%C5%AE&w=05009900&p=&_asf=pic.sogou.com&_ast=1540275417&sc=index&sut=2318&sst0=1540275417414"
        dd = "https://pic.sogou.com/pics/recommend?category=%C3%F7%D0%C7&from=home#%E5%85%A8%E9%83%A8"
        res = requests.post(dd)
        print(res.text)
        xml = etree.HTML(res.content)
        img = xml.xpath('//div[@class="pic-box"]/a/img/@href')
        print(img)

GetSouGouImge().open_sougou()