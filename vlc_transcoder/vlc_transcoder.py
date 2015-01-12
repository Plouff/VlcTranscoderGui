#! python3
# -*-coding: utf-8 -*-

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
import settings
from NzPyQtToolBox.EasterEgg import EasterEgg

# Import standard modules
import logging


"""
Script wrapper
"""
if __name__ == '__main__':
    import sys

    # Configure logger
#     LoggingTools.initLogger(logging.DEBUG)
    LoggingTools.initLogger(logging.INFO)

    # Demo mode
    settings.demoMode = False

    # Create the app
    app = QtWidgets.QApplication(sys.argv)

    # Plug easter egg
    easterEgg = EasterEgg(app, "demo", settings.toggleDemo)
    logging.debug(str(easterEgg))

    # Create the main view
    view = MainView()
    # Create the main model
    model = MainModel()
    # Create the main controller
    controller = MainController(model, view)

    # Initialize the GUI
    controller.initGUI()

    sys.exit(app.exec_())
