"""
@file TranscoderModel.py
The Model for the transcoder
"""

class Model():
    """
    This is a the 'Model' part of the MVC implementation. It contains data
    regarding the settings of the transcoder
    """
    def __init__():
        muxer=['avi', 'asf', 'mpeg', 'mp4', 'ogg', 'ps', 'ts', 'dummy']
        muxerDesc={ 'mpeg1': ('MPEG-1 multiplexing - recommended for'
                'portability. Only works with mp1v video and mpga audio, but '
                'works on all known players'),
                'ts': ('MPEG Transport Stream, primarily used for streaming '
                'MPEG. Also used in DVDs'),
                'ps': ('MPEG Program Stream, primarily used for saving MPEG '
                'data to disk.'),
                'mp4': ('MPEG-4 mux format, used only for MPEG-4 video and '
                'MPEG audio.'),
                'avi': 'AVI',
                'asf': 'ASF',
                'dummy': 'dummy output, can be used in creation of MP3 files.',
                'ogg': ('Xiph.org\'s ogg container format. Can contain audio, '
                'video, and metadata.')
                  }

        vCodec=['mp1v', 'mp2v', 'mp4v', 'SVQ1', 'SVQ3', 'DVDv', 'WMV1',
            'WMV2', 'WMV3', 'DVSD', 'MJPG', 'H263', 'h264', 'theo', 'IV20',
            'IV40', 'RV10', 'cvid', 'VP31', 'FLV1', 'CYUV', 'HFYU', 'MSVC',
            'MRLE', 'AASC', 'FLIC', 'QPEG', 'VP8']

        vCodecDesc={'mp1v': 'MPEG-1 Video - recommended for portability',
                    'mp2v': 'MPEG-2 Video - used in DVDs',
                    'mp4v': 'MPEG-4 Video',
                    'SVQ1': 'Sorenson Video v1',
                    'SVQ3': 'Sorenson Video v3',
                    'DVDv': 'VOB Video - used in DVDs',
                    'WMV1': 'Windows Media Video v1',
                    'WMV2': 'Windows Media Video v2',
                    #'WMV3': 'Windows Media Video v3, also called Windows Media 9 (unsupported)',
                    'DVSD': 'Digital Video',
                    'MJPG': 'MJPEG',
                    'H263': 'H263',
                    'h264': 'H264',
                    'theo': 'Theora',
                    'IV20': 'Indeo Video',
                    #'IV40': 'Indeo Video version 4 or later (unsupported)',
                    'RV10': 'Real Media Video',
                    'cvid': 'Cinepak',
                    'VP31': 'On2 VP',
                    'FLV1': 'Flash Video',
                    'CYUV': 'Creative YUV',
                    'HFYU': 'Huffman YUV',
                    'MSVC': 'Microsoft Video v1',
                    'MRLE': 'Microsoft RLE Video',
                    'AASC': 'Autodesc RLE Video',
                    'FLIC': 'FLIC video',
                    'QPEG': 'QPEG Video',
                    'VP8' : 'VP8 Video'
                    }

        aCodec={'mpga': 'MPEG audio (recommended for portability)',
                'mp3' : 'MPEG Layer 3 audio',
                'mp4a': 'MP4 audio',
                'a52' : 'Dolby Digital (A52 or AC3)',
                'vorb': 'Vorbis',
                'spx' : 'Speex',
                'flac': 'FLAC (loss less)'
                }
        aBitrate=['96', '128', '192', '256']
        sampleRate=['44056', '44100', '48000']

