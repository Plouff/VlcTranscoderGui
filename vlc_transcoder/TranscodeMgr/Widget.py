#! python3
# -*-coding: utf-8 -*-

"""
@file TModel.py
The model for the transcoding status table
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
        # Create table view
        self.table = QtWidgets.QTableView(self)
        self.table.setModel(self.model)
        # Create progress bar
        self.progBar = QtWidgets.QProgressBar(self)

        # Define layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.table, 0, 0)
        grid.addWidget(self.progBar, 1, 0)
        self.setLayout(grid)

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
        self.progBar.setValue(prog)

if __name__ == '__main__':
    import sys
    from random import Random

    LoggingTools.initLogger(logging.INFO)
    # LoggingTools.initLogger(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Create the directory widget
    transcWidget = TranscoderMgrWidget()

    randGen = Random()

    for i in range(30):
        num = randGen.randint(0, 999999999)
        transcWidget.appendFile(num)

    # Show the widget
    transcWidget.setGeometry(500, 100, 600, 600)
    transcWidget.show()
    transcWidget.raise_()
    sys.exit(app.exec_())
