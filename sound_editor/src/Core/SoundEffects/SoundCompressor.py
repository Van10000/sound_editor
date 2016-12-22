import functools
import numpy as np
from Core import Utils
from Core.WaveState import WaveState


class SoundCompressor:
    WINDOW_SIZE = np.int64(20000)

    @staticmethod
    def compress(wave_state, intensity):
        new_channels = [
            SoundCompressor.compress_channel(ch,
                                             SoundCompressor.WINDOW_SIZE,
                                             intensity)
            for ch in wave_state.channels]
        return wave_state.get_with_changed_channels(new_channels)

    @staticmethod
    def compress_channel(channel, window_size, intensity):
        if len(channel) < window_size:
            return channel
        abs_channel = np.absolute(channel)
        middle_level = sum(abs_channel) / len(abs_channel)
        if window_size % 2 == 1:
            window_size += 1
        cur_sum = sum(abs_channel[0:window_size])
        half_size = window_size // 2
        float_window_size = np.float64(window_size)
        result = np.full((len(channel),), 0, dtype=WaveState.WaveState.SAMPLE_TYPE)
        for i in range(0, len(channel)):
            if i - half_size >= 0 and i + half_size < len(channel):
                cur_sum -= abs_channel[i - half_size]
                cur_sum += abs_channel[i + half_size]
            cur_avg = cur_sum / float_window_size
            cur_ratio = cur_avg / middle_level
            diff = cur_ratio - 1
            diff *= intensity
            cur_ratio = 1 + diff
            cur_res = abs_channel[i] / cur_ratio
            if channel[i] < 0:
                cur_res = -cur_res
            np.put(result, i, cur_res)
        return result

