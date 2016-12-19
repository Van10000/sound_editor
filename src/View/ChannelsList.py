from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.WaveState import WaveState
from View.Channel import Channel
from View.Constants import Constants
from View.ActionsPanel import ActionsPanel
from View.TimePanel import TimePanel


class ChannelsList(QtGui.QWidget):
    def __init__(self, track_model, parent=None):
        super(ChannelsList, self).__init__(parent)
        self.track_model = track_model

        self.channels = [Channel(ch_model)
                         for ch_model in self.track_model.channel_models]
        for channel, channel_model in zip(self.channels, self.track_model.channel_models):
            channel_model.call_after_change.append(channel.repaint)

        self.time_panel = TimePanel(self.channels[0])
        self.track_model.call_after_change.append(self.time_panel.repaint)

        self.channels_layout = QtGui.QVBoxLayout()
        self.channels_layout.addWidget(self.time_panel)
        for channel in self.channels:
            self.channels_layout.addWidget(channel)

        self.wrapping_widget = QtGui.QWidget()
        self.wrapping_widget.setLayout(self.channels_layout)
        self.wrapping_widget.setStyleSheet(Constants.TRACK_BACKGROUND_COLOR)

        self.wrapping_layout = QtGui.QFormLayout()
        self.wrapping_layout.addRow(self.wrapping_widget)
        self.setLayout(self.wrapping_layout)

    def update_track(self):
        for channel, channel_model in zip(self.channels, self.track_model.channel_models):
            channel.reset_channel_model(channel_model)
        self.time_panel.reset_channel(self.channels[0])