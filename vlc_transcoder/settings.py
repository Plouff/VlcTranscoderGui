#! python3
# -*-coding: utf-8 -*-

"""
@file settings.py
Global settings for the project
"""

# Import standard modules
import logging


# A variable for the demo mode
class GlobalVars():
    demoMode = False


def toggleDemo():
    """
    Helper to toggle a boolean for demo mode
    """
    if GlobalVars.demoMode:
        GlobalVars.demoMode = False
        logging.info("Demo mode disabled")
    else:
        GlobalVars.demoMode = True
        logging.info("Demo mode enabled")
