#! python3
#-*-coding: utf-8 -*-

"""
@file MainView.py
The View of the transcoder GUI
"""

# Import PyQt modules
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

# Import custom modules
from Tabs.ConfigurationTab import ConfigurationTab
from Tabs.InputFilesTab import InputFilesTab
from Tabs.TranscodeTab import TranscodeTab

# Import standard modules


class MainView(QtWidgets.QWidget):
    """
    This is the View part of the MVC implementation. It will describe the GUI
    of the application
    """
    updateFiles = pyqtSignal(QtCore.QAbstractTableModel)
    launchTranscoding = pyqtSignal(QtCore.QObject)

    def __init__(self):
        """
        The constructor of the View
        """
        super().__init__()

        # Initial the main Window
        self.initUI()

    def initUI(self):
        """
        This methods will call contained objects methods to generate the GUI
        """
        # Set GUI title
        self.setWindowTitle("VLC Transcoder")
        # Init tabs
        self._tabWidget = self.initTabs()

        # Create layout and add the tabs
        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self._tabWidget)

        # Set an Icon
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # Set Layout
        self.setLayout(mainLayout)

    def initTabs(self):
        """
        Initiate the tabs of the GUI

        @return A @c QTabWidget containing the defined tabs
        """
        # Create a tab widget
        tabWidget = QtWidgets.QTabWidget(self)

        # Create the configuration tab
        self.confTab = ConfigurationTab(self)
        # Create the input files tab
        self.inputTab = InputFilesTab(self)
        # Create the transcode tab
        self.transcodeTab = TranscodeTab(self)

        tabWidget.addTab(self.confTab, "&Output Configuration")
        tabWidget.addTab(self.inputTab, "&Input files")
        tabWidget.addTab(self.transcodeTab, "&Transcoding")

        # Connect signals
        self.transcodeTab.launchTranscoding.connect(self.launchTranscoding)

        return tabWidget

    def getSelectedExtensions(self):
        """
        docstring for getSelectedExtensions
        """
        return self.inputTab.getSelectedExtensions()

    def getFilesFromInputTab(self, model):
        self.updateFiles.emit(model)

    def getConfig(self):
        return self.confTab.getConfig()