# coding=utf8


"""
lesson 1 from this exerise is that mix in must be from right to left
that is MyClass(object, Mixin1, Mixin2) is wrong
and MyClass(Mixin2, Mixin1, object) is right
"""


class Mixin1(object):
    def test(self):
        print "Mixin1"


class Mixin2(object):
    def test(self):
        print "Mixin2"


class MyClass(Mixin2, Mixin1, object):
    pass

if __name__ == '__main__':
    obj = MyClass()
    obj.test()
