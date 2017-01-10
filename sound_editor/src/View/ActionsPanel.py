from PyQt4 import QtGui, QtCore
from View import Constants
from View.EffectsDialog import EffectsDialog


class ActionsPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ActionsPanel, self).__init__(parent)
        self.effects_names = []
        self.effects_widgets = []
        self.actions_layout = QtGui.QFormLayout()
        self.effect_button = QtGui.QPushButton("Effect")
        self.effect_button.clicked.connect(self.show_effects_dialog)
        self.actions_layout.addRow(self.effect_button)

        self.wrapping_widget = QtGui.QWidget()
        self.wrapping_widget.setStyleSheet(Constants.TRACK_BACKGROUND_COLOR)
        self.wrapping_widget.setLayout(self.actions_layout)

        self.wrapping_layout = QtGui.QVBoxLayout()
        self.wrapping_layout.addWidget(self.wrapping_widget)

        self.setLayout(self.wrapping_layout)

        self.setFixedWidth(150)
        self.setMinimumWidth(150)

    def show_effects_dialog(self):
        for widget in self.effects_widgets:
            widget.validate()
        effects_dialog = EffectsDialog(self.effects_names,
                                       self.effects_widgets,
                                       self.parent())
        effects_dialog.show()

    def add_effect(self, name, widget):
        self.effects_names.append(name)
        self.effects_widgets.append(widget)

    def add_action_view(self, actions_view):
        self.actions_layout.addRow(actions_view)

    def add_button(self, name, action):
        button = QtGui.QPushButton(name)
        button.clicked.connect(action)
        self.add_action_view(button)
        return button
