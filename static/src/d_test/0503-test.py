import requests
import os
import re


def play_music(song):
    URL1 = 'https://api.bzqll.com/music/tencent/search?key=579621905&s=' + song + '&limit=1&offset=0&type=song'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", }
    url = str(requests.get(URL1, headers=header).text)
    url = str(re.findall(r'\"url\":\".*?"', url)).replace("['\"url\":\"", '').replace("\"\']", '')  # 处理获得真实的URL
    t = requests.get(url, headers=header).content
    PICTURE_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'\music')
    file = os.path.join(PICTURE_dir, "music.wav")  # 这里最好绝对路径，Nao机器人的路径可不好弄
    with open(file, "wb+") as f:
        f.write(t)
        f.close()
    os.system(file)  # 开始尝试用系统的播放，但是没有声音，后面会给出解决方法


if __name__ == '__main__':
    # play_music("我好想你")
    a = 2433219332010101011
    print(1 / 11)
    print(type(a))
