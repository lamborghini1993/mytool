# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 15:54:32
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 15:54:32
@Desc:  一些公共定义函数
"""

import os
import codecs
import time
import traceback


if "g_Manager" not in globals():
    g_Manager = {}


def set_manager(sFlag, obj):
    global g_Manager
    g_Manager[sFlag] = obj

def get_manager(sFlag):
    global g_Manager
    obj = g_Manager.get(sFlag, None)
    return obj

def call_manager_func(sFlag, sFunc, *args):
    obj = get_manager(sFlag)
    func = getattr(obj, sFunc)
    if not func:
        return None
    result = func(*args)
    return result


def getpwd():
    pwd = os.getcwd()
    return pwd


def write_to_file(filename, msg):
    pathname = os.path.join(getpwd(), filename)
    pathname += ".log"
    dirname = os.path.dirname(pathname)
    makedirs(dirname)
    msg = "[{}]{}\n".format(time_to_str(), msg)
    with codecs.open(pathname, "a", "utf-8") as myfile:
        myfile.write(msg)


def filter_crlf(msg):
    msg = msg.replace("\r", "")
    msg = msg.replace("\n", "")
    return msg


def makedirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def dowland_pic(dirpath, name, picdata):
    makedirs(dirpath)
    filename = os.path.join(dirpath, name)
    filename = os.path.join(getpwd(), filename)
    with open(filename, "wb") as fpic:
        fpic.write(picdata)


def get_run_time(func):
    def wrapped_func(*args):
        begintime = time.time()
        result = func(*args)
        endtime = time.time()
        print("%s() %s" % (func.__name__, endtime - begintime))
        return result
    return wrapped_func


def get_sencond():
    curtime = int(time.time())
    return curtime


def time_to_str(ti=-1, timeformat="%Y-%m-%d %H:%M:%S"):
    if ti < 0:
        ltime = time.localtime()
    else:
        ltime = time.localtime(ti)
    strtime = time.strftime(timeformat, ltime)
    return strtime


def get_trace_text(*args):
    """用于获得回溯栈信息文本"""
    txtlist = []
    txtlist.append("-----------------------------------------------------")
    stacklist = traceback.extract_stack()
    for filename, lineno, name, line in stacklist[:-2]:
        txt = " File '%s', line %s, CallFunctor '%s', in '%s'" % (
            filename, lineno, line, name)
        txtlist.append(txt)
    if args:
        txt = "其他信息："
        for tmp in args:
            txt = "%s%s," % (txt, tmp)
        txt = txt[:-1]
        txtlist.append(txt)
    return txtlist


def trace_msg(*args):
    """回溯栈信息（调用情况）,用于调用不明的bug分析"""
    txtlist = get_trace_text(*args)
    for txt in txtlist:
        print(txt)



