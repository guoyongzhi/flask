# a = 3782854
# # b = 204500
# print(a - b)
# print(a + b)

import os
import subprocess
import time



def main():   # 调用exe，但是不会输出内容到控制台
    os.chdir(r'G:\work\iControl\Entrance Management_V2\UnitTestWeiGengSDK\bin\Debug')
    path_01 = r"UnitTestWeiGengSDK.exe"
    r_v = os.popen(path_01).read()
    print("11111", r_v)
    # return r_v

def mainn():  # 调用exe，可以输出全部内容到控制台
    os.chdir(r'E:\work_test\iControl\Entrance Management_V2\WGDemoWin\bin\Debug')
    path_01 = r"WGDemoWin.exe"
    s = subprocess.Popen(path_01,bufsize=0, stdout=subprocess.PIPE,universal_newlines=True)
    while True:
        nextline=s.stdout.readline()
        print(nextline.strip())
        if nextline=="":
            break


# print(222, main())
# content = os.popen('ping www.baidu.com').read()
# print(type(content))

# import threading
# import time
# # a = input("请输入是否开始线程：")
#
# b = input("请输入要运行的次数：")
# def fun1():
#     while True:
#         time.sleep(5)
#         fun2()
#
# def fun2(b, c):
#     while int(b)>0:
#         try:
#             c = input("请输入0打断程序运行：")
#         except TimeoutError as e:
#             c = 1
#         if c == '0':
#             break
#         for i in range(0, int(b)):
#             print(i)
# threads = []
# threads.append(threading.Thread(target=fun1()))
# threads.append(threading.Thread(target=fun2()))
#
# if __name__ == '__main__':
#     for t in threads:
#         t.start()


a = (1,5,3,9,7)
b = (0,2,6,4,8)
for aa, bb in zip(a, b):
    print(aa, "---华丽的分割线---", bb)
print('-------------------------')
for aa, bb in zip(range(1,20), range(40, 20,-2)):
    print(aa, "---华丽的分割线---", bb)

def add(a=1, b=1, c=1):
    print(a+b)
    print(c)

add()