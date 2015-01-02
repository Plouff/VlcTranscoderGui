#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderRunnable.py
The worker for transcoding
"""

# Import PyQt modules
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

# Import custom modules
import settings

# Import standard modules
import logging


class TranscoderSignals(QtCore.QObject):
    """
    Signals for the transcoder
    """
    updateStatus = pyqtSignal(str, str)
    updateError = pyqtSignal(str, str)


class Transcoder(QtCore.QRunnable):
    """
    A worker to transcode videos
    """

    def __init__(self, file, model):
        """
        The class constructor
        """
        super().__init__()
        self.file = file
        self.model = model
        self.signal = TranscoderSignals()

        # Connect signals
        self.signal.updateStatus.connect(self.model.setStatus)
        self.signal.updateError.connect(self.model.setError)

    def __repr__(self):
        msg = "{}(@{}: file={}".format(
            self.__class__.__name__, hex(id(self)), self.file)
        return msg

    def run(self):
        """
        Specific implementation of the process function
        """
        logging.info(
            'Starting trancoding of file "{}"'.format(self.file))

        # Set status "Transcoding"
        self.signal.updateStatus.emit(self.file, "Transcoding")

        try:
            if settings.demoMode:
                self.demo()

        except Exception as e:
            # Set status "Error"
            self.signal.updateStatus.emit(self.file, "Error")
            self.signal.updateError.emit(self.file, str(e))
            raise e

        # Set status "Scanned"
        self.signal.updateStatus.emit(self.file, "Transcoded")

        logging.info('End of transcoding of "{}"'.format(self.file))

    def demo(self):
            import random
            import time
            print("transcoding...")

            rand = random.Random()
            num = rand.randint(0, 4)
            if num == 0:
                1 / 0
            elif num == 1:
                illegal = num.thisIsABug
            else:
                time.sleep(5)
