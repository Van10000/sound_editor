from PyQt4 import QtGui
from View.EffectsParamsWidgets.EffectParamsWidget import EffectParamsWidget
from View.Utils.NamedLineEdit import NamedLineEdit


class FadeParamsWidget(EffectParamsWidget):
    def __init__(self, track_model, parent=None):
        super().__init__(parent)
        self.track_model = track_model
        self.start_time_line = NamedLineEdit("start time")
        self.finish_time_line = NamedLineEdit("finish time")
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.addRow(self.start_time_line)
        self.main_layout.addRow(self.finish_time_line)
        self.setLayout(self.main_layout)
        self.setMinimumWidth(50)
        self.setMinimumHeight(50)

    @property
    def start_time_text(self):
        return self.start_time_line.line_edit.text()

    @property
    def finish_time_text(self):
        return self.finish_time_line.line_edit.text()

    def __str__(self):
        return "start time:{}, finish_time:{}".format(self.start_time_text,
                                                      self.finish_time_text)

    def set_bounds(self):
        start_frame, finish_frame = self.track_model.get_captured_start_and_finish()
        self.set_bounds_frame(start_frame, finish_frame)

    def set_bounds_frame(self, start_frame, finish_frame):
        start_time = self.track_model.get_time_from_frame(start_frame)
        finish_time = self.track_model.get_time_from_frame(finish_frame)
        self.set_bounds_time(start_time, finish_time)

    def set_bounds_time(self, start_time, finish_time):
        self.start_time_line.line_edit.setText(str(start_time))
        self.finish_time_line.line_edit.setText(str(finish_time))

    def apply_fade(self, fade_func):
        try:
            start_time = int(round(float(self.start_time_text)))
            finish_time = int(round(float(self.finish_time_text)))
        except ValueError:
            message_box = QtGui.QMessageBox()
            message_box.warning(self.parent(), "Fade wasn't applied", "Time should be a decimal number")
            return False
        else:
            start_frame = self.track_model.get_frame_from_time(start_time)
            finish_frame = self.track_model.get_frame_from_time(finish_time)
            fade_func(start_frame, finish_frame)
            return True

    def validate(self):
        self.set_bounds()