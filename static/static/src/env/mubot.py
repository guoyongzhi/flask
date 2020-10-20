import os
import time
from aip import AipSpeech

APP_ID = '16007067'
API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class mubot(object):
    def __init__(self):
        self.path = r"alll.txt"

    def get_zhang(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            aaa = f.readlines()
            f.close()
        i = 0
        for m, aa in zip(range(1, len(aaa)), aaa):
            Bigtit = "最佳赘婿"
            fielname = aa.split()[0]
            if fielname == '------------':
                i += 1
                if (i - 1) <= 901:
                    pass
                else:
                    self.get_len(Bigtit, "第" + str(i - 2) + "章")
            if i > 901:
                if fielname == "第" + str(i - 1) + "章":
                    content = ''.join(fielname + ' ' + aa.split()[1] + '\n')
                else:
                    content = ''.join(fielname + '\n')
                # if os.path.exists('最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i)+ "章.txt") ==False:
                #     os.mkdir('最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i) + "章.txt")
                src = '最佳赘婿' + '\\文本\\第' + str(i - 1) + "章.txt"
                with open(src, 'a', encoding='utf-8') as fb:
                    fb.write(content)
                    fb.close()
                # print(src, "小说保存完成")

    def get_len(self, Bigtit, litit):
        filename = Bigtit + '\\文本\\' + litit + '.txt'
        with open(filename, 'r', encoding='utf-8') as fb:
            aaa = fb.readlines()
            fb.close()
        content = "".join(aaa)
        print("正在合成小说：", filename)
        changdu = len(content)
        # print(content, changdu)
        res = bytes()
        if changdu % 2048 == 0:
            for i in range(0, int(changdu / 2048)):
                a = self.Get_WenBen(filename, i)
                try:
                    res += self.wenben_get_yuyin(a)
                except:
                    print("错误返回dict" + filename, i)
        elif changdu < 2048:
            a = self.Get_WenBen(filename, 0)
            try:
                res += self.wenben_get_yuyin(a)
            except:
                print("错误返回dict" + filename)
        else:
            for i in range(1, int(changdu / 2048) + 1):
                a = self.Get_WenBen(filename, i)
                try:
                    res += self.wenben_get_yuyin(a)
                except Exception as e:
                    print("错误返回dict" + filename, i, e)
                    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(res, dict):
            mp3name = Bigtit + '\\语言\\' + litit + '.mp3'
            with open(mp3name, 'wb') as f:
                f.write(res)
            print(mp3name, "合成完成")

    def wenben_get_yuyin(self, wenben):
        APP_ID = '16007067'
        API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
        SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        result = client.synthesis(wenben, 'zh', 1, {
            'vol': 8,  # 音量
            'per': 0,  # 音色
            'pit': 7,  # 语调
            'spd': 6  # 语速
        })
        # print(result)
        return result

    def Get_WenBen(self, filename, lenth):
        f = open(filename, 'r', encoding='utf-8')
        changdu = 0
        ab = ''
        am = f.readlines()
        for a in am:
            changdu += len(a)
            if 2048 * (lenth - 1) <= changdu < 2048 * lenth:
                a = a.rstrip()
                a = a.lstrip()
                ab += a
        f.close()
        return ab

    def delbialline(self):
        infp = open(self.path, 'r', encoding='utf-8')
        outfp = open('alll.txt', 'w', encoding='utf-8')
        lines = infp.readlines()
        for a, li in range(len(lines)), lines:
            if li.split():
                outfp.writelines(li)
        infp.close()
        outfp.close()


# mubot().get_zhang()
# mubot().delbialline()
mubot().get_len(r"I:\work\flask\static\static\src\env", "政治")
