#! python3
#-*-coding: utf-8 -*-

"""
@file Threading.py
Simple multi threading management in Qt from:
    https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
"""


# Import PyQt modules
from PyQt5 import QtCore

# Import custom modules
# Import standard modules
from abc import ABCMeta, abstractmethod
import logging


class Worker(QtCore.QObject):
    """
    A worker class to be sent to a dedicated thread.
    """
    # Declare class as abstract
    __metaclass__ = ABCMeta

    finished = QtCore.pyqtSignal()
    errorStr = QtCore.pyqtSignal(str)
    updatedStr = QtCore.pyqtSignal(str)
    updatedInt = QtCore.pyqtSignal(int)
    updatedInt = QtCore.pyqtSignal(int)

    @abstractmethod
    def __repr__(self):
        msg = "{}@{}".format(
            self.__class__.__name__, hex(id(self)),
        )
        return msg

    @abstractmethod
    def process(self):
        """
        The processing method of the worker
        """
        self.finished.emit()


def sendWorkerOnThread(worker, thread, errStrHandler=None):
    """
    Used to send a given work on a given thread

    @param[in] worker a @c Worker object that implement the @c process method
    @param[in] thread a @c QThread object to receive the worker
    @param[in] errStrHandler a @c method to receive error messages from the thread
    """
    # Set worker thread
    worker.moveToThread(thread)

    # Connect error to the error handling function
    if errStrHandler:
        worker.errorStr.connect(errStrHandler)

    # Connect
    thread.started.connect(worker.process)
    #worker.finished.connect(worker.deleteLater)
    worker.finished.connect(worker.printFinished)
    #worker.finished.connect(thread.quit)
    #worker.finished.connect(thread.quit)
    #thread.finished.connect(thread.deleteLater)
    thread.finished.connect(printFinished)

    # Start
    thread.start()
    logging.debug("Thread starting with worker {}".format(worker))

def printFinished():
    logging.debug("Thread sent finished")

