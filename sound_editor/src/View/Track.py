from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSound
import os
import tempfile
from View.ChannelsList import ChannelsList
from View.ActionsPanel import ActionsPanel
import time


class Track(QtGui.QWidget):
    UPDATE_PLAYING_TRACK_TIME = 100

    def __init__(self, track_model, window):
        super(Track, self).__init__(window)
        track_model.call_after_wave_state_changed.append(self.update_track)
        track_model.call_after_change.append(self.repaint)
        self.track_model = track_model
        self.window = window

        self.channels_list = ChannelsList(self.track_model)
        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.addWidget(self.channels_list)
        self.actions_panel = ActionsPanel(self.parent())
        self.horizontal_layout.addWidget(self.actions_panel)

        self.setLayout(self.horizontal_layout)
        self._temp_sound_file = None
        self._q_sound_object = None
        self._time_of_start = 0
        self._played_start = 0
        self._play_sound_timer = QtCore.QTimer()
        self._play_sound_timer.setSingleShot(False)
        self._play_sound_timer.timeout.connect(self.tick_timer)
        self.play_pause_button = None

    @property
    def captured_area_container(self):
        return self.track_model.captured_area_container

    @property
    def wave_state(self):
        return self.track_model.wave_state

    def update_track(self):
        self.channels_list.update_track()

    def _delete_temp_sound_file(self):
        if self._temp_sound_file is not None:
            os.remove(self._temp_sound_file)
            self._temp_sound_file = None
            self._q_sound_object = None

    def play(self):
        (opened, file) = tempfile.mkstemp()
        os.close(opened)
        if self.captured_area_container.is_released:
            self._played_start = self.captured_area_container.start
            wave_state = self.wave_state.get_part(
                self._played_start, len(self.wave_state))
        else:
            self._played_start = 0
            wave_state = self.wave_state
        wave_state.save_to_file(file)
        self._q_sound_object = QSound(file)
        self._temp_sound_file = file
        self._q_sound_object.play()
        self._time_of_start = time.time()
        self._play_sound_timer.start(Track.UPDATE_PLAYING_TRACK_TIME)

    def tick_timer(self):
        cur_time = time.time()
        passed_time = cur_time - self._time_of_start
        frame_number = self._played_start + int(self.wave_state.frame_rate *
                                                passed_time)
        if frame_number > len(self.wave_state):
            self.window.switch_play_pause(self)
        else:
            self.captured_area_container.capture_segment(frame_number, 0)
        self.track_model.update()

    def set_play_pause_button(self, button):
        self.play_pause_button = button

    def stop(self):
        if self._q_sound_object is not None:
            self._q_sound_object.stop()
            self._play_sound_timer.stop()
            self._delete_temp_sound_file()

    def closeEvent(self, event):
        self._delete_temp_sound_file()
