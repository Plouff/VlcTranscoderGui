#! python3
#-*-coding: utf-8 -*-
"""
@file NzToolBox/Findfiles.py
Find files recrusively from a given root dir
"""

import os
import fnmatch
import sys


def findFiles(rootDir, patterns):
    if not isinstance(patterns, type([])):
        raise TypeError("In findFiles: 'patterns' argument must be a list. "
                        "You provided a '{}'".format(type(patterns).__name__)
                        )
    for root, dirs, files in os.walk(rootDir):
        for basename in files:
            for pattern in patterns:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename


if __name__ == '__main__':
    try:
        sys.argv[1] != ''
        for filename in findFiles(sys.argv[1], ['*.py']):
            print('Found Python source:', filename)
    except:
        for filename in findFiles('.', ['*.py']):
            print('Found Python source:', filename)
