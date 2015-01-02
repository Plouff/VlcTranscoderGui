#! python3
#-*-coding: utf-8 -*-

"""
@file vlc_transcoder.py
VLC Transcoder GUI

A GUI to transcode videos with VLC

author: Nassim Zga
created: 20/10/14
"""

# Import PyQt modules
from PyQt5 import QtWidgets

# Import custom modules
from MainView import MainView
from MainModel import MainModel
from MainController import MainController
from NzToolBox import LoggingTools

# Import standard modules
import logging

"""
Script wrapper
"""
if __name__ == '__main__':
    import sys

    # Configure logger
    # LoggingTools.initLogger(logging.DEBUG)
    LoggingTools.initLogger(logging.INFO)

    # Create the app
    app = QtWidgets.QApplication(sys.argv)

    # Create the main view
    view = MainView()
    # Create the main model
    model = MainModel()
    # Create the main controller
    controller = MainController(model, view)

    # Initialize the GUI
    controller.initGUI()

    sys.exit(app.exec_())


# vlc -vvv input_stream --sout
# #transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}: CALL
# "C:\Program Files\VideoLAN\VLC\vlc" -I dummy -vvv %1
#--sout=#transcode{acodec="mpga",ab="512",channels="2",samplerate="44100"}: \
#    standard{access="file",mux="mpeg1",dst="%_commanm%.mp3"}
#vlc://quit
