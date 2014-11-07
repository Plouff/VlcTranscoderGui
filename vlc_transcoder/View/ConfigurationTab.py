#! python3
#-*-coding: utf-8 -*-

"""
@file ConfigurationTab.py
The Configuration Tab of the GUI
"""

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from NzPyQtToolbox import NzQWidgets


class ConfigurationTab(QtWidgets.QWidget):
    """
    This tab holds the settings for the transcoding
    """
    def __init__(self, parent=None):
        """
        The constructor for the Configuration tab of the GUI

        @param parent QtWidgets.QWidget: The parent widget
        """
        super().__init__(parent)
        self.parent=parent

        grid = QtWidgets.QGridLayout()
        cRow=0
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
        resizeDisCheckB = NzQWidgets.NzQDisablingCheckBox(text="Resize",
                                                          parent=self)
        grid.addWidget(resizeDisCheckB, cRow, 0)

        # Resize by Height
        byHeightDisRadio = NzQWidgets.NzQDisablingRadioButton(text="Height",
                                                              parent=self,
                                                              isInMutexGroup=True)
        byHeightCombo = QtWidgets.QComboBox(self)
        byHeightDisRadio.setChecked(True)

        customHeightDisCheckB = NzQWidgets.NzQDisablingCheckBox(text="Custom",
                                                                parent=self)
        customHeightLineEd = QtWidgets.QLineEdit(self)
        customHeightDisCheckB.addSlaveWidget(customHeightLineEd)
        customHeightDisCheckB.addSlaveWidget(byHeightCombo, False)

        grid.addWidget(byHeightDisRadio, cRow, 1)
        grid.addWidget(byHeightCombo, cRow, 2)
        grid.addWidget(customHeightDisCheckB, cRow, 3)
        grid.addWidget(customHeightLineEd, cRow, 4)

        cRow += 1
        # Resize by Width
        byWidthDisRadio = NzQWidgets.NzQDisablingRadioButton(text="Width",
                                                             parent=self,
                                                             isInMutexGroup=True)
        byWidthCombo = QtWidgets.QComboBox(self)

        customWidthDisCheckB = NzQWidgets.NzQDisablingCheckBox(text="Custom",
                                                               parent=self)
        customWidthLineEd = QtWidgets.QLineEdit(self)
        customWidthDisCheckB.addSlaveWidget(customWidthLineEd)
        customWidthDisCheckB.addSlaveWidget(byWidthCombo, False)

        grid.addWidget(byWidthDisRadio, cRow, 1)
        grid.addWidget(byWidthCombo, cRow, 2)
        grid.addWidget(customWidthDisCheckB, cRow, 3)
        grid.addWidget(customWidthLineEd, cRow, 4)

        cRow += 1
        # Resize by Percent
        byPercentDisRadio = NzQWidgets.NzQDisablingRadioButton(text="Percent",
                                                            parent=self,
                                                            isInMutexGroup=True)

        byPercentSpin = QtWidgets.QSpinBox(self)
        byPercentSpin.setSuffix("%")
        byPercentSpin.setRange(0, 100)

        grid.addWidget(byPercentDisRadio, cRow, 1)
        grid.addWidget(byPercentSpin, cRow, 2)

        # QButtonGroup for mutually exclusive resize options
        resizeGroup = QtWidgets.QButtonGroup(self)
        resizeGroup.addButton(byHeightDisRadio)
        resizeGroup.addButton(byWidthDisRadio)
        resizeGroup.addButton(byPercentDisRadio)

        # Create disable links for "resize by height" radio button
        for wdg in (byWidthCombo, customWidthDisCheckB, customWidthLineEd,
                    byPercentSpin):
            byHeightDisRadio.addSlaveWidget(wdg, False)
        for wdg in (byHeightCombo, customHeightDisCheckB, customHeightLineEd):
            byHeightDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by width" radio button
        for wdg in (byHeightCombo, customHeightDisCheckB, customHeightLineEd,
                    byPercentSpin):
            byWidthDisRadio.addSlaveWidget(wdg, False)
        for wdg in (byWidthCombo, customWidthDisCheckB, customWidthLineEd):
            byWidthDisRadio.addSlaveWidget(wdg)

        # Create disable links for "resize by percent" radio button
        for wdg in (byHeightCombo, customHeightDisCheckB, customHeightLineEd,
                    byWidthCombo, customWidthDisCheckB, customWidthLineEd):
            byPercentDisRadio.addSlaveWidget(wdg, False)
        byPercentDisRadio.addSlaveWidget(byPercentSpin)

        # Add slave widget to be disabled by resizeDisCheckB
        for wdg in (byHeightDisRadio, byHeightCombo, customHeightDisCheckB,
                    customHeightLineEd, byWidthDisRadio, byWidthCombo,
                    customWidthDisCheckB, customWidthLineEd, byPercentDisRadio,
                    byPercentSpin):
            resizeDisCheckB.addSlaveWidget(wdg)

        resizeGroup.setExclusive(True)

        return cRow

