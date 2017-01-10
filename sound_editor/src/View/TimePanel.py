import math
from PyQt4 import QtGui, QtCore
from ViewModel.ViewUtils.TimeFormatter import TimeFormatter


class TimePanel(QtGui.QWidget):
    TIME_COLOR = QtGui.QColor(0, 0, 0)

    def __init__(self, channel, parent=None):
        super(TimePanel, self).__init__(parent)
        self.channel = channel
        self.setFixedHeight(30)

    @property
    def channel_model(self):
        return self.channel.channel_model

    def reset_channel(self, channel):
        self.channel = channel

    def get_coordinate_from_frame_number(self, frame_number):
        ratio = self.channel_model.get_ratio_from_frame_number(frame_number)
        return ratio * self.width()

    def paintEvent(self, event):
        grid_density = self.channel.grid_density
        frames = self.channel_model.get_vertical_grid_frames(grid_density)
        time_moments = [self.channel_model.get_time_from_frame(frame)
                        for frame in frames]
        coordinates = [self.get_coordinate_from_frame_number(frame)
                       for frame in frames]
        time_precision = TimePanel.get_time_precision(time_moments)
        for time, coordinate in zip(time_moments, coordinates):
            time_formatted = TimeFormatter.format(time, time_precision)
            self.draw_time_moment(coordinate, time_formatted)

    def draw_time_moment(self, coordinate, time_str):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(TimePanel.TIME_COLOR))
        width = 1.5 * self.width() / self.channel.grid_density
        height = self.height() * 0.9
        x = coordinate - 10
        y = self.height() * 0.05
        text_rectangle = QtCore.QRectF(x, y, width, height)
        painter.drawText(text_rectangle, time_str)

    @staticmethod
    def get_time_precision(time_moments):
        moments_number_ratio = math.log10(10 * len(time_moments))
        range_size_ratio = math.log10(time_moments[-1] - time_moments[0])
        total_coefficient = moments_number_ratio - range_size_ratio
        return int(max(total_coefficient, 0))
