from PyQt4 import QtGui, QtCore
from Core.WaveState.WaveState import WaveState
from View.Track import Track
# import vlc
import sys
from ViewModel.TrackModel import TrackModel
from ViewModel.ViewModel import ViewModel


class Window(QtGui.QMainWindow):

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

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName()
        wave_state = WaveState.read_from_file(file_name)
        track_model = TrackModel(wave_state, self.view_model)
        self.view_model.add_track_model(track_model)
        track = Track(track_model, on_delete=self.delete_track)
        self.scroll_layout.addRow(track)

    def delete_track(self, track):
        self.scroll_layout.removeWidget(track)
        self.view_model.delete_track_model(track.track_model)
        track.close()
