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


def write_to_file(filename, sMsg):
    filepath = os.path.join(getpwd(), filename)
    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with codecs.open(filepath, "a", "utf-8") as myfile:
        myfile.write(sMsg + "\n")
