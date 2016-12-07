from PyQt4 import QtGui

from ViewModel.ViewUtils.CapturedAreaContainer import CapturedAreaContainer
from View.ChannelsList import ChannelsList
from View.EffectsPanel import EffectsPanel


class Track(QtGui.QWidget):

    def __init__(self, track_model, on_delete=None, parent=None):
        super(Track, self).__init__(parent)
        track_model.call_after_wave_state_changed.append(self.update_track)
        track_model.call_after_change.append(self.repaint)
        self.track_model = track_model
        self.on_delete = on_delete

        self.channels_list = ChannelsList(self.track_model)
        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addWidget(self.channels_list)
        self.horizontal_layout.addWidget(EffectsPanel(self))

        if self.on_delete is not None:
            delete_button = QtGui.QPushButton("Delete")
            delete_button.clicked.connect(lambda: self.on_delete(self))
            delete_button.setFixedWidth(50)
            delete_button.setMinimumWidth(50)
            self.horizontal_layout.addWidget(delete_button)

        self.setLayout(self.horizontal_layout)

    def update_track(self):
        self.channels_list.update_track()