from PyQt4 import QtGui, QtCore
from Core.WaveState.WaveState import WaveState
from View.EffectsParamsWidgets.ChangeSpeedParamsWidget import ChangeSpeedParamsWidget
from View.EffectsParamsWidgets.FadeInParamsWidget import FadeInParamsWidget
from View.EffectsParamsWidgets.FadeOutParamsWidget import FadeOutParamsWidget
from View.Track import Track
# import vlc
import sys
from ViewModel.TrackModel import TrackModel
from ViewModel.ViewModel import ViewModel


class Window(QtGui.QMainWindow):
    OPPOSITE_TEXT = {"On": "Off", "Off": "On"}

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Sound editor")
        self.view_model = ViewModel()
        self.view_model.call_after_change.append(self.repaint)

        self.statusBar()

        main_menu = self.menuBar()
        self.file_menu = main_menu.addMenu('&File')
        self.edit_menu = main_menu.addMenu('&Edit')

        self.add_menu_item(self.file_menu, "&Open", self.open_file, QtGui.QKeySequence.Open)
        self.add_menu_item(self.edit_menu, "&Copy", self.view_model.copy, QtGui.QKeySequence.Copy)
        self.add_menu_item(self.edit_menu, "&Paste", self.view_model.paste, QtGui.QKeySequence.Paste)
        self.add_menu_item(self.edit_menu, "&Delete", self.view_model.delete, QtGui.QKeySequence.Delete)
        self.add_menu_item(self.edit_menu, "&Reverse", self.view_model.reverse, QtGui.QKeySequence("Ctrl+R"))
        self.add_menu_item(self.edit_menu, "&Select all", self.view_model.select_all, QtGui.QKeySequence.SelectAll)
        self.add_menu_item(self.edit_menu, "&Paste to new track", self.paste_to_new_track, QtGui.QKeySequence.New)
        self.add_menu_item(self.edit_menu, "&Sum active tracks", self.add_sum, QtGui.QKeySequence("Alt+S"))

        self.scroll_layout = QtGui.QFormLayout()

        self.scroll_widget = QtGui.QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.setCentralWidget(self.scroll_area)
        self.show()

    def create_menu_item_action(self, name, func, shortcut):
        menu_item_action = QtGui.QAction(name, self)
        menu_item_action.triggered.connect(func)
        menu_item_action.setShortcut(shortcut)
        return menu_item_action

    def add_menu_item(self, menu, name, func, shortcut):
        action = self.create_menu_item_action(name, func, shortcut)
        menu.addAction(action)

    def save_master_to_file(self):
        pass

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName()
        if file_name != "":
            wave_state = WaveState.read_from_file(file_name)
            track_model = TrackModel(wave_state, self.view_model)
            self.add_track_model(track_model)

    def paste_to_new_track(self):
        track_model = self.view_model.get_pasted_to_new_track_model()
        self.add_track_model(track_model)

    def add_track_model(self, track_model):
        self.view_model.add_track_model(track_model)
        track = Track(track_model, self)
        track.actions_panel.add_effect("Fade in", FadeInParamsWidget(track_model))
        track.actions_panel.add_effect("Fade out", FadeOutParamsWidget(track_model))
        track.actions_panel.add_effect("Change speed", ChangeSpeedParamsWidget(track_model))
        add_button = track.actions_panel.add_button
        add_button("Delete", lambda: self.delete_track(track))
        add_button("Save", lambda: self.save_to_file(track_model.wave_state))
        add_button("Adjust loudness", lambda: self.adjust_loudness(track_model))
        on_off_button = QtGui.QPushButton("On")
        on_off_button.clicked.connect(lambda: self.switch_on_off(track_model, on_off_button))
        track.actions_panel.add_action_view(on_off_button)

        # on_off_button = QtGui.QPushButton("On")
        # TODO: write button and connect it with some action

        self.scroll_layout.addRow(track)

    def delete_track(self, track):
        self.scroll_layout.removeWidget(track)
        self.view_model.delete_track_model(track.track_model)
        track.close()

    def adjust_loudness(self, track_model):
        dialog = QtGui.QInputDialog(self)
        ratio_and_bool = dialog.getDouble(self, "Adjust loudness", "Input ratio:", 1)
        if ratio_and_bool[1]:
            track_model.adjust_loudness(ratio_and_bool[0])

    def switch_on_off(self, track_model, button):
        track_model.is_active = not track_model.is_active
        button.setText(self.OPPOSITE_TEXT[button.text()])

    def add_sum(self):
        wave_state = self.view_model.get_sum()
        track_model = TrackModel(wave_state, self.view_model)
        self.add_track_model(track_model)

    @staticmethod
    def save_to_file(wave_state):
        file_name = QtGui.QFileDialog.getSaveFileName()
        if file_name != "":
            wave_state.save_to_file(file_name)
