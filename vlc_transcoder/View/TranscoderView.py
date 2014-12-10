#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderView.py
The View of the transcoder GUI
"""

# Import PyQt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import custom modules
from View.ConfigurationTab import *
from View.InputFilesTab import *

# Import standard modules


class TranscoderView(QtWidgets.QWidget):
    """
    This is the View part of the MVC implementation. It will describe the GUI
    of the application
    """
    def __init__(self):
        """
        The constructor of the View
        """
        super().__init__()

    def initUI(self):
        """
        This methods will call contained objects methods to generate the GUI
        """
        # Set GUI title
        self.setWindowTitle("VLC Transcoder")
        # Initialize tabs
        tabWidget = self.initTabs()
        # Create layout and add the tabs
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
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
        # Create the widget
        tabWidget = QtWidgets.QTabWidget()
        # Create the configuration tab
        conftab = ConfigurationTab(self)
        # Create the input files tab
        inputtab = InputFilesTab(self)

        tabWidget.addTab(conftab, "Output Configuration")
        tabWidget.addTab(inputtab, "Input files")

        return tabWidget
