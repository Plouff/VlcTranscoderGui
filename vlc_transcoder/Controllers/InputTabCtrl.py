#! python3
#-*-coding: utf-8 -*-

"""
@file InputTabCtrl.py
The Controller for the input files tab
"""

# Import PyQt modules
from PyQt5 import QtCore

# Import custom modules
from NzPyQtToolBox.NzToolTipList import \
    TooltipedDataListModel as TooltipListModel
from NzPyQtToolBox.DebugTrace import qtDebugTrace
from DirMgr.TModel import TranscoderDirMgrTableModel
from NzPyQtToolBox.DirMgr.TDelegate import DirectoryManagerTableDelegate

# Import standard modules


class InputTabCtrl():
    """
    The controller for the input tab widgets
    """
    def __init__(self, model, view):
        """
        The class constructor

        @param model the model of the MVC GUI
        @param view the tab for the controller
        """
        # Save pointers to model and view
        self.model = model
        self.view = view

    def connectModelAndView(self):
        """
        Create models and connect them to the different views.
        """
        # Get file extensions
        extensions = self.model.videoFilexExt
        # Create files extensions checkboxes
        self.view.extmgr.createCheckboxes(extensions, maxColumnCount=8)
        self.buildDirMgr(self.view.dirmgr)

    def buildDirMgr(self, dirMgr):
        """
        Build the Directory Manager Widget
        """
        # Create and set model to the widget and its table view
        additionnalHeaders = ["Status", "Extensions", "File count", "Files",
                              "Error"]
        self.model.dirMgrModel = TranscoderDirMgrTableModel(
            dirMgr.getTableView(), additionnalHeaders)
        dirMgr.setModelToView(self.model.dirMgrModel)

        # Create and set delegate to the widget
        self.delegate = DirectoryManagerTableDelegate(dirMgr)
        dirMgr.setItemDelegate(self.delegate)
