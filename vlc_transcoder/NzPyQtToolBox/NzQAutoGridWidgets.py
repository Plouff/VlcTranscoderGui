#! python3
#-*-coding: utf-8 -*-

"""
@file NzQAutoGridWidgets.py
A widget to generate a grid of widgets
"""

# Import PyQt modules
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# Import custom modules
from NzToolBox import LoggingTools
from NzPyQtToolBox.DebugTrace import qtDebugTrace

# Import standard modules
from pprint import pprint
import logging
import warnings


class NzQAutoGridCheckboxes(QtWidgets.QWidget):
    """
    A widget to generate a grid of checkboxes

    @section Usage Usage
    @subsection init Initialize the widget
    You first need to create an empty widget. Just set @c maxRowCount or @c
    maxColumnCount to constraint the grid that will be generated.

    @subsection create Create the widget
    Call @c createCheckboxes using @c data argument to provide the texts for
    the checkboxes. If @c data is a @c dic then the @e keys will be used as
    text for the checkboxes and the @e values will be used for the tooltip.

    @subsection get_data Get data from the widget
    Simply access the public atttribute @c self.choices.
    This is a list of the @c text of the checkboxes selected at the moment

    @subsection Limitation Limitation
    At the moment the order of the element will be different if
    you provide @c maxRowCount or @c maxColumnCount, even if you provide the
    same list of data

    @todo This widget could be a ModelView widget to automatically update the
    checkboxes if the input data changes
    """
    def __init__(self, maxRowCount=0, maxColumnCount=0, parent=None):
        """
        The class constructor

        @param[in] data If @c data is a dictionnary then a checkbox with a
        tooltip will be displayed, else if it is just a list simple checkboxes
        are created

        @param[in] maxRowCount int: The maximum number of checkboxes per row.
        Use @c 0 for no maximum
        @param[in] maxColumnCount int: The maximum number of checkboxes per
        column Use @c 0 for no maximum

        @warning At least one, but only one of the parameter @c maxRowCount and
        @c maxColumnCount must be @c >0. In other word you need to constraint
        the number of rows or columns but not both.

        @return An empty widget pointer
        """
        super().__init__(parent)
        # Check paremeters
        if maxRowCount > 0 and maxColumnCount > 0:
            raise RuntimeError(
                "maxRowCount and maxColumnCount can't be set a the same time")
        elif maxRowCount == 0 and maxColumnCount == 0:
            raise RuntimeError(
                "maxRowCount and maxColumnCount can't be 0 at the same time")
        else:
            logging.debug("maxRowCount={} - maxColumnCount={}".format(
                maxRowCount, maxColumnCount))
            # Save the input parameters
            self._maxRowCount = maxRowCount
            self._maxColumnCount = maxColumnCount

            # Create a matrice that will contain the checkboxes pointers
            self._checkboxes = [[]]

            # Some stuff to generate a list with checkboxes data that are
            # checked
            self.choices = []
            self._checkedMapper = QtCore.QSignalMapper(self)
            self._checkedMapper.mapped[QtWidgets.QWidget].connect(
                self._updateListOfChoices)

    def createCheckboxes(self, data):
        """
        Process the data to generate the checkboxes

        @param[in] data The input data to be displayed
        @param[in] parent The parent widget

        @return a boolean depending on success of the creation of the widget
        """
        # Create the grid
        grid = QtWidgets.QGridLayout(self)
        self.setLayout(grid)

        # Get length of the data
        itemCount = len(data)

        # If no item trigger a warning
        if itemCount == 0:
            warnings.warn('Got an empty list/dic of text to display')
            return False
        else:
            cRow = 0
            cCol = 0
            for item in self._checkBoxPyGenerator(data):
                # Create a QCheckBox widget with text
                box = QtWidgets.QCheckBox(item['text'])
                # Add tooltip (is empty if a list is received)
                box.setToolTip(item['tooltip'])
                # Add checkbox to the grid
                grid.addWidget(box, cRow, cCol)

                # Save checkbox in the matrice
                self._checkboxes[cRow].append(box)

                # Connect the checkbox to the signal mapper
                box.clicked.connect(self._checkedMapper.map)
                self._checkedMapper.setMapping(box, box)

                # Update row and column counters
                (cRow, cCol) = self._updateIndex(cRow, cCol)
            return True

    def _checkBoxPyGenerator(self, data):
        """
        Create a Python Generator to loop over the data
        """
        for text in data:
            #qtDebugTrace()
            try:
                # If data is a dictionnary, we can extract a tooltip
                tooltip = data[text]
            except:
                # Else tooltip will be empty
                tooltip = ''
            logging.debug("Item: text '{}', tooltip '{}'".format(
                text, tooltip))
            yield {'text': text, 'tooltip': tooltip}

    def _updateIndex(self, cRow, cCol):
        """
        A python generator (yield) that computes the row and column index on
        the go depending on @c maxRowCount and @c maxColumnCount

        @return A tuple (row, column) for the next item
        """
        # Update current row and column
        #qtDebugTrace()
        if self._maxRowCount > 0:
            if cRow < self._maxRowCount - 1:
                cRow += 1
                # Create new empty row
                self._checkboxes.append([])
            else:
                cCol += 1
                cRow = 0
        elif self._maxColumnCount > 0:
            if cCol < self._maxColumnCount - 1:
                cCol += 1
            else:
                cRow += 1
                cCol = 0
                # Create new empty row
                self._checkboxes.append([])
        else:
            cRow = -1
            cCol = -1

        #logging.debug("({}, {}) < ({} , {})".format(
            #cRow, cCol, self._maxRowCount, self._maxColumnCount))
        return (cRow, cCol)

    def _updateListOfChoices(self, checkBox):
        """
        Update the list of choices checked.
        Depending on the state of the checkbox, its @c text is added or removed
        to the list of current choices

        @param[in] checkBox The checkbox that state changed
        """
        if checkBox.isChecked():
            self.choices.append(checkBox.text())
            logging.debug("{} added to choices ({})".format(
                checkBox.text(), self.choices))
        else:
            self.choices.remove(checkBox.text())
            logging.debug("{} removed from choices ({})".format(
                checkBox.text(), self.choices))


if __name__ == '__main__':
    import sys
    from collections import OrderedDict

    LoggingTools.initLogger(logging.DEBUG)

    textlist = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10',
                '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18']

    textodic = OrderedDict([
        ('dic #1', 'item #1'),
        ('dic #2', 'item #2'),
        ('dic #3', 'item #3'),
        ('dic #4', 'item #4'),
        ('dic #5', 'item #5'),
        ('dic #6', 'item #6'),
        ('dic #7', 'item #7'),
        ('dic #8', 'item #8'),
        ('dic #9', 'item #9'),
        ('dic #10', 'item #10'),
        ('dic #11', 'item #11'),
        ('dic #12', 'item #12'),
        ('dic #13', 'item #13'),
        ('dic #14', 'item #14'),
        ('dic #15', 'item #15'),
        ('dic #16', 'item #16'),
        ('dic #17', 'item #17'),
        ('dic #18', 'item #18')
    ])

    app = QtWidgets.QApplication(sys.argv)

    # Create empty widget
    wdgtList = NzQAutoGridCheckboxes(maxColumnCount=7)
    wdgtOdic = NzQAutoGridCheckboxes(maxRowCount=4)

    # Fill widget
    wdgtList.createCheckboxes(textlist)
    wdgtOdic.createCheckboxes(textodic)

    wdgtList.show()
    wdgtOdic.show()

    sys.exit(app.exec_())
