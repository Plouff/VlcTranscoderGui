#! python3
# -*-coding: utf-8 -*-

"""
@file TranscodingConfing.py
The configuration for the transcoder
"""

# Import PyQt modules
from PyQt5 import Qt

# Import standard modules
import logging


class TranscodingConfig(Qt.QObject):
    """
    A class the contain the configuration selected by the user
    """

    def __init__(self, encaps, vcodec, vbitrate, acodec, abitrate, achannels,
            asamplerate, width, height, aspectratio, deinterlace):
        """
        The class constructor
        """
        self.encaps = encaps
        self.vcodec = vcodec
        self.vbitrate = vbitrate
        self.acodec = acodec
        self.abitrate = abitrate
        self.achannels = achannels
        self.asamplerate = asamplerate
        self.width = width
        self.height = height
        self.aspectratio = aspectratio
        self.deinterlace = deinterlace

        logging.info(str(self))

    def __repr__(self, *args, **kwargs):
        msg = ("encaps={}, vcodec={}, vbitrate={}\n".format(
                self.encaps, self.vcodec, self.vbitrate) +
            "acodec={}, abitrate={}, achannels={}, asamplerate={}\n".format(
                self.acodec, self.abitrate, self.achannels, self.asamplerate) +
            "width={}, height={}, aspectratio={}, deinterlace={}".format(
                self.width, self.height, self.aspectratio,
                str(self.deinterlace))
              )
        return msg
