from ViewModel.ViewUtils.FramesGridUtils import FramesGridUtils


class PowOfTwoChannelCompressor:
    def __init__(self, channel, max_frames_number):
        self.channel = channel
        self.max_frames_number = max_frames_number

    def get_compressed(self, start=0, stop=-1):
        if stop == -1:
            stop = len(self.channel)
        compressed_indexes = FramesGridUtils.get_steps_coordinates(start, stop, self.max_frames_number)
        return [self.channel[index] for index in compressed_indexes]
