from PyQt4 import QtGui
from View.Utils.NamedLineEdit import NamedLineEdit


class TimeInputWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_time_line = NamedLineEdit("start time")
        self.finish_time_line = NamedLineEdit("finish time")
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.addRow(self.start_time_line)
        self.main_layout.addRow(self.finish_time_line)
        self.setLayout(self.main_layout)
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

    @property
    def start_time_text(self):
        return self.start_time_line.line_edit.text()

    @property
    def finish_time_text(self):
        return self.finish_time_line.line_edit.text()

    def set_bounds_time(self, start_time, finish_time):
        self.start_time_line.line_edit.setText(str(start_time))
        self.finish_time_line.line_edit.setText(str(finish_time))

    def get_bounds_time(self):
        try:
            return float(self.start_time_text), float(self.finish_time_text)
        except ValueError:
            message_box = QtGui.QMessageBox()
            message_box.warning(self.parent(), "Wrong input",
                                "Time should be a decimal number")
            return False
