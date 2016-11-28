from PyQt4 import QtGui, QtCore
from pyqtgraph import PlotWidget, PlotDataItem, ViewBox
from Core.CapturedAreaContainer import CapturedAreaContainer
from Core.WaveState import WaveState


from View.Channel import Channel
from View.ChannelsList import ChannelsList
from View.Constants import Constants
from View.EffectsPanel import EffectsPanel


class Track(QtGui.QWidget):

    def __init__(self, wave_state, on_delete=None, parent=None):
        super(Track, self).__init__(parent)
        self.waveState = wave_state
        self.captured_area_container = CapturedAreaContainer()

        self.channels_list = ChannelsList(self.waveState, self.captured_area_container)

        self.captured_area_container.on_change = self.channels_list.repaint

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