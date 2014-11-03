#! python3
#-*-coding: utf-8 -*-

"""
@file CommonWidgetsActions.py
Package for common actions on widgets
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class ZQDisableGroup():
    """
    This class enables to have a master widget that will disable slave widgets
    depending on the value of the master widget
    """
    def __init__(self, QtWidgets.QWidget masterWidget):
        """
        The class constructor

        @param masterWidget QtWidgets.QWidget: the master widget which value
        will determine the state of the slave widgets
        """
        self.masterWidget = masterWidget
        self.slaveWidgets = []

    def addSlaveWidget(self, QtWidgets.QWidget slaveWidget):
        self.slaveWidgets.append(slaveWidget)
