from PyQt4 import QtGui


class EffectsDialog(QtGui.QDialog):
    def __init__(self, effects_names, effects_widgets, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.effects_names = effects_names
        self.effects_widgets = effects_widgets
        self.combo_box = QtGui.QComboBox(self)
        self.combo_box.addItems(effects_names)
        self.combo_box.activated[int].connect(self.switch_effect)
        self.current_effect_index = 0
        self.combo_box.setCurrentIndex(self.current_effect_index)
        self.effects_layout = QtGui.QFormLayout()
        self.effects_layout.addRow(self.combo_box)
        self.effects_layout.addRow(effects_widgets[self.current_effect_index])
        self.main_effects_widget = QtGui.QWidget()
        self.main_effects_widget.setLayout(self.effects_layout)
        self.apply_button = QtGui.QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_effect)
        self.main_layout = QtGui.QFormLayout()
        self.main_layout.addRow(self.main_effects_widget)
        self.main_layout.addRow(self.apply_button)
        self.setLayout(self.main_layout)

    def switch_effect(self, selected_effect_index):
        self.effects_layout.removeWidget(self.effects_widgets[self.current_effect_index])
        self.effects_widgets[self.current_effect_index].hide()
        self.effects_layout.addRow(self.effects_widgets[selected_effect_index])
        self.effects_widgets[selected_effect_index].show()
        self.current_effect_index = selected_effect_index

    def apply_effect(self):
        if self.effects_widgets[self.current_effect_index].apply_effect():
            self.hide()

