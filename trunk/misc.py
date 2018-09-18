# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-03-21 13:51:13
@Desc: 各种通用函数
"""

import json
import os
import time
import traceback
import codecs
import sys

def JsonDump(data, path, **myArgs):
    dJsonArgs = {
        "ensure_ascii"  : False,
        "allow_nan"     : False,
        "indent"        : 4,
    }
    dJsonArgs.update(myArgs)
    coding = dJsonArgs.pop("encoding", "utf-8")
    with open(path, "w", encoding=coding) as fp:
        json.dump(data, fp, **dJsonArgs)


def JsonLoad(path, default=None, **myArgs):
    if not os.path.exists(path):
        return default
    coding = myArgs.pop("encoding", "utf-8")
    with open(path, "r", encoding=coding) as fp:
        default = json.load(fp, **myArgs)
    return default


def Time2Str(ti=-1, timeformat="%Y-%m-%d %H:%M:%S"):
    if ti < 0:
        ltime = time.localtime()
    else:
        ltime = time.localtime(ti)
    strtime = time.strftime(timeformat, ltime)
    return strtime


def TraceMsg(*args):
    """回溯栈信息（调用情况）,用于调用不明的bug分析"""
    txtlist = GetTraceText(*args)
    for txt in txtlist:
        print(txt)
        
        
def GetTraceText(*args):
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

def PythonError(msg=""):
    sErrTrace = traceback.format_exc()
    tb = sys.exc_info()[-1]
    while tb.tb_next is not None:
        tb = tb.tb_next
    sInfo = tb.tb_frame.f_locals
    sLog = "----TraceErr----\n%s\n----TraceInfo----\n%s\n----extra----\n%s\n" % (sErrTrace, sInfo, msg)
    return sLog


def Write2File(filename, msg, sType="a+"):
    filename += ".log"
    msg = "[{}]{}\n".format(Time2Str(), msg)
    with codecs.open(filename, sType, "utf-8") as myfile:
        myfile.write(msg)


def GetSecond():
    curtime = int(time.time())
    return curtime
