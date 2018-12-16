# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-16 21:36:56
@Desc: 各种杂乱的
"""

import os
import sys
import time
import json
import traceback
import codecs
import logging

if "g_GlobalMgr" not in globals():
    g_GlobalMgr = {}


# --------------------全局管理器相关-------------------------------------
def SetManager(sFlag, obj):
    global g_GlobalMgr
    g_GlobalMgr[sFlag] = obj


def GetManager(sFlag, default=None):
    return g_GlobalMgr.get(sFlag, default)


def CallManagerFunc(sFlag, sfunc, *args):
    obj = GetManager(sFlag)
    func = getattr(obj, sfunc, None)
    if not func:
        raise Exception("error CallManagerFunc %s %s" % (sFlag, sfunc))
    return func(*args)


# ------------------------时间相关---------------------------------
def GetSecond():
    curtime = int(time.time())
    return curtime


def Time2Str(ti=-1, timeformat="%Y-%m-%d %H:%M:%S"):
    if ti < 0:
        ltime = time.localtime()
    else:
        ltime = time.localtime(ti)
    strtime = time.strftime(timeformat, ltime)
    return strtime


def Str2Time(sTime, timeformat="%Y-%m-%d %H:%M:%S"):
    oTime = time.strptime(sTime, timeformat)
    iTime = int(time.mktime(oTime))
    return iTime


def GetRunTime(func):
    """获取func运行时间"""
    def WrappedFunc(*args):
        begintime = time.time()
        result = func(*args)
        endtime = time.time()
        print("%s() %s" % (func.__name__, endtime - begintime))
        return result
    return WrappedFunc


# ------------------------文件相关---------------------------------
def JsonDump(data, path, **myArgs):
    dJsonArgs = {
        "ensure_ascii": False,
        "allow_nan": False,
        "indent": 4,
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


def Write2File(filename, msg, sType="a+"):
    filename += ".log"
    msg = "[{}]{}\n".format(Time2Str(), msg)
    with codecs.open(filename, sType, "utf-8") as myfile:
        myfile.write(msg)


def DowlandPic(dirpath, name, picdata):
    MakeDirs(dirpath)
    filename = os.path.join(dirpath, name)
    with open(filename, "wb") as fpic:
        fpic.write(picdata)


def MakeDirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


# ------------------------栈相关---------------------------------
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


def SysExceptHook(type, value, tb):
    """
    对于unchecked 异常,其实也是提供钩子来帮助我们处理的
    我们可以在钩子里面记录崩溃栈追踪或者发送崩溃数据
    重定向 sys.excepthook = SysExceptHook
    """
    msg = "".join(traceback.format_tb(tb))
    value = str(value)
    while tb.tb_next is not None:
        tb = tb.tb_next
    info = tb.tb_frame.f_locals
    result = msg + value + "\n" + info
    print(result)


# ------------------------logging---------------------------------
def InitLogging(sFileName):
    """这里默认编码为gbk，暂时不知道如何修改"""
    logging.basicConfig(
        filename=sFileName + ".log",
        format="[%(asctime)s %(levelname)s %(message)s]",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    ch = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(ch)


def InitLogging2(sFileName):
    handler = logging.FileHandler(filename=sFileName, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s %(message)s]"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    logger.addHandler(ch)
