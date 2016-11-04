from PyQt4 import QtGui, QtCore
from Core.SmartChannelCompressor import SmartChannelCompressor
import functools


class Channel(QtGui.QWidget):
    MINIMAL_CHANNEL_LEN = 100

    def __init__(self, channel, sample_width, parent=None):
        super(Channel, self).__init__(parent)
        self.channel_compressed = SmartChannelCompressor(channel, 1000)
        self.channel = channel
        self.numbers_range = 256 ** sample_width
        self.start_frame = 0
        self.finish_frame = len(channel)

    def __len__(self):
        return self.finish_frame - self.start_frame

    @property
    def zero_amplitude(self):
        return self.numbers_range // 2

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
        frame_values = self \
            .channel_compressed \
            .get_compressed_smart(self.start_frame, self.finish_frame)

        width_coefficient = self.width() / len(frame_values)
        height_coefficient = self.height() / self.numbers_range
        for i in range(len(frame_values) - 1):
            start = QtCore.QPointF(width_coefficient * i,
                                   (self.zero_amplitude - frame_values[i]) * height_coefficient)
            finish = QtCore.QPointF(width_coefficient * (i + 1),
                                    (self.zero_amplitude - frame_values[i + 1]) * height_coefficient)
            self._draw_line(start, finish, painter)

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
        self.start_frame = get_bound_scaled(self.start_frame)
        self.finish_frame = get_bound_scaled(self.finish_frame)
        self.repaint()

    def wheelEvent(self, event):
        scale_factor = 1.15
        if event.delta() > 0:
            scale_factor = 1 / scale_factor
        self.scale(len(self.channel) // 2, scale_factor)
        self.repaint()
        # def mouseMoveEvent(self, event):
        # if event.buttons() == QtCore.Qt.MidButton:

    def _get_scaled_len(self, scale_factor):
        scaled_len = scale_factor * len(self)
        if scaled_len < self.MINIMAL_CHANNEL_LEN:
            scaled_len = self.MINIMAL_CHANNEL_LEN
        if scaled_len > len(self.channel):
            scaled_len = len(self.channel)
        return scaled_len

    @staticmethod
    def _get_bound_scaled(bound, mid_frame, scale_factor):
        prev_bound_dist = mid_frame - bound
        new_bound_dist = prev_bound_dist * scale_factor
        return int(mid_frame - new_bound_dist)

    @staticmethod
    def _draw_line(start, finish, painter):
        painter.drawLine(QtCore.QLineF(start, finish))