#! python3
#-*-coding: utf-8 -*-

"""
@file DirectoryManagerWidget.py
The Model for the transcoder
"""

# Import PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

# Import custom PyQt modules
from DirectoryManagerTableModel import *
from DirectoryManagerTableDelegate import *
from DebugTrace import qtDebugTrace

# Import custom modules

# Import standard modules
import sys
import logging
import LoggingTools
from pprint import pprint


class DirectoryManagerWidget(QtWidgets.QWidget):
    """
    A simple test widget to contain and own the model and table.
    """
    def __init__(self, headers=[], parent=None):
        super().__init__(parent)

        _layout = QtWidgets.QVBoxLayout(self)

        # A table view
        self._tableView = QtWidgets.QTableView()

        # Create and set the model to the table
        self._model = DirectoryManagerTableModel(headers, self._tableView)
        self._tableView.setModel(self._model)

        # TEMPORARY
        #self._model.insertRows(1, 5)

        # Create and set delegate to the table
        _delegate = DirectoryManagerTableDelegate(masterWidget=self)
        self._tableView.setItemDelegate(_delegate)
        self._model.setDelegate(_delegate)

        for row in range(0, self._model.rowCount(self)):
            self._tableView.openPersistentEditor(self._model.index(row, 0))

        # Resize first column to fit the size of the buttons
        self._tableView.resizeColumnToContents(0)

        _layout.addWidget(self._tableView)

    def getModel(self):
        return self._model

    def getTableView(self):
        return self._tableView


if __name__ == '__main__':
    LoggingTools.initLogger(logging.INFO)
    app = QtWidgets.QApplication(sys.argv)

    dirWidget = DirectoryManagerWidget()
        #headers=["Status", "Files found"])

    # Show the widget
    dirWidget.setGeometry(900, 100, 600, 600)
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
