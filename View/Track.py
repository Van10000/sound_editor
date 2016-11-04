from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.WaveState import WaveState


# By now consider there's only one channel
from View.Channel import Channel


class Track(QtGui.QWidget):
    def __init__(self, wave_state, parent=None):
        super(Track, self).__init__(parent)
        self.waveState = wave_state

        print("sample_width:{}".format(wave_state.sample_width))
        self.channel = Channel(wave_state.channels[0], wave_state.sample_width, self)
        self.channel.resize(500, 200)
        # self.plot = PlotWidget(self)
        # plot_item = self.plot.getPlotItem()
        # plot_item.getViewBox().scaleBy(x=1, y=0.05)
        # # plot_item.getViewBox().enableAutoRange(axis=ViewBox.XAxis, enable=True)
        # plot_item.addItem(PlotDataItem(wave_state.channels[0]))
        # plot_item.setDownsampling(auto=True, mode='peak')
        # self.plot.resize(500, 200)

    def paintEvent(self, paint_event):
        self.channel.paintEvent(paint_event)
        # self.plot.paintEvent(paint_event)