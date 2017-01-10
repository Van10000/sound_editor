import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
import numpy as np

from Core.WaveState import WaveUtils
from Tests.NumpyArraysTestCase import NumpyArraysTest
import unittest


class TestWaveUtils(NumpyArraysTest):
    @staticmethod
    def channelsToNumpy(channels):
        return [np.array(channel, dtype=np.int64) for channel in channels]

    def test_frames_to_samples(self):
        self.check_frames_to_samples([1, 2, 3], 1, [1, 2, 3])
        self.check_frames_to_samples([1, 0, 2, 0], 2, [1, 2])
        self.check_frames_to_samples([1, 1, 2, 1], 2, [256 + 1, 256 + 2])
        self.check_frames_to_samples([3, 2, 1, 0], 4, [65536 + 512 + 3])

    def check_frames_to_samples(self, frames, sample_width, expected_samples):
        self.assert_numpy_array_equal(
            WaveUtils.frames_to_samples(bytes(frames),
                                        sample_width),
            expected_samples)

    def test_samples_to_frames(self):
        self.check_samples_to_frames([1, 2], 2, [1, 0, 2, 0])
        self.check_samples_to_frames([1, 2], 1, [1, 2])

    def check_samples_to_frames(self, samples, sample_width, expected_frames):
        self.assertSequenceEqual(WaveUtils.samples_to_frames(
            self.to_numpy_array(samples), sample_width),
            expected_frames)

    def test_samples_to_channels(self):
        self.check_samples_to_channels([1, 2, 3, 4], [[1, 3], [2, 4]])

    def check_samples_to_channels(self, samples, expected_channels):
        self.assert_numpy_array_equal(
            WaveUtils.samples_to_channels(samples,
                                          len(expected_channels)),
            expected_channels)

    def test_channels_to_samples(self):
        self.check_channels_to_samples([[1, 3], [2, 4]], [1, 2, 3, 4])
        self.check_channels_to_samples([[1], [2]], [1, 2])

    def check_channels_to_samples(self, channels, expected_samples):
        self.assert_numpy_array_equal(WaveUtils.channels_to_samples(channels),
                                      self.to_numpy_array(expected_samples))

    def test_change_channel_resolution(self):
        self.check_change_channel_resolution([1, 3, 5, 9],
                                             [1, 2, 3, 4, 5, 7, 9],
                                             np.int64)
        self.check_change_channel_resolution([1, 11], [1, 3, 5, 7, 9, 11],
                                             np.int64)
        self.check_change_channel_resolution([1], [1, 1, 1], np.int64)
        self.check_change_channel_resolution([1, 3], [1, 1, 2, 3], np.int64)

    def check_change_channel_resolution(self, channel,
                                        expected_changed_channel,
                                        data_type):
        coefficient = len(expected_changed_channel) / len(channel)
        self.assert_numpy_array_equal(WaveUtils.change_channel_resolution(
            channel, coefficient, data_type), expected_changed_channel)

    def test_get_average_channel(self):
        self.check_get_average_channel([[1, 2], [3, 4]], [2, 3])
        self.check_get_average_channel([[1], [7], [7]], [5])
        self.check_get_average_channel([[1], [7], [8]], [5])

    def check_get_average_channel(self, channels, expected_average_channel):
        self.assert_numpy_array_equal(
            WaveUtils.get_average_channel(self.channelsToNumpy(channels)),
            expected_average_channel)

    def test_change_channel_sample_width(self):
        self.check_change_channel_sample_width([1, 2], [2, 4], 2)
        self.check_change_channel_sample_width([4, 6], [2, 3], 0.5)
        self.check_change_channel_sample_width([16, 24], [4, 6], 0.25)

    def check_change_channel_sample_width(self, channel, expected_changed,
                                          multiplier):
        self.assert_numpy_array_equal(
            WaveUtils.change_channels_sample_width(
                [self.to_numpy_array(channel)], multiplier),
            [expected_changed])

    def test_get_appended(self):
        self.check_get_appended([[1, 2], [1, 2]], [[3, 4], [3, 4]],
                                [[1, 2, 3, 4], [1, 2, 3, 4]])
        self.check_get_appended([[1, 2], [3, 4]], [[], []], [[1, 2], [3, 4]])

    def check_get_appended(self, channels1, channels2, expected):
        self.assert_numpy_array_equal(WaveUtils.get_appended(
            self.channelsToNumpy(channels1),
            self.channelsToNumpy(channels2)), expected)

    def test_get_reversed(self):
        self.check_get_reversed([[1, 2, 3], [4, 5, 6]],
                                [[3, 2, 1], [6, 5, 4]])

    def check_get_reversed(self, channels, expected_reversed):
        self.assert_numpy_array_equal(
            WaveUtils.get_reversed(self.channelsToNumpy(channels)),
            expected_reversed)


if __name__ == '__main__':
    unittest.main()

