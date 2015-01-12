#! python3
# -*-coding: utf-8 -*-

"""
@file EEasterEgg.py
An easter egg class to trigger some action given a password
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QEvent
import logging


class EasterEggSignal(QtCore.QObject):
    """
    Signals for the EasterEgg class
    """
    found = pyqtSignal()


class EasterEgg(QtCore.QObject):
    """
    A Class to create easter eggs based on keyboard input
    """

    found = pyqtSignal()

    def __init__(self, app, password, slot):
        """
        Class constructor

        @param app: The QApplication
        @param password: The password to trigger the easter egg
        @param slot: The slot to connect
        """
        super().__init__()

        # Setup the event filter so that the EasterEgg class will get all
        # events before the app
        app.installEventFilter(self)

        # Connect the slot to be executed
        self._signal = EasterEggSignal()
        self._signal.found.connect(slot)
        # Only to __repr__ it
        self._slot = slot

        # Save the password that will trigger the easter egg
        self._password = password
        self._index = 0

    def __repr__(self):
        msg = ("{}@{}(password={!r}, slot={}, _index={})".format(
            self.__class__.__name__, hex(id(self)), self._password,
            str(self._slot), self._index))
        return msg

    def eventFilter(self, obj, event):
        """
        Process the filtering of events

        @param obj: The object that trigger the event
        @param event: The event sent by the object
        """
        # All widget will send the event so we filter on the type of the widget
        if event.type() == QEvent.KeyPress and isinstance(obj, QtGui.QWindow):

            # Get key text
            keypressed = event.text()
            logging.debug("got key: {}".format(keypressed))
            logging.debug("obj: {}".format(obj.__class__.__name__))

            # Increment index when the match the next character in password
            if self._password[self._index] == keypressed:
                logging.debug("match at idx {} with '{}'".format(
                    self._index, self._password))
                self._index = self._index + 1

                # If the index is the length of the password then this is a
                # full match
                if self._index == len(self._password):
                    self._signal.found.emit()
                    self._index = 0
                    logging.debug("Full match detect easter egg launched")

            # If the first letter is sent when index is not 0 then
            # index must be one
            # For ex, if pass is ABC and we receive ABA we must not reset the
            # index but set it to 1 on the 2nd A
            elif self._password[0] == keypressed:
                self._index = 1

            # Check case for double letters in pass
            # For ex if we get AAA when the pass is AAB, then on the 3rd
            # 'A' index must be 2 not 0
#             else:
#                 right = self._index
#                 while self._index > 0:
#                     if self._password[:self._index - 1] == \
#                         self._password[right - self._index + 1: self._index - 1]:
#                         break
#                     self._index = self._index - 1
        return False
