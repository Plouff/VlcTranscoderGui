#! python3
#-*-coding: utf-8 -*-

"""
@file InputFilesTab.py
The Input files Tab of the GUI
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from NzPyQtToolbox import NzQWidgets
import pprint


class InputFilesTab(QtWidgets.QWidget):
    """
    This tab contains a file browser to select files to transcode
    """
    def __init__(self, parent):
        """
        The constructor for the Configuration tab of the GUI

        @param parent QtWidgets.QWidget: The parent widget
        """
        super().__init__(parent)
        self.parent = parent

        grid = QtWidgets.QGridLayout()
        cRow=0

        addRootDirLabel=QtWidgets.QLabel('Add root directory', self.parent)
        addRootDirBut=QtWidgets.QToolButton(self.parent)
        addRootDirBut.setText('...')

        grid.addWidget(addRootDirLabel, 0, 1)
        grid.addWidget(addRootDirBut, 0, 2)

        addRootDirBut.pressed.connect(self.openFileBrowser)

        # set Layout
        self.setLayout(grid)


    def openFileBrowser(self):
        rootdir = QtWidgets.QFileDialog.getExistingDirectory(self,
                    'Root directory', '/', QtWidgets.QFileDialog.ShowDirsOnly |
                    QtWidgets.QFileDialog.DontResolveSymlinks)

        if rootdir:
            controller = self.getController()
            controller.addRootDirectory(rootdir)
            pprint.pprint(controller.model.rootDirList)

    def getController(self):
        return self.parent.getController()

