import sys

from PyQt4 import QtGui

from View import Window


dir = r"C:\Users\ISmir\Desktop\учёба\2 курс\python\sound_editor\sounds" + "\\"

# state = WaveState.WaveState.read_from_file(dir + "small.wav")
# new_state = WaveState.WaveState.read_from_file(dir + "temp_small.wav")
# merged = state.get_appended(new_state)
# merged.output_to_file(dir + "merged.wav")
app = QtGui.QApplication(sys.argv)
main_window = Window.Window()
sys.exit(app.exec_())
