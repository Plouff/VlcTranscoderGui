#! python3
# -*-coding: utf-8 -*-

"""
@file TModel.py
The model for the transcoding status table
"""

# Import PyQt modules
from PyQt5 import QtCore

# Import standard modules
import logging
import warnings
from pprint import pformat


class TModel(QtCore.QAbstractTableModel):
    '''
    A table model for the trancoding manager
    '''

    updateProgress = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        '''
        Class constructor

        @param[in] parent The parent widget of the model (default: @c None)
        '''
        super().__init__(parent)
        self._filesdata = []
        self._headers = ['File', 'Status']

    def __repr__(self):
        msg = '{}@{}(_headers={}, _filesdata={})'.format(
            self.__class__.__name__, self.__class__, str(self._headers),
            str(self._filesdata))
        return msg

    def rowCount(self, parent=None):
        return len(self._filesdata)

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
            data = self._filesdata[row][column]
            return data

        #if role == QtCore.Qt.DecorationRole:
            #row = index.row()
            #column = index.column()

        if role == QtCore.Qt.DisplayRole:
            # On DisplayRole just retrieve the data in the data structure
            column = index.column()
            row = index.row()
            value = self._filesdata[row][column]
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
                newRow = self.getEmptyRow()
                # Insert it in the directory data structure
                self._filesdata.insert(row + 1 + i, newRow.copy())
            # Mandatory call of endInsertRows
            self.endInsertRows()
            return True

    def getEmptyRow(self):
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

        @param[in] file: The name of the file to look for

        @return The row corresponding to the file or @c -1 in case of
        error
        """
        for i, row in enumerate(self._filesdata):
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

    def appendFile(self, file):
        """
        Append a file to the widget

        @param[in] file: the file path to append
        """
        self.insertRows(self.rowCount(), 1)
        curRow = self._filesdata[self.rowCount() - 1]
        curRow[0] = file
        curRow[1] = "Waiting"

    def setStatus(self, file, status):
        row = self.getFileRow(file)
        self._filesdata[row][1] = status

    def computeUpdateProgress(self):
        """
        Compute the progress of the transcoding and request an update of the
        corresponding status bar
        """
        waitCount = 0
        for row in self._filesdata:
            if row[1] == 'Waiting':
                waitCount = waitCount + 1

        prog = waitCount / self.rowCount()
        prog = int(prog)

        self.updateProgress.emit(prog)
