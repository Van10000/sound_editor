from PyQt4 import QtGui, QtCore
from Core.TimeFormatter import TimeFormatter
from View.Channel import Channel
import math


class TimePanel(QtGui.QWidget):
    TIME_COLOR = QtGui.QColor(0, 0, 0)

    def __init__(self, channel, parent=None):
        super(TimePanel, self).__init__(parent)
        self.channel = channel
        self.setFixedHeight(30)

    def paintEvent(self, event):
        frames = self.channel.get_vertical_grid_frames()
        time_moments = [self.channel.get_time_from_frame(frame) for frame in frames]
        coordinates = [self.channel.get_coordinate_from_frame(frame) for frame in frames]
        time_precision = int(max(math.log10(10 * len(time_moments)) -
                                 math.log10(time_moments[-1] - time_moments[0]), 0))
        for time, coordinate in zip(time_moments, coordinates):
            self.draw_time_moment(coordinate, TimeFormatter.format(time, time_precision))

    def draw_time_moment(self, coordinate, time_str):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(TimePanel.TIME_COLOR))
        width = 1.5 * self.width() / self.channel.grid_density
        height = self.height() * 0.9
        x = coordinate - 10
        y = self.height() * 0.05
        text_rectangle = QtCore.QRectF(x, y, width, height)
        painter.drawText(text_rectangle, time_str)






