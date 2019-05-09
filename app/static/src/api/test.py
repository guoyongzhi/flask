from aip import AipSpeech

APP_ID = '16007067'
API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_hecheng():
    result = client.synthesis('你好百度', 'zh', 1, {
        'vol': 5, 'per': 4
    })
    return result


result = get_hecheng()
if not isinstance(result, dict):
    with open(u'xx.war', 'wb') as f:
        f.write(result)
        f.close()


# print(result, type(result))

def get_fenli(filename):
    with open(filename, 'rb') as fp:
        yuyin = fp.read()
        fp.close()
    result = client.asr(yuyin, 'pcm', 16000, {
        'lan': 'zh',
        'dev_pid': 1536,
    })
    return result


# print(get_fenli('xx.war'))
# ii = 5642
# for i in range(0, int(ii % 2048)):
#     print(1)



jia = 4
yi = 5
c = 18
bin = 45
bi = 0
for i in range(0, 60):
    # print(i)
    if c == 0.0:
        print(i, c, bi)
    else:
        r = int(c) / 50
        c = c - (r * jia + r * yi)
        bi += int(r * 45)
        print(r, c, bi)
