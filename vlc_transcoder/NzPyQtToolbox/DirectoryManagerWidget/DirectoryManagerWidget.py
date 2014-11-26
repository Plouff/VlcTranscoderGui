#! python3
#-*-coding: utf-8 -*-

"""
@file DirectoryManagerWidget.py
The Model for the transcoder
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
from pprint import pprint
from DirectoryManagerTableModel import *
from DirectoryManagerTableDelegate import *


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
        initialRows = [["" for i in range(len(headers))]]
        initialRows = [["" for i in range(len(headers))] for i in range(10)]
        self._model = DirectoryManagerTableModel(initialRows, headers,
                                                 self._tableView)
        self._tableView.setModel(self._model)

        # Create and set delegate to the table
        _delegate = DirectoryManagerTableDelegate(masterWidget=self)
        self._tableView.setItemDelegate(_delegate)
        self._model.setDelegate(_delegate)

        for row in range(0, self._model.rowCount(self)):
            self._tableView.openPersistentEditor(self._model.index(row, 0))

        _layout.addWidget(self._tableView)

    def getModel(self):
        return self._model

    def getTableView(self):
        return self._tableView



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle("plastique")

    dirWidget = DirectoryManagerWidget(headers=["Controls", "Status",
                                                "Directory", "Files found"])
    # Show the widget
    dirWidget.setGeometry(900, 100, 600, 600)
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
