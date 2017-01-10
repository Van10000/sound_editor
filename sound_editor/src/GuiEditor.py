import sys

from PyQt4 import QtGui
from View import Window

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = Window.Window()
    sys.exit(app.exec_())
