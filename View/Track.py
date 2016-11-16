from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.WaveState import WaveState


# By now consider there's only one channel
from View.Channel import Channel


class Track(QtGui.QWidget):
    BACKGROUND_COLOR = "background-color: rgb(200, 200, 200);"

    def __init__(self, wave_state, parent=None):
        super(Track, self).__init__(parent)
        self.waveState = wave_state

        self.channels = [Channel(ch, wave_state.sample_width, self) for ch in wave_state.channels]

        self.channels_layout = QtGui.QVBoxLayout()
        for channel in self.channels:
            self.channels_layout.addWidget(channel)

        self.wrapping_widget = QtGui.QWidget()
        self.wrapping_widget.setStyleSheet(Track.BACKGROUND_COLOR)
        self.wrapping_widget.setLayout(self.channels_layout)

        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addWidget(self.wrapping_widget)
        self.setLayout(self.horizontal_layout)

        # self.plot = PlotWidget(self)
        # plot_item = self.plot.getPlotItem()
        # plot_item.getViewBox().scaleBy(x=1, y=0.05)
        # # plot_item.getViewBox().enableAutoRange(axis=ViewBox.XAxis, enable=True)
        # plot_item.addItem(PlotDataItem(wave_state.channels[0]))
        # plot_item.setDownsampling(auto=True, mode='peak')
        # self.plot.resize(500, 200)