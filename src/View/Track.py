from PyQt4 import QtGui

from ViewModel.ViewUtils.CapturedAreaContainer import CapturedAreaContainer
from View.ChannelsList import ChannelsList
from View.ActionsPanel import ActionsPanel


class Track(QtGui.QWidget):

    def __init__(self, track_model, parent=None):
        super(Track, self).__init__(parent)
        track_model.call_after_wave_state_changed.append(self.update_track)
        track_model.call_after_change.append(self.repaint)
        self.track_model = track_model

        self.channels_list = ChannelsList(self.track_model)
        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addWidget(self.channels_list)
        self.actions_panel = ActionsPanel(self.parent())
        self.horizontal_layout.addWidget(self.actions_panel)

        self.setLayout(self.horizontal_layout)

    def update_track(self):
        self.channels_list.update_track()

    def switch_on_off(self):
        self.track_model.is_active = not self.track_model.is_active
        # TODO: change button view somehow