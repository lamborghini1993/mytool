#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

lstIgnore = [".git", ".vscode", "__pycache__", "pubcode", "log"]

def IsIgnore(sDir):
    for sTmp in lstIgnore:
        if sDir.find(sTmp) != -1:
            return True
    return False

for sDir, lstDir, lstFile in os.walk(os.getcwd()):
    if IsIgnore(sDir):
        continue
    for sFile in lstFile:
        if not sFile.endswith(".ui"):
            continue
        sUIFile = os.path.join(sDir, sFile)
        sPYFile = sUIFile[:-3] + "_ui.py"
        os.system("pyuic5 -o %s %s" % (sPYFile, sUIFile))
        print("ui2py:" + sPYFile)
