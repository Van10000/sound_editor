from PyQt4 import QtGui, QtCore


class TracksArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TracksArea, self).__init__(parent)
        self.setLayout(QtGui.QVBoxLayout())

    def add_track(self, track):
        pass
        self.show()