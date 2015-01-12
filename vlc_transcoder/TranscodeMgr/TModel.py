#! python3
# -*-coding: utf-8 -*-

"""
@file TModel.py
The model for the transcoding status table
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

# Import standard modules
import logging
import warnings
from pprint import pformat


class TModel(QtCore.QAbstractTableModel):
    '''
    A table model for the trancoding manager
    '''
    updateProgress = pyqtSignal(int)

    def __init__(self, parent=None):
        '''
        Class constructor

        @param parent The parent widget of the model (default: @c None)
        '''
        super().__init__(parent)
        self.filesdata = []
        self._headers = ['File', 'Status', 'Error Message']

    def __repr__(self):
        msg = '{}@{}(_headers={}, filesdata={})'.format(
            self.__class__.__name__, self.__class__, str(self._headers),
            str(self.filesdata))
        return msg

    def rowCount(self, parent=None):
        return len(self.filesdata)

    def columnCount(self, parent=None):
        return len(self._headers)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            # Header of columns
            if orientation == QtCore.Qt.Horizontal:
                # Check if we can find a header or print error msg in header
                if section < len(self._headers):
                    return self._headers[section]
                else:
                    return "HEARDER LIST TOO SHORT"
                    raise RuntimeError("Header list to short")
            else:
                # Print row number for rows containing a dir
                return "#{}".format(section + 1)

    def data(self, index, role):
        if role == QtCore.Qt.ToolTipRole:
            column = index.column()
            row = index.row()
            data = self.filesdata[row][column]
            return data

        #if role == QtCore.Qt.DecorationRole:
            #row = index.row()
            #column = index.column()

        if role == QtCore.Qt.DisplayRole:
            # On DisplayRole just retrieve the data in the data structure
            column = index.column()
            row = index.row()
            value = self.filesdata[row][column]
            return value

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if row >= self.rowCount() + 1:
            # Check that the row is inserted at most at the last postion
            msg = "Tried to insert row at position {} but the table ".format(
                row)
            msg = msg + "only has {} rows".format(self.rowCount())
            warnings.warn(msg, RuntimeWarning)
            return False
        elif row < 0:
            # Check that row is not inserted at an index < 0
            raise RuntimeError("Can't insert row at position {}".format(row))
            return False
        else:
            logging.debug("row {} - count {}".format(row, count))
            # Mandatory call of beginInsertRows
            self.beginInsertRows(parent, row + 1, (row + 1) + (count - 1))
            for i in range(count):
                # Get an empty with correct length
                newRow = self._getEmptyRow()
                # Insert it in the directory data structure
                self.filesdata.insert(row + 1 + i, newRow.copy())
            # Mandatory call of endInsertRows
            self.endInsertRows()
            return True

    def _getEmptyRow(self):
        """
        Generate an empty with the correct number of columns

        @return A list containing as many empty strings as the number of
        columns
        """
        return ["" for j in range(self.columnCount())]

    def getFileRow(self, file):
        """
        Get the row of a given file. If the file can't be found a
        @c RuntimeError is raised.

        @param file: The name of the file to look for

        @return The row corresponding to the file or @c -1 in case of
        error
        """
        for i, row in enumerate(self.filesdata):
            # Loop thru row in file structure with the index i
            # logging.debug("Looking for {} in {}".format(file, pformat(row)))
            if file in row:
                # Check if the directory is in the current row
                return i
        else:
            # If the directory can't be raise a RuntimeError
            raise RuntimeError(
                "Can't find file {} in list of files\n{}".format(
                    file, pformat(self._headers)))
            return -1

    def getColumnByHeader(self, header):
        return self._headers.index(header)

    def appendFile(self, file):
        """
        Append a file to the widget. the file will be added if the not already
        in the model

        @param file: the file path to append
        """
        for row in self.filesdata:
            filecol = self.getColumnByHeader('File')
            if row[filecol] == file:
                return
        else:
            startIndex = self.index(self.rowCount() - 1, 0)
            endIndex = self.index(self.rowCount() - 1, 1)
            self.insertRows(self.rowCount(), 1)
            curRow = self.filesdata[self.rowCount() - 1]
            col = self.getColumnByHeader('File')
            curRow[col] = file
            col = self.getColumnByHeader('Status')
            curRow[col] = "Waiting"
            self.dataChanged.emit(startIndex, endIndex)

    def setFileWithHeader(self, file, header, data):
        """
        Set the data in the table with file and header

        @param file: The file to update
        @param header: The header of the column to update
        @param data: The data to set
        """
        row = self.getFileRow(file)
        col = self.getColumnByHeader(header)
        self.filesdata[row][col] = data
        index = self.index(row, col)
        self.dataChanged.emit(index, index)

    def setStatus(self, file, status):
        """
        Set the status to a given file in the table

        @param file: The file to update
        @param status: The status to apply
        """
        self.setFileWithHeader(file, 'Status', status)
        self.computeUpdateProgress()

    def setError(self, file, error):
        """
        Set the status to a given file in the table

        @param file: The file to update
        @param error: The error message to apply
        """
        self.setFileWithHeader(file, 'Error Message', error)

    def setFiles(self, files):
        """
        Set a list of files to the table with status 'Waiting'

        @param files: A list of files to set
        """
        # First, empty the model
        self.filesdata = []
        # Reset the views since the model has been brutally updated
        self.modelReset.emit()

        # Second, fill the model
        for f in files:
            self.appendFile(f)

    def DEBUGsetStatus(self, row, status):
        """
        A debug function to set a status giving a row index

        @param row: The row to set
        @param status: The status to apply
        """
        col = self.getColumnByHeader('Status')
        self.filesdata[row][col] = status
        index = self.index(row, col)
        self.dataChanged.emit(index, index)
        self.computeUpdateProgress()

    def computeUpdateProgress(self):
        """
        Compute the progress of the transcoding and request an update of the
        corresponding status bar
        """
        waitCount = 0
        statuscol = self.getColumnByHeader('Status')
        matchingStatus = ['Waiting', 'Transcoding']
        for row in self.filesdata:
            if row[statuscol] in matchingStatus:
                waitCount = waitCount + 1

        prog = 1 - (waitCount / self.rowCount())
        prog = int(prog * 100)

        logging.debug("new progress: {}%".format(prog))

        self.updateProgress.emit(prog)
