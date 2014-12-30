#! python3
#-*-coding: utf-8 -*-

"""
@file InputFilesTab.py
The Input files Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

# Import custom modules
from TranscodeMgr.Widget import TranscoderMgrWidget


class TranscodeTab(QtWidgets.QWidget):
    '''
    This tab will launch transcoding and track the status
    '''
    launchTranscoding = pyqtSignal(QtCore.QAbstractTableModel)

    def __init__(self, parent):
        '''
        The constructor for the Transcoding tab of the GUI

        @param parent The parent widget
        '''
        super().__init__(parent)
        self.parent = parent

        # Create the transcoding status widget
        self.transcWidget = TranscoderMgrWidget(self)

        self.updateBut = QtWidgets.QPushButton("Update list")
        self.updateBut.setMaximumWidth(100)
        self.launchBut = QtWidgets.QPushButton("Transcode all")
        self.launchBut.setMaximumWidth(100)

        # Connect buttons
        self.updateBut.pressed.connect(self.getFilesFromInputTab)
        self.launchBut.pressed.connect(self.launchTranscoding)

        # Create grid layout
        grid = QtWidgets.QGridLayout()
        # TODO: fix spanning issue
#         grid.addWidget(self.transcWidget, 0, 0, 1, 3, QtCore.Qt.AlignLeft)
        grid.addWidget(self.transcWidget, 0, 0)
        grid.addWidget(self.updateBut, 1, 0)
        grid.addWidget(self.launchBut, 1, 1)

        self.setLayout(grid)

    def getFilesFromInputTab(self):
        self.parent.getFilesFromInputTab(self.transcWidget.model)
