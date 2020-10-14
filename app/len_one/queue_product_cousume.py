from queue import Queue
import threading
import time
# 生产消费模型
q = Queue(maxsize=10)


def product(name):
    count = 1
    while True:
        q.put('步枪编号{}'.format(count))
        print('{}生产步枪第{}支'.format(name, count))
        count += 1
        time.sleep(2)


def consumer(name):
    while True:
        print('{}装备了{}'.format(name, q.get()))
        time.sleep(2)
        
        q.task_done()


threading_list = []
# 部队线程
p = threading.Thread(target=product, args=('张三',))
k = threading.Thread(target=consumer, args=('李四',))
w = threading.Thread(target=consumer, args=('王五',))
s = threading.Thread(target=consumer, args=('王六',))

threading_list.append(p)
threading_list.append(k)
threading_list.append(w)
threading_list.append(s)

p.start()
k.start()
w.start()
s.start()


a = 1
while True:
    for i in threading_list:
        print(i, i.is_alive())
    time.sleep(5)
    if a == 2:
        print(s.ident)
    a += 1

# while True:
#     print("开始了")
#     time.sleep(5)

