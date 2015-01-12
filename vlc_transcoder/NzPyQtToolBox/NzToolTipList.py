#! python3
#-*-coding: utf-8 -*-

"""
@file NzToolTipList.py
A list data model to easily create list of items with tooltip
"""

# Import PyQt modules
from PyQt5 import QtCore


class TooltipedDataListModel(QtCore.QAbstractListModel):
    """
    TooltipedDataListModel: An extension of the list model to easily deal with
    tooltip for simple lists
    """
    def __init__(self, tooltipDic={}, parent=None):
        """
        The class constructor

        @param[in] tooltipDic dic: The dictionnary containing the couples
        (display string, tooltip string)
        @param[in] parent The parent widget
        """
        super().__init__(parent)
        self._tooltipDic = tooltipDic

    def rowCount(self, parent=None):
        """
        Mandatory implementation of base class's rowCount

        @param parent: The parent node
        @return The numbers of rows
        """
        return len(self._tooltipDic.keys())

    def data(self, index, role):
        """
        Mandatory implementation of base class's data

        @param index: The index object of the item
        @param role: The current role being executed

        @return Data to be displayed in the corresponding views
        """
        row = index.row()
        curlist = list(self._tooltipDic.keys())
        if role == QtCore.Qt.DisplayRole:
            return curlist[row]
        if role == QtCore.Qt.ToolTipRole:
            key = curlist[row]
            return self._tooltipDic[key]
            try:
                key = curlist[row]
                return self._tooltipDic[key]
            except:
                return ''

    def update(self, tooltipDic):
        """
        Update the list model with a new set of data

        @param[in] tooltipDic dic: The new data for the model
        """
        self._tooltipDic = tooltipDic

        # emit dataChanged
        startIndex = self.index(0, 0)
        endIndex = self.index(self.rowCount(), 0)
        self.dataChanged(startIndex, endIndex)
