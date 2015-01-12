#! python3
# -*-coding: utf-8 -*-

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
import subprocess
from subprocess import CalledProcessError
import tempfile
import os
import shutil


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

    def __init__(self, file, model, config):
        """
        The class constructor
        """
        super().__init__()
        self.file = file
        self.model = model
        self.config = config
        self.signal = TranscoderSignals()

        # Connect signals
        self.signal.updateStatus.connect(self.model.setStatus)
        self.signal.updateError.connect(self.model.setError)

    def __repr__(self):
        msg = "{}@{}(file={}, config={}".format(
            self.__class__.__name__, hex(id(self)), self.file, self.config)
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
            if settings.GlobalVars.demoMode:
                self.demo()
            else:
                self.launchTranscoder()

        except Exception as e:
            # Set status "Error"
            self.signal.updateStatus.emit(self.file, "Error")
            self.signal.updateError.emit(self.file, str(e))
            raise e

        # Set status "Scanned"
        self.signal.updateStatus.emit(self.file, "Transcoded")

        logging.info('End of transcoding of "{}"'.format(self.file))

    def getVlcErrorMsg(self, e):
        """
        Get a formatted VLC error given @c CalledProcessError from a VLC
         execution

        @param e: a @c CalledProcessError exception
        """
        if e.returncode == 1:
            vlcerror = 'Unspecified error (code 1) {}'.format(e.output)
        elif e.returncode == 2:
            vlcerror = 'Not enough memory (code 2) {}'.format(e.output)
        elif e.returncode == 3:
            vlcerror = 'Timeout (code 3) {}'.format(e.output)
        elif e.returncode == 4:
            vlcerror = 'Module not found (code 4) {}'.format(e.output)
        elif e.returncode == 5:
            vlcerror = 'Object not found (code 5) {}'.format(e.output)
        elif e.returncode == 6:
            vlcerror = 'Variable not found (code 6) {}'.format(e.output)
        elif e.returncode == 7:
            vlcerror = 'Bad variable value (code 7) {}'.format(e.output)
        elif e.returncode == 8:
            vlcerror = 'Item not found (code 8) {}'.format(e.output)
        else:
            vlcerror = "Unkown Error (code {}), desc.: {}".format(
                e.returncode, e.output)
        return vlcerror

    def launchTranscoder(self):
        cfg = self.config
        vlcpath = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"

        # Create temporary file path
        tmpoutfile = tempfile.NamedTemporaryFile()
        tmpoutfilename = tmpoutfile.name
        tmpoutfile.close()

        # Create command line argument for vlc
        args = (r'-I dummy -vvv FILE ' +
                '--sout=#transcode{{vcodec={},vb={},height={},'.format(
                    cfg.vcodec, cfg.vbitrate, cfg.height) +
                'acodec={},ab={},channels={}}}'.format(
                    cfg.acodec, cfg.abitrate, cfg.achannels, cfg.asamplerate) +
                ':std{{access=file,mux={},dst="{}"'.format(
                    cfg.encaps, tmpoutfilename)
                )
        if cfg.deinterlace:
            args = args + r',deinterlace} vlc://quit'
        else:
            args = args + r"} vlc://quit"
            # args = args + r'}'

        # Debug print
        logging.debug("vlc " + args)

        argslist = args.split(' ')

        # Since the file may contain space characters we need to add it after
        # the split of the command line
        argslist[argslist.index('FILE')] = self.file

        # Create final command
        cmd = [vlcpath] + argslist

        try:
            logging.info(cmd)
            subprocess.check_call(cmd)
            outputfile = self.createOutputFilename(self.file)

        except CalledProcessError as e:
            vlcerror = self.getVlcErrorMsg(e)

            msg = "Failed to transcode file: '{}'. ".format(self.file)
            msg = msg + "VLC returned error: {}".format(vlcerror)
            raise RuntimeError(msg)
            raise e
        except FileNotFoundError as e:
            raise RuntimeError("Couldn't find command '{}'".format(cmd[0]))
            raise e

        shutil.move(tmpoutfilename, outputfile)

        # vlcpath -I dummy -vvv "%%i" --sout=#transcode{vcodec=%vcodec%,
        # vb=%vb%,height=%height%,acodec=%acodec%,ab=%ab%,channels=2,
        # samplerate=%samplerate%}:std{access=file,mux=%mux%,dst=!temp_out!}
        # vlc://quit

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
                time.sleep(3)

    def createOutputFilename(self, file, suffix='_transcoded'):
        """
        Create a file name with a give suffix

        @param file: The file to suffix
        @param suffix: The suffix to apply (default: '_transcoded'

        @return: A file path with the given suffix
        """
        split = os.path.splitext(file)
        return split[0] + suffix + '.' + self.config.encaps

if __name__ == '__main__':
    pass
