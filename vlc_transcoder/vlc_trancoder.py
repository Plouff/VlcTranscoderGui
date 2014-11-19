#! python3
#-*-coding: utf-8 -*-

"""
VLC Transcoder GUI

A GUI to transcode videos with VLC

author: Nassim Zga
created: 20/10/14
"""

from PyQt5 import QtWidgets

from View.TranscoderView import *
from Model.TranscoderModel import *
from Controller.TranscoderController import *


"""
Script wrapper
"""
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    view = View(app)
    model = Model()
    controller = Controller(model, view)
    sys.exit(app.exec_())


# vlc -vvv input_stream --sout #transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}:
# CALL "C:\Program Files\VideoLAN\VLC\vlc" -I dummy -vvv %1
#--sout=#transcode{acodec="mpga",ab="512",channels="2",samplerate="44100"}:standard{access="file",mux="mpeg1",dst="%_commanm%.mp3"}
#vlc://quit
