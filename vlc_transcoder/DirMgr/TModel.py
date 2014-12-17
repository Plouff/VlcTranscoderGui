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

    def data(self, index, role):
        if role == QtCore.Qt.TextAlignmentRole:
            pass
            statusCol = self.getColumByHeader('Status')
            filesCountCol = self.getColumByHeader('File count')
            column = index.column()
            if column == statusCol or column == filesCountCol:
                return QtCore.Qt.AlignCenter
        else:
            return super().data(index, role)

    #
    # CUSTOM METHODS
    #
    def setStatus(self, dir, status):
        """
        Set the status column in the model.

        @param[in] dir The directory row to be updated
        @param[in] status The status to write
        """
        self._setDataWithDirnHeader(dir, 'Status', status)

    def setFileCount(self, dir, data):
        """
        Set the file count column in the model.

        @param[in] dir The directory row to be updated
        @param[in] data The data to write
        """
        self._setDataWithDirnHeader(dir, 'File count', data)

    def setFiles(self, dir, data):
        """
        Set the files column in the model.

        @param[in] dir The directory row to be updated
        @param[in] data The data to write
        """
        self._setDataWithDirnHeader(dir, 'Files', data)

    def appendFile(self, dir, data):
        """
        Append a file to list of files in the files column in the model.

        @param[in] dir The directory row to be updated
        @param[in] data The data to write
        """
        self._appendDataWithDirnHeader(dir, 'Files', data)

    def setExtensions(self, dir, data):
        """
        Set the extension column in the model.

        @param[in] dir The directory row to be updated
        @param[in] data The data to write
        """
        self._setDataWithDirnHeader(dir, 'Extensions', data)

    def setError(self, dir, data):
        """
        Set the extension column in the model.

        @param[in] dir The directory row to be updated
        @param[in] data The data to write
        """
        self._setDataWithDirnHeader(dir, 'Error', data)
