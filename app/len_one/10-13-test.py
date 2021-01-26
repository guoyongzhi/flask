import requests
import time
import json

from bs4 import BeautifulSoup

# 打开页面
# date = {"-": "getUCGI869693537142286", "g_tk": 1621225741, "sign": "zzag25mhbrjmoh1bb3c6a43dd2473ef3cf669470847f43e",
#         "loginUin": 1983496818, "hostUin": 0, "format": "json", "inCharset": "utf8", "outCharset": "utf-8", "notice": 0,
#         "platform": "yqq.json", "needNewCode": 0,
#         "data": {"detail": {"module": "musicToplist.ToplistInfoServer", "method": "GetDetail",
#                             "param": {"topId": 4, "offset": 0, "num": 20, "period": "2021-01-15"}
#                             },
#                         "comm": {"ct": 24, "cv": 0}
#                  }
#         }
# 热歌排行榜
# res = requests.get(
#     'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI40891151230639133&g_tk=1621225741&sign=zzamsciyh7z387bb3c6a43dd2473ef3cf669470847f43e&loginUin=1983496818&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A4%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222021-01-15%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D')
# json_str = json.loads(res.text)
# data = json_str['detail']['data']['songInfoList']
#
# # print(data)
# for d in data:
#     song_name = d['title']
#     singer = d['singer'][0]['name']
#     print(song_name + '-' + singer)
from axf.dbmysql import my_si_db

headers = {
    'cookie': 'cna=k6VYGE+5mx8CAQ6SXJJm9vJr; miid=989991361842943446; tracknick=%5Cu56DE%5Cu5FC6%5Cu7684%5Cu5B63%5Cu8282%5Cu90A3%5Cu4E48%5Cu75DB; enc=iIh%2BTJzZ%2FrjeJdGbyvfl85wzmKfr%2ByrSjDotIvAa%2Bx5ehuOxVSJiLfGnTchvxWq5PLDJyeMB9CjzKiOSSqK43g%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=E100W4%2Fj4AgowWuc9IBmp%2F9NHHvlyiyk4e0py5cDV5d7rpKyrshqf7QoV5n579OghjchLkaAk3YDD1zcKN2IY5HJOQ%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; t=8924e502708f4881fbcbf1cc633cf4e6; cookie2=155e94c9e42a6dfa8f2f18f0d4c37525; _tb_token_=3ee8b4e50616e; xlly_s=1; _m_h5_tk=1a41856d1984f9a6deb4a521ba1ce47b_1610963935152; _m_h5_tk_enc=147d6a390e0ceec3ab3d11d3af2f6131; tfstk=cedNBgfvqfhat5Cje114fSu6zq5OZs8MoW75IKKnjBsjUNXGi7EARrSF8Z176Of..; l=eBLaWgaHODsWmfs8BOfahurza77OSBdYYuPzaNbMiOCPO8fp5LvRW6G7NuL9C3GAhsI9R3-ormWaBeYBqI2jPGKnNSVsr4Dmn; isg=BNvb7wuwP2eZHXzG1wlYr8ftZD9FsO-ycxSiH80Yt1rxrPuOVYB_AvkqRg4il0eq',
    'eagleeye - traceid': '2128009916109517731227608e2fed', 'mtop-x-provider': '84a0353847a1f6fa1632f770a86de7659511401ab39416e1b264f151f676f011',
    'pragma': 'no-cache', 's-rt': '290', 's_group': 'tao-session', 's_host': '5765485370756c5765584e6b356144374c4c317a557242646b523775653171354a424341785947646946633d',
    's_ip': '4547514b6531634d364c454638453351', 's_read_unit': '[CN:CENTER]', 's_status': 'STATUS_NOT_EXISTED',
    's_tag': '285873024598016|134217728^1|^^', 's_tid': '2128009916109517731227608e2fed',
    's_ucode': 'CN:CENTER',
    's_v': '4.0.1.4',
    'server': 'Tengine/Aserver',
    'status': '200', 'x-aserver-sret': 'SUCCESS', 'x-eagleeye-id': '2128009916109517731227608e2fed',
    'x-node': 'd5f64a100478ab7bdd193458d4e056f2',
    'x-powered-by': 'm.taobao.com'
    # ':path': '/h5/mtop.alimama.union.xt.en.api.entry/1.0/?jsv=2.5.1&appKey=12574478&t=1610936709171&sign=3ee6f19087546f87c62a6e366e659290&api=mtop.alimama.union.xt.en.api.entry&v=1.0&AntiCreep=true&timeout=20000&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22pNum%22%3A0%2C%22pSize%22%3A%2260%22%2C%22refpid%22%3A%22mm_26632258_3504122_32538762%22%2C%22variableMap%22%3A%22%7B%5C%22q%5C%22%3A%5C%22%E5%A5%B3%E8%A3%85%5C%22%2C%5C%22navigator%5C%22%3Afalse%2C%5C%22clk1%5C%22%3A%5C%2205ae6c9955d205d09a510e1b3f38d13f%5C%22%2C%5C%22recoveryId%5C%22%3A%5C%22201_11.92.48.11_4293403_1610936708234%5C%22%7D%22%2C%22qieId%22%3A%2236308%22%2C%22spm%22%3A%22a2e0b.20350158.31919782%22%2C%22app_pvid%22%3A%22201_11.92.48.11_4293403_1610936708234%22%2C%22ctm%22%3A%22spm-url%3A%3Bpage_url%3Ahttps%253A%252F%252Fuland.taobao.com%252Fsem%252Ftbsearch%253Frefpid%253Dmm_26632258_3504122_32538762%2526keyword%253D%2525E5%2525A5%2525B3%2525E8%2525A3%252585%2526clk1%253D05ae6c9955d205d09a510e1b3f38d13f%2526upsId%253D05ae6c9955d205d09a510e1b3f38d13f%22%7D'
}
url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/?jsv=2.5.1&appKey=12574478&t=1610957033279&sign=4b8777485fc1e5a89bf24810a31f42a8&api=mtop.alimama.union.xt.en.api.entry&v=1.0&AntiCreep=true&timeout=20000&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22pNum%22%3A0%2C%22pSize%22%3A%2260%22%2C%22refpid%22%3A%22mm_26632258_3504122_32538762%22%2C%22variableMap%22%3A%22%7B%5C%22q%5C%22%3A%5C%22%E6%83%85%E4%BE%A3%E5%8D%AB%E8%A1%A3%E6%96%B0%E6%AC%BE2020%E7%88%86%E6%AC%BE%5C%22%2C%5C%22navigator%5C%22%3Afalse%2C%5C%22clk1%5C%22%3A%5C%2205ae6c9955d205d09a510e1b3f38d13f%5C%22%2C%5C%22union_lens%5C%22%3A%5C%22recoveryid%3A201_11.87.178.209_4338767_1610941611920%3Bprepvid%3A201_11.92.48.11_4392644_1610956483883%5C%22%2C%5C%22recoveryId%5C%22%3A%5C%22201_11.27.22.26_4410980_1610957031206%5C%22%7D%22%2C%22qieId%22%3A%2236308%22%2C%22spm%22%3A%22a2e0b.20350158.31919782%22%2C%22app_pvid%22%3A%22201_11.27.22.26_4410980_1610957031206%22%2C%22ctm%22%3A%22spm-url%3Aa2e0b.20350158.search.1%3Bpage_url%3Ahttps%253A%252F%252Fuland.taobao.com%252Fsem%252Ftbsearch%253Frefpid%253Dmm_26632258_3504122_32538762%2526keyword%253D%2525E6%252583%252585%2525E4%2525BE%2525A3%2525E5%25258D%2525AB%2525E8%2525A1%2525A3%2525E6%252596%2525B0%2525E6%2525AC%2525BE2020%2525E7%252588%252586%2525E6%2525AC%2525BE%2526clk1%253D05ae6c9955d205d09a510e1b3f38d13f%2526upsId%253D05ae6c9955d205d09a510e1b3f38d13f%2526spm%253Da2e0b.20350158.search.1%2526pid%253Dmm_26632258_3504122_32538762%2526union_lens%253Drecoveryid%25253A201_11.87.178.209_4338767_1610941611920%25253Bprepvid%25253A201_11.92.48.11_4392644_1610956483883%22%7D'
res = requests.get(url=url, headers=headers)

print(res.text)
json_str = json.loads(res.text[12:-1])
date_list = json_str['data']['recommend']['resultList']
print(date_list)
for i in date_list:
    itemId = i['itemId']
    sql = 'select * from taobaotable where itemId="{}"'.format(itemId)
    res = my_si_db(sql, 'test')
    if res:
        if res[0]:
            if res[0][3] == i['itemId']:
                print("已存在")
            else:
                print("商品不匹配", i)
    else:
        sql = 'insert into taobaotable(floorId, itemName, itemId, shopTitle, pic, url, provcity, price, promotionPrice, monthSellCount) ' \
              'values ({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}",{9});'.format(i['floorId'], i['itemName'],
                                                                                   i['itemId'], i['shopTitle'],
                                                                                   i['pic'], i['url'],
                                                                                   i['provcity'], i['price'], i['promotionPrice'], i['monthSellCount'])
        res = my_si_db(sql, 'test')

