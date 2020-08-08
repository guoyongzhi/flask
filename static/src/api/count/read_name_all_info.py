import os
import random


class read_name_all_info():
    def __init__(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            self.file_dir = file_dir
            self.files = files
    
    def run(self):
        name_list = self.get_count()
        a = random.randint(0, len(name_list) - 1)
        info = self.get_info(name_list[a])
        b = random.randint(0, len(info) - 1)
        a = info[b]
        bb = a.split('、')
        return bb[1]
    
    def get_count(self):
        name_list = []
        for name in self.files:
            if name[-3:] == 'txt':
                name_list.append(self.file_dir + '\\' + name)
        return name_list
    
    def get_info(self, name):
        with open(name, mode='r') as f:
            name = f.readlines()
        return name
    
"""
    try:
        for i in name:
            if i == '\n':
                name.remove('\n')
    except Exception as e:
        print(e)  # new_name = ''
    for n in name:  #     new_name += n
    f.write(new_name)  # f.close()
    with open(self.file_dir + '\\' + name, mode='') as m:
        m.write(new_name)
        m.close()
        """
if __name__ == '__main__':
    a = read_name_all_info(r'I:\work\flask\static\src\api\count').run()
    print(a)
