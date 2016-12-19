
class SimpleScalingChannelCompressor:
    def __init__(self, channel, max_frames_number):
        self.channel = channel
        self.max_frames_number = max_frames_number

    def get_max_step(self, length):
        return max(int(length / self.max_frames_number), 1)

    def get_compressed(self, start=0, stop=None):
        if stop is None:
            stop = len(self.channel)
        return self.channel[start:stop:self.get_max_step(stop - start)]

    def __len__(self):
        return len(self.channel) / self.get_max_step(len(self.channel))