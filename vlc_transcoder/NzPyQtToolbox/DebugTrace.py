#! python3
#-*-coding: utf-8 -*-

"""
@file DebugTrace.py
A utility function to debug code. Source:
    http://stackoverflow.com/questions/1736015/debugging-a-pyqt4-app
"""


def qtDebugTrace():
    '''Set a tracepoint in the Python debugger that works with Qt'''
    from PyQt5.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()
