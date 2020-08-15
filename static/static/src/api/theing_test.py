from threading import Thread
import multiprocessing
import time
import _thread

ast = 0


def func1(i):
    global ast
    while ast < 20:
        time.sleep(1)
        ast += 1
        print("线程休眠时长", ast)


# t1 = Thread(target=func1)
t1 = _thread.start_new_thread(func1, (1, ))
# print('t1:', t1)
# t1.start()
a = 0
while a < 50:
    print('t1:', _thread.get_ident())
    time.sleep(2)
    a += 2
    print("主进程程休眠时长", a)
