#! python3
#-*-coding: utf-8 -*-

"""
@file InputFilesTab.py
The Input files Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import custom modules
#from NzPyQtToolbox import NzQWidgets
from NzPyQtToolbox.NzQAutoGridWidgets import NzQAutoGridCheckboxes
from TranscoderDirMgrWidget import TranscoderDirMgrWidget
from TranscoderDirMgrTableModel import TranscoderDirMgrTableModel
from NzPyQtToolbox.DirectoryManagerWidget.DirectoryManagerTableDelegate \
    import DirectoryManagerTableDelegate

# Import standard modules
import pprint


class InputFilesTab(QtWidgets.QWidget):
    """
    This tab contains a file browser to select files to transcode
    """
    def __init__(self, parent):
        """
        The constructor for the Configuration tab of the GUI

        @param parent The parent widget
        """
        super().__init__(parent)
        self.parent = parent

        # Get the general model of the app
        try:
            self.model = self.parent.controller.model
        except AttributeError as e:
            raise RuntimeError("model is not set properly")
        if self.model is None:
            raise RuntimeError("model is not set properly")

        # Create the directory manager widget
        extmgr = self.initExtMgr()

        # Create the extensions manager widget
        dirmgr = self.initDirMgr()

        # Create the grid
        grid = QtWidgets.QGridLayout()

        # Add the video file extensions for the search
        # Add widgets to the grid
        grid.addWidget(extmgr, 0, 0)
        grid.addWidget(dirmgr, 1, 0)

        self.setLayout(grid)

    def initExtMgr(self):
        extensions = self.model.videoFilexExt
        extmgr = NzQAutoGridCheckboxes(extensions, maxColumnCount=8,
                                       parent=self)
        return extmgr

    def initDirMgr(self):
        # Create the directory widget
        dirWidget = TranscoderDirMgrWidget()

        # Create and set model to the widget and its table view
        additionnalHeaders = ["Status", "Files"]
        self.dirMgrModel = TranscoderDirMgrTableModel(
            dirWidget.getTableView(), additionnalHeaders)
        dirWidget.setModelToView(self.dirMgrModel)

        # Create and set delegate to the widget
        self.delegate = DirectoryManagerTableDelegate(dirWidget)
        dirWidget.setItemDelegate(self.delegate)

        return dirWidget
