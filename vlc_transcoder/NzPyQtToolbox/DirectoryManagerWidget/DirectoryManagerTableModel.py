#! python3
#-*-coding: utf-8 -*-

"""
@file DirectoryManagerTableDelegate.py
The Model for the transcoder
"""

# Import PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

# Import custom PyQt modules
from DebugTrace import qtDebugTrace

# Import standard modules
import sys
import logging
import warnings
from pprint import pprint, pformat


class DirectoryManagerTableModel(QtCore.QAbstractTableModel):
    """
    This table model implements the basic behavior of a view. It means add
    directories when the + button is pressed and remove rows when the - button
    is pressed
    """
    directoryAdded = QtCore.pyqtSignal(str)
    newButtonCreated = QtCore.pyqtSignal(QtCore.QModelIndex,
                                         QtCore.QModelIndex)

    def __init__(self, parent=None, additionnalHeaders=[]):
        """
        Class constructor

        @param[in] parent The parent widget of the model (default: @c None)
        @param[in] additionnalHeaders The list of additionnal headers to create
        columns at instantiation (default @c [])
        """
        super().__init__(parent)
        # Append additionnal header to the list of headers
        self._headers = ['Ctrl', 'Directory'] + additionnalHeaders
        logging.debug(self._headers)

        # Initialiaze and empty data structure
        self._directoryData = [[]]
        # Add an empty to the data structure
        emptyRow = self.getEmptyRow()
        self._directoryData[0] = emptyRow

        # Store parent
        self.parent = parent

        # The static index of the columns
        self._butColumn = 0
        self._dirColumn = 1

    def __repr__(self):
        msg = ('{}@{}(parent={!r}@{}, headers={}, _butColumn={!r}, '.format(
            self.__class__.__name__, hex(id(self)),
            self.parent.__class__.__name__, hex(id(self.parent)),
            self._headers, self._butColumn) +
            '_dirColumn={}, _directoryData={})'.format(
                self._dirColumn, self._directoryData)
        )
        return msg

    #
    # STANDARD QT METHODS
    #
    def rowCount(self, parent=None):
        return len(self._directoryData)

    def columnCount(self, parent=None):
        return len(self._headers)

    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
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
                # Header of rows
                if self.isLastRow(section):
                    # Don't print number for last row
                    return ''
                else:
                    # Print row number for rows containing a dir
                    return "#{}".format(section + 1)

    def data(self, index, role):
        if role == QtCore.Qt.ToolTipRole:
            # The tooltip role depends on the row
            row = index.row()
            column = index.column()

            if column == self._butColumn:
                # For +/- button column
                if self.isLastRow(row):
                    # If it's the last row it's a + button
                    return "Add new directory"
                else:
                    # else it's a - button
                    dir = self._directoryData[row][self._dirColumn]
                    return "Remove directory: {}".format(dir)

            elif column == self._dirColumn:
                # On directory column return the name of the dir
                dir = self._directoryData[row][column]
                return dir

        #if role == QtCore.Qt.DecorationRole:
            #row = index.row()
            #column = index.column()

        if role == QtCore.Qt.DisplayRole:
            # On DisplayRole just retrieve the data in the data structure
            column = index.column()
            row = index.row()
            if column != self._butColumn:
                value = self._directoryData[row][column]
                return value

    '''
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        The setData() function is called when the user change the value of a
        cell
        """
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            logging.debug("Row {} - Column {}".format(row, column))
        return True
    '''

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if row >= self.rowCount() + 1:
            # Check that the row is inserted at most at the last postion
            msg = "Tried to insert row at position {} but the table ".format(
                row)
            msg = msg + "only has {} rows".format(self.rowCount())
            warnings.warn(msg, RuntimeWarning)
            return False
        if row < 0:
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
                self._directoryData.insert(row + 1 + i, newRow)
            # Mandatory call of endInsertRows
            self.endInsertRows()
            return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        if row >= self.rowCount() + 1:
            # Check that the row is inserted at most at the last postion
            msg = "Tried to remove row at position {} but the table ".format(
                row)
            msg = msg + "only has {} rows".format(self.rowCount())
            warnings.warn(msg, RuntimeWarning)
            return False
        if row < 0:
            # Check that row is not inserted at an index < 0
            raise RuntimeError("Can't remove row at position {}".format(row))
            return False
        else:
            logging.debug("row {}".format(row))
            # Mandatory call of beginInsertRows
            self.beginRemoveRows(parent, row, row)
            # Remove row from directory data structure
            dir = self._directoryData.pop(row)
            # Ask delegate to remove the button from the list of buttons
            self._delegate.removeButton(row)

            # Emit dataChanged
            logging.debug("emitted row {}".format(row))
            index = self.index(row, 0)
            self.dataChanged.emit(index, index)

            # Mandatory call of endRemoveRows
            self.endRemoveRows()
            logging.info("Removed dir: {}".format(dir[1]))
            return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        raise NotImplementedError(
            "Not implemented since the widget only needs removeRow()")

    #
    # CUSTOM METHODS
    #

    # Getters and Setters
    def setDelegate(self, delegate):
        """
        Getter for the delegate of the table view

        @param[in] delegate The delegate of the corresponding table view
        """
        self._delegate = delegate

    def getDirectoryColumn(self):
        """
        Get the column of the directories

        @return The colum number of the directories
        """
        return self._dirColumn

    def getDirectoryColumn(self):
        """
        Get the column of the directories

        @return The colum number of the directories
        """
        return self._dirColumn

    def isLastRow(self, row):
        """
        Helper to check if a row index is the last one

        @param[in] row The row index to check

        @return A boolean
        """
        if row == (self.rowCount() - 1):
            return True
        else:
            return False

    def isLastColumn(self, column):
        """
        Helper to check if a column index is the last one

        @param[in] column The column index to check

        @return A boolean
        """
        if column == (self.columnCount() - 1):
            return True
        else:
            return False

    def getEmptyRow(self):
        """
        Generate an empty with the correct number of columns

        @return A list containing as many empty strings as the number of
        columns
        """
        return ["" for j in range(self.columnCount())]

    def addRemoveDirectory(self, button):
        """
        Decide whether to add or remove depending on the postion of the button
        pressed

        @param[in] button The button that was pressed
        """
        # Use delegate to get the row of the button that was pressed
        row = self._delegate.getIndexOfButton(button)
        logging.debug("Row #{} - rowCount {}".format(
            row, self.rowCount()))

        if self.isLastRow(row):
            # If the row is the last => add a new directory
            logging.debug("Add dir: row {}".format(row))
            self.addDirectory(row)
        else:
            # Else remove a row
            logging.debug("Remove dir: row {}".format(row))
            self.removeRow(row)

    def addDirectory(self, row):
        """
        Add a directory to the model and create the new last row containing the
        + button.

        @param[in] row The row where to add the new directory
        """
        # Use the QFileDialog to get the new directory from the user
        newDir = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent, 'Root directory', '/',
            QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        #newDir = "test"

        logging.debug(newDir)

        if newDir:
            #qtDebugTrace()
            # Set the directory path in the given row
            self._directoryData[row][self._dirColumn] = newDir
            logging.debug("dirs\n {}".format(pformat(self._directoryData)))

            # Insert a new row after the current one
            self.insertRows(row, 1)

            # Emit dataChanged
            startIndex = self.index(row, self._dirColumn)
            logging.debug("emitted row {}".format(row))
            endIndex = self.index(row + 1, self.columnCount())
            self.dataChanged.emit(startIndex, startIndex)

            # Emit newButtonCreated with indexes of the changed area
            self.newButtonCreated.emit(startIndex, startIndex)

            logging.info("New directory added: {}".format(newDir))

            # Emit DirectoryAdded with the name of the directory
            self.directoryAdded.emit(newDir)
            return True

        return False

    def getDirectoryRow(self, dir):
        """
        Get the row of a given directory. If the directory can't be found a
        @c RuntimeError is raised.

        @param[in] dir The name of the directory to look for

        @return The row corresponding to the directory or @c -1 in case of
        error
        """
        for i, row in enumerate(self._directoryData):
            # Loop thru row in directory structure with the index i
            logging.debug("Looking for {} in {}".format(dir, pformat(row)))
            if dir in row:
                # Check if the directory is in the current row
                return i
        else:
            # If the directory can't be raise a RuntimeError
            raise RuntimeError("Can't find dir {} in list of dirs\n{}".format(
                dir, pformat(self._directoryData)))
            return -1

    def _setDataWithDirnHeader(self, dir, header, data):
        """
        Set data to the cell found with a directory name and a header.

        @param[in] dir The name of the directory row to set
        @param[in] header The name of the header column to set
        @param[in] data The name data to set
        """
        # Check that header exists
        try:
            statusCol = self._headers.index(header)
        except:
            raise RuntimeError("Header '{}' doesn't exist in {}".format(
                header, self._headers))
        # Get directory row
        dirRow = self.getDirectoryRow(dir)

        # Set new data
        self._directoryData[dirRow][statusCol] = data

        # Emit dataChanged
        index = self.index(dirRow, statusCol)
        self.dataChanged.emit(index, index)