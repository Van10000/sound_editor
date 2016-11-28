import wave

import numpy as np

from Core import WaveUtils


# Immutable class
from Core.NumpyUtils import NumpyUtils


class WaveState:

    @staticmethod
    def read_from_file(file_name):
        with wave.open(file_name, "rb") as wave_read:
            sample_width = wave_read.getsampwidth()
            frame_rate = wave_read.getframerate()
            channels = WaveUtils.frames_to_channels(
                wave_read.readframes(wave_read.getnframes()),
                sample_width, wave_read.getnchannels())
            return WaveState(sample_width, frame_rate, channels,
                             WaveState.get_default_loudness(len(channels[0])))

    @staticmethod
    def get_default_loudness(length):
        return np.empty((length,), dtype=np.float32).fill(1)

    @staticmethod
    def get_empty_wave_state():
        return WaveState(4, 44100, [NumpyUtils.to_numpy_array([0])])

    def __init__(self, sample_width, frame_rate, channels, loudness=None):
        self.sample_width = sample_width
        self.frame_rate = frame_rate
        self.channels = channels
        self.loudness = WaveState.get_default_loudness(len(self.channels[0])) if loudness is None else loudness

    def __str__(self):
        return str.format("channels_number:{0}, sample_width:{1}, "
                          "frame_rate:{2}, frames_number:{3}",
                          self.channels_number, self.sample_width,
                          self.frame_rate, self.frames_number)

    def get_with_changed_tempo_and_pitch(self, coefficient):
        return WaveState(self.sample_width,
                         int(self.frame_rate * coefficient),
                         self.channels,
                         self.loudness)

    def get_part(self, start_sample, end_sample):
        new_channels = [channel[start_sample:end_sample]
                        for channel in self.channels]
        new_loudness = self.loudness[start_sample:end_sample]
        return WaveState(self.sample_width, self.frame_rate,
                         new_channels, new_loudness)

    def get_with_deleted_part(self, start_sample, end_sample):
        new_channels = [np.append(channel[:start_sample], channel[end_sample:])
                        for channel in self.channels]
        new_loudness = np.append(self.loudness[:start_sample],
                                 self.loudness[end_sample:])
        return WaveState(self.sample_width, self.frame_rate,
                         new_channels, new_loudness)

    def get_appended(self, wave_state):
        wave_state = wave_state.to_same_format(self)
        return WaveState(self.sample_width, self.frame_rate,
                         WaveUtils.get_appended(self.channels,
                                                wave_state.channels),
                         np.append(self.loudness, wave_state.loudness))

    @property
    def samples_number(self):
        return len(self.channels[0])

    @property
    def channels_number(self):
        return len(self.channels)

    @property
    def frames_number(self):
        return self.channels_number * self.samples_number * self.sample_width

    def output_to_file(self, file_name):
        with wave.open(file_name, "wb") as wave_write:
            wave_write.setparams((self.channels_number, self.sample_width,
                                  self.frame_rate, self.frames_number,
                                  'NONE', 'not compressed'))
            wave_write.writeframes(
                WaveUtils.channels_to_frames(
                    (self.channels * self.loudness).astype(dtype=np.int64),
                    self.sample_width))

    def to_same_format(self, wave_state):
        new_self = self
        if new_self.frame_rate != wave_state.frame_rate:
            new_self = new_self.get_with_changed_frame_rate(
                wave_state.frame_rate)
        if new_self.sample_width != wave_state.sample_width:
            new_self = new_self.get_with_changed_sample_width(
                wave_state.sample_width)
        if new_self.channels_number != wave_state.channels_number:
            new_self = new_self.get_with_changed_channels_number(
                wave_state.channels_number)
        return new_self

    def get_with_changed_frame_rate(self, new_frame_rate):  # TODO: probably it's better to use FFT
        coefficient = new_frame_rate / self.frame_rate
        new_channels = WaveUtils.change_channels_resolution(
            self.channels, coefficient, np.int64)
        new_loudness = WaveUtils.change_channel_resolution(
            self.loudness, coefficient, np.float32)
        return WaveState(self.sample_width, new_frame_rate,
                         new_channels, new_loudness)

    def get_with_changed_channels_number(self, new_channels_number):
        average_channel = WaveUtils.get_average_channel(self.channels)
        if new_channels_number > self.channels_number:
            new_channels = [self.channels[i]
                            if i < self.channels_number
                            else average_channel
                            for i in range(new_channels_number)]
        else:
            new_channels = [average_channel
                            for i in range(new_channels_number)]
        return WaveState(self.sample_width, self.frame_rate, new_channels)

    def get_with_changed_sample_width(self, new_sample_width):
        if new_sample_width not in [1, 2, 4]:
            raise Exception("Incorrect sample width")
        return WaveState(new_sample_width, self.frame_rate,
                         WaveUtils.change_channels_sample_width(
                             self.channels,
                             new_sample_width / self.sample_width))

