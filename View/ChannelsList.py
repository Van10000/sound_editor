from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.WaveState import WaveState
from View.Channel import Channel
from View.Constants import Constants
from View.EffectsPanel import EffectsPanel
from View.TimePanel import TimePanel


class ChannelsList(QtGui.QWidget):
    def __init__(self, wave_state, captured_area_container, parent=None):
        super(ChannelsList, self).__init__(parent)
        self.waveState = wave_state

        self.channels = [Channel(ch, wave_state.sample_width, wave_state.frame_rate, captured_area_container)
                         for ch in wave_state.channels]
        self.time_panel = TimePanel(self.channels[0])

        self.channels_layout = QtGui.QVBoxLayout()
        self.channels_layout.addWidget(self.time_panel)
        for channel in self.channels:
            self.channels_layout.addWidget(channel)

        self.wrapping_widget = QtGui.QWidget()
        self.wrapping_widget.setLayout(self.channels_layout)
        self.wrapping_widget.setStyleSheet(Constants.TRACK_BACKGROUND_COLOR)

        self.wrapping_layout = QtGui.QFormLayout()
        self.wrapping_layout.addWidget(self.wrapping_widget)
        self.setLayout(self.wrapping_layout)

    def scale(self, x_mid_ratio, scale_factor):
        for channel in self.channels:
            frame_len = channel.finish_frame - channel.start_frame
            frame_mid = channel.start_frame + frame_len * x_mid_ratio
            channel.scale(frame_mid, scale_factor)
        self.time_panel.repaint()

    def wheelEvent(self, event):
        scale_factor = 1.15
        if event.delta() > 0:
            scale_factor = 1 / scale_factor
        click_location_ratio = event.x() / self.width()
        self.scale(click_location_ratio, scale_factor)