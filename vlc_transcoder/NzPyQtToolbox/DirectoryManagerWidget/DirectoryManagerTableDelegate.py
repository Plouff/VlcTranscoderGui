#! python3
#-*-coding: utf-8 -*-

"""
@file DirectoryManagerTableDelegate.py
The Model for the transcoder
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

# Import custom modules

# Import standard modules
import sys
import logging
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
        self._butClickedMapper.mapped[QtWidgets.QWidget].connect(
            self.model.addRemoveDirectory)

    def getButtonClickedMapper(self):
        return self._butClickedMapper

    def getIndexOfButton(self, button):
        return self._plusMinusButList.index(button)

    def removeButton(self, position):
        logging.debug("removeButton: position {}".format(position))
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
                logging.error("paint: Row {} - Column {} - RowCount {}".format(
                    row, column, index.model().rowCount()))
                logging.exception(e)
                sys.exit()
            except RuntimeError as e:
                logging.error("paint: Row {} - Column {} - RowCount {}".format(
                    row, column, index.model().rowCount()))
                logging.exception(e)
                sys.exit()

        else:
            # If the cell is not a special then the default delegate painter
            # doing the job
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parentTable, option, index):
        column = index.column()
        row = index.row()
        if column == 0:
            # Create a container widget
            centeredBut = QtWidgets.QWidget(parentTable)
            #logging.debug("parentTable {}".format(parentTable))
            self._plusMinusButList.append(QtWidgets.QPushButton(centeredBut))

            # Define maximum size of the _plusMinusButList
            self._plusMinusButList[row].setMaximumSize(25, 25)

            # Connect the _plusMinusButList clicked signal to our mapper
            self._plusMinusButList[row].clicked.connect(
                self._butClickedMapper.map)

            # We use the mapper to send the button that triggered the signal
            self._butClickedMapper.setMapping(self._plusMinusButList[row],
                                              self._plusMinusButList[row])

            # Create a layout to center the _plusMinusButList
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(self._plusMinusButList[row])
            hbox.setAlignment(self._plusMinusButList[row],
                              QtCore.Qt.AlignCenter)
            hbox.setContentsMargins(0, 0, 0, 0)
            centeredBut.setLayout(hbox)
            logging.debug(
                "created editor: Row {} - Column {} - Editor {}".format(
                    row, column, str(self._plusMinusButList[row])))
            return centeredBut

        else:
            return QtWidgets.QStyledItemDelegate.createEditor(
                self, parentTable, option, index)
