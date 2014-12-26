#! python3
#-*-coding: utf-8 -*-

"""
@file InputFilesTab.py
The Input files Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtWidgets


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
