#! python3
#-*-coding: utf-8 -*-

"""
@file ZQDisablingCheckBox.py
Contains a checkbox that has the ability to disable slave widgets
"""

# Import PyQt modules
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import standard modules
# abc: abstract class
from abc import ABCMeta


class NzQDisablingWidget(QtCore.QObject):
    """
    This abstract class defines a checkbox widget that will disable slave
    widgets depending on the value of the master widget
    """
    __metaclass__ = ABCMeta

    def __init__(self, isInMutexGroup=False, **kwds):
        """
        The class constructor

        @param[in] _isInMutexGroup bool: To define if the button is part of a
        group of buttons that are mutually exclusive
        @param[in] kwds** Other parameters are sent to base class constructor
        """
        super().__init__(**kwds)

        # Will contain the list of slave widgets
        self._slaveWidgets = []
        self._slaveStateWhenMasterIsEnabled = {}
        self._isInMutexGroup = isInMutexGroup

    def addSlaveWidget(self, slaveWidget, isEnabledWhenMasterIsEnabled=True):
        """
        Add a slave widget that state will depend on the value of the master
        widget

        @param slaveWidget QtWidgets.QWidget: A slave Qt widget to append to
        the list of slave widgets
        @param isEnabledWhenMasterIsEnabled bool: The state taken by the slave
        widget when its master is enabled
        """
        self._slaveWidgets.append(slaveWidget)
        self._slaveStateWhenMasterIsEnabled[slaveWidget] = \
            isEnabledWhenMasterIsEnabled

        # Set initial state of the widget
        if self.isChecked():
            slaveWidget.setEnabled(
                self._slaveStateWhenMasterIsEnabled[slaveWidget])
        else:
            slaveWidget.setEnabled(
                not self._slaveStateWhenMasterIsEnabled[slaveWidget])


    def updateSlaveStatus(self):
        """
        Method used to set the state of the slave widgets when the master
        widget is triggered

        @warning When using this class to create derived class, this slot
        method must be connected to the right master widget signal. For example
        `toggled` for a radio button or `stateChanged` for a check button.
        """
        for swdgt in self._slaveWidgets:
            if self.isChecked():
                swdgt.setEnabled(self._slaveStateWhenMasterIsEnabled[swdgt])
            else:
                if not self._isInMutexGroup:
                    swdgt.setEnabled(
                        not self._slaveStateWhenMasterIsEnabled[swdgt])

        QtWidgets.QApplication.processEvents()
        self.updateSlaveDisablingWidgetsStatus()


    def updateSlaveDisablingWidgetsStatus(self):
        """
        In case of nested disabling widgets, we need to launch the
        updateSlaveStatus() method of children master widgets. This is the
        purpose of this method
        """
        for swdgt in self._slaveWidgets:
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

        @param text str: the text of the radio button
        @param parent QtWidgets.QWidget: the parent widget
        @param _isInMutexGroup bool: To define if the button is part of a group of
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
        @param _isInMutexGroup bool: To define if the button is part of a group of
        buttons that are mutually exclusive
        """
        super().__init__(**kwds)
        # On click signal handling
        self.stateChanged.connect(self.updateSlaveStatus)
