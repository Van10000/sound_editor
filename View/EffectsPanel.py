from PyQt4 import QtGui, QtCore


class EffectsPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(EffectsPanel, self).__init__(parent)
        self.setLayout(QtGui.QVBoxLayout())