import os
import random


class read_name_all_info(object):
    def __init__(self, file_dir):
        file_name_dict = dict()
        for root, dirs, files in os.walk(file_dir):
            file_name_dict[root] = file_dir, files
        self.file_name_dict = file_name_dict
    
    def run(self):
        res = ""
        name_list = self.get_count()
        if name_list:
            am = random.randint(0, len(name_list) - 1)
            info = self.get_file_content(name_list[am])
            b = random.randint(0, len(info) - 1)
            aa = info[b]
            bb = aa.split('、')
            res = bb[1]
        return res
    
    def get_count(self):
        name_list = []
        if self.file_name_dict:
            name = self.file_name_dict.keys()
            for n in name:
                file_dir, files = self.file_name_dict[n]
                if files:
                    for i in files:
                        if i[-3:] == 'txt':
                            name_list.append(os.path.join(n, i))
        return name_list
    
    @classmethod
    def get_file_content(cls, name):
        try:
            with open(name, mode='r', encoding='GBK') as f:
                content = f.readlines()
        except UnicodeDecodeError:
            with open(name, mode='r', encoding='utf-8') as f:
                content = f.readlines()
        return content
    
    
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
