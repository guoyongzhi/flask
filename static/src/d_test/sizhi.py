import requests
import json

url = 'https://api.ownthink.com/bot'
headers = {"Content-Type": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, "
                         "like Gecko)Chrome/70.0.3538.25 Safari/537.36Core/1.70.3741.400 QQBrowser/10.5.3863.400"}

while True:
    talk = input("请输入内容：")
    data = {"appid": "1ac9c3cf079bbf0c5f795625bd159fbe", "Secret": "b49389fda4894414b122bbf024f6259e", "spoken": talk,
            "userid": 1}
    res = requests.post(url, data, headers=headers)
    result = json.loads(res.text)
    if result['message'] == 'success':
        print(result['data']['info']['text'])
    else:
        print(result)
    if talk == '退出':
        break
