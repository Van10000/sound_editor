import functools
from ViewModel.AbstractModel import AbstractModel
from ViewModel.ViewUtils.FramesGridUtils import FramesGridUtils
from ViewModel.ViewUtils.PowOfTwoChannelCompressor import PowOfTwoChannelCompressor


class ChannelModel(AbstractModel):
    MINIMAL_CHANNEL_LEN = 100
    COMPRESSION_COEFFICIENT = 1000

    def __init__(self, channel, sample_width, frame_rate, track_model):
        super().__init__()
        self.channel_compressor = PowOfTwoChannelCompressor(channel, ChannelModel.COMPRESSION_COEFFICIENT)
        self.track_model = track_model
        self.frame_rate = frame_rate
        self.channel = channel
        self.numbers_range = 256 ** sample_width
        self.start_frame = 0
        self.finish_frame = len(channel)

    def __len__(self):
        return self.finish_frame - self.start_frame

    def get_time_from_frame(self, frame_number):
        return frame_number / self.frame_rate

    def get_ratio_from_frame_number(self, frame_number):
        relative_frame = self.get_relative_frame_number(frame_number)
        ratio = relative_frame / len(self)
        return ratio

    def get_frame_number_from_ratio(self, ratio):
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
        return FramesGridUtils.get_steps_coordinates(self.start_frame, self.finish_frame, density)

    def get_relative_frame_number(self, frame_number):
        if frame_number < self.start_frame:
            return 0
        if frame_number > self.finish_frame:
            return len(self)
        return frame_number - self.start_frame

    def get_compressed_channel(self):
        return self.channel_compressor.get_compressed(self.start_frame, self.finish_frame)

    def scale(self, mid_frame, scale_factor):
        """
        Scales the view relative to mid_frame.
        Point mid_frame stays at the same position on the screen.
        """
        scaled_len = self._get_scaled_len(scale_factor)
        real_scale_factor = scaled_len / len(self)
        get_bound_scaled = functools.partial(ChannelModel._get_bound_scaled,
                                             mid_frame=mid_frame,
                                             scale_factor=real_scale_factor)
        self.start_frame = max(0, get_bound_scaled(self.start_frame))
        self.finish_frame = min(len(self.channel), get_bound_scaled(self.finish_frame))
        self._after_change()

    def _get_scaled_len(self, scale_factor):
        scaled_len = scale_factor * len(self)
        if scaled_len < self.MINIMAL_CHANNEL_LEN:
            scaled_len = self.MINIMAL_CHANNEL_LEN
        if scaled_len > len(self.channel):
            scaled_len = len(self.channel)
        return scaled_len

    @staticmethod
    def _get_bound_scaled(bound, mid_frame, scale_factor):
        prev_bound_dist = mid_frame - bound
        new_bound_dist = prev_bound_dist * scale_factor
        return int(mid_frame - new_bound_dist)