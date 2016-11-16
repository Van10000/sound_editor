from Core.ChannelCompressor import ChannelCompressor
#  TODO: tests


class SmartChannelCompressor(ChannelCompressor):
    def __init__(self, channel, max_frames_number, mode='simple'):
        super().__init__(channel, mode)
        self.max_frames_number = max_frames_number

    def get_max_step(self, length):
        return max(int(length / self.max_frames_number), 1)

    def get_compressed_smart(self, start=0, stop=-1):
        if stop == -1:
            stop = len(self.channel)
        return self.get_compressed(start, stop,
                                   self.get_max_step(stop - start))

    def __len__(self):
        return len(self.channel) / self.get_max_step(len(self.channel))