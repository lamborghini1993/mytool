# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 15:08:25
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 15:08:25
@Desc:  构造任意参数的（类）函数
"""


import weakref
from .pubfunc import pubmisc


class Functor(object):
    def __init__(self, func, *args):
        if pubmisc.IsBoundMethod(func):
            self._obj = weakref.ref(func.__self__)
            self._objdesc = str(func.__self__)
            self._func = func.__func__
        else:
            self._obj = None
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
