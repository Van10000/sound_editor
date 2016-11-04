from PyQt4 import QtGui, QtCore
from Core.WaveState import WaveState
from View.Track import Track
import sys


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Sound editor")

        open_file_action = QtGui.QAction("&Open", self)
        open_file_action.triggered.connect(self.open_file)

        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(open_file_action)

        self.show()

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName()
        wave_state = WaveState.read_from_file(file_name)
        track = Track(wave_state, self)
        track.setGeometry(0, 50, 1000, 1000)
        # layout = QtGui.QVBoxLayout()
        # layout.addWidget(track)
        track.show()

