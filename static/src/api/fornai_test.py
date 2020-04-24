import time
import _thread


class json_post(object):
    def __init__(self):
        self.a = 0
        self.b = 0
    
    def __set__(self, instance, value):
        self.a[instance] = value
    
    def __get__(self, instance, owner):
        return self.a.get(instance, 0)


class json_get(json_post):
    def __init__(self):
        super().__init__()
        self.aa = 0
        self.cc = 0
        self.dd = []


# j = json_get()
# j.a = 1
# j.b = [1]
# j.cc = 100
# j.dd = [30]
# print(j.a)
# print(j.__dict__)
# p = json_post()
# p.b = [10]
# print(p.a)
# print(p.__dict__)

class mai(object):
    def __init__(self):
        self.obj = json_post()
    
    def run(self):
        try:
            _thread.start_new_thread(self.set_value, ('Thread-set',))
            # _thread.start_new_thread(self.get_value, ('Thread-get',))
            self.get_value('get')
        except Exception as e:
            print(e)
    
    def set_value(self, name):
        self.obj.b = 1
        print("存值开始了")
        while True:
            self.obj.a += 1
            time.sleep(3)
            print(name + str(self.obj.a))
            if self.obj.a == 100:
                self.obj.b = 0
                self.obj.a = 0
                print("存值退出了")
                break
    
    def get_value(self, name):
        print("拿值开始了")
        while True:
            if self.obj.a < 100:
                print(name + str(self.obj.__dict__))
                time.sleep(5)
            else:
                print("拿值退出了")
                break


if __name__ == '__main__':
    new = mai()
    new.run()
