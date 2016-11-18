from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.WaveState import WaveState


from View.Channel import Channel
from View.ChannelsList import ChannelsList
from View.Constants import Constants
from View.EffectsPanel import EffectsPanel


class Track(QtGui.QWidget):

    def __init__(self, wave_state, on_delete=None, parent=None):
        super(Track, self).__init__(parent)
        self.waveState = wave_state

        self.channels_list = ChannelsList(self.waveState)

        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addWidget(self.channels_list)
        self.horizontal_layout.addWidget(EffectsPanel(self))

        if on_delete is not None:
            self.delete_button = QtGui.QPushButton("Delete")
            self.delete_button.clicked.connect(lambda: on_delete(self))
            self.delete_button.setFixedWidth(50)
            self.delete_button.setMinimumWidth(50)
            self.horizontal_layout.addWidget(self.delete_button)

        self.setLayout(self.horizontal_layout)

        # self.plot = PlotWidget(self)
        # plot_item = self.plot.getPlotItem()
        # plot_item.getViewBox().scaleBy(x=1, y=0.05)
        # # plot_item.getViewBox().enableAutoRange(axis=ViewBox.XAxis, enable=True)
        # plot_item.addItem(PlotDataItem(wave_state.channels[0]))
        # plot_item.setDownsampling(auto=True, mode='peak')
        # self.plot.resize(500, 200)