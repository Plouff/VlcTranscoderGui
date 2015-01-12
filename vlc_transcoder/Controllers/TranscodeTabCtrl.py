#! python3
#-*-coding: utf-8 -*-

"""
@file TranscodeTabCtrl
The Controller for the transcode tab
"""

# Import PyQt modules
from PyQt5 import QtCore
# Import custom modules
# Import standard modules


class TranscodeTabCtrl(QtCore.QObject):
    """
    The controller for the transcode tab
    """
    def __init__(self, model, view):
        """
        The class constructor

        @param model the model of the MVC GUI
        @param view the view of the MVC GUI
        """
        # TODO: put transcoding stuff from the main controller here

        # Save pointers to model and view
        self.model = model
        self.view = view
