import functools
from ViewModel.AbstractModel import AbstractModel
from ViewModel.ViewUtils.FramesGridUtils import FramesGridUtils
from ViewModel.ViewUtils.PowOfTwoChannelCompressor \
    import PowOfTwoChannelCompressor
import Core.Utils as Utils


class ChannelModel(AbstractModel):
    MINIMAL_CHANNEL_LEN = 100
    COMPRESSION_COEFFICIENT = 1000

    def __init__(self, channel, sample_width, frame_rate, track_model):
        super().__init__()
        self.channel_compressor = PowOfTwoChannelCompressor(
            channel, ChannelModel.COMPRESSION_COEFFICIENT)
        self.track_model = track_model
        self.frame_rate = frame_rate
        self.channel = channel
        self.numbers_range = 256 ** sample_width

    @property
    def start_frame(self):
        return self.track_model.start_frame

    @property
    def finish_frame(self):
        return self.track_model.finish_frame

    def __len__(self):
        return self.finish_frame - self.start_frame

    def get_time_from_frame(self, frame_number):
        return frame_number / self.frame_rate

    def get_ratio_from_frame_number(self, frame_number):
        relative_frame = self.get_relative_frame_number(frame_number)
        ratio = relative_frame / len(self)
        return ratio

    def get_frame_number_from_ratio(self, ratio):
        ratio = Utils.put_in_bounds(ratio, 0, 1)
        return int(self.start_frame + len(self) * ratio)

    @property
    def captured_area_container(self):
        return self.track_model.captured_area_container

    @property
    def start_frame_time(self):
        return self.get_time_from_frame(self.start_frame)

    @property
    def finish_frame_time(self):
        return self.get_time_from_frame(self.finish_frame)

    @property
    def zero_amplitude(self):
        return self.numbers_range // 2

    def get_vertical_grid_frames(self, density):
        return FramesGridUtils.get_steps_coordinates(self.start_frame,
                                                     self.finish_frame,
                                                     density)

    def get_relative_frame_number(self, frame_number):
        if frame_number < self.start_frame:
            return 0
        if frame_number > self.finish_frame:
            return len(self)
        return frame_number - self.start_frame

    def get_compressed_channel(self):
        return self.channel_compressor.get_compressed(self.start_frame,
                                                      self.finish_frame)
