import requests
import json
headers = {"Cookie": "UM_distinctid=172b59426052c6-0ae0ede1b1ab8c-34564a7c-1fa400-172b594260624f;CNZZDATA1000214860"
                     "=157799959-1592178930-null%7C1592178930; "
                     "gr_user_id=2dd58613-bba9-44cc-9505-b778900b4b6f;JSESSIONID=0198F61914835FC183DD233109693DAF"
                     ";gr_session_id_22222-22222-22222-22222=16a60451-d9e5-4b29-a9ca-19b15b7777f6;CNZZDATA1274031688"
                     "=771303685-1604714880-null%7C1604714880;gr_session_id_22222-22222-22222-22222_16a60451-d9e5"
                     "-4b29-a9ca-19b15b7777f6=true;login-token=BfVxWx-DeYRLEsCOVF8U1UJaq3LOgWlOuBOj9y01mPpyN42z5d"
                     "-gdzxzl4ve6Uj1_JXmqDUuGSXRy7lO14_-uSJcYSLFfqW3x49yr6auSTqW4W0UjNC"
                     "-LcYK_u46UjYt777Vnao9TJ1TV0v4hdI7qf4SECBnBlFG8lWPEnM52znVLd8OEgFTBNaZPdxvqjufpmLZ-JoEfknIIG"
                     "-EUoVJRliIzeCuw8VI0UiO_YbhC0tXG1lJfwyAS_fextXuHk"
                     "-twmueDAONjxgEWWy0rppCuXpDpy6duiPeHzVRK4ivO5fjYoBrsTmZmrEKJZnpSwZDNhJpcuXsNk"
                     "-YTzVOmDQ7xdBC2vOcrXkc1GZzQ-Hdm7U1tMbZtkTtBB7ax0Inlmu31KFoxmHuPB_StoT2OWwY_m_ZOI-i; "
                     "Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1604717321;Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c"
                     "=1604718789",
           "Content-Type": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, "
                         "like Gecko)Chrome/70.0.3538.25 Safari/537.36Core/1.70.3741.400 QQBrowser/10.5.3863.400"}
url = "http://www.tuling123.com/robot-chat/robot/chat/708871/WrA7?geetest_challenge=&geetest_validate=&geetest_seccode="
while True:
    talk = input("请输入内容：")
    data = {"perception": {"inputText": {"text": str(talk)}}, "userInfo": {"userId": "demo"}}
    res = requests.post(url, json.dumps(data), headers=headers)
    result = json.loads(res.text)
    if result['type'] == 'success':
        print(result['data']['results'][0]['values']['text'])
    else:
        print(result)
    if talk == '退出':
        break
