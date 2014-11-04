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
import pprint


class NzQDisablingWidget(QtCore.QObject):
    """
    This abstract class defines a checkbox widget that will disable slave widgets
    depending on the value of the master widget
    """
    __metaclass__ = ABCMeta

    def __init__(self, isInMutexGroup=False, **kwds):
        """
        The class constructor

        @param isInMutexGroup bool: To define if the button is part of a group of
        buttons that are mutually exclusive
        """
        super().__init__(**kwds)

        # Will contain the list of slave widgets
        self.slaveWidgets = []
        self.slaveStateWhenMasterIsEnabled = {}
        self.isInMutexGroup = isInMutexGroup

    def addSlaveWidget(self, slaveWidget, isEnabledWhenMasterIsEnabled=True):
        """
        Add a slave widget that state will depend on the value of the master
        widget

        @param slaveWidget QtWidgets.QWidget: A slave Qt widget to append to
        the list of slave widgets
        @param isEnabledWhenMasterIsEnabled bool: The state taken by the slave
        widget when its master is enabled
        """
        self.slaveWidgets.append(slaveWidget)
        self.slaveStateWhenMasterIsEnabled[slaveWidget] = \
            isEnabledWhenMasterIsEnabled

        # Set initial state of the widget
        if self.isChecked():
            slaveWidget.setEnabled(self.slaveStateWhenMasterIsEnabled[slaveWidget])
        else:
            slaveWidget.setEnabled(not self.slaveStateWhenMasterIsEnabled[slaveWidget])


    def updateSlaveStatus(self):
        """
        Method used to set the state of the slave widgets when the master
        widget is triggered

        @warning When using this class to create derived class, this slot
        method must be connected to the right master widget signal. For example
        `toggled` for a radio button or `stateChanged` for a check button.
        """
        for swdgt in self.slaveWidgets:
            if self.isChecked():
                swdgt.setEnabled(self.slaveStateWhenMasterIsEnabled[swdgt])
            else:
                if not self.isInMutexGroup:
                    swdgt.setEnabled(not self.slaveStateWhenMasterIsEnabled[swdgt])

        QtWidgets.QApplication.processEvents()
        self.updateSlaveDisablingWidgetsStatus()


    def updateSlaveDisablingWidgetsStatus(self):
        """
        In case of nested disabling widgets, we need to launch the
        updateSlaveStatus() method of children master widgets. This is the
        purpose of this method
        """
        for swdgt in self.slaveWidgets:
            if swdgt.isEnabled():
                try:
                    swdgt.updateSlaveStatus()
                except:
                    pass


class NzQDisablingRadioButton(QtWidgets.QRadioButton, NzQDisablingWidget):
    """
    This class defines a master radio button widget that will disable slave
    widgets depending on the value of the master
    """
    def __init__(self, **kwds):
        """
        Constructor of disabling Radio buttons

        @param text str: the text of the checkbox
        @param parent QtWidgets.QWidget: the parent widget
        @param isInMutexGroup bool: To define if the button is part of a group of
        buttons that are mutually exclusive
        """
        super().__init__(**kwds)
        # On click signal handling
        self.toggled.connect(self.updateSlaveStatus)

class NzQDisablingCheckBox(QtWidgets.QCheckBox, NzQDisablingWidget):
    """
    This class defines a master checkbox widget that will disable slave widgets
    depending on the value of the master
    """
    def __init__(self, **kwds):
        """
        Constructor of disabling Checkbox

        @param text str: the text of the checkbox
        @param parent QtWidgets.QWidget: the parent widget
        @param isInMutexGroup bool: To define if the button is part of a group of
        buttons that are mutually exclusive
        """
        super().__init__(**kwds)
        # On click signal handling
        self.stateChanged.connect(self.updateSlaveStatus)
