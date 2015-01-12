#! python3
# -*-coding: utf-8 -*-

"""
@file Widget.py
The Directory Manager Widget
"""

# Import PyQt
from PyQt5 import QtWidgets

# Import custom PyQt modules
from NzPyQtToolBox.DirMgr.TModel import DirectoryManagerTableModel
from NzPyQtToolBox.DirMgr.TDelegate import DirectoryManagerTableDelegate


# Import custom modules

# Import standard modules
import sys
import logging
import LoggingTools


class DirectoryManagerWidget(QtWidgets.QWidget):
    """
    A widget to contain and own the model and table to manage directories in a
    table view.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the table view
        self.tableView = QtWidgets.QTableView()

        # The layout
        _layout = QtWidgets.QVBoxLayout(self)
        _layout.addWidget(self.tableView)

        self.ctrlButCol = 0

    def __repr__(self):
        model = self.getModel()
        delegate = self.getDelegate()
        tableview = self.tableView
        msg = ("{}@{}(tableView={!r}@{}, model={!r}, _delegate={!r}".format(
            self.__class__.__name__, hex(id(self)),
            tableview.__class__.__name__, hex(id(tableview)), model, delegate)
        )
        return msg

    def setModelToView(self, model):
        """
        Set a directory manager table model to a table view. Some internal
        stuff is also done.

        @param[in] model The DirectoryManagerTableModel to set to the table
        view
        """
        if not isinstance(model, DirectoryManagerTableModel):
            raise RuntimeError(("Model assigned to this widget must inherit "
                                "from DirectoryManagerTableModel. Got type "
                                "{}".format(model.__class__.__name__)))
        self.model = model
        # Qt setModel
        self.tableView.setModel(self.model)

        # Connect newButtonCreated to a method that will create the button on
        # the next row
        self.model.signals.newButtonCreated.connect(
            self._createPersistentEditorOnNextRow)

        # Connect directoryAdded to the method that will process the new
        # directory
        self.model.signals.directoryAdded.connect(self._processNewDirectory)

    def getModel(self):
        """
        Getter for the model

        @return The model in use
        """
        if not self.model:
            raise RuntimeError(("No model set to the widget. You must use "
                                "method setModelToView to set it up"))
        return self.model

    def getDelegate(self):
        """
        Getter for the delegate

        @return The delegate in use
        """
        return self._delegate

    def setItemDelegate(self, delegate):
        """
        A custom setItemDelegate method.
        It will set the delegate to the table view (Qt standard) and to the
        model (custom implementation).
        Then it will ask the delagate to create the buttons in initial rows.

        @param[in] delagate The item delegate that deals with the view
        """
        if not isinstance(delegate, DirectoryManagerTableDelegate):
            raise RuntimeError(("Model assigned to this widget must inherit "
                                "from DirectoryManagerTableDelegate"))
        self._delegate = delegate
        # Qt setItemDelegate
        self.tableView.setItemDelegate(delegate)
        # Custom setItemDelegate
        self.model.setDelegate(delegate)

        # Create +/- intial buttons
        for row in range(self.model.rowCount(self)):
            self.tableView.openPersistentEditor(
                self.model.index(row, self.ctrlButCol))

        # Resize first column to fit the size of the buttons
        self.tableView.resizeColumnToContents(self.ctrlButCol)

    def _createPersistentEditorOnNextRow(self, startIndex):
        """
        Create a +/- button when a new row is added.

        @param[in] startIndex The @c QModelIndex that define where the change
        occured
        """
        #qtDebugTrace()
        startRow = startIndex.row()

        # Check the index is valid
        if startRow == -1:
            logging.error("Invalid row {} from index: {}".format(
                startRow, startIndex))
            msg = ("Received an invalid QModelIndex, "
                   "can't open persistent editor")
            raise RuntimeError(msg)

        elif self.model.isLastRow(startRow + 1):
            # if the signal was emitted from the last row => create new button
            self.tableView.openPersistentEditor(
                self.model.index(startRow + 1, self.ctrlButCol))
            logging.debug("Persisent editor created on row {}".format(
                startRow + 1))

    def _processNewDirectory(self, dirpath):
        """
        An abstract method (even if we don't use ABC module).
        This method needs to be implement in derived classes to process the
        newly added directory
        """
        currentFuncName = sys._getframe().f_code.co_name
        raise NotImplementedError(
            "method {} must be implemented in subclasses".format(
                currentFuncName))

if __name__ == '__main__':
    LoggingTools.initLogger(logging.INFO)
    #LoggingTools.initLogger(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Create the directory widget
    dirWidget = DirectoryManagerWidget()

    # Create and set model to the widget and its table view
    additionnalHeaders = ["Test1", "Test2", "Test3"]
    model = DirectoryManagerTableModel(dirWidget, additionnalHeaders)
    dirWidget.setModelToView(model)

    # Create and set delegate to the widget
    delegate = DirectoryManagerTableDelegate(dirWidget)
    dirWidget.setItemDelegate(delegate)

    # Show the widget
    dirWidget.setGeometry(900, 100, 600, 600)
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
