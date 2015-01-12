#! python3
#-*-coding: utf-8 -*-

"""
@file MainController.py
The Controller for the transcoder
"""

# Import PyQt modules
from PyQt5 import QtCore


# Import custom modules
from Controllers.ConfTabCtrl import ConfTabCtrl
from Controllers.InputTabCtrl import InputTabCtrl
from Controllers.TranscodeTabCtrl import TranscodeTabCtrl
from Workers.DirRunnable import DirRunnable
from Workers.TranscoderRunnable import Transcoder


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
        self._model = model
        self._view = view

        # Register the controller in the model and the view
        self._model.controller = self
        self._view.controller = self

        # Create dedicated controllers
        self._confTabCtrl = ConfTabCtrl(model, view.confTab)
        self._inputTabCtrl = InputTabCtrl(model, view.inputTab)
        self._transcodeTabCtrl = TranscodeTabCtrl(model, view.transcodeTab)
        self._pool = QtCore.QThreadPool()
        self._pool.setMaxThreadCount(3)

        # Connect signals
        self._view.updateFiles.connect(self.updateFiles2Transcode)
        self._view.launchTranscoding.connect(self.launchTranscoding)

    def initGUI(self):
        """
        Initialaze the whole GUI
        """
        # Connect models to views
        self.connectModelAndView()
        # Show GUI
        self._view.show()

    def addRootDirectory(self, rootDir):
        """
        Append a root directory to the list of root directories in the Model
        """
        self._model.addRootDirectory(rootDir)

    def connectModelAndView(self):
        """
        Create models and connect them to the different views
        """
        self._confTabCtrl.connectModelAndView()
        self._inputTabCtrl.connectModelAndView()

    def processDirectory(self, dirpath):
        """
        Define the processing for new directories

        @param[in] dirpath The directory just added by the user
        """
        # Get the list of extensions
        extSelected = self._view.getSelectedExtensions()

        # Create a directory worker
        dirrunnable = DirRunnable(dirpath, extSelected, self._model.dirMgrModel)

        # Set waiting status
        self._model.dirMgrModel.setStatus(dirpath, "Waiting")

        # Send worker to thread pool
        self._pool.start(dirrunnable)

    def raiseThreadError(self, msg):
        raise RuntimeError("Thread Error: {}".format(msg))

    def updateFiles2Transcode(self, transcModel):
        """
        Update the list of files of the transcoding tab

        @param transcModel: The model of the transcoding table view
        """
        files = self._inputTabCtrl.getFilesFromInputTab()
        transcModel.setFiles(files)

    def launchTranscoding(self, model):
        """
        Launch the transcoders in different threads

        @param model: The model of the transcoding table view
        """
        # Get config
        config = self._view.getConfig()

        # Create a transcoder worker
        for row in model.filesdata:
            col = model.getColumnByHeader('File')
            file = row[col]
            transcoder = Transcoder(file, model, config)
            # Send worker to thread pool
            self._pool.start(transcoder)
