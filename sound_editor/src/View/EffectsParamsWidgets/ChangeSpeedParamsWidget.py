from PyQt4 import QtGui
from View.EffectsParamsWidgets.EffectParamsWidget import EffectParamsWidget
from View.Utils.NamedLineEdit import NamedLineEdit
from View.Utils.TimeInputWidget import TimeInputWidget


class ChangeSpeedParamsWidget(EffectParamsWidget):
    def __init__(self, track_model, parent=None):
        super().__init__(parent)
        self.track_model = track_model
        self.time_input = TimeInputWidget(self.parent())
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.addRow(self.time_input)
        self.speed_ratio_input = NamedLineEdit("speed ratio")
        self.main_layout.addRow(self.speed_ratio_input)
        self.setLayout(self.main_layout)

    def set_bounds(self):
        start_frame, finish_frame = self.track_model.get_captured_start_and_finish()
        self.set_bounds_frame(start_frame, finish_frame)

    def set_bounds_frame(self, start_frame, finish_frame):
        start_time = self.track_model.get_time_from_frame(start_frame)
        finish_time = self.track_model.get_time_from_frame(finish_frame)
        self.time_input.set_bounds_time(start_time, finish_time)

    def validate(self):
        self.set_bounds()
        self.speed_ratio_input.line_edit.setText("1")

    def apply_effect(self):
        start_time, finish_time = self.time_input.get_bounds_time()
        try:
            ratio = float(self.speed_ratio_input.line_edit.text())
        except ValueError:
            message_box = QtGui.QMessageBox()
            message_box.warning(self.parent(), "Wrong input", "Speed ratio should be a decimal number")
            return False
        else:
            start_frame, finish_frame = map(self.track_model.get_frame_from_time,
                                            (start_time, finish_time,))
            self.track_model.change_speed(start_frame, finish_frame, ratio)
            return True