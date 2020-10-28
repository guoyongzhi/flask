a = dict(a=1, b=2)
if a:
    print(11)
b = dict()
print('-------')
if b:
    print(222)

import json

a = '龙.🍦🍦🍦.一哥'
ac = json.dumps(a)
print(ac, type(ac))
ac = r'"\u69d1\u4fd0\ud83d\udc63\ud83e\udd29"'
# print(ac, type(ac))
ab = json.loads(ac, encoding='utf-8')
print(ab, type(ab))
