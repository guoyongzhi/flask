import re

pattern = re.compile('[\u4e00-\u9fa5A-Za-z0-9]')
str = r'《46' '4 ''&%*('""'阿大是。，<>》'

print(pattern.search(str))

a = re.findall('[\u4e00-\u9fa5A-Za-z0-9_。，？《》！@#￥%…&*（）—+{}：“” ]', str)
ch = ''.join(a)
print(ch)
