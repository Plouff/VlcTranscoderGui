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

    def __init__(self, headers=[], parentTable=None):
        super().__init__(parentTable)
        self._headers = ['Ctrl', 'Directory'] + headers
        self._directoryData = [[]]
        emptyRow = self.getEmptyRow()
        self._directoryData[0] = emptyRow
        logging.debug(self._headers)
        self.parentTable = parentTable

    def setDelegate(self, delegate):
        self._delegate = delegate

    def rowCount(self, parentTable=None):
        return len(self._directoryData)

    def columnCount(self, parentTable=None):
        return len(self._headers)

    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self._headers):
                    return self._headers[section]
                else:
                    return "Hearder list too short"
            else:
                if self.isLastRow(section):
                    return ''
                else:
                    return "#{}".format(section + 1)

    def getEmptyRow(self):
        return ["" for j in range(self.columnCount())]

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

        #if role == QtCore.Qt.ToolTipRole:
            #row = index.row()
            #column = index.column()

        #if role == QtCore.Qt.DecorationRole:
            #row = index.row()
            #column = index.column()

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._directoryData[row][column]
            return value

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        The createEditor() function is called when the user starts editing an
        item
        """
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            logging.debug("Row {} - Column {}".format(row, column))

            #color = QtGui.QColor(value)

            #if color.isValid():
                #self.__colors[row][column] = color
                #self.dataChanged.emit(index, index)
                #return True
        return True

    def isLastRow(self, row):
        if row == (self.rowCount() - 1):
            return True
        else:
            return False

    def isLastColumn(self, column):
        if column == (self.columnCount() - 1):
            return True
        else:
            return False

    def addRemoveDirectory(self, button):
        row = self._delegate.getIndexOfButton(button)
        logging.debug("Row #{} - rowCount {}".format(
            row, self.rowCount()))
        if self.isLastRow(row):
            logging.debug("Add dir: row {}".format(row))
            self.addDirectory(row)
        else:
            logging.debug("Remove dir: row {}".format(row))
            self.removeRow(row)

    def addDirectory(self, row):
        rootDir = QtWidgets.QFileDialog.getExistingDirectory(
            self.parentTable, 'Root directory', '/',
            QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        #rootDir = "test"
        logging.debug(rootDir)
        if rootDir:
            #qtDebugTrace()
            logging.debug("dirs\n {}".format(pformat(self._directoryData)))
            self._directoryData[row][1] = rootDir
            logging.debug("dirs\n {}".format(pformat(self._directoryData)))
            startIndex = self.index(row, 1)
            self.insertRows(row, 1)
            self.dataChanged.emit(startIndex, startIndex)
            self.parentTable.openPersistentEditor(self.index(row + 1, 0))

            logging.info("New directory added: {}".format(rootDir))
            return True

        return False

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if row >= self.rowCount() + 1:
            msg = "Tried to insert row at position {} but the table ".format(row)
            msg = msg + "only has {} rows".format(self.rowCount())
            warnings.warn(msg, RuntimeWarning)
            return False
        else:
            logging.debug("row {} - count {}".format(row, count))
            self.beginInsertRows(parent, row + 1, (row + 1) + (count - 1))
            for i in range(count):
                newRow = self.getEmptyRow()
                self._directoryData.insert(row + 1 + i, newRow)
            self.endInsertRows()
            return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        logging.debug("row {}".format(row))
        self.beginRemoveRows(parent, row, row)
        #pprint(self._directoryData)
        self._directoryData.pop(row)
        #pprint(self._directoryData)
        index = self.index(row + 1, 0)
        self._delegate.removeButton(row)
        self.dataChanged.emit(index, index)
        self.endRemoveRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        raise NotImplementedError(
            "Not implemented since the widget only needs removeRow()")
