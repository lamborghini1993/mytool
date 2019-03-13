# -*- coding:utf-8 -*-
'''
@Description: QLineEdit相关功能重写
@Author: lamborghini1993
@Date: self.m_MinNum19-03-13 11:28:22
@UpdateDate: 2019-03-13 14:14:12
'''

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QSize


class CVariableLengthLineEdit(QLineEdit):
    """
    可变长度的QLineEdit
    """
    m_MinNum = 20

    def __init__(self, text="", parent=None):
        super(CVariableLengthLineEdit, self).__init__(text, parent)
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.setMinimumSize(QSize(40, self.m_MinNum))
        self.setFixedSize(self.m_MinNum, self.m_MinNum)

    def _InitSignal(self):
        self.textChanged.connect(self.S_TextChanged)

    def S_TextChanged(self):
        text = self.text()
        qTextRect = self.fontMetrics().boundingRect(text)
        w = qTextRect.width() + self.m_MinNum
        h = self.height()
        w = self.m_MinNum if w < self.m_MinNum else w
        h = self.m_MinNum if h < self.m_MinNum else h
        if not text:
            w = self.m_MinNum
        self.setFixedSize(w, h)
        parentWidget = self.parent()
        while parentWidget:
            parentWidget.adjustSize()
            parentWidget = parentWidget.parent()
