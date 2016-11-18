from PyQt4 import QtGui, QtCore
from View.Constants import Constants


class EffectsPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(EffectsPanel, self).__init__(parent)
        self.effects_layout = QtGui.QFormLayout()
        self.add_effect_button = QtGui.QPushButton("Add effect")
        self.effects_layout.addRow(self.add_effect_button)

        self.wrapping_widget = QtGui.QWidget()
        self.wrapping_widget.setStyleSheet(Constants.TRACK_BACKGROUND_COLOR)
        self.wrapping_widget.setLayout(self.effects_layout)

        self.wrapping_layout = QtGui.QVBoxLayout()
        self.wrapping_layout.addWidget(self.wrapping_widget)

        self.setLayout(self.wrapping_layout)

        self.setFixedWidth(150)
        self.setMinimumWidth(150)

    def add_effect(self, effect_view):
        self.effects_layout.addRow(effect_view)