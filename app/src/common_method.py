

# 公共获取参数

class CommonMethod(object):
    def __init__(self, temp):
        self.temp = temp
        
    def select_page_common(self, index, page, key, *args, **kwargs):
        date_dict = dict()
        date_dict[index] = self.temp.get(index)
        date_dict[page] = self.temp.get(page)
        date_dict[key] = self.temp.get(key)
        for i in args:
            date_dict[i] = self.temp.get(i)
        return date_dict
    
    def common_all(self, *args, **kwargs):
        date_dict = dict()
        for i in args:
            if type(self.temp.get(i)) is int:
                date_dict[i] = self.temp.get(i)
            else:
                date_dict[i] = self.temp.get(i) if self.temp.get(i) else ''
        return date_dict


if __name__ == '__main__':
    a = [1, 2, 3, 4]
    b = [*a, 5, 6]
    
    
    def ab(*args):
        date_dict = dict()
        date_list = []
        if type(args) is tuple:
            for i in args:
                if type(i) is list:
                    date_list.append(i)
                else:
                    if type(i) is int:
                        date_dict[i] = i
                    else:
                        date_dict[i] = i if i else ''
        if date_dict:
            return date_dict
        return date_list
    
    
    print(ab(a))
    print(ab(b))
    print(ab('1223', 'dd', None))
    
    cm = CommonMethod(a)
