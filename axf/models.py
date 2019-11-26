#!/usr/bin/Python-3.6.2
import requests

url = 'https://www.baidu.com'
re = requests.get(url)

print(re.text)
print(re.status_code)