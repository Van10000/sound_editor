import math
from Core.SmartChannelCompressor import SmartChannelCompressor
# TODO: find out the problem(works too slow, probably self.get_step is wrong
# TODO: write tests


class PowOfTwoChannelCompressor(SmartChannelCompressor):
    def __init__(self, channel, max_frames_number):
        super().__init__(channel, max_frames_number)

    def get_step(self, length):
        return self._to_power_of_two(max(int(length / self.max_frames_number), 1))

    def get_compressed_smart(self, start=0, stop=-1):
        if stop == -1:
            stop = len(self.channel)
        return self.get_compressed(start, stop,
                                   self.get_step(stop - start))

    def __len__(self):
        return len(self.channel) / self.get_step(len(self.channel))

    @staticmethod
    def _to_power_of_two(number):
        return int(round(math.log(number, 2)))  # TODO: think about bounds on number