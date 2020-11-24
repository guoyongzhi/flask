import json
import requests


def find_music(talk):
    name = talk.split()
    if talk[2:] == '':
        return '亲点歌格式不对哦~ 点歌请艾特我回复点歌 【歌名】'
    if len(name) > 1:
        songname = name[1]
    elif len(name) == 1:
        name = talk.split('-')
        if len(name) > 1:
            songname = name[1]
        else:
            songname = talk[2:]
            if not songname:
                return '亲点歌格式不对哦~ 点歌请艾特我回复点歌 【歌名】'
    if '排行榜' == songname:
        return '亲暂未开通排行榜点歌哦~功能持续更新中，敬请期待 点歌请艾特我回复点歌 【歌名】'
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1' \
          '&remoteplace=txt.yqq.song&searchid=55989056282747366&t=0&aggr=1&cr=1&catZhida=1&' \
          'lossless=0&flag_qc=0&p=1&n=10&w=' + songname + '&g_tk_new_20200303=1945000638&' \
                                                          'g_tk=654347293&loginUin=1983496818&' \
                                                          'hostUin=0&format=json&inCharset=utf8&' \
                                                          'outCharset=utf-8&notice=0&' \
                                                          'platfin talk orm=yqq.json&needNewCode=0 '
    res = requests.get(url=url)
    jm = json.loads(res.text)
    try:
        psid = jm['data']['song']['list'][0]['id']
        songer = jm['data']['song']['list'][0]['singer'][0]['name']
        songname = jm['data']['song']['list'][0]['title']
    except Exception:
        return '点歌失败，找不到该歌曲'
    test = "https://i.y.qq.com/v8/playsong.html?songid={}&source=yqq#wechat_redirect".format(psid)
    return '非常好听的《' + songname + ' - ' + str(songer) + '》来咯~ 点击链接欣赏:\n' + test