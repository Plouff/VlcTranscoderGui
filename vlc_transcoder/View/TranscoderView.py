#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderView.py
The View of the transcoder GUI
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from View.ConfigurationTab import *
from View.InputFilesTab import *

class View(QtWidgets.QWidget):
    """
    This is the View part of the MVC implementation. It will describe the GUI
    of the application
    """
    def __init__(self,  app):
        """
        The constructor of the View

        @param app QtWidgets.QApplication: the root QApplication
        """
        super().__init__()
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
        inputtab = InputFilesTab(self)

        tabWidget.addTab(conftab, "Configuration")
        tabWidget.addTab(inputtab, "Input files")

        return tabWidget


    def getController(self):
        return self.controller
