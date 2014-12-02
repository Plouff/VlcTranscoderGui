#! python3
#-*-coding: utf-8 -*-
"""
@file NzToolBox/Findfiles.py
Find files recrusively from a given root dir
"""

# Import standard modules
import os
import fnmatch
import sys


def findFiles(rootDir, patterns):
    """
    Produces a generator to find files recursively in a given root directory.

    @param[in] rootDir The top directory for the search
    @param[in] patterns list: A pattern to be found using @c fnmatch

    @return A generator (@c yield) over the hierarchy

    @par Usage:
        The @c patterns must be a list of @c fnmatch supported patterns.
        @c fnmatch enables to use Unix like patterns, for example, "*.py"
    """
    if not os.path.exists(rootDir):
        # Check that rootDir exists
        raise RuntimeError("Directory doesn't exist: {}".format(rootDir))
    if not os.path.isdir(rootDir):
        # Check that rootDir is a directory
        raise RuntimeError("File is a not directory: {}".format(rootDir))
    else:
        if not isinstance(patterns, type([])):
            # Check that patterns is a list
            raise TypeError(
                "In findFiles: 'patterns' argument must be a list. "
                "You provided a '{}'".format(type(patterns).__name__))
        for root, dirs, files in os.walk(rootDir):
            for basename in files:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename


if __name__ == '__main__':
    # A basic exemple
    try:
        sys.argv[1] != ''
        for filename in findFiles(sys.argv[1], ['*.py']):
            print('Found Python source:', filename)
    except:
        for filename in findFiles('.', ['*.py']):
            print('Found Python source:', filename)
