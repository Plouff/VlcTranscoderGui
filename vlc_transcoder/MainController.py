#! python3
#-*-coding: utf-8 -*-

"""
@file MainController.py
The Controller for the transcoder
"""

# Import PyQt modules
from PyQt5 import QtCore

# Import custom modules
from NzPyQtToolBox.NzToolTipList import \
    TooltipedDataListModel as TooltipListModel
from Controllers.ConfTabCtrl import ConfTabCtrl
from Controllers.InputTabCtrl import InputTabCtrl

from NzToolBox.WholeToolBox import *
from NzPyQtToolBox.DebugTrace import qtDebugTrace

# Import standard modules
import logging


class MainController():
    """
    This is a the 'Controller' part of the MVC implementation. It deals with
    the communication between the View and the Model
    """
    def __init__(self, model, view):
        """
        The class constructor

        @param model the model of the MVC GUI
        @param view the view of the MVC GUI
        """
        # Save pointers to model and view
        self.model = model
        self.view = view

        # Register the controller in the model and the view
        self.model.controller = self
        self.view.controller = self

        # Create dedicated controllers
        self.confTabCtrl = ConfTabCtrl(model, view.confTab)
        self.inputTabCtrl = InputTabCtrl(model, view.inputTab)

    def initGUI(self):
        """
        Initialaze the whole GUI
        """
        # Connect models to views
        self.connectModelAndView()
        # Show GUI
        self.view.show()

    def addRootDirectory(self, rootDir):
        """
        Append a root directory to the list of root directories in the Model
        """
        self.model.addRootDirectory(rootDir)

    def connectModelAndView(self):
        """
        Create models and connect them to the different views
        """
        self.confTabCtrl.connectModelAndView()
        self.inputTabCtrl.connectModelAndView()

    def processDirectory(self, dir):
        """
        Define the processing for new directories

        @param[in] dir The directory just added by the user
        """
        # Get the list of extensions
        extSelected = self.view.getSelectedExtensions()

        logging.info(
            'looking for files in directory "{}" with extensions {}'.format(
                dir, extSelected))

        # Get a generator to look for files
        files = findFilesbyExtension(dir, extSelected)
        #files = findFilesbyExtension(dir, ['*.log'])
        count = 0

        # Set status "Scanning"
        self.model.dirMgrModel.setStatus(dir, "Scanning")

        try:
            for f in files:
                # Find next file
                logging.debug("File found: {}".format(f))
                count += 1
                # Update the model
                self.model.dirMgrModel.updateFileCount(dir, count)
        except Exception as e:
            # Set status "Scan Error"
            self.model.dirMgrModel.setStatus(dir, "Scan Error")
            raise e

        # Set status "Scanned"
        self.model.dirMgrModel.setStatus(dir, "Scanned")
