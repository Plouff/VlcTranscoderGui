#! python3
#-*-coding: utf-8 -*-

"""
@file MainView.py
The View of the transcoder GUI
"""

# Import PyQt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import custom modules
from Tabs.ConfigurationTab import ConfigurationTab
from Tabs.InputFilesTab import InputFilesTab

# Import standard modules


class MainView(QtWidgets.QWidget):
    """
    This is the View part of the MVC implementation. It will describe the GUI
    of the application
    """
    def __init__(self):
        """
        The constructor of the View
        """
        super().__init__()

        # Initialize tabs
        self.tabWidget = self.initTabs()

    def initUI(self):
        """
        This methods will call contained objects methods to generate the GUI
        """
        # Set GUI title
        self.setWindowTitle("VLC Transcoder")
        # Create layout and add the tabs
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        # Set an Icon
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # Show widget
        self.setLayout(mainLayout)
        self.show()

    def initTabs(self):
        """
        Initiate the tabs of the GUI

        @return A @c QTabWidget containing the defined tabs
        """
        # Create the configuration tab
        self.confTab = ConfigurationTab(self)
        # Create the input files tab
        self.inputTab = InputFilesTab(self)

        self.tabWidget.addTab(self.confTab, "&Output Configuration")
        self.tabWidget.addTab(self.inputTab, "&Input files")

        return self.tabWidget
