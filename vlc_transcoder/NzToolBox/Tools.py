#! python3
# -*-coding: utf-8 -*-

"""
@file Tools.py
Some various tools
"""
# Import standard modules
import sys
import os
import re


def getProgramBaseFolder():
    """
    Get the folder of the top level file that launched the program

    @return: A @c string of the folder
    """
    return os.path.dirname(sys.argv[0])


def escapeSpaces(text):
    """
    Escape spaces in the given string

    @return: A @c string with spaces replaced by "\ "
    """
    return re.sub(" ", r"\\ ", text)

if __name__ == '__main__':
    print(getProgramBaseFolder())
    print(escapeSpaces("df ze fsdf "))
