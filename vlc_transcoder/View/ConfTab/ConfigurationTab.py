#! python3
#-*-coding: utf-8 -*-

"""
@file ConfigurationTab.py
The Configuration Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import custom modules
from NzPyQtToolbox import NzQWidgets

# Import standard modules


class ConfigurationTab(QtWidgets.QWidget):
    """
    This tab holds the settings for the transcoding
    """
    def __init__(self, parent=None):
        """
        The constructor for the Configuration tab of the GUI

        @param parent The parent widget
        """
        super().__init__(parent)
        self.parent = parent

        grid = QtWidgets.QGridLayout()
        cRow = 0
        # Encapsulation
        encapsLabel = QtWidgets.QLabel("Encapsulation:")
        parent.encapsCombo = QtWidgets.QComboBox(self)
        grid.addWidget(encapsLabel, cRow, 0)
        grid.addWidget(parent.encapsCombo, cRow, 1)

        # Change current row
        cRow += 1

        # Add video configuration widgets
        cRow = self.createVideoWidgets(grid, cRow)

        # Change current row
        cRow += 1

        # Add audio configuration widgets
        cRow = self.createAudioWidgets(grid, cRow)

        # Change current row
        cRow += 1

        # Add general configuration widgets
        cRow = self.createGeneralAspectWidgets(grid, cRow)

        # Change current row
        cRow += 1

        # Deinterlace
        deinterlaceCheckB = QtWidgets.QCheckBox("Deinterlace")
        grid.addWidget(deinterlaceCheckB, cRow, 0)

        # set Layout
        self.setLayout(grid)

    def createVideoWidgets(self, grid, cRow):
        """
        Adds widgets for audio configuration

        @param grid QGridLayout: The current grid layout widget
        @param cRow int: The current line number in the grid

        @return cRow int: The final row index after the widgets were created
        """
        # Video Codec
        vCodecLabel = QtWidgets.QLabel("Video Codec:")
        self.parent.vCodecCombo = QtWidgets.QComboBox(self)

        grid.addWidget(vCodecLabel, cRow, 0)
        grid.addWidget(self.parent.vCodecCombo, cRow, 1)

        # Bit rate
        vBitRateLabel = QtWidgets.QLabel("Bit rate:")
        autoBitRateDisCkBox = NzQWidgets.NzQDisablingCheckBox(text='Auto',
                                                              parent=self)
        autoBitRateDisCkBox.setChecked(True)

        vBitRateSpin = QtWidgets.QSpinBox(self)
        autoBitRateDisCkBox.addSlaveWidget(vBitRateSpin,
                                           isEnabledWhenMasterIsEnabled=False)

        # Add widgets
        grid.addWidget(vBitRateLabel, cRow, 3)
        grid.addWidget(autoBitRateDisCkBox, cRow, 4)
        grid.addWidget(vBitRateSpin, cRow, 5)

        return cRow

    def createAudioWidgets(self, grid, cRow):
        """
        Adds widgets for video configuration

        @param grid QGridLayout: The current grid layout widget
        @param cRow int: The current line number in the grid

        @return cRow int: The final row index after the widgets were created
        """

        # Audio Codec
        aCodecLabel = QtWidgets.QLabel("Audio Codec:")
        self.parent.aCodecCombo = QtWidgets.QComboBox(self)

        grid.addWidget(aCodecLabel, cRow, 0)
        grid.addWidget(self.parent.aCodecCombo, cRow, 1)

        # Audio bitrate
        aBitRateLabel = QtWidgets.QLabel("Audio bit rate:")
        self.parent.aBitRateCombo = QtWidgets.QComboBox(self)

        grid.addWidget(aBitRateLabel, cRow, 2)
        grid.addWidget(self.parent.aBitRateCombo, cRow, 3)

        # Channels
        aChannelsLabel = QtWidgets.QLabel("Channels:")
        aChannelsSpin = QtWidgets.QSpinBox(self)
        aChannelsSpin.setValue(2)

        grid.addWidget(aChannelsLabel, cRow, 4)
        grid.addWidget(aChannelsSpin, cRow, 5)

        # Sample rate
        aSampleRateLabel = QtWidgets.QLabel("Sample rate")
        self.parent.aSampleRateCombo = QtWidgets.QComboBox(self)

        grid.addWidget(aSampleRateLabel, cRow, 6)
        grid.addWidget(self.parent.aSampleRateCombo, cRow, 7)

        return cRow

    def createGeneralAspectWidgets(self, grid, cRow):
        """
        Adds widgets for general aspect configuration

        @param grid QGridLayout: The current grid layout widget
        @param cRow int: The current line number in the grid

        @return cRow int: The final row index after the widgets were created
        """
        resizeDisCheckB = NzQWidgets.NzQDisablingCheckBox(
            text="Resize", parent=self)
        grid.addWidget(resizeDisCheckB, cRow, 0)

        # Resize by standard resolution
        byStdResolDisRadio = NzQWidgets.NzQDisablingRadioButton(
            text="Std Resolution", parent=self, isInMutexGroup=True)
        self.parent.byStdResolCombo = QtWidgets.QComboBox(self)
        byStdResolDisRadio.setChecked(True)

        grid.addWidget(byStdResolDisRadio, cRow, 1)
        grid.addWidget(self.parent.byStdResolCombo, cRow, 2)

        cRow += 1
        # Resize by Height
        byHeightDisRadio = NzQWidgets.NzQDisablingRadioButton(
            text="Height", parent=self, isInMutexGroup=True)
        self.parent.byHeightCombo = QtWidgets.QComboBox(self)

        customHeightDisCheckB = NzQWidgets.NzQDisablingCheckBox(
            text="Custom", parent=self)
        customHeightLineEd = QtWidgets.QLineEdit(self)
        customHeightDisCheckB.addSlaveWidget(customHeightLineEd)
        customHeightDisCheckB.addSlaveWidget(self.parent.byHeightCombo, False)

        grid.addWidget(byHeightDisRadio, cRow, 1)
        grid.addWidget(self.parent.byHeightCombo, cRow, 2)
        grid.addWidget(customHeightDisCheckB, cRow, 3)
        grid.addWidget(customHeightLineEd, cRow, 4)

        cRow += 1
        # Resize by Width
        byWidthDisRadio = NzQWidgets.NzQDisablingRadioButton(
            text="Width", parent=self, isInMutexGroup=True)
        self.parent.byWidthCombo = QtWidgets.QComboBox(self)

        customWidthDisCheckB = NzQWidgets.NzQDisablingCheckBox(
            text="Custom", parent=self)
        customWidthLineEd = QtWidgets.QLineEdit(self)
        customWidthDisCheckB.addSlaveWidget(customWidthLineEd)
        customWidthDisCheckB.addSlaveWidget(self.parent.byWidthCombo, False)

        grid.addWidget(byWidthDisRadio, cRow, 1)
        grid.addWidget(self.parent.byWidthCombo, cRow, 2)
        grid.addWidget(customWidthDisCheckB, cRow, 3)
        grid.addWidget(customWidthLineEd, cRow, 4)

        cRow += 1
        # Resize by Percent
        byPercentDisRadio = NzQWidgets.NzQDisablingRadioButton(
            text="Percent", parent=self, isInMutexGroup=True)

        byPercentSpin = QtWidgets.QSpinBox(self)
        byPercentSpin.setSuffix("%")
        byPercentSpin.setRange(0, 100)
        byPercentSpin.setValue(50)

        grid.addWidget(byPercentDisRadio, cRow, 1)
        grid.addWidget(byPercentSpin, cRow, 2)

        # QButtonGroup for mutually exclusive resize options
        resizeGroup = QtWidgets.QButtonGroup(self)
        resizeGroup.addButton(byStdResolDisRadio)
        resizeGroup.addButton(byHeightDisRadio)
        resizeGroup.addButton(byWidthDisRadio)
        resizeGroup.addButton(byPercentDisRadio)

        # Create disable links for "resize by standard resolution" radio button
        for wdg in (self.parent.byHeightCombo, customHeightDisCheckB,
                    customHeightLineEd, self.parent.byWidthCombo,
                    customWidthDisCheckB, customWidthLineEd, byPercentSpin):
            byStdResolDisRadio.addSlaveWidget(wdg, False)

        byStdResolDisRadio.addSlaveWidget(self.parent.byStdResolCombo)

        # Create disable links for "resize by height" radio button
        for wdg in (self.parent.byWidthCombo, customWidthDisCheckB,
                    customWidthLineEd, byPercentSpin,
                    self.parent.byStdResolCombo):
            byHeightDisRadio.addSlaveWidget(wdg, False)

        for wdg in (self.parent.byHeightCombo, customHeightDisCheckB,
                    customHeightLineEd):
            byHeightDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by width" radio button
        for wdg in (self.parent.byHeightCombo, customHeightDisCheckB,
                    customHeightLineEd, byPercentSpin,
                    self.parent.byStdResolCombo):
            byWidthDisRadio.addSlaveWidget(wdg, False)

        for wdg in (self.parent.byWidthCombo, customWidthDisCheckB,
                    customWidthLineEd):
            byWidthDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by percent" radio button
        for wdg in (self.parent.byHeightCombo, customHeightDisCheckB,
                    customHeightLineEd, self.parent.byWidthCombo,
                    customWidthDisCheckB, customWidthLineEd,
                    self.parent.byStdResolCombo):
            byPercentDisRadio.addSlaveWidget(wdg, False)
        byPercentDisRadio.addSlaveWidget(byPercentSpin)

        # Add slave widget to be disabled by resizeDisCheckB
        for wdg in (byHeightDisRadio, self.parent.byHeightCombo,
                    customHeightDisCheckB, customHeightLineEd, byWidthDisRadio,
                    self.parent.byWidthCombo, customWidthDisCheckB,
                    customWidthLineEd, byPercentDisRadio, byPercentSpin,
                    byStdResolDisRadio, self.parent.byStdResolCombo):
            resizeDisCheckB.addSlaveWidget(wdg)

        resizeGroup.setExclusive(True)

        return cRow
