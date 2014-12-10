#! python3
#-*-coding: utf-8 -*-

"""
@file TranscoderModel.py
The Model for the transcoder
"""

from collections import OrderedDict


class TranscoderModel():
    """
    This is a the 'Model' part of the MVC implementation. It contains data
    regarding the settings of the transcoder
    """
    def __init__(self):
        """
        The class constructor
        """
        self.defineAudioVideoParameters()
        self.defineResizeParameters()
        self.defineVideoFileExtensions()

    def defineAudioVideoParameters(self):
        """
        Defines audio and video parameters such as the encapsulators,
        audio/video codecs and so on
        """
        self.encapsulatorsODic = OrderedDict([
            ('mpeg', ('MPEG-1 multiplexing - recommended for '
                      'portability. Only works with mp1v video and mpga '
                      'audio, but works on all known players')),
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

        self.vCodecODic = OrderedDict([
            ('h264', 'H264'),
            ('H263', 'H263'),
            ('mp1v', 'MPEG-1 Video - recommended for portability'),
            ('mp2v', 'MPEG-2 Video - used in DVDs'),
            ('mp4v', 'MPEG-4 Video'),
            ('SVQ1', 'Sorenson Video v1'),
            ('SVQ3', 'Sorenson Video v3'),
            ('DVDv', 'VOB Video - used in DVDs'),
            ('WMV1', 'Windows Media Video v1'),
            ('WMV2', 'Windows Media Video v2'),
            ('WMV3', ('Windows Media Video v3, also called Windows Media 9 '
                      '(unsupported)')),
            ('DVSD', 'Digital Video'),
            ('MJPG', 'MJPEG'),
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
            ('VP8', 'VP8 Video')
        ])

        self.aCodecODic = OrderedDict([
            ('mp3', 'MPEG Layer 3 audio'),
            ('mpga', 'MPEG audio (recommended for portability)'),
            ('mp4a', 'MP4 audio'),
            ('a52', 'Dolby Digital (A52 or AC3)'),
            ('vorb', 'Vorbis'),
            ('spx', 'Speex'),
            ('flac', 'FLAC (loss less)')
        ])

        self.aBitRateList = ['96kB/s', '128kB/s', '192kB/s', '256kB/s']

        self.aSampleRateList = ['44056Hz', '44100Hz', '48000Hz']

    def defineResizeParameters(self):
        """
        Defines classical resize parameters
        """
        self.stdResolutionOdic = OrderedDict([
            ('640x480', 'VGA'),
            ('800x600', 'SVGA'),
            ('1280x720', 'HD 720'),
            ('1920x1080', 'HD 1080'),
            ('2048x1080', '2K'),
            ('4096x2160', '4K')
        ])

        self.vHeightList = ['480', '600', '720', '1080', '2048', '4096']
        self.vWidthList = ['640', '800', '1280', '1920', '2160']

    def defineVideoFileExtensions(self):
        self.videoFilexExt = OrderedDict([
            ('.3g2',  '3GPP2 Multimedia File'),
            ('.3gp',  '3GPP Multimedia File'),
            ('.asf',  'Advanced Systems Format File'),
            ('.asx',  'Microsoft ASF Redirector File'),
            ('.avi',  'Audio Video Interleave File'),
            ('.flv',  'Flash Video File'),
            ('.m4v',  'iTunes Video File'),
            ('.mov',  'Apple QuickTime Movie'),
            ('.mp4',  'MPEG-4 Video File'),
            ('.mpg',  'MPEG Video File'),
            ('.rm ',  'Real Media File'),
            ('.swf',  'Shockwave Flash Movie'),
            ('.vob',  'DVD Video Object File'),
            ('.wmv',  'Windows Media Video File')
        ])
