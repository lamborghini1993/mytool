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


def getpwd():
    pwd = os.getcwd()
    return pwd


def write_to_file(filename, msg):
    pathname = os.path.join(getpwd(), filename)
    pathname += ".txt"
    dirname = os.path.dirname(pathname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with codecs.open(pathname, "a", "utf-8") as myfile:
        myfile.write(msg + "\t\n")
