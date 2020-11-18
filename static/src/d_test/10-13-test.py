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


# print(bb(1, 2).x)
# print(len('@ '.replace(' ', '')))

a = '@🍉 🍉 🍉'
if ' ' in a:
    res = a.split()
    print(res)
who = '桂C 自尊白-大石'
talk = '桂C 自尊白-大石 他这是交警拍的哦'
test_who = who.split(' ')
for i in test_who:
    if i in talk:
        talk = talk.replace(str(i) + ' ', '')
print(622, who, test_who, talk)
