# from static.src.api.fs_test import *
import enum

# get_inp().get_CPU()


class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)
    
    def __add__(self, other):
        return Vector(self.a + other.a, self.b + other.b)


def get_new():
    v1 = Vector(2, 10)
    v2 = Vector(5, -2)
    print(v1 + v2)
    # print(a, type(a), b, type(b))
    # print(a, b)
    return None


a = 10


def test(a):
    a = a + 1
    print(a)


test(a)

get_new()