from PyQt4 import QtGui, QtCore
from Core.FramesGridUtils import FramesGridUtils
from Core.PowOfTwoChannelCompressor import PowOfTwoChannelCompressor
from Core.SmartChannelCompressor import SmartChannelCompressor
import functools


class Channel(QtGui.QWidget):
    MINIMAL_CHANNEL_LEN = 100
    CAPTURED_AREA_COLOR = QtGui.QColor(16, 50, 245, 80)
    GRID_COLOR = QtGui.QColor(104, 104, 82, 50)
    _ONE_VERTICAL_GRID_LINE_SIZE = 60

    def __init__(self, channel, sample_width, frame_rate, captured_area_container, parent=None):
        super(Channel, self).__init__(parent)
        self.channel_compressed = PowOfTwoChannelCompressor(channel, 1000)
        self.captured_area_container = captured_area_container
        self.frame_rate = frame_rate
        self.channel = channel
        self.grid_density = 0
        self.recalculate_grid_density()
        self.numbers_range = 256 ** sample_width
        self.start_frame = 0
        self.finish_frame = len(channel)
        self.setMinimumSize(100, 100)

    def __len__(self):
        return self.finish_frame - self.start_frame

    @property
    def zero_amplitude(self):
        return self.numbers_range // 2

    def get_time_from_frame(self, frame_number):
        return frame_number / self.frame_rate

    def get_frame_from_coordinate(self, x_coordinate):
        ratio = x_coordinate / self.width()
        relative_frame = len(self) * ratio
        return int(self.start_frame + relative_frame)

    def get_coordinate_from_frame(self, frame):
        if frame < self.start_frame:
            return 0
        if frame >= self.finish_frame:
            return self.width()
        relative_frame = frame - self.start_frame
        ratio = relative_frame / len(self)
        return ratio * self.width()

    @property
    def start_frame_time(self):
        return self.get_time_from_frame(self.start_frame)

    @property
    def finish_frame_time(self):
        return self.get_time_from_frame(self.finish_frame)

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
        if self.captured_area_container.is_captured:
            self.fill_background(self.get_coordinate_from_frame(self.captured_area_container.start),
                                 self.get_coordinate_from_frame(self.captured_area_container.finish),
                                 Channel.CAPTURED_AREA_COLOR)
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

    def get_vertical_grid_frames(self):
        return FramesGridUtils.get_steps_coordinates(self.start_frame, self.finish_frame, self.grid_density)

    def fill_background(self, start_x, finish_x, color):
        painter = QtGui.QPainter(self)
        width = finish_x - start_x + 1
        painter.fillRect(start_x, 0, width, self.height(), QtGui.QBrush(color))

    def draw_vertical_grid(self):
        frame_numbers = self.get_vertical_grid_frames()
        grid_lines = [self._get_vertical_line(frame_number) for frame_number in frame_numbers]
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(Channel.GRID_COLOR))
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

    def recalculate_grid_density(self):
        self.grid_density = int(self.width() / Channel._ONE_VERTICAL_GRID_LINE_SIZE)

    def mousePressEvent(self, event):
        self.captured_area_container.drop()
        if event.button() == QtCore.Qt.LeftButton:
            self.captured_area_container.capture(self.get_frame_from_coordinate(event.x()))

    def mouseMoveEvent(self, event):
        if self.captured_area_container.is_captured:
            self.captured_area_container.move(self.get_frame_from_coordinate(event.x()))

    def mouseReleaseEvent(self, event):
        self.captured_area_container.move(self.get_frame_from_coordinate(event.x()))
        self.captured_area_container.release()

    def resizeEvent(self, event):
        self.recalculate_grid_density()