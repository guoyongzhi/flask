import os
from aip import AipSpeech


APP_ID = '16007067'
API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class mubot(object):
    def __init__(self):
        self.path = r"all.txt"

    def get_zhang(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            aaa = f.readlines()
            f.close()
        i = 1
        for m, aa in zip(range(1, len(aaa)),aaa):
            fielname = aa.split()[0]
            if fielname=='------------':
                i += 1
                print(i)
            else:
                content = ''.join(fielname + '\n')
                if os.path.exists('最佳赘婿' + '\\第' + str(i) + "章") ==False:
                    os.mkdir('最佳赘婿' + '\\第' + str(i) + "章")
                # if os.path.exists('最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i)+ "章.txt") ==False:
                #     os.mkdir('最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i) + "章.txt")
                src = '最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i)+ "章.txt"
                with open(src, 'a', encoding='utf-8') as fb:
                    fb.write(content)
                    fb.close()


    def get_len(self):
        i = 98
        # for i in range(1, 732):
        filename = '最佳赘婿' + '\\第' + str(i) + "章" + "\\第" + str(i)+ "章.txt"
        ii = 0
        with open(filename, 'r', encoding='utf-8') as fb:
            line = fb.readlines()
            fb.close()
        txt = ''.join(line)
        ii += len(txt)
        print(ii)
        if ii % 2048 == 0:
            print('整除的：', txt)
        elif ii < 2048:
            print('小的：', txt)
        else:
            print('除外的：', txt)


    def get_hecheng(self):
        result  = client.synthesis('你好百度', 'zh', 1, {
            'vol': 9,'per':4
            })
        return result


    def delbialline(self):
        infp = open(self.path, 'r', encoding='utf-8')
        outfp = open('all.txt', 'w', encoding='utf-8')
        lines = infp.readlines()
        for li in lines:
            if li.split():
                outfp.writelines(li)
        infp.close()
        outfp.close()






mubot().get_len()