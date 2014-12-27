#! python3
#-*-coding: utf-8 -*-

"""
@file InputFilesTab.py
The Input files Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtWidgets
from TranscodeMgr.Widget import TranscoderMgrWidget


class TranscodeTab(QtWidgets.QWidget):
    '''
    This tab will launch transcoding and track the status
    '''

    def __init__(self, parent):
        '''
        The constructor for the Transcoding tab of the GUI

        @param parent The parent widget
        '''
        super().__init__(parent)
        self.parent = parent

        # Create the transcoding status widget
        self.transcWidget = TranscoderMgrWidget(self)

        self.launchBut = QtWidgets.QPushButton("Transcode all")
        self.launchBut.setMaximumWidth(100)

        # Create grid layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.transcWidget, 0, 0)
        grid.addWidget(self.launchBut, 1, 0)

        self.setLayout(grid)
