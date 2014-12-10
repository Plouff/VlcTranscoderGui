#! python3
#-*-coding: utf-8 -*-

"""
@file TModel.py
The table model for the Transcoder extension of the Directory Manager Widget
"""

# Import PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

# Import custom PyQt modules
from NzPyQtToolBox.DirMgr.TModel import DirectoryManagerTableModel
from DebugTrace import qtDebugTrace

# Import standard modules
import sys
import logging
import warnings
from pprint import pprint, pformat


class TranscoderDirMgrTableModel(DirectoryManagerTableModel):
    """
    This class inherits from DirectoryManagerTableModel to add the management
    of directories.
    It means setting the status of the scan (scanning/scanned) and update the
    count of files found during the scan of directories.
    """

    def __init__(self, parent=None, additionnalHeaders=[]):
        """
        Class constructor

        @param[in] parent The parent widget of the model (default: @c None)
        @param[in] additionnalHeaders The list of additionnal headers to create
        columns at instantiation (default @c [])
        """
        super().__init__(parent, additionnalHeaders)

    #
    # STANDARD QT METHODS
    #
    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    #def data(self, index, role):
        ##
        ## TODO Debug this....
        ##
        #if role == QtCore.Qt.TextAlignmentRole:
            #statusCol = self._headers.index('Status')
            #filesCol = self._headers.index('Files')
            #column = index.column()
            #if column == statusCol or column == filesCol:
                #return QtCore.Qt.AlignCenter
        #else:
            #super().data(index, role)

    #
    # CUSTOM METHODS
    #
    def updateFileCount(self, dir, count):
        #logging.debug(pformat(self._directoryData))
        # Get column number for Files
        filesCol = self._headers.index('Files')
        # Get row number of current directory
        dirRow = self.getDirectoryRow(dir)
        logging.debug("dirRow {} - filesCol {}".format(dirRow, filesCol))
        # Set new count of files
        self._directoryData[dirRow][filesCol] = count
        # Emit dataChanged for other views
        index = self.index(dirRow, filesCol)
        self.dataChanged.emit(index, index)

    def _setStatus(self, dir, status):
        self._setDataWithDirnHeader(dir, 'Status', status)

    def setScanningStatus(self, dir):
        self._setStatus(dir, "Scanning")

    def setScannedStatus(self, dir):
        self._setStatus(dir, "Scanned")
