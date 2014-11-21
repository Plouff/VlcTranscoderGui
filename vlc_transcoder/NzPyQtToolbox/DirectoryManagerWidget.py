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
        emptyList = [["" for i in range(len(headers))]]
        emptyList = [["" for i in range(len(headers))] for i in range(10)]
        self._model = DirectoryManagerTableModel(emptyList, headers,
                                                 self._tableView)
        self._tableView.setModel(self._model)

        # Create and set delegate to the table
        _delegate = DirectoryManagerTableDelegate(masterWidget=self)
        self._tableView.setItemDelegate(_delegate)

        for row in range(0, self._model.rowCount(self)):
            self._tableView.openPersistentEditor(self._model.index(row, 0))

        _layout.addWidget(self._tableView)

    def getModel(self):
        return self._model

    def getTableView(self):
        return self._tableView


class DirectoryManagerTableDelegate(QtWidgets.QStyledItemDelegate):
    """
    Class that defines and implement the visual customization of the table
    view to show:
        @li "+" and "-" buttons to add delete directories
        @li a status icon

    @todo Add a running bar instead of the icon
    """
    def __init__(self, masterWidget):
        """
        Class constructor

        @param[in] masterWidget The master widget containing this table
        delegate
        """
        # Set some pointers
        self.masterWidget = masterWidget
        self.model = masterWidget.getModel()
        self.parentTable = masterWidget.getTableView()

        # Call parent constructor
        super(DirectoryManagerTableDelegate, self).__init__(self.parentTable)

        # Create a signal mapper for "+/-" buttons
        self.mapper = QtCore.QSignalMapper(self.parentTable)

        # Connect our mapper to a dedicated method
        self.mapper.mapped[int].connect(self.model.addNewDirectory)

    '''
    def paint(self, painter, option, index):
        """
        Method to draw the model.

        @param[in] painter The painter to use to draw
        @param[in] option The QStyleOptionViewItem defining the needed object
        option
        @param[in] index The index information of the cell being dealt with
        """

        painter = QtGui.QPainter()
        column = index.column()
        if column == 0:
            # Save the current configuration of the painter to restore it later
            painter.save()

            # Get item data
            #value = index.data(QtCore.Qt.DisplayRole).toBool()
            value = "+"

            # fill style options with item data
            style = QtWidgets.QApplication.style()
            plusButton = QtWidgets.QPushButton("+")
            #plusButton.state |= QtGui.QStyle.State_Enabled
            plusButton.setEnabled(True)

            # draw item data as CheckBox
            style.drawControl(QtGui.QStyle.CE_CheckBox, plusButton, painter)

            # Restore the initial configuration of the painter
            painter.restore()
        else:
            # If the cell is not a special then the default delegate painter
            # doing the job
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
    '''

    def createEditor(self, parentTable, option, index):
        column = index.column()
        row = index.row()
        #print("createEditor: Row {} - Column {}".format(row, column))
        if column == 0:
            # Create a container widget
            centeredBut = QtWidgets.QWidget(parentTable)
            #print("createEditor - parentTable {}".format(parentTable))
            if index.model().isLastRow(row):
                # If this is the last row, create a "+" push button as
                # our editor
                button = QtWidgets.QPushButton("+", centeredBut)
            else:
                # Else, create a "-" push button as our editor
                button = QtWidgets.QPushButton("-", centeredBut)

            # Define maximum size of the button
            button.setMaximumSize(25, 25)

            # Connect the button clicked signal to our mapper
            button.clicked.connect(self.mapper.map)

            # We use the mapper to send the row index of the button
            self.mapper.setMapping(button, row)
            self.mapper.setMapping(button, str(button))

            # Create a layout to center the button
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(button)
            hbox.setAlignment(button, QtCore.Qt.AlignCenter)
            hbox.setContentsMargins(0, 0, 0, 0)
            centeredBut.setLayout(hbox)
            return centeredBut

        #elif column == 2:
            ## create the ProgressBar as our editor.
            #editor = QtGui.QProgressBar(parentTable)
            #return editor

        else:
            return QtWidgets.QStyledItemDelegate.createEditor(self,
                                                              parentTable,
                                                              option, index)

    #def sizeHint(self, option, index):
        #column = index.column()
        #row = index.row()
        #if column == 0:
            #print("sizeHint: Row {} - Column {}".format(row, column))
            #return QtCore.QSize(50, 50)
        #else:
            #return QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)

    def setEditorData(self, editor, index):
        """
        The setEditorData() function is called when an editor is created to
        initialize it with data from the model
        """
        pass


class DirectoryManagerTableModel(QtCore.QAbstractTableModel):

    def __init__(self, directoryStatus=[[]], headers=[], parent=None):
        super().__init__(parent)
        self._directoryStatus = directoryStatus
        self._headers = headers
        self.parent = parent

    def rowCount(self, parent=None):
        return len(self._directoryStatus)

    def columnCount(self, parent):
        return len(self._directoryStatus[0])

    def flags(self, index):
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | \
                QtCore.Qt.ItemIsSelectable
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
                return "#{}".format(section + 1)

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
            value = self._directoryStatus[row][column]
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

    def addNewDirectory(self, row):
        #print("addNewDirectory - row #{}".format(row))
        if self.isLastRow(row):
            print("Add dir")
            rootdir = QtWidgets.QFileDialog.getExistingDirectory(self.parent,
                'Root directory', '/', QtWidgets.QFileDialog.ShowDirsOnly |
                QtWidgets.QFileDialog.DontResolveSymlinks)
            print(rootdir)
        else:
            print("Remove dir")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle("plastique")

    dirWidget = DirectoryManagerWidget(headers=["Controls", "Status",
                                                "Directory", "Files found"])
    # Show the widget
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
