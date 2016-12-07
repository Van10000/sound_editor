import functools

from PyQt4 import QtGui, QtCore

from ViewModel.ViewUtils.FramesGridUtils import FramesGridUtils
from ViewModel.ViewUtils.PowOfTwoChannelCompressor import PowOfTwoChannelCompressor


class Channel(QtGui.QWidget):
    CAPTURED_AREA_COLOR = QtGui.QColor(16, 50, 245, 80)
    GRID_COLOR = QtGui.QColor(104, 104, 82, 50)
    _ONE_VERTICAL_GRID_LINE_SIZE = 60

    def __init__(self, channel_model, parent=None):
        super(Channel, self).__init__(parent)
        self.parent = parent
        self.channel_model = channel_model
        self.setMinimumSize(100, 100)

    @property
    def grid_density(self):
        return int(self.width() / Channel._ONE_VERTICAL_GRID_LINE_SIZE)

    @property
    def captured_area_container(self):
        return self.channel_model.captured_area_container

    def get_frame_number_from_coordinate(self, x_coordinate):
        ratio = x_coordinate / self.width()
        return self.channel_model.get_frame_number_from_ratio(ratio)

    def get_coordinate_from_frame_number(self, frame_number):
        ratio = self.channel_model.get_ratio_from_frame_number(frame_number)
        return ratio * self.width()

    def paintEvent(self, paint_event):
        frame_values = self.channel_model.get_compressed_channel()

        width_coefficient = self.width() / len(frame_values)
        height_coefficient = self.height() / self.channel_model.numbers_range
        points = []

        for i in range(len(frame_values)):
            x_coord = width_coefficient * i
            y_coord = (self.channel_model.zero_amplitude - frame_values[i]) * height_coefficient
            points.append(QtCore.QPointF(x_coord, y_coord))

        self.fill_captured_area()
        self.draw_vertical_grid()
        self._draw_lines_by_points(points)

    def scale(self, mid_frame, scale_factor):
        self.channel_model.scale(mid_frame, scale_factor)
        self.repaint()

    def fill_captured_area(self):
        if self.captured_area_container.is_captured:
            self.fill_background(self.get_coordinate_from_frame_number(self.captured_area_container.start),
                                 self.get_coordinate_from_frame_number(self.captured_area_container.finish),
                                 Channel.CAPTURED_AREA_COLOR)

    def fill_background(self, start_x, finish_x, color):
        painter = QtGui.QPainter(self)
        width = finish_x - start_x + 1
        painter.fillRect(start_x, 0, width, self.height(), QtGui.QBrush(color))

    def draw_vertical_grid(self):
        frame_numbers = self.channel_model.get_vertical_grid_frames(self.grid_density)
        frame_coordinates = [self.get_coordinate_from_frame_number(frame_number)
                             for frame_number in frame_numbers]
        grid_lines = [self._get_vertical_line(frame_coordinate)
                      for frame_coordinate in frame_coordinates]
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(Channel.GRID_COLOR))
        Channel._draw_lines(grid_lines, painter)

    def _get_vertical_line(self, coordinate):
        return QtCore.QLineF(QtCore.QPointF(coordinate, 0),
                             QtCore.QPointF(coordinate, self.height()))

    def _draw_lines_by_points(self, points):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(0, 0, 0))
        for i in range(len(points) - 1):
            Channel._draw_line(points[i], points[i + 1], painter)

    @staticmethod
    def _draw_lines(lines, painter):
        for line in lines:
            painter.drawLine(line)

    @staticmethod
    def _draw_line(start, finish, painter):
        painter.drawLine(QtCore.QLineF(start, finish))

    def reset_channel_model(self, channel_model):
        self.channel_model = channel_model

    def mousePressEvent(self, event):
        self.captured_area_container.drop()
        if event.button() == QtCore.Qt.LeftButton:
            frame_number = self.get_frame_number_from_coordinate(event.x())
            self.captured_area_container.capture(frame_number)

    def mouseMoveEvent(self, event):
        frame_number = self.get_frame_number_from_coordinate(event.x())
        self.captured_area_container.move(frame_number)

    def mouseReleaseEvent(self, event):
        frame_number = self.get_frame_number_from_coordinate(event.x())
        self.captured_area_container.move(frame_number)
        self.captured_area_container.release()

    def wheelEvent(self, event):
        scale_factor = 1.15
        if event.delta() > 0:
            scale_factor = 1 / scale_factor
        click_location_ratio = event.x() / self.width()
        self.channel_model.track_model.scale(click_location_ratio, scale_factor)