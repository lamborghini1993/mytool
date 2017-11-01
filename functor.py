# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 15:08:25
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 15:08:25
@Desc:  构造任意参数的（类）函数
"""


import weakref
import types


def isboundmethod(func):
    if not isinstance(func, types.MethodType):
        return False
    if not func.__self__:
        return False
    return True


class Functor(object):
    def __init__(self, func, *args):
        if isboundmethod(func):
            self._obj = weakref.ref(func.__self__)
            self._objdesc = str(func.__self__)
            self._func = func.__func__
        else:
            self._obj = func
            self._func = func
        self._args = args

    def __call__(self, *args):
        if not self._obj:
            return self._func(*(self._args + args))
        obj = self._obj()
        if not obj:
            raise Warning("实例对象已经被释放,引用:%s,绑定方法:%s" %
                          (self._objdesc, self._func))
        return self._func(obj, *(self._args + args))


class CTest(object):
    def test(self):
        print("Test...")


def test():
    obj = CTest()
    func = Functor(obj.test)
    del obj
    func()


test()
