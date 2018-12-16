# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-16 21:31:17
@Desc: 数据库相关函数
"""

import marshal
import binascii


def ValueMarshalHex(xValue):
    sData = marshal.dumps(xValue)
    sHex = binascii.b2a_hex(sData)
    sStr = sHex.decode()
    return sStr


def HexMarshalValue(sHex):
    sData = binascii.a2b_hex(sHex)
    value = marshal.loads(sData)
    return value


def GetDefaultData(sType):
    if sType in ("int", "real", "integer"):
        return 0
    if sType in ("text", "str"):
        return ""
    if sType in ("list",):
        return []
    if sType in ("dict",):
        return {}
    if sType in ("set",):
        return set()
    raise Exception("未定义的类型:%s" % sType)


def GetInsertValue(xValue, sType):
    """通过sType类型获取对应的插入数据库的xValue的值"""
    if sType in ("int", "real", "integer"):
        return str(xValue)
    if sType in ("text", "datetime"):
        return "'%s'" % xValue
    if sType in ("blob", "list", "dict", "set",):
        sStr = ValueMarshalHex(xValue)
        return "'%s'" % sStr
    raise Exception("未定义的类型:%s" % sType)


def GetResultData(sData, sType):
    """通过数据库的的值sData和对应的插入sType,获取真实值"""
    if sType in ("int", "real", "integer", "text", "datetime"):
        return sData
    if sType in ("blob", "list", "dict", "set",):
        return HexMarshalValue(sData)
    raise Exception("未定义的类型:%s" % sType)


def GetInsertSql(sTableName, tData, lstColInfo):
    """
    获取插入一条信息的sql语句
    lstColInfo = [
        ("Time", "datetime"),
        ("Type", "text"),
        ("Goods", "text"),
        ("buyer", "text"),
        ("Price", "real"),
        ("Num", "integer"),
        ("Remark", "text"),
    ]
    """
    assert len(tData) == len(lstColInfo)
    lstKey = []
    lstValue = []
    for iIndex in range(len(tData)):
        key, sType = lstColInfo[iIndex]
        xValue = tData[iIndex]
        value = GetInsertValue(xValue, sType)
        lstKey.append(key)
        lstValue.append(value)
    sKey = ",".join(lstKey)
    sValue = ",".join(lstValue)
    sql = "insert into %s(%s) values(%s)" % (sTableName, sKey, sValue)
    return sql
