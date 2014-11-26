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
        self._plusMinusButList = []

        # Call parent constructor
        super(DirectoryManagerTableDelegate, self).__init__(self.parentTable)

        # Create a signal mapper for "+/-" buttons
        self._butClickedMapper = QtCore.QSignalMapper(self.parentTable)
        self._butClickedMapper.mapped[int].connect(
            self.model.addRemoveDirectory)

        # A signal to remove buttons for the list of buttons
        #self._rowRemovedSignal = QtCore.pyqtSignal()

        self._minusButClicked = self.model.getMinusButClickedMapper()
        #self._minusButClicked.connect(self.removeButton)

    def getButtonClickedMapper(self):
        return self._butClickedMapper

    def removeButton(self, position):
        #print("removeButton: position {}".format(position))
        self._plusMinusButList.pop(position)

    def paint(self, painter, option, index):
        """
        Method to draw the model.

        @param[in] painter The painter to use to draw
        @param[in] option The QStyleOptionViewItem defining the needed object
        option
        @param[in] index The index information of the cell being dealt with
        """

        column = index.column()
        row = index.row()
        if column == 0:
            try:
                if index.model().isLastRow(row):
                    self._plusMinusButList[row].setText("+")
                else:
                    self._plusMinusButList[row].setText("-")
            except IndexError as e:
                print("paint: Row {} - Column {} - RowCount {}".format(row, column,
                                                                       index.model().rowCount()))
                print(e)
                raise
                sys.exit()
            except RuntimeError as e:
                print("paint: Row {} - Column {} - RowCount {}".format(row, column,
                                                                       index.model().rowCount()))
                print(e)
                raise
                sys.exit()

        else:
            # If the cell is not a special then the default delegate painter
            # doing the job
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parentTable, option, index):
        column = index.column()
        row = index.row()
        #print("createEditor: Row {} - Column {}".format(row, column))
        if column == 0:
            # Create a container widget
            centeredBut = QtWidgets.QWidget(parentTable)
            #print("createEditor - parentTable {}".format(parentTable))
            self._plusMinusButList.append(QtWidgets.QPushButton(centeredBut))

            # Define maximum size of the _plusMinusButList
            self._plusMinusButList[row].setMaximumSize(25, 25)

            # Connect the _plusMinusButList clicked signal to our mapper
            self._plusMinusButList[row].clicked.connect(
                self._butClickedMapper.map)

            # We use the mapper to send the row index of the _plusMinusButList
            self._butClickedMapper.setMapping(self._plusMinusButList[row], row)
            self._butClickedMapper.setMapping(self._plusMinusButList[row],
                                              str(self._plusMinusButList[row]))

            # Create a layout to center the _plusMinusButList
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(self._plusMinusButList[row])
            hbox.setAlignment(self._plusMinusButList[row],
                              QtCore.Qt.AlignCenter)
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



