#! python3
# -*-coding: utf-8 -*-

"""
@file ConfigurationTab.py
The Configuration Tab of the GUI
"""

# Import PyQt modules
from PyQt5 import QtWidgets
from PyQt5 import Qt

# Import custom modules
from NzPyQtToolBox.NzQDisablingWidgets import NzQDisablingCheckBox
from NzPyQtToolBox.NzQDisablingWidgets import NzQDisablingRadioButton 
from Controllers.TranscodingConfig import TranscodingConfig

# Import standard modules
import re


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

        grid = QtWidgets.QGridLayout()
        cRow = 0
        # Encapsulation
        encapsLabel = QtWidgets.QLabel("Encapsulation:")
        self.encapsCombo = QtWidgets.QComboBox(self)
        grid.addWidget(encapsLabel, cRow, 0)
        grid.addWidget(self.encapsCombo, cRow, 1)

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
        self.deinterlaceCheckB = QtWidgets.QCheckBox("Deinterlace")
        grid.addWidget(self.deinterlaceCheckB, cRow, 0)

        # set Layout
        self.setLayout(grid)

    def __repr__(self):
        config = self.getConfig()
        return str(config)

    def createVideoWidgets(self, grid, cRow):
        """
        Adds widgets for audio configuration

        @param grid QGridLayout: The current grid layout widget
        @param cRow int: The current line number in the grid

        @return cRow int: The final row index after the widgets were created
        """
        # Video Codec
        vCodecLabel = QtWidgets.QLabel("Video Codec:")
        self.vCodecCombo = QtWidgets.QComboBox(self)

        grid.addWidget(vCodecLabel, cRow, 0)
        grid.addWidget(self.vCodecCombo, cRow, 1)

        # Bit rate
        vBitRateLabel = QtWidgets.QLabel("Bit rate:")
        self.autoBitRateDisCkBox = NzQDisablingCheckBox(
            text='Auto', parent=self)
        self.autoBitRateDisCkBox.setChecked(True)

        self.vBitRateSpin = QtWidgets.QSpinBox(self)
        self.autoBitRateDisCkBox.addSlaveWidget(
            self.vBitRateSpin, isEnabledWhenMasterIsEnabled=False)

        # Add widgets
        grid.addWidget(vBitRateLabel, cRow, 3)
        grid.addWidget(self.autoBitRateDisCkBox, cRow, 4)
        grid.addWidget(self.vBitRateSpin, cRow, 5)

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
        self.aCodecCombo = QtWidgets.QComboBox(self)

        grid.addWidget(aCodecLabel, cRow, 0)
        grid.addWidget(self.aCodecCombo, cRow, 1)

        # Audio bitrate
        aBitRateLabel = QtWidgets.QLabel("Audio bit rate:")
        self.aBitRateCombo = QtWidgets.QComboBox(self)

        grid.addWidget(aBitRateLabel, cRow, 2)
        grid.addWidget(self.aBitRateCombo, cRow, 3)

        # Channels
        aChannelsLabel = QtWidgets.QLabel("Channels:")
        self.aChannelsSpin = QtWidgets.QSpinBox(self)
        self.aChannelsSpin.setValue(2)

        grid.addWidget(aChannelsLabel, cRow, 4)
        grid.addWidget(self.aChannelsSpin, cRow, 5)

        # Sample rate
#         aSampleRateLabel = QtWidgets.QLabel("Sample rate")
#         self.aSampleRateCombo = QtWidgets.QComboBox(self)
# 
#         grid.addWidget(aSampleRateLabel, cRow, 6)
#         grid.addWidget(self.aSampleRateCombo, cRow, 7)

        return cRow

    def createGeneralAspectWidgets(self, grid, cRow):
        """
        Adds widgets for general aspect configuration

        @param grid QGridLayout: The current grid layout widget
        @param cRow int: The current line number in the grid

        @return cRow int: The final row index after the widgets were created
        """
        self.resizeDisCheckB = NzQDisablingCheckBox(
            text="Resize", parent=self)
        grid.addWidget(self.resizeDisCheckB, cRow, 0)

        # Resize by standard resolution
        byStdResolDisRadio = NzQDisablingRadioButton(
            text="Std Resolution", parent=self, isInMutexGroup=True)
        self.byStdResolCombo = QtWidgets.QComboBox(self)
        byStdResolDisRadio.setChecked(True)

        grid.addWidget(byStdResolDisRadio, cRow, 1)
        grid.addWidget(self.byStdResolCombo, cRow, 2)

        cRow += 1
        # Resize by Height
        byHeightDisRadio = NzQDisablingRadioButton(
            text="Height", parent=self, isInMutexGroup=True)
        self.byHeightCombo = QtWidgets.QComboBox(self)

        customHeightDisCheckB = NzQDisablingCheckBox(
            text="Custom", parent=self)
        self.customHeightLineEd = QtWidgets.QLineEdit(self)
        self.customHeightLineEd.setText("0")
        self.customHeightLineEd.setValidator(
            Qt.QIntValidator(0, 99999, self))

        customHeightDisCheckB.addSlaveWidget(self.customHeightLineEd)
        customHeightDisCheckB.addSlaveWidget(self.byHeightCombo, False)

        grid.addWidget(byHeightDisRadio, cRow, 1)
        grid.addWidget(self.byHeightCombo, cRow, 2)
        grid.addWidget(customHeightDisCheckB, cRow, 3)
        grid.addWidget(self.customHeightLineEd, cRow, 4, 1, 2)

        cRow += 1
        # Resize by Width
        byWidthDisRadio = NzQDisablingRadioButton(
            text="Width", parent=self, isInMutexGroup=True)
        self.byWidthCombo = QtWidgets.QComboBox(self)

        customWidthDisCheckB = NzQDisablingCheckBox(
            text="Custom", parent=self)
        self.customWidthLineEd = QtWidgets.QLineEdit(self)
        self.customWidthLineEd.setText("0")
        self.customWidthLineEd.setValidator(
            Qt.QIntValidator(0, 99999, self))

        customWidthDisCheckB.addSlaveWidget(self.customWidthLineEd)
        customWidthDisCheckB.addSlaveWidget(self.byWidthCombo, False)

        grid.addWidget(byWidthDisRadio, cRow, 1)
        grid.addWidget(self.byWidthCombo, cRow, 2)
        grid.addWidget(customWidthDisCheckB, cRow, 3)
        grid.addWidget(self.customWidthLineEd, cRow, 4, 1, 2)

        cRow += 1
        # Resize by Percent
        byPercentDisRadio = NzQDisablingRadioButton(
            text="Percent", parent=self, isInMutexGroup=True)

        self.byPercentSpin = QtWidgets.QSpinBox(self)
        self.byPercentSpin.setSuffix("%")
        self.byPercentSpin.setRange(0, 100)
        self.byPercentSpin.setValue(50)

        grid.addWidget(byPercentDisRadio, cRow, 1)
        grid.addWidget(self.byPercentSpin, cRow, 2)

        # QButtonGroup for mutually exclusive resize options
        resizeGroup = QtWidgets.QButtonGroup(self)
        resizeGroup.addButton(byStdResolDisRadio)
        resizeGroup.addButton(byHeightDisRadio)
        resizeGroup.addButton(byWidthDisRadio)
        resizeGroup.addButton(byPercentDisRadio)

        # Create disable links for "resize by standard resolution" radio button
        for wdg in (self.byHeightCombo, customHeightDisCheckB,
                    self.customHeightLineEd, self.byWidthCombo,
                    customWidthDisCheckB, self.customWidthLineEd,
                    self.byPercentSpin):
            byStdResolDisRadio.addSlaveWidget(wdg, False)

        byStdResolDisRadio.addSlaveWidget(self.byStdResolCombo)

        # Create disable links for "resize by height" radio button
        for wdg in (self.byWidthCombo, customWidthDisCheckB,
                    self.customWidthLineEd, self.byPercentSpin,
                    self.byStdResolCombo):
            byHeightDisRadio.addSlaveWidget(wdg, False)

        for wdg in (self.byHeightCombo, customHeightDisCheckB,
                    self.customHeightLineEd):
            byHeightDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by width" radio button
        for wdg in (self.byHeightCombo, customHeightDisCheckB,
                    self.customHeightLineEd, self.byPercentSpin,
                    self.byStdResolCombo):
            byWidthDisRadio.addSlaveWidget(wdg, False)

        for wdg in (self.byWidthCombo, customWidthDisCheckB,
                    self.customWidthLineEd):
            byWidthDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by percent" radio button
        for wdg in (self.byHeightCombo, customHeightDisCheckB,
                    self.customHeightLineEd, self.byWidthCombo,
                    customWidthDisCheckB, self.customWidthLineEd,
                    self.byStdResolCombo):
            byPercentDisRadio.addSlaveWidget(wdg, False)
        byPercentDisRadio.addSlaveWidget(self.byPercentSpin)

        # Add slave widget to be disabled by self.resizeDisCheckB
        for wdg in (byHeightDisRadio, self.byHeightCombo,
                    customHeightDisCheckB, self.customHeightLineEd,
                    byWidthDisRadio, self.byWidthCombo, customWidthDisCheckB,
                    self.customWidthLineEd, byPercentDisRadio,
                    self.byPercentSpin, byStdResolDisRadio,
                    self.byStdResolCombo):
            self.resizeDisCheckB.addSlaveWidget(wdg)

        resizeGroup.setExclusive(True)

        return cRow

    def getConfig(self):
        """
        Get the configuration for the transcoding

        @return: a TranscodingConfig class object containing the data
        """
        # Encapsulator
        encaps = self.encapsCombo.currentText()

        # Video
        vcodec = self.vCodecCombo.currentText()
        if self.autoBitRateDisCkBox.isChecked():
            vbitrate = self.vBitRateSpin.value()
        else:
            vbitrate = 0

        # Audio
        acodec = self.aCodecCombo.currentText()
        abitrateTmp = self.aBitRateCombo.currentText()
        abitrateTmp = re.match(r"(\d+)\w.*", abitrateTmp, re.IGNORECASE)
        abitrate = abitrateTmp.group(1)
        achannels = self.aChannelsSpin.value()
#         asamplerateTmp = self.aSampleRateCombo.currentText()
#         asamplerateTmp = re.match(r"(\d+)\w.*", asamplerateTmp, re.IGNORECASE)
#         asamplerate = asamplerateTmp.group(1)

        # Resize
        width = 0
        height = 0
        aspectratio = 1
        if self.resizeDisCheckB.isChecked():
            # To get height, width and aspect ration we only check which widget
            # is enabled
            if self.byStdResolCombo.isEnabled():
                size = self.byStdResolCombo.currentText()
                pat = re.compile(r"(\d+)x(\d+)", re.IGNORECASE)
                m = re.match(pat, size)
                width = m.group(1)
                height = m.group(2)
            elif self.byHeightCombo.isEnabled():
                height = self.byHeightCombo.currentText()
            elif self.customHeightLineEd.isEnabled():
                height = self.customHeightLineEd.text()
            elif self.customWidthLineEd.isEnabled():
                height = self.customWidthLineEd.text()
            elif self.byWidthCombo.isEnabled():
                width = self.byWidthCombo.currentText()
            elif self.byPercentSpin.isEnabled():
                aspectratio = self.byPercentSpin.value()

        # Deinterlace
        deinterlace = self.deinterlaceCheckB.isChecked()

        # TODO: Sample is not supported for the moment (set to None)
        config = TranscodingConfig(encaps, vcodec, vbitrate, acodec, abitrate,
            achannels, None, width, height, aspectratio,
            deinterlace)

        return config
