#! python3
# -*-coding: utf-8 -*-

"""
@file TModel.py
The model for the transcoding status _tableView
"""
# Import PyQt modules
from PyQt5 import QtWidgets

# Import custom modules
from TranscodeMgr.TModel import TModel
from NzToolBox import LoggingTools

# Import standard modules
import logging


class TranscoderMgrWidget(QtWidgets.QWidget):
    '''
    The transcoding manager widget
    '''

    def __init__(self, parent=None):
        '''
        Class constructor
        @param[in] parent: The parent widget
        '''
        super().__init__(parent)
        # Create model
        self.model = TModel()
        # Create _tableView view
        self._tableView = QtWidgets.QTableView(self)
        self._tableView.setModel(self.model)
        # Create progress bar
        self.progBar = QtWidgets.QProgressBar(self)
        self.progBar.setMinimum(0)
        self.progBar.setMaximum(100)
        self.progBar.setValue(0)

        # Define layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self._tableView, 0, 0)
        grid.addWidget(self.progBar, 1, 0)
        self.setLayout(grid)
        self.setContentsMargins(0, 0, 0, 0)

        # Connect the update progress signal from the model
        self.model.updateProgress.connect(self.updateProgress)

    def appendFile(self, file):
        """
        Append a file to the widget

        @param[in] file: the file path to append
        """
        self.model.appendFile(file)

    def updateProgress(self, prog):
        """
        Update the progress bar

        @param prog: The value to update
        """
        logging.debug("Update progress: {}%".format(prog))
        self.progBar.setValue(prog)

if __name__ == '__main__':
    import sys
    from random import Random
    from PyQt5.QtCore import QTimer

    # LoggingTools.initLogger(logging.INFO)
    LoggingTools.initLogger(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Create the directory widget
    transcWidget = TranscoderMgrWidget()

    # Create random number generator
    randGen = Random()

    # Set number of row in the _tableView
    rows = 120

    # Fill _tableView with random numbers
    for i in range(rows):
        num = randGen.randint(0, 999999999)
        transcWidget.appendFile(num)

    # Show the widget
    transcWidget.setGeometry(500, 100, 600, 600)
    transcWidget.show()
    transcWidget.raise_()

    # Randomly change status
    timer = QTimer()
    for i in range(rows*2):
        row = randGen.randint(0, rows - 1)
        transcWidget.model.DEBUGsetStatus(row, 'Done')

    sys.exit(app.exec_())
