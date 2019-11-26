import os


class fileIsTure(object):
    def __init__(self, a, b):
        self.url = r'D:\\tmp\\newTai\\'
        self.star = a
        self.stop = b

    def run(self):
        a, v = self.IsExists()
        self.SaveTxt(a, v)
        print(a)

    def IsExists(self):
        a = []
        v = 0
        for i in range(self.star, self.stop + 1):
            # print(self.url + str(i) + '.jpg')
            if os.path.exists(self.url + 'people' + str(i) + '.jpg'):
                pass
            else:
                v += 1
                a.append(i)
        print(v)
        return a, v

    def SaveTxt(self, msg, v):
        with open('abc.txt', 'a') as f:
            f.write(str(self.star) + '-------' + str(self.stop) + str('文件不存在区间内总数是：') + str(v) + str(msg) + '\n')
            f.close()


if __name__ == '__main__':
    f = fileIsTure(1, 10000)
    f.run()
# 1123-7645    21111-31107 （9983项）   130001-186066（）
# for i in range(0, 1):
#     print(i)
