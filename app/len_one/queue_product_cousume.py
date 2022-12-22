from queue import Queue
import threading
import time
import numpy as np
# 生产消费模型
q = Queue(maxsize=10)


def product(name):
    count = 1
    while count < 5:
        q.put('步枪编号{}'.format(name + str(count)))
        print('{}生产步枪第{}支'.format(name, count))
        count += 1
        time.sleep(10)


def consumer(name):
    # np.random.seed(0)
    while True:
        if q.empty():
            time.sleep(3)
            continue
        stop_name = q.get(block=True, timeout=1)
        p = np.array([0.7, 0.3])
        index = np.random.choice([0, 1], p=p.ravel())
        if index == 0:
            print("装配失败", stop_name)
            q.put(stop_name)
            continue
        else:
            time.sleep(2)
            print('{}装备了{}'.format(name, stop_name))
            q.task_done()


threading_list = []
# 部队线程
p = threading.Thread(target=product, args=('张三',))
# k = threading.Thread(target=product, args=('李四',))
# w = threading.Thread(target=product, args=('王五',))
s = threading.Thread(target=consumer, args=('王六',))

threading_list.append(p)
# threading_list.append(k)
# threading_list.append(w)
threading_list.append(s)

p.start()
# k.start()
# w.start()
s.start()


# a = 1
# while True:
#     for i in threading_list:
#         print(i, i.is_alive())
#     time.sleep(5)
#     if a == 2:
#         print(s.ident)
#     a += 1
#
# # while True:
#     print("开始了")
#     time.sleep(5)

