# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-28 14:19:56
@Desc: 自定义同步信号，类似QT中的pyqtSignal
"""

import weakref

from .pubfunc import pubmisc


class CMySignal:
    def __init__(self):
        self.m_FuncList = []

    def connect(self, func):
        if pubmisc.IsBoundMethod(func):
            _obj = weakref.ref(func.__self__)
            _fn = func.__func__
        else:
            _obj = None
            _fn = func
        self.m_FuncList.append((_obj, _fn))

    def emit(self, *args):
        for (_obj, _fn) in self.m_FuncList:
            if not _obj:
                _fn(*args)
                continue
            obj = _obj()
            if not obj:
                print("实例对象已经被销毁:%s %s" % (_obj, _fn))
                continue
            _fn(obj, *args)
