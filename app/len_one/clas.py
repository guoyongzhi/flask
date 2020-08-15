class IDMed(object):
    def __init__(self):
        self.ID = 0

    def set_values(self, date_dice):
        if type(date_dice) is dict:
            for k in date_dice:
                for name, value in list(vars(self).items()):
                    if k == name:
                        exec('self.{} = date_dice[k]'.format(name))


class PageMed(IDMed):
    def __init__(self):
        super().__init__()
        self.pageIndex = 0
        self.pageSize = 10
        self.key = ''
    
    def set_values(self, date_dice):
        if type(date_dice) is dict:
            for k in date_dice:
                for name, value in list(vars(self).items()):
                    if k == name:
                        exec('self.{} = date_dice[k]'.format(name))


class dd(PageMed):
    def __init__(self):
        super().__init__()
        self.username = 0
        self.Pass = ''
    
    def __str__(self):
        return 'username=%s,Pass=%s' % (self.username, self.Pass)
    
    def set_values(self, date_dice):
        if type(date_dice) is dict:
            for k in date_dice:
                for name, value in list(vars(self).items()):
                    if k == name:
                        exec('self.{} = date_dice[k]'.format(name))

    def list_all_member(self):
        print(list(vars(self).items()))
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


class cc(IDMed):
    def __init__(self):
        super().__init__()
        self.name = ''

    def set_values(self, date_dice):
        if type(date_dice) is dict:
            for k in date_dice:
                for name, value in list(vars(self).items()):
                    if k == name:
                        exec('self.{} = date_dice[k]'.format(name))

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))


if __name__ == '__main__':
    d = dd()
    d.set_values({'username': '001', 'Pass': '001', 'ID': 1})
    d.list_all_member()
    print(d)
    
    c = cc()
    c.set_values({'name': "北京", 'ID': 10})
    c.list_all_member()
