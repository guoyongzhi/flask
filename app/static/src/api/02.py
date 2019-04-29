import re

f = open(r"D:\BaiduNetdiskDownload\tset.txt",encoding='UTF-8')
fd = f.read()
# print(fd)

#print(f.read())
pat = '[0-9].*?笔'
pat1 = '¥.*?[0-9]'
myDate = re.compile(pat).findall(fd)
myDate2 = re.compile(pat1).findall(fd)

number = re.compile('([0-9]+.[0-9])')

all1 = number.findall(fd, string="[u4e00-\u9fa5]")
print("多少笔:%s" % all1)
print("多少字节:%s" % myDate)
print("多少:%s" % myDate2)
f.close()

p2 = re.compile('[^\u4e00-\u9fa5]')
zh = " ".join(p2.split(fd)).strip()
zh = ",".join(zh.split())
print(zh, myDate2, myDate)

f.close()