import wave
import numpy as np

from Core.WaveState import WaveUtils
from Core.NumpyUtils import NumpyUtils


class WaveState:
    # Immutable class
    SAMPLE_TYPE = np.int64

    @staticmethod
    def read_from_file(file_name):
        with wave.open(file_name, "rb") as wave_read:
            sample_width = wave_read.getsampwidth()
            frame_rate = wave_read.getframerate()
            channels = WaveUtils.frames_to_channels(
                wave_read.readframes(wave_read.getnframes()),
                sample_width, wave_read.getnchannels())
            return WaveState(sample_width, frame_rate, channels)

    @staticmethod
    def get_empty_wave_state():
        return WaveState(4, 44100, [NumpyUtils.to_numpy_array([0])])

    def __init__(self, sample_width, frame_rate, channels):
        self.sample_width = sample_width
        self.frame_rate = frame_rate
        self.channels = channels

    def __str__(self):
        return ("channels_number:{0}, sample_width:{1}, "
                "frame_rate:{2}, frames_number:{3}").format(
            self.channels_number, self.sample_width,
            self.frame_rate, self.frames_number)

    def __len__(self):
        return len(self.channels[0])

    def get_with_changed_tempo_and_pitch(self, coefficient):
        return WaveState(self.sample_width,
                         int(self.frame_rate * coefficient),
                         self.channels)

    def get_part_with_changed_tempo_and_pitch(self, start_sample, end_sample, coefficient):
        part = self.get_part(start_sample, end_sample)
        with_deleted_part = self.get_with_deleted_part(start_sample, end_sample)
        part = part.get_with_changed_tempo_and_pitch(coefficient)
        return with_deleted_part.get_inserted(part, start_sample)

    def get_part(self, start_sample, end_sample):
        new_channels = [channel[start_sample:end_sample]
                        for channel in self.channels]
        return WaveState(self.sample_width, self.frame_rate, new_channels)

    def get_with_replaced_part(self, start_sample, part):
        with_deleted = self.get_with_deleted_part(start_sample,
                                                  start_sample + len(part))
        with_inserted = with_deleted.get_inserted(part, start_sample)
        return with_inserted

    def get_with_deleted_part(self, start_sample, end_sample):
        new_channels = [np.append(channel[:start_sample], channel[end_sample:])
                        for channel in self.channels]
        return WaveState(self.sample_width, self.frame_rate, new_channels)

    def get_with_reversed_part(self, start_sample, end_sample):
        new_channels = [np.append(channel[:start_sample],
                                  np.append(channel[end_sample:start_sample:-1],
                                            channel[end_sample:]))
                        for channel in self.channels]
        return WaveState(self.sample_width, self.frame_rate, new_channels)

    def get_appended(self, wave_state):
        wave_state = wave_state.to_same_format(self)
        return WaveState(self.sample_width, self.frame_rate,
                         WaveUtils.get_appended(self.channels,
                                                wave_state.channels))

    def get_inserted(self, wave_state, start_sample):
        wave_state = wave_state.to_same_format(self)
        start_part = self.get_part(0, start_sample)
        finish_part = self.get_part(start_sample, len(self))
        return start_part.get_appended(wave_state).get_appended(finish_part)

    def get_added(self, wave_state):
        wave_state = wave_state.to_same_format(self)
        return WaveState(self.sample_width, self.frame_rate,
                         WaveUtils.get_sum_channels(self.channels,
                                                    wave_state.channels))

    @property
    def samples_number(self):
        return len(self.channels[0])

    @property
    def channels_number(self):
        return len(self.channels)

    @property
    def frames_number(self):
        return self.channels_number * self.samples_number * self.sample_width

    def save_to_file(self, file_name):
        with wave.open(file_name, "wb") as wave_write:
            wave_write.setparams((self.channels_number, self.sample_width,
                                  self.frame_rate, self.frames_number,
                                  'NONE', 'not compressed'))
            frames = WaveUtils.channels_to_frames(self.channels,
                                                  self.sample_width)
            wave_write.writeframes(frames)

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

    def get_with_changed_frame_rate(self, new_frame_rate):
        coefficient = new_frame_rate / self.frame_rate
        new_channels = WaveUtils.change_channels_resolution(
            self.channels, coefficient, self.SAMPLE_TYPE)
        return WaveState(self.sample_width, new_frame_rate,
                         new_channels)

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
        if new_sample_width not in WaveUtils.TYPES:
            raise Exception("Incorrect sample width")
        return WaveState(new_sample_width, self.frame_rate,
                         WaveUtils.change_channels_sample_width(
                             self.channels,
                             new_sample_width / self.sample_width))

    def get_with_changed_loudness(self, loudness_ratios_array):
        correct_channels = \
            [(ch * loudness_ratios_array).astype(dtype=self.SAMPLE_TYPE)
             for ch in self.channels]
        return WaveState(self.sample_width, self.frame_rate, correct_channels)

