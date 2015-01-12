#! python3
#-*-coding: utf-8 -*-
"""
@file NzToolBox/Findfiles.py
Find files recrusively from a given root dir
"""

# Import custom modules

# Import standard modules
import os
import fnmatch
import sys
import re
import logging


def findFiles(rootDir, patterns):
    """
    Produces a generator to find files recursively in a given root directory.

    @param[in] rootDir The top directory for the search
    @param[in] patterns list: A pattern to be found using @c fnmatch

    @return A generator (@c yield) over the hierarchy

    @par Usage:
        The @c patterns must be a list of @c fnmatch supported patterns.
        @c fnmatch enables to use Unix like patterns, for example, "*.py"

     @bug <tt>os.access(rootDir, os.R_OK)</tt> doesn't work on Windows:
         http://bugs.python.org/issue2528
    """
    if patterns == []:
        # Check patterns list is not empty
        raise RuntimeError("Pattern list is empty")
    elif not os.access(rootDir, os.X_OK):
        # Check that rootDir exists (can't use os.exists since os.stat fails)
        raise RuntimeError("Directory doesn't exist: {}".format(rootDir))
    elif not os.path.isdir(rootDir):
        # Check that rootDir is a directory
        raise RuntimeError("File is a not directory: {}".format(rootDir))
    elif not os.access(rootDir, os.R_OK):
        # Check that rootDir is readable
        raise RuntimeError("No read access for directory {}".format(rootDir))
    else:
        if not isinstance(patterns, type([])):
            # Check that patterns is a list
            raise TypeError(
                "In findFiles: 'patterns' argument must be a list. "
                "You provided a '{}'".format(type(patterns).__name__))
        # Look for files
        logging.debug("Root: {} - patterns: {}".format(rootDir, patterns))
        for root, dirs, files in os.walk(rootDir):
            for basename in files:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename


def processInputExtensions(rawExtensions):
    """
    Format the input extensions to fit @c Findfiles format.

    @param[in] rawExtensions A list of patterns to be processed

    @return A list of extensions compliant with @c fnmatch
    """
    if rawExtensions == []:
        # Check patterns list is not empty
        raise RuntimeError("Pattern list is empty")
        return []
    else:
        pat = re.compile(r'.*\*?\.(\w+)', re.IGNORECASE)
        processedExt = []
        for extStr in rawExtensions:
            tmp = re.match(pat, extStr)
            if tmp is None:
                raise RuntimeError(
                    "Unsupported extension raw string: {}".format(extStr))
            else:
                processedExt.append("*." + tmp.group(1))

        logging.debug("Converted {} to {}".format(rawExtensions, processedExt))
        return processedExt


def findFilesbyExtension(rootDir, rawExtensions):
    """
    Find files matching a list of extensions.

    @param[in] rootDir The root directory for the search
    @param[in] rawExtensions The list of raw extensions
    """
    #qtDebugTrace()
    processedExt = processInputExtensions(rawExtensions)

    return findFiles(rootDir, processedExt)


if __name__ == '__main__':
    # A basic exemple
    if len(sys.argv) > 1:
        for filename in findFiles(sys.argv[1], ['*.py']):
            print('Found Python source:', filename)
    else:
        for filename in findFiles('.', ['*.py']):
            print('Found Python source:', filename)
