from Core.SoundEffects.SoundCompressor import SoundCompressor
from Core.WaveState.Loudness import Loudness
from Core import Utils
from ViewModel.AbstractModel import AbstractModel
from ViewModel.ChannelModel import ChannelModel
from ViewModel.ViewUtils.CapturedAreaContainer import CapturedAreaContainer
import functools


class TrackModel(AbstractModel):
    MINIMAL_LEN = 100

    def __init__(self, wave_state, view_model):
        super().__init__()
        self.wave_state = wave_state
        self.channel_models = list(self.build_channel_models())
        self.call_after_wave_state_changed = []
        self.captured_area_container = CapturedAreaContainer()
        self.captured_area_container.call_after_capture.append(
            self.drop_other_captures)
        self.captured_area_container.call_after_change.append(
            self._after_change)
        self.start_frame = 0
        self.finish_frame = len(wave_state)
        self.view_model = view_model
        self.is_active = True

    def __len__(self):
        return self.finish_frame - self.start_frame

    def _wave_state_changed(self):
        for func in self.call_after_wave_state_changed:
            func()
        self._after_change()

    def build_channel_models(self):
        for channel in self.wave_state.channels:
            sample_width = self.wave_state.sample_width
            frame_rate = self.wave_state.frame_rate
            yield ChannelModel(channel, sample_width, frame_rate, self)

    def get_time_from_frame(self, frame_number):
        return frame_number / self.wave_state.frame_rate

    def get_frame_from_time(self, time):
        return round(int(time * self.wave_state.frame_rate))

    @property
    def captured_start(self):
        return self.captured_area_container.start

    @property
    def captured_finish(self):
        return self.captured_area_container.finish

    def update_channel_models(self):
        self.channel_models = list(self.build_channel_models())

    def drop_other_captures(self):
        self.view_model.drop_capture_from_other_tracks(self)

    def get_selected_part(self):
        if self.captured_area_container.is_released:
            return self.wave_state.get_part(self.captured_start,
                                            self.captured_finish)

    def update(self):
        self._wave_state_changed()

    def set_wave_state(self, new_wave_state):
        window_length = len(self)
        if len(new_wave_state) <= window_length:
            self.start_frame = 0
            self.finish_frame = len(new_wave_state)
        else:
            if len(new_wave_state) <= self.finish_frame:
                self.finish_frame = len(new_wave_state)
                self.start_frame = self.finish_frame - window_length
        self.wave_state = new_wave_state
        self.update_channel_models()

    def insert_part(self, part_wave_state):
        if self.captured_area_container.is_released:
            new_state = self.wave_state.get_inserted(
                part_wave_state, self.captured_start)

            self.set_wave_state(new_state)
            self.captured_area_container.capture_segment(
                self.captured_start, len(part_wave_state))

            self._wave_state_changed()

    def delete_selected_part(self):
        if self.captured_area_container.is_released:
            new_state = self.wave_state.get_with_deleted_part(
                self.captured_start, self.captured_finish)
            self.set_wave_state(new_state)
            self.captured_area_container.capture_segment(self.captured_start,
                                                         0)

            self._wave_state_changed()

    def reverse_selected_part(self):
        if self.captured_area_container.is_released:
            new_state = self.wave_state.get_with_reversed_part(
                self.captured_start, self.captured_finish)
            self.set_wave_state(new_state)

            self._wave_state_changed()

    def get_captured_start_and_finish(self):
        start = 0
        finish = len(self.wave_state)
        if self.captured_area_container.is_released:
            start = self.captured_area_container.start
            finish = self.captured_area_container.finish
        return start, finish

    def apply_loudness(self, loudness):
        new_state = self.wave_state.get_with_changed_loudness(loudness)
        self.set_wave_state(new_state)
        self._wave_state_changed()

    def adjust_loudness(self, ratio):
        start, finish = self.get_captured_start_and_finish()
        loudness = Loudness.get_constant_loudness(finish - start, ratio)
        loudness = Loudness.get_on_segment(loudness, start,
                                           len(self.wave_state))
        self.apply_loudness(loudness)

    def scale(self, x_mid_ratio, scale_factor):
        """
        Scales the view relative to mid_frame.
        Point mid_frame stays at the same position on the screen.
        """
        mid_frame = self.start_frame + len(self) * x_mid_ratio

        scaled_len = self._get_scaled_len(scale_factor)
        real_scale_factor = scaled_len / len(self)
        get_bound_scaled = functools.partial(TrackModel._get_bound_scaled,
                                             mid_frame=mid_frame,
                                             scale_factor=real_scale_factor)
        self.start_frame = max(0, get_bound_scaled(self.start_frame))
        self.finish_frame = min(len(self.wave_state),
                                get_bound_scaled(self.finish_frame))
        self._after_change()

    def fade(self, start_frame, finish_frame, from_start):
        loudness = Loudness.get_fade(finish_frame - start_frame, from_start)
        loudness = Loudness.get_on_segment(loudness, start_frame,
                                           len(self.wave_state))
        self.apply_loudness(loudness)

    def fade_in(self, start_frame, finish_frame):
        self.fade(start_frame, finish_frame, True)

    def fade_out(self, start_frame, finish_frame):
        self.fade(start_frame, finish_frame, False)

    def get_changed_speed_wave_state(self, start_frame, finish_frame, ratio):
        if start_frame <= 0 and finish_frame >= len(self.wave_state):
            return self.wave_state.get_with_changed_tempo_and_pitch(ratio)
        else:
            return self.wave_state.\
                get_part_with_changed_tempo_and_pitch(start_frame,
                                                      finish_frame, ratio)

    def change_speed(self, start_frame, finish_frame, ratio):
        new_state = self.get_changed_speed_wave_state(start_frame,
                                                      finish_frame, ratio)
        finish_time, start_time = map(self.get_time_from_frame,
                                      (finish_frame, start_frame))
        self.set_wave_state(new_state)
        finish_frame, start_frame = map(self.get_frame_from_time,
                                        (finish_time, start_time,))
        # reset finish and start frames because
        # frame rate could have been changed
        new_length = int(round((finish_frame - start_frame) / ratio))
        self.captured_area_container.capture_segment(start_frame,
                                                     new_length)
        self._wave_state_changed()

    def compress_sound(self, start_frame, finish_frame, ratio):
        new_state = self.wave_state.get_compressed(start_frame,
                                                   finish_frame,
                                                   ratio)
        self.set_wave_state(new_state)
        self.captured_area_container.capture_segment(
            start_frame, finish_frame - start_frame)
        self._wave_state_changed()

    def _get_scaled_len(self, scale_factor):
        return Utils.put_in_bounds(self.MINIMAL_LEN, len(self.wave_state),
                                   scale_factor * len(self))

    @staticmethod
    def _get_bound_scaled(bound, mid_frame, scale_factor):
        prev_bound_dist = mid_frame - bound
        new_bound_dist = prev_bound_dist * scale_factor
        return int(mid_frame - new_bound_dist)
