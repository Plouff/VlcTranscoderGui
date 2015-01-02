#! python3
#-*-coding: utf-8 -*-

"""
@file DirRunner.py
The worker for the threaded management of directories
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

# Import custom modules
from NzToolBox.FindFiles import findFilesbyExtension
from NzPyQtToolBox.DebugTrace import qtDebugTrace

# Import standard modules
import logging

class DirRunnableSignals(QtCore.QObject):
    """
    Signals for the directory worker
    """
    updateStatus = pyqtSignal(str, str)
    updateExt = pyqtSignal(str, list)
    updateCount = pyqtSignal(str, int)
    appendFile = pyqtSignal(str, str)
    updateError = pyqtSignal(str, str)

class DirRunnable(QtCore.QRunnable):
    """
    The worker for the threaded management of directories
    """

    def __init__(self, rootDir, extensions, dirMgrModel):
        """
        docstring for __init__
        """
        self.rootDir = rootDir
        self.extensions = extensions
        self.dirMgrModel = dirMgrModel

        # Connect runner to model
        self.signal = DirRunnableSignals()
        self.signal.updateStatus.connect(self.dirMgrModel.setStatus)
        self.signal.updateExt.connect(self.dirMgrModel.setExtensions)
        self.signal.updateCount.connect(self.dirMgrModel.setFileCount)
        self.signal.appendFile.connect(self.dirMgrModel.appendFile)
        self.signal.updateError.connect(self.dirMgrModel.setError)

        super().__init__()

    def __repr__(self):
        msg = "{}(@{}: dir={}, ext={})".format(
            self.__class__.__name__, hex(id(self)), self.rootDir,
            str(self.extensions)
        )
        return msg

    def run(self):
        """
        Specific implementation of the process function
        """
        #qtDebugTrace()
        logging.info(
            'looking for files in directory "{}" with extensions {}'.format(
                self.rootDir, self.extensions))

        # Set status "Scanning"
        self.signal.updateStatus.emit(self.rootDir, "Scanning")
        self.signal.updateExt.emit(self.rootDir, self.extensions.copy())

        try:
            # Get a generator to look for files
            files = findFilesbyExtension(self.rootDir, self.extensions)
            #files = findFilesbyExtension(self.rootDir, ['*.log'])
            self.signal.updateCount.emit(self.rootDir, 0)
            for count, f in enumerate(files):
                # Find next file
                logging.debug("File found: {}".format(f))
                # Update the model
                self.signal.updateCount.emit(self.rootDir, count + 1)
                self.signal.appendFile.emit(self.rootDir, f)
        except Exception as e:
            # Set status "Scan Error"
            self.signal.updateStatus.emit(self.rootDir, "Scan Error")
            self.signal.updateError.emit(self.rootDir, str(e))
            raise e

        # Set status "Scanned"
        self.signal.updateStatus.emit(self.rootDir, "Scanned")

        logging.info(
            'End of processing of "{}"'.format(self.rootDir))
