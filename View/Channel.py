from PyQt4 import QtGui, QtCore
from Core.FramesGridUtils import FramesGridUtils
from Core.PowOfTwoChannelCompressor import PowOfTwoChannelCompressor
from Core.SmartChannelCompressor import SmartChannelCompressor
import functools


class Channel(QtGui.QWidget):
    MINIMAL_CHANNEL_LEN = 100
    DEFAULT_GRID_DENSITY = 20

    def __init__(self, channel, sample_width, frame_rate, grid_density=DEFAULT_GRID_DENSITY, parent=None):
        super(Channel, self).__init__(parent)
        self.channel_compressed = PowOfTwoChannelCompressor(channel, 2500)
        self.frame_rate = frame_rate
        self.channel = channel
        self.grid_density = grid_density
        self.numbers_range = 256 ** sample_width
        self.start_frame = 0
        self.finish_frame = len(channel)
        self.setMinimumSize(100, 100)

    def __len__(self):
        return self.finish_frame - self.start_frame

    @property
    def zero_amplitude(self):
        return self.numbers_range // 2

    def get_time(self, frame_number):
        return frame_number / self.frame_rate

    @property
    def start_frame_time(self):
        return self.get_time(self.start_frame)

    @property
    def finish_frame_time(self):
        return self.get_time(self.finish_frame)

    def paintEvent(self, paint_event):
        frame_values = self \
            .channel_compressed \
            .get_compressed_smart(self.start_frame, self.finish_frame)

        width_coefficient = self.width() / len(frame_values)
        height_coefficient = self.height() / self.numbers_range
        points = []
        for i in range(len(frame_values)):
            x_coord = width_coefficient * i
            y_coord = (self.zero_amplitude - frame_values[i]) * height_coefficient

            points.append(QtCore.QPointF(x_coord, y_coord))
        self.draw_vertical_grid()
        self._draw_lines_by_points(points)

    def scale(self, mid_frame, scale_factor):
        """
        Scales the view relative to mid_frame.
        Point mid_frame stays at the same position on the screen.
        """
        scaled_len = self._get_scaled_len(scale_factor)
        real_scale_factor = scaled_len / len(self)
        get_bound_scaled = functools.partial(Channel._get_bound_scaled,
                                             mid_frame=mid_frame,
                                             scale_factor=real_scale_factor)
        self.start_frame = max(0, get_bound_scaled(self.start_frame))
        self.finish_frame = min(len(self.channel), get_bound_scaled(self.finish_frame))
        self.repaint()

    def _get_scaled_len(self, scale_factor):
        scaled_len = scale_factor * len(self)
        if scaled_len < self.MINIMAL_CHANNEL_LEN:
            scaled_len = self.MINIMAL_CHANNEL_LEN
        if scaled_len > len(self.channel):
            scaled_len = len(self.channel)
        return scaled_len

    def get_vertical_grid_coordinates(self):
        return FramesGridUtils.get_steps_coordinates(self.start_frame, self.finish_frame, self.grid_density)

    def draw_vertical_grid(self):
        frame_numbers = self.get_vertical_grid_coordinates()
        grid_lines = [self._get_vertical_line(frame_number) for frame_number in frame_numbers]
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(104, 104, 82, 80)))
        Channel._draw_lines(grid_lines, painter)

    def _get_vertical_line(self, frame_number):
        if self.start_frame <= frame_number <= self.finish_frame:
            frame_relative = frame_number - self.start_frame
            frame_window = self.finish_frame - self.start_frame
            width_coefficient = self.width() / frame_window
            return QtCore.QLineF(QtCore.QPointF(width_coefficient * frame_relative, 0),
                                 QtCore.QPointF(width_coefficient * frame_relative, self.height()))

    def _draw_lines_by_points(self, points):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(0, 0, 0))
        for i in range(len(points) - 1):
            Channel._draw_line(points[i], points[i + 1], painter)

    @staticmethod
    def _get_bound_scaled(bound, mid_frame, scale_factor):
        prev_bound_dist = mid_frame - bound
        new_bound_dist = prev_bound_dist * scale_factor
        return int(mid_frame - new_bound_dist)

    @staticmethod
    def _draw_lines(lines, painter):
        for line in lines:
            painter.drawLine(line)

    @staticmethod
    def _draw_line(start, finish, painter):
        painter.drawLine(QtCore.QLineF(start, finish))