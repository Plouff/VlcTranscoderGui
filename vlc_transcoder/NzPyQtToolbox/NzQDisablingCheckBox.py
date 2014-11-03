#! python3
#-*-coding: utf-8 -*-

"""
@file ZQDisablingCheckBox.py
Contains a checkbox that has the ability to disable slave widgets
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Abstract class
from abc import ABCMeta, abstractmethod

class NzQDisablingCheckBoxOLD(QtWidgets.QCheckBox):
    """
    This class defines a checkbox widget that will disable slave widgets
    depending on the value of the master widget
    """
    def __init__(self, text=None, parent=None):
        """
        The class constructor with text

        @param text str: the text of the checkbox
        @param parent QtWidgets.QWidget: the master widget
        """
        # Call to super constructor
        if text == None:
            super().__init__(parent)
        else:
            super().__init__(text, parent)

        # Will contain the list of slave widgets
        self.slaveWidgets = []
        self.slaveStateWhenMasterIsEnabled = {}

        # Click event handling
        self.stateChanged.connect(self.updateSlaveStatus)


    def addSlaveWidget(self, slaveWidget, isEnabledWhenMasterIsEnabled=True):
        self.slaveWidgets.append(slaveWidget)
        self.slaveStateWhenMasterIsEnabled[slaveWidget] = \
            isEnabledWhenMasterIsEnabled
        # Set initial state of the widget
        if self.isChecked():
            slaveWidget.setEnabled(self.slaveStateWhenMasterIsEnabled[slaveWidget])
        else:
            slaveWidget.setEnabled(not self.slaveStateWhenMasterIsEnabled[slaveWidget])

    def updateSlaveStatus(self):
        for swdgt in self.slaveWidgets:
            if self.isChecked():
                swdgt.setEnabled(self.slaveStateWhenMasterIsEnabled[swdgt])
            else:
                swdgt.setEnabled(not
                                       self.slaveStateWhenMasterIsEnabled[swdgt])

        if self.isChecked():
            self.updateSlaveDisablingWidgetsStatus()

    def updateSlaveDisablingWidgetsStatus(self):
        for swdgt in self.slaveWidgets:
            if isinstance(swdgt, NzQDisablingCheckBox):
                swdgt.updateSlaveStatus()


class NzQDisablingWidget():
    """
    This abstract class defines a checkbox widget that will disable slave widgets
    depending on the value of the master widget
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        """
        The class constructor with text
        """
        # Will contain the list of slave widgets
        self.slaveWidgets = []
        self.slaveStateWhenMasterIsEnabled = {}

    def addSlaveWidget(self, slaveWidget, isEnabledWhenMasterIsEnabled=True):
        self.slaveWidgets.append(slaveWidget)
        self.slaveStateWhenMasterIsEnabled[slaveWidget] = \
            isEnabledWhenMasterIsEnabled

        # Set initial state of the widget
        if self.isChecked():
            slaveWidget.setEnabled(self.slaveStateWhenMasterIsEnabled[slaveWidget])
        else:
            slaveWidget.setEnabled(not self.slaveStateWhenMasterIsEnabled[slaveWidget])


    def updateSlaveStatus(self):
        for swdgt in self.slaveWidgets:
            if self.isChecked():
                swdgt.setEnabled(self.slaveStateWhenMasterIsEnabled[swdgt])
            else:
                if not self.isInMutexGroup:
                    swdgt.setEnabled(not self.slaveStateWhenMasterIsEnabled[swdgt])

        QtWidgets.QApplication.processEvents()
        self.updateSlaveDisablingWidgetsStatus()


    def updateSlaveDisablingWidgetsStatus(self):
        for swdgt in self.slaveWidgets:
            if swdgt.isEnabled():
                try:
                    swdgt.updateSlaveStatus()
                except:
                    pass


class NzQDisablingCheckBox(QtWidgets.QCheckBox, NzQDisablingWidget):
    """
    This class defines a master checkbox widget that will disable slave widgets
    depending on the value of the master

    @param text str: the text of the checkbox
    @param parent QtWidgets.QWidget: the master widget
    """
    def __init__(self, text=None, parent=None, isInMutexGroup=False):
        super(QtWidgets.QCheckBox, self).__init__()
        super(NzQDisablingWidget, self).__init__()
        if text:
            self.setText(text)
        if parent:
            self.setParent(parent)
        self.isInMutexGroup = isInMutexGroup

        # Click signal handling
        self.stateChanged.connect(self.updateSlaveStatus)


class NzQDisablingRadioButton(QtWidgets.QRadioButton, NzQDisablingWidget):
    """
    This class defines a master radio button widget that will disable slave
    widgets depending on the value of the master

    @param text str: the text of the radio button
    @param parent QtWidgets.QWidget: the master widget
    """
    def __init__(self, text=None, parent=None, isInMutexGroup=False):
        super(QtWidgets.QRadioButton, self).__init__()
        super(NzQDisablingWidget, self).__init__()
        if text:
            self.setText(text)
        if parent:
            self.setParent(parent)
        self.isInMutexGroup = isInMutexGroup

        # Click signal handling
        self.toggled.connect(self.updateSlaveStatus)

