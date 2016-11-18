from PyQt4 import QtGui, QtCore
from View.Channel import Channel


class TiredError(Exception):
    pass


class TimePanel(QtGui.QWidget):
    def __init__(self, channel):
        self.channel = channel

    def paintEvent(self, event):
        coordinates = self.channel.get_vertical_grid_coordinates()
        raise TiredError()





