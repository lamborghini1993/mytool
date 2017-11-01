# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-01 15:54:32
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-01 15:54:32
@Desc:  一些公共定义函数
"""

import traceback
import time
import os
import random
import binascii
import platform
import marshal
import socket
import chardet


if "g_Manager" not in globals():
    g_Manager = {}


def SetManager(sFlag, oManager):
    g_Manager[sFlag] = oManager


def GetManager(sFlag):
    if sFlag not in g_Manager:
        return None
    return g_Manager[sFlag]


def NewSetManager(sFlag, cls, *args):
    obj = GetManager(sFlag)
    if obj:
        return
    obj = cls(*args)
    g_Manager[sFlag] = obj


# 直接执行全局对象的函数，主要应用场合：
# 想一句代码写完调用，不想写GetManager时
# 做为异步回调时，能解决引用问题
def CallManagerFunc(sFlag, sFunc, *args):
    obj = GetManager(sFlag)
    func = getattr(obj, sFunc, None)
    if not func:
        return None
    return func(*args)


# ======================中间调用函数=====================
# 用于获得回溯栈信息文本
def GetTraceText(*args):
    sTxtList = []
    sTxtList.append("-----------------------------------------------------")
    lStack = traceback.extract_stack()
    for sFileName, iLineNo, sName, sLine in lStack[:-2]:
        sTxt = " File '%s', line %s, CallFunctor '%s', in '%s'" % (
            sFileName, iLineNo, sLine, sName)
        sTxtList.append(sTxt)
    if args:
        sTxt = "其他信息："
        for s in args:
            sTxt = "%s%s," % (sTxt, s)
        sTxt = sTxt[:-1]
        sTxtList.append(sTxt)
    return sTxtList
# ======================中间调用函数=====================


# =====================使用的函数=======================
def GetRunTime(func):
    def WrappedFunc(*args):
        iBeginTime = time.time()
        xx = func(*args)
        iEndTIme = time.time()
        print("%s() %s" % (func.__name__, iEndTIme - iBeginTime))
        return xx
    return WrappedFunc


# 获取当前时间(秒)
def GetSecond():
    iTime = time.time()
    return iTime


# 格式化输出
def TimeStr(ti=0, sFormat="%Y-%m-%d %H:%M:%S"):
    if ti:
        t = time.localtime(ti)
    else:
        t = time.localtime()
    return time.strftime(sFormat, t)


def GetCurtime():
    FORMAT = "%Y-%m-%d %X"
    sTime = time.strftime(FORMAT, time.localtime())
    return sTime


def LogFile(sFileName, sMsg):
    sPath = os.getcwd()
    sPath += "/log"
    try:
        os.mkdir(sPath)
    except:
        pass
    lstDir = sFileName.split("/")
    iLen = len(lstDir)
    for x in range(0, iLen - 1):
        sPath += "/%s" % lstDir[x]
        try:
            os.mkdir(sPath)
        except:
            pass
    sPath += "/%s.txt" % lstDir[-1]
    sTxt = "[%s]%s\n" % (GetCurtime(), sMsg)
    try:
        fp = open(sPath, "a")
        fp.writelines(sTxt)
    finally:
        fp.close()


# 回溯栈信息（调用情况）,用于调用不明的bug分析
def TraceMsg(*args):
    sTxtList = GetTraceText(*args)
    for sTxt in sTxtList:
        print(sTxt)


def Warn(*tMsg):
    stackList = traceback.extract_stack(limit=2)
    sInfo = stackList[0]
    sMsg = " ".join(tMsg)
    sOut = "WARNING:%s  (%s)\n%s (line %s)" % (
        sMsg, sInfo[2], sInfo[0], sInfo[1])
    print(sOut)


def Text2Hex(sUText):
    return binascii.b2a_hex(sUText)


def Hex2Text(sHex):
    return binascii.a2b_hex(sHex)


def DataMarshalHex(xData):
    """1.marshel数据  2.转hex16进制"""
    sData = marshal.dumps(xData)
    sHex = Text2Hex(sData)
    return sHex


def HexMarshalData(sHex):
    """1.将hex16进制转字符串 2.字符串marshal还原为初始数据"""
    sData = Hex2Text(sHex)
    xData = marshal.loads(sData)
    return xData


def IsWindows():
    sPlatform = platform.system()
    if sPlatform == "Windows":
        return True
    return False


def IsLinux():
    sPlatform = platform.system()
    if sPlatform == "Linux":
        return True
    return False


def ConvertByteToInt(byteStr):
    num = 0
    i = 0
    for char in byteStr:
        iByte = ord(char)
        num += iByte << i * 8
        i += 1
    return num


def ConvertIntToByte(num, iLen=4):
    result = ""
    for i in xrange(iLen):
        iByte = (num >> (8 * i)) & 0xff
        result += chr(iByte)
    return result


# 浅复制字典，替代性能低下的copy.copy
def CopyDict(srcdict):
    dNewDict = {}
    dNewDict.update(srcdict)
    return dNewDict


def GetPlatform():
    return platform.system()


def IsLinux():
    if GetPlatform() == "Linux":
        return True
    return False


def IsWindows():
    if GetPlatform() == "Windows":
        return True
    return False


def LstInt2Str(lstInt):
    sResult = ""
    iFirst = True
    for iNum in lstInt:
        if iFirst:
            sResult = "%d" % iNum
            iFirst = False
            continue
        sResult += ",%d" % iNum
    return sResult


def Str2LstInt(sStr):
    lstStr = sStr.split(",")
    lstInt = []
    for sNum in lstStr:
        if sNum:
            lstInt.append(int(sNum))
    return lstInt


def IsString(sStr):
    """判断是否为一般字符串"""
    if isinstance(sStr, str):
        return True
    return False


def IsUnicode(sStr):
    """判断是否为unicode"""
    if isinstance(sStr, unicode):
        return True
    return False


def TransCoding(sStr, sCoding):
    """将str转为coding编码"""
    sOldCoding = chardet.detect(sStr).get("encoding")  # 获取字符串的编码
    try:
        sResult = sStr.decode(sOldCoding).encode(sCoding)
        return sResult
    except:
        pass
    try:
        sResult = sStr.decode()
        return sResult
    except:
        pass
    return sStr


class CSysErr(object):
    '''将错误信息输出到文件'''

    def __init__(self):
        super(CSysErr, self).__init__()
        self.m_Console = sys.stdout

    def write(self, sMsg):
        if sMsg != "\n":
            LogFile("syserr", sMsg)
        # self.m_Console.write(sMsg)


class CSysOut(object):
    def __init__(self):
        super(CSysOut, self).__init__()
        self.m_Console = sys.stdout

    def write(self, sMsg):
        if sMsg != "\n":
            LogFile("sysout", sMsg)
        # self.m_Console.write(sMsg)
# =====================使用的函数=======================
