#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderGui.py
The Graphical User InterfaCe of the transcoder
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from View.ConfigurationTab import *

class View(QtWidgets.QWidget):
    """
    This is the View part of the MVC implementation. It will describe the GUI
    of the application
    """
    def __init__(self,  app=None):
        """
        The constructor of the View

        @param app QtWidgets.QApplication: the root QApplication
        """
        super(View, self).__init__()
        self.app = app
        self.tabs = self.initUI()

    def initUI(self):
        """
        This methods will call of child methods to generate the GUI
        """
        self.setWindowTitle("VLC Transcoder")
        tabWidget = self.initTabs()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setLayout(mainLayout)
        self.show()

    def initTabs(self):
        """
        Initiate the tabs of the GUI
        """
        tabWidget = QtWidgets.QTabWidget()
        conftab = ConfigurationTab(self)
        filefindertab = QtWidgets.QWidget()

        tabWidget.addTab(conftab, "Configuration")
        tabWidget.addTab(filefindertab, "Input files")

        return tabWidget


