from PyQt4 import QtGui


class NamedLineEdit(QtGui.QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.line_edit = QtGui.QLineEdit()
        self.name = QtGui.QLabel(name)
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.addWidget(self.name)
        self.main_layout.addWidget(self.line_edit)
        self.setLayout(self.main_layout)