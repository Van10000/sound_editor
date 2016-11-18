from PyQt4 import QtGui, QtCore
from Core.WaveState import WaveState
from View.Track import Track
# import vlc
import sys


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Sound editor")

        open_file_action = QtGui.QAction("&Open", self)
        open_file_action.triggered.connect(self.open_file)
        open_file_action.setShortcut(QtGui.QKeySequence.Open)

        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(open_file_action)

        self.scroll_layout = QtGui.QFormLayout()

        self.scroll_widget = QtGui.QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.setCentralWidget(self.scroll_area)
        self.show()

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName()
        wave_state = WaveState.read_from_file(file_name)
        track = Track(wave_state, on_delete=self.delete_track)
        self.scroll_layout.addRow(track)

    def delete_track(self, track):
        self.scroll_layout.removeWidget(track)
        track.close()
