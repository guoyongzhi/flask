class a(object):
    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b
        

class bb(a):
    def __init__(self, a=1, b=2):
        super(bb, self).__init__(a, b)
    
    @property
    def x(self):
        print(111)
        return 124


print(bb(1, 2).x)
