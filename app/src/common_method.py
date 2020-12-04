

# 公共获取参数

class Parameter(dict):
    def __init__(self, parameter_dict=None, source=None, temp=None):
        if parameter_dict:
            super(Parameter, self).__init__(parameter_dict)
        self.source = source
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
    
    @classmethod
    def common_check_required(cls, date_dict, *args):
        result = False
        if not args:
            return None
        result_list = []
        for i in args:
            if date_dict[i] is not None and date_dict[i] != '':
                result_list.append(i)
        if len(result_list) == len(args):
            result = True
        return result


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
    
    cm = Parameter(a)

