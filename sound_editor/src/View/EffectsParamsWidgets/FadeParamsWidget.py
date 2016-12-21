from PyQt4 import QtGui
from View.EffectsParamsWidgets.EffectParamsWidget import EffectParamsWidget
from View.Utils.NamedLineEdit import NamedLineEdit
from View.Utils.TimeInputWidget import TimeInputWidget


class FadeParamsWidget(EffectParamsWidget):
    def __init__(self, track_model, parent=None):
        super().__init__(parent)
        self.track_model = track_model
        self.time_input = TimeInputWidget(self.parent())
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.addRow(self.time_input)
        self.setLayout(self.main_layout)

    def set_bounds(self):
        start_frame, finish_frame = self.track_model.get_captured_start_and_finish()
        self.set_bounds_frame(start_frame, finish_frame)

    def set_bounds_frame(self, start_frame, finish_frame):
        start_time = self.track_model.get_time_from_frame(start_frame)
        finish_time = self.track_model.get_time_from_frame(finish_frame)
        self.time_input.set_bounds_time(start_time, finish_time)

    def apply_fade(self, fade_func):
        start_time, finish_time = self.time_input.get_bounds_time()
        start_frame, finish_frame = map(self.track_model.get_frame_from_time,
                                        (start_time, finish_time,))
        fade_func(start_frame, finish_frame)
        return True

    def validate(self):
        self.set_bounds()