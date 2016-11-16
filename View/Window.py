from PyQt4 import QtGui, QtCore
from Core.WaveState import WaveState
from View import TracksArea
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
        track = Track(wave_state)
        self.scroll_layout.addRow(track)

