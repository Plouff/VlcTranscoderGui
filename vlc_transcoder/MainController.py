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
        self.model = model
        self.view = view

        # Register the controller in the model and the view
        self.model.controller = self
        self.view.controller = self

        # Create dedicated controllers
        self.confTabCtrl = ConfTabCtrl(model, view.confTab)
        self.inputTabCtrl = InputTabCtrl(model, view.inputTab)
        self.transcodeTabCtrl = TranscodeTabCtrl(model, view.transcodeTab)
        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(3)

        # Connect signals
        self.view.updateFiles.connect(self.updateFiles2Transcode)
        self.view.launchTranscoding.connect(self.launchTranscoding)

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

    def processDirectory(self, dirpath):
        """
        Define the processing for new directories

        @param[in] dirpath The directory just added by the user
        """
        # Get the list of extensions
        extSelected = self.view.getSelectedExtensions()

        # Create a directory worker
        dirrunnable = DirRunnable(dirpath, extSelected, self.model.dirMgrModel)

        # Set waiting status
        self.model.dirMgrModel.setStatus(dirpath, "Waiting")

        # Send worker to thread pool
        self.pool.start(dirrunnable)

    def raiseThreadError(self, msg):
        raise RuntimeError("Thread Error: {}".format(msg))

    def updateFiles2Transcode(self, transcModel):
        """
        Update the list of files of the transcoding tab

        @param transcModel: The model of the transcoding table view
        """
        files = self.inputTabCtrl.getFilesFromInputTab()
        transcModel.setFiles(files)

    def launchTranscoding(self, model):
        """
        Launch the transcoders in different threads

        @param model: The model of the transcoding table view
        """
        # Get config
        config = self.view.getConfig()

        # Create a transcoder worker
        for row in model.filesdata:
            col = model.getColumnByHeader('File')
            file = row[col]
            transcoder = Transcoder(file, model, config)
            # Send worker to thread pool
            self.pool.start(transcoder)
