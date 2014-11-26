#! python3
#-*-coding: utf-8 -*-
"""
@file LoggingTools.py
Logging tools
"""

# Import standard modules
import logging


def parseLoggingLevel(loglevel):
    """
    Parse logging level from command line
    from: https://docs.python.org/3.4/howto/logging.html

    Assuming loglevel is bound to the string value obtained from the
    command line argument. Convert to upper case to allow the user to
    specify --log=DEBUG or --log=debug
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)

def initLogger(level=logging.DEBUG):
    """
    Initialize a logger with default display attributes and with DEBUG level
    """
    logging.basicConfig(
        format='%(levelname)s-%(module)s:%(lineno)d-%(funcName)s: %(message)s',
        level=level)

