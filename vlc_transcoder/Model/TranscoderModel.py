#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderModel.py
The Model for the transcoder
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from collections import OrderedDict


class TooltipedDataListModel(QtCore.QAbstractListModel):
    """
    TooltipedDataListModel: An extension of the list model to easyly deal with
    tooltip for simple lists
    """
    def __init__(self, tooltipDic = {}, parent=None):
        """
        The class constructor

        @param tooltipDic dic: The dictionnary containing the couples
        (display string, tooltip string)
        """
        super().__init__(parent)
        self.__tooltipDic=tooltipDic

    def rowCount(self, parent):
        """
        Mandatory implementation of base class's rowCount

        @param parent: The parent node
        """
        return len(self.__tooltipDic.keys())

    def data(self, index, role):
        """
        Mandatory implementation of base class's data

        @param index: The index object of the item
        @param role: The current role being executed
        """
        row=index.row()
        curlist=list(self.__tooltipDic.keys())
        if role == QtCore.Qt.DisplayRole:
            return curlist[row]
        if role == QtCore.Qt.ToolTipRole:
            key=curlist[row]
            return self.__tooltipDic[key]
            try:
                key=curlist[row]
                return self.__tooltipDic[key]
            except:
                return ''


class Model():
    """
    This is a the 'Model' part of the MVC implementation. It contains data
    regarding the settings of the transcoder
    """
    def __init__(self):
        """
        The class constructor
        """
        self.defineAudioVideoParameters()
        self.rootDirList=[]

    def defineAudioVideoParameters(self):
        """
        Defines audio and video parameters such as the encapsulators,
        audio/video codecs and so on
        """
        self.encapsulatorsODic=OrderedDict([
            ('mpeg', ('MPEG-1 multiplexing - recommended for '
                      'portability. Only works with mp1v video and mpga audio, but '
                      'works on all known players')),
            ('ts', ('MPEG Transport Stream, primarily used for streaming '
                    'MPEG. Also used in DVDs')),
            ('ps', ('MPEG Program Stream, primarily used for saving MPEG '
                    'data to disk.')),
            ('mp4', ('MPEG-4 mux format, used only for MPEG-4 video and '
                     'MPEG audio')),
            ('avi', 'AVI'),
            ('asf', 'ASF'),
            ('ogg', ('Xiph.org\'s ogg container format. Can contain audio, '
                     'video, and metadata')),
            ('dummy', 'dummy output, can be used in creation of MP3 files')
        ])

        self.vCodecODic=OrderedDict([
            ('h264', 'H264'),
            ('mp1v', 'MPEG-1 Video - recommended for portability'),
            ('mp2v', 'MPEG-2 Video - used in DVDs'),
            ('mp4v', 'MPEG-4 Video'),
            ('SVQ1', 'Sorenson Video v1'),
            ('SVQ3', 'Sorenson Video v3'),
            ('DVDv', 'VOB Video - used in DVDs'),
            ('WMV1', 'Windows Media Video v1'),
            ('WMV2', 'Windows Media Video v2'),
            ('WMV3', 'Windows Media Video v3, also called Windows Media 9 (unsupported)'),
            ('DVSD', 'Digital Video'),
            ('MJPG', 'MJPEG'),
            ('H263', 'H263'),
            ('theo', 'Theora'),
            ('IV20', 'Indeo Video'),
            #('IV40', 'Indeo Video version 4 or later (unsupported)'),
            ('RV10', 'Real Media Video'),
            ('cvid', 'Cinepak'),
            ('VP31', 'On2 VP'),
            ('FLV1', 'Flash Video'),
            ('CYUV', 'Creative YUV'),
            ('HFYU', 'Huffman YUV'),
            ('MSVC', 'Microsoft Video v1'),
            ('MRLE', 'Microsoft RLE Video'),
            ('AASC', 'Autodesc RLE Video'),
            ('FLIC', 'FLIC video'),
            ('QPEG', 'QPEG Video'),
            ('VP8' , 'VP8 Video')
         ])

        self.aCodecODic=OrderedDict([
            ('mpga', 'MPEG audio (recommended for portability)'),
            ('mp3' , 'MPEG Layer 3 audio'),
            ('mp4a', 'MP4 audio'),
            ('a52' , 'Dolby Digital (A52 or AC3)'),
            ('vorb', 'Vorbis'),
            ('spx' , 'Speex'),
            ('flac', 'FLAC (loss less)')
        ])

        self.aBitRateList=['96kB/s', '128kB/s', '192kB/s', '256kB/s']

        self.aSampleRateList=['44056Hz', '44100Hz', '48000Hz']


    def addRootDirectory(self, rootDir):
        """
        Add a root directory to the list of directories to process

        @param rootDir: A path to a directory to be processed
        """
        if rootDir not in self.rootDirList:
            self.rootDirList.append(rootDir)
