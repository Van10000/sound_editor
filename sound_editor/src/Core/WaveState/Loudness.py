import numpy as np


class Loudness:
    LOUDNESS_TYPE = np.float32

    @staticmethod
    def get_fade_in(fade_length):
        return Loudness.get_fade(fade_length, True)

    @staticmethod
    def get_fade_out(fade_length):
        return Loudness.get_fade(fade_length, False)

    @staticmethod
    def get_general_fade(fade_length, to_ratio, from_start):
        step = Loudness.LOUDNESS_TYPE(1 / fade_length)
        loudness = np.arange(to_ratio, 1, step)
        if not from_start:
            loudness = loudness[::-1]
        return loudness[:fade_length:]

    @staticmethod
    def get_fade(fade_length, from_start):
        return Loudness.get_general_fade(fade_length, 0, from_start)

    @staticmethod
    def get_ones(length):
        return Loudness.get_constant_loudness(length, 1)

    @staticmethod
    def get_constant_loudness(length, value):
        loudness = np.full((length,), fill_value=Loudness.LOUDNESS_TYPE(value))
        return loudness

    @staticmethod
    def get_on_segment(loudness, start, total_length):
        """
        :param loudness: loudness for fragment of track
        :param start: place where this loudness starts
        :param total_length: total length of the track
        :return: loudness for the whole track
        """
        finish = start + len(loudness)
        loudness = np.append(Loudness.get_ones(start), loudness)
        loudness = np.append(loudness, Loudness.get_ones(total_length - finish))
        return loudness