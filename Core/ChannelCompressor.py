import numpy as np


class ChannelCompressor:
    def __init__(self, channel, mode='simple'):
        self.channel = channel
        self.mode = mode

    def get_compressed(self, start, stop, step):
        if self.mode == 'simple':
            return self._get_every_kth(start, stop, step)

    def _get_every_kth(self, start, stop, step):
        return self.channel[start:stop:step]