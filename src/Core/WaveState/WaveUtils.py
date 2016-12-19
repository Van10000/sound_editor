import numpy as np

SAMPLE_TYPE = np.int64

TYPES = {
    1: np.int8,
    2: np.int16,
    4: np.int32
    }


def frames_to_samples(frames, sample_width):
    return np.fromstring(frames, dtype=TYPES[sample_width]).astype(dtype=SAMPLE_TYPE)


def samples_to_frames(samples, sample_width):
    return samples.astype(TYPES[sample_width]).tostring()


def samples_to_channels(samples, channels_number):
    return [samples[channel_index::channels_number]
            for channel_index in range(channels_number)]


def _channels_to_samples_generator(channels):
    for sample_index in range(len(channels[0])):
        for channel_index in range(len(channels)):
            yield channels[channel_index][sample_index]


def channels_to_samples(channels):
    # for channel in channels:
    #     if len(channel) != len(channels[0]):
    #         raise Exception("All the channels must have equal length")
    return np.fromiter(_channels_to_samples_generator(channels), dtype=SAMPLE_TYPE)


def frames_to_channels(frames, sample_width, channels_number):
    return samples_to_channels(frames_to_samples(frames, sample_width),
                               channels_number)


def channels_to_frames(channels, sample_width):
    return samples_to_frames(channels_to_samples(channels), sample_width)


def _get_approximation_at_position(channel, position):
    lower_bound = int(position)
    upper_bound = min(lower_bound + 1, len(channel) - 1)
    diff_sample = channel[upper_bound] - channel[lower_bound]
    diff_pos = position - lower_bound
    return channel[lower_bound] + diff_sample * diff_pos


def _change_channel_resolution_generator(channel, new_len):
    for frame_index in range(new_len):
        position_in_channel = frame_index / (new_len - 1) * (len(channel) - 1)
        yield _get_approximation_at_position(channel, position_in_channel)


def change_channel_resolution(channel, coefficient, data_type):
    new_len = int(round(len(channel) * coefficient))
    return np.fromiter(_change_channel_resolution_generator(
                       channel, new_len), data_type)


def change_channels_resolution(channels, coefficient, data_type):
    return [change_channel_resolution(channel, coefficient, data_type)
            for channel in channels]


def get_average_channel(channels):
    return sum(channels) // len(channels)


def change_channels_sample_width(channels, sample_width_multiplier):
    return [(channel * sample_width_multiplier).astype(dtype=SAMPLE_TYPE)
            for channel in channels]


def get_appended(chs1, chs2):
    return [np.append(chs1[i], chs2[i]) for i in range(len(chs1))]

# TODO: check if there is 'insert' function in numpy. Most likely, there is.


def get_reversed(channels):
    return [channel[::-1] for channel in channels]