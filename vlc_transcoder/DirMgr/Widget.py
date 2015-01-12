#! python3
#-*-coding: utf-8 -*-

"""
@file Widget.py
The Transcoder extension of the Diretory Manager Widget
"""

# Import PyQt
from PyQt5 import QtWidgets

# Import custom PyQt modules
from NzPyQtToolBox.DirMgr.Widget import DirectoryManagerWidget
from NzPyQtToolBox.DirMgr.TDelegate import DirectoryManagerTableDelegate

from DirMgr.TModel import TranscoderDirMgrTableModel

# Import custom modules
import LoggingTools

# Import standard modules
import sys
import logging


class TranscoderDirMgrWidget(DirectoryManagerWidget):
    """
    The transcoder directory manager widget.
    It enables to add directories to be scanned for video files. It displays
    the status of the search and the number of video files found.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent

    def _processNewDirectory(self, dirpath):
        """
        Define the processing of each new directory added

        @param[in] dirpath The directory just added by the user

        @todo Improve this ugly inteface...
        """
        self._parent.processDirectory(dirpath)

    def getFiles(self):
        """
        Get the list of files found diring the processing
        """
        return self.model.getFiles()

if __name__ == '__main__':
    LoggingTools.initLogger(logging.INFO)
    #LoggingTools.initLogger(logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Create the directory widget
    dirWidget = TranscoderDirMgrWidget()

    # Create and set model to the widget and its table view
    additionnalHeaders = ["Status", "Extensions", "File count", "Files",
                          "Error"]
    model = TranscoderDirMgrTableModel(
        dirWidget.tableView, additionnalHeaders)
    dirWidget.setModelToView(model)

    # Create and set delegate to the widget
    delegate = DirectoryManagerTableDelegate(dirWidget)
    dirWidget.setItemDelegate(delegate)

    # Show the widget
    dirWidget.setGeometry(900, 100, 600, 600)
    dirWidget.show()
    dirWidget.raise_()
    sys.exit(app.exec_())
