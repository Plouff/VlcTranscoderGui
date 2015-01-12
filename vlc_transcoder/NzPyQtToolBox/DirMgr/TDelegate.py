#! python3
# -*-coding: utf-8 -*-

"""
@file TDelegate.py
The table delegate for the Directory Manager Widget
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# Import custom modules

# Import standard modules
import logging


class DirectoryManagerTableDelegate(QtWidgets.QStyledItemDelegate):
    """
    Class that defines and implement the visual customization of the table
    view to show "+" and "-" buttons to add/delete directories
    """
    def __init__(self, parent):
        """
        Class constructor

        @param[in] parent The parent widget containing this table delegate
        """
        # Store parent
        self._parent = parent

        # Get model and table view from parent
        self._model = parent.getModel()
        self._parentTable = parent.tableView

        # Initialize the list of button objects
        self._plusMinusButList = []

        # Call parent constructor
        super(DirectoryManagerTableDelegate, self).__init__(self._parentTable)

        # Create a signal mapper for "+/-" buttons
        self._butClickedMapper = QtCore.QSignalMapper(self._parentTable)
        self._butClickedMapper.mapped[QtWidgets.QWidget].connect(
            self._model.addRemoveDirectory)

    def __repr__(self):
        msg = ("{}@{}(parent={}@{}, model={!r}, _plusMinusButList={})".format(
            self.__class__.__name__, hex(id(self)),
            self._parent.__class__.__name__, hex(id(self._parent)),
            self._model, self._plusMinusButList))
        return msg

    #
    # STANDARD QT METHODS
    #
    def paint(self, painter, option, index):
        """
        Method to draw the model on the view.

        @param[in] painter The painter to use to draw
        @param[in] option The QStyleOptionViewItem defining the needed object
        option
        @param[in] index The index information of the cell being dealt with
        """

        # Get row and column
        column = index.column()
        row = index.row()
        if column == 0:
            try:
                if index.model().isLastRow(row):
                    self._plusMinusButList[row].setText("+")
                else:
                    self._plusMinusButList[row].setText("-")
            except IndexError as e:
                msg = "paint: Row {} - Column {} - RowCount {}\n".format(
                    row, column, index.model().rowCount())
                msg = msg + "buts\n{}".format(self._plusMinusButList)
                logging.error(msg)
                logging.exception(e)
            except RuntimeError as e:
                logging.error("paint: Row {} - Column {} - RowCount {}".format(
                    row, column, index.model().rowCount()))
                logging.exception(e)

        else:
            # If the cell is not a special then the default delegate painter
            # doing the job
            super().paint(painter, option, index)

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

    #
    # CUSTOM METHODS
    #
    def getIndexOfButton(self, button):
        """
        Get index of a given button object in the list of +/- buttons

        @param[in] button The +/- button that index is needed
        """
        return self._plusMinusButList.index(button)

    def removeButton(self, index):
        """
        Helper to remove a +/- button from the list of +/- buttons

        @param[in] index The index of the +/- button to remove

        @return the button object removed
        """
        logging.debug("removeButton: position {}".format(index))
        return self._plusMinusButList.pop(index)
