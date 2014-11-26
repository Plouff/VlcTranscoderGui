#! python3
#-*-coding: utf-8 -*-

"""
@file DirectoryManagerTableDelegate.py
The Model for the transcoder
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
from pprint import pprint

from DebugTrace import qtDebugTrace


class DirectoryManagerTableModel(QtCore.QAbstractTableModel):

    # Create a signal mapper for "-" buttons
    _minusButClicked = QtCore.pyqtSignal(int)

    def __init__(self, directoryData=[[]], headers=[], parentTable=None):
        super().__init__(parentTable)
        self._directoryData = directoryData
        self._headers = headers
        self.parentTable = parentTable

    def setDelegate(self, delegate):
        self._delegate = delegate

    def getMinusButClickedMapper(self):
        return self._minusButClicked

    def rowCount(self, parentTable=None):
        return len(self._directoryData)

    def columnCount(self, parentTable=None):
        return len(self._directoryData[0])

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
                return "#{}".format(section)

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
            #print("setData: Row {} - Column {}".format(row, column))

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

    def addRemoveDirectory(self, button):
        row = self._delegate.getIndexOfButton(button)
        print("addRemoveDirectory - row #{} - rowCount {}".format(
            row, self.rowCount()))
        if self.isLastRow(row):
            print("Add dir: row {}".format(row))
            self.addDirectory(row)
            print("rowCount {}".format(self.rowCount()))
        else:
            print("Remove dir: row {}".format(row))
            self.removeRow(row)
            print("rowCount {}".format(self.rowCount()))

    def addDirectory(self, row):
        rootDir = QtWidgets.QFileDialog.getExistingDirectory(self.parentTable,
            'Root directory', '/', QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        #rootDir = "test"
        print(rootDir)
        if rootDir:
            self._directoryData[row][2] = rootDir
            startIndex = self.index(row, 0)
            endIndex = self.index(self.rowCount(), self.columnCount())
            self.insertRows(row, 1)
            self.dataChanged.emit(startIndex, endIndex)
            self.parentTable.openPersistentEditor(self.index(row + 1, 0))
            return True

        return False

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        #print("insertRows: row {} - count {}".format(row, count))
        self.beginInsertRows(parent, row + 1, row + count)
        newRow = self.getEmptyRow()
        for i in range(count):
            self._directoryData.insert(row + 1 + i, newRow)
        self.endInsertRows()
        return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        #print("removeRow: row {}".format(row))
        self.beginRemoveRows(parent, row, row)
        #pprint(self._directoryData)
        self._directoryData.pop(row)
        #pprint(self._directoryData)
        index = self.index(row + 1, 0)
        #self._minusButClicked.emit(row)
        self._delegate.removeButton(row)
        self.dataChanged.emit(index, index)
        self.endRemoveRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        raise NotImplementedError(
            "Not implemented since the widget only needs removeRow()")
