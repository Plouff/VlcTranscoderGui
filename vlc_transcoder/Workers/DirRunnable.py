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


class DirRunnable(QtCore.QRunnable):
    """
    The worker for the threaded management of directories
    """
    errorStr = pyqtSignal(str)

    def __init__(self, rootDir, extensions, dirMgrModel):
        """
        docstring for __init__
        """
        self.rootDir = rootDir
        self.extensions = extensions
        self.dirMgrModel = dirMgrModel
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
        self.dirMgrModel.setStatus(self.rootDir, "Scanning")
        self.dirMgrModel.setExtensions(self.rootDir, self.extensions.copy())

        try:
            # Get a generator to look for files
            files = findFilesbyExtension(self.rootDir, self.extensions)
            #files = findFilesbyExtension(self.rootDir, ['*.log'])
            self.dirMgrModel.setFileCount(self.rootDir, 0)
            for count, f in enumerate(files):
                # Find next file
                logging.debug("File found: {}".format(f))
                # Update the model
                self.dirMgrModel.setFileCount(self.rootDir, count + 1)
                self.dirMgrModel.appendFile(self.rootDir, f)
        except Exception as e:
            # Set status "Scan Error"
            self.dirMgrModel.setStatus(self.rootDir, "Scan Error")
            self.dirMgrModel.setError(self.rootDir, str(e))
            #self.errorStr.emit(str(e))
            raise e

        # Set status "Scanned"
        self.dirMgrModel.setStatus(self.rootDir, "Scanned")

        logging.info(
            'End of threaded processing of "{}"'.format(self.rootDir))


    def printFinished(self):
        """
        To debug events
        """
        logging.debug("Worker {} sent 'finished' signal".format(str(self)))
