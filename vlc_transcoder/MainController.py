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

# Import standard modules


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
