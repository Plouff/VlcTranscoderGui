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
from NzPyQtToolbox.DirectoryManagerWidget.DirectoryManagerWidget import DirectoryManagerWidget
from NzPyQtToolbox.DirectoryManagerWidget.DirectoryManagerTableModel import DirectoryManagerTableModel
from NzPyQtToolbox.DirectoryManagerWidget.DirectoryManagerTableDelegate import DirectoryManagerTableDelegate
from TranscoderDirMgrTableModel import TranscoderDirMgrTableModel
from NzPyQtToolbox.DebugTrace import qtDebugTrace
from NzToolBox.WholeToolBox import *

# Import custom modules

# Import standard modules
import sys
import logging
import LoggingTools
from pprint import pprint


class TranscoderDirMgrWidget(DirectoryManagerWidget):
    """
    The transcoder directory manager widget.
    It enables to add directories to be scanned for video files. It displays
    the status of the search and the number of video files found.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def DirectoryAddedProcessing(self, dir):
        """
        Define the processing of each new directory added
        """
        logging.info('Subprocess launched with directory: {}'.format(dir))
        # Set status "Scanning"
        self._model.setScanningStatus(dir)

        # Get a generator to look for files
        files = findFiles(dir, ['*.log'])
        count = 0
        for f in files:
            # Find next file
            logging.debug(f)
            count += 1
            # Update the model
            self._model.updateFileCount(dir, count)

        # Set status "Scanned"
        self._model.setScannedStatus(dir)

if __name__ == '__main__':
    LoggingTools.initLogger(logging.INFO)
    #LoggingTools.initLogger(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Create the directory widget
    dirWidget = TranscoderDirMgrWidget()

    # Create and set model to the widget and its table view
    additionnalHeaders = ["Status", "Files"]
    model = TranscoderDirMgrTableModel(
        dirWidget.getTableView(), additionnalHeaders)
    dirWidget.setModelToView(model)

    # Create and set delegate to the widget
    delegate = DirectoryManagerTableDelegate(dirWidget)
    dirWidget.setItemDelegate(delegate)

    # Show the widget
    dirWidget.setGeometry(900, 100, 600, 600)
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
