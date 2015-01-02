#! python3
#-*-coding: utf-8 -*-

"""
@file TModel.py
The table model for the Directory Manager Widget
"""

# Import PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.Qt import QDir

# Import custom PyQt modules
from DebugTrace import qtDebugTrace

# Import standard modules
import logging
import warnings
import os
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
                    dirpath = self._directoryData[row][self._dirColumn]
                    return "Remove directory: {}".format(dirpath)

            else:
                # For other cells display the content of the cell
                data = self._directoryData[row][column]
                data = self.stringConverter(data)
                return data

        #if role == QtCore.Qt.DecorationRole:
            #row = index.row()
            #column = index.column()

        if role == QtCore.Qt.DisplayRole:
            # On DisplayRole just retrieve the data in the data structure
            column = index.column()
            row = index.row()
            if column != self._butColumn:
                value = self._directoryData[row][column]
                # If the data is a list then we convert it into a string
                value = self.stringConverter(value)
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
            dirpath = self._directoryData.pop(row)
            # Ask delegate to remove the button from the list of buttons
            self._delegate.removeButton(row)

            # Emit dataChanged
            logging.debug("emitted row {}".format(row))
            index = self.index(row, 0)
            self.dataChanged.emit(index, index)

            # Mandatory call of endRemoveRows
            self.endRemoveRows()
            logging.info("Removed dirpath: {}".format(dirpath[1]))
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
        newDir = QDir.toNativeSeparators(newDir)

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
            # endIndex = self.index(row + 1, self.columnCount())
            self.dataChanged.emit(startIndex, startIndex)

            # Emit newButtonCreated with indexes of the changed area
            self.newButtonCreated.emit(startIndex, startIndex)

            logging.info("New directory added: {}".format(newDir))

            # Emit DirectoryAdded with the name of the directory
            self.directoryAdded.emit(newDir)
            return True

        return False

    def getDirectoryRow(self, dirpath):
        """
        Get the row of a given directory. If the directory can't be found a
        @c RuntimeError is raised.

        @param[in] dirpath The name of the directory to look for

        @return The row corresponding to the directory or @c -1 in case of
        error
        """
        for i, row in enumerate(self._directoryData):
            # Loop thru row in directory structure with the index i
            #logging.debug("Looking for {} in {}".format(dirpath, pformat(row)))
            if dirpath in row:
                # Check if the directory is in the current row
                return i
        else:
            # If the directory can't be raise a RuntimeError
            raise RuntimeError("Can't find dirpath {} in list of dirs\n{}".format(
                dirpath, pformat(self._directoryData)))
            return -1

    def getColumnByHeader(self, name):
        """
        Get the column number of a given header.

        @param[in] name The name of the column

        @return a positive @c int if successful or @c -1 otherwise
        """
        try:
            return self._headers.index(name)
        except:
            raise RuntimeError("Can't find column header: '{}''".format(name))
            return -1

    def stringConverter(self, data):
        """
        Convert the data into a string if necessary.

        If a cell holds something else than a string then it can't be displayed
        directly. So we need to convert the data into a string.
        At the moment only @c list are supported.

        @param[in] data The data to be displayed

        @return a @c string
        """
        if data is not None:
            if isinstance(data, list):
                try:
                    data = ", ".join(data)
                except Exception as e:
                    raise e
        return data

    def _setDataWithDirnHeader(self, dirpath, header, data):
        """
        Set data to the cell found with a directory name and a header.

        @param[in] dirpath The name of the directory row to set
        @param[in] header The name of the header column to set
        @param[in] data The name data to set
        """
        # Check that header exists
        try:
            col = self._headers.index(header)
        except:
            raise RuntimeError("Header '{}' doesn't exist in {}".format(
                header, self._headers))
        # Get directory row
        dirRow = self.getDirectoryRow(dirpath)

        # Set new data
        self._directoryData[dirRow][col] = data

        # Emit dataChanged
        index = self.index(dirRow, col)
        self.dataChanged.emit(index, index)

    def _appendDataWithDirnHeader(self, dirpath, header, data):
        """
        Append data to the cell found with a directory name and a header.

        @param[in] dirpath The name of the directory row to set
        @param[in] header The name of the header column to set
        @param[in] data The name data to be appended
        """
        # Check that header exists
        try:
            col = self._headers.index(header)
        except:
            raise RuntimeError("Header '{}' doesn't exist in {}".format(
                header, self._headers))
        # Get directory row
        dirRow = self.getDirectoryRow(dirpath)

        # Set new data
        curData = self._directoryData[dirRow][col]
        logging.debug("curData: {}".format(curData))

        if isinstance(curData, list):
            curData.append(data)
            newData = curData
        else:
            newData = [data]

        # Set new data
        self._directoryData[dirRow][col] = newData

        # Emit dataChanged
        index = self.index(dirRow, col)
        self.dataChanged.emit(index, index)

if __name__ == '__main__':
    from PyQt5.Qt import QApplication
    import os
    import sys
    import fnmatch

    print(os.sep)
    app = QApplication(sys.argv)
    newDir = QtWidgets.QFileDialog.getExistingDirectory(
        None, 'Root directory', os.sep,
        QtWidgets.QFileDialog.ShowDirsOnly |
        QtWidgets.QFileDialog.DontResolveSymlinks)
    newDir = QDir.toNativeSeparators(newDir)

    for root, dirs, files in os.walk(newDir):
        for basename in files:
            if fnmatch.fnmatch(basename, '*.txt'):
                filename = os.path.join(root, basename)
                print(filename)
    sys.exit(app.exec_())