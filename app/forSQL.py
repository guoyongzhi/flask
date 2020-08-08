
sql = 'INSERT INTO log_discernrecord(UserName,UserNum,DeptName,DiscernAddr,EntryType,DiscernTime,Mobile,' \
      'SystemName,Remark,ValidSalt,IsSuccess,AddTime,LastUpdateTime)VALUE("001", "0001", "一年级", "通道二", 1, NOW()' \
      ', "17721531888", "人民大学", "22222", CEILING(RAND() * 90000 + 10000), 1, NOW(),NOW());\n'
a = ''
m = 0
for i in range(1, 50000000 + 1):
    a += sql
    print('当前处理执行{0}个，总数{1}'.format(i, 50000000))
    if i % 50000 == 0:
        m += 1
        print('开始写txt第' + str(i) + '的50000个')
        with open('识别记录-{}.txt'.format(m), mode='a+') as f:
            f.write(a)
            f.close()
        a = ''
