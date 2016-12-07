from ViewModel.AbstractModel import AbstractModel
from ViewModel.ChannelModel import ChannelModel
from ViewModel.ViewUtils.CapturedAreaContainer import CapturedAreaContainer


class TrackModel(AbstractModel):
    def __init__(self, wave_state, view_model):
        super().__init__()
        self.wave_state = wave_state
        self.channel_models = list(self.build_channel_models())
        self.call_after_wave_state_changed = []
        self.captured_area_container = CapturedAreaContainer()
        self.captured_area_container.call_after_capture.append(self.drop_other_captures)
        self.captured_area_container.call_after_change.append(self._after_change)
        self.view_model = view_model

    def _wave_state_changed(self):
        for func in self.call_after_wave_state_changed:
            func()
        self._after_change()

    def scale(self, x_mid_ratio, scale_factor):
        for channel in self.channel_models:
            frame_mid = channel.start_frame + len(channel) * x_mid_ratio
            channel.scale(frame_mid, scale_factor)
        self._after_change()

    def build_channel_models(self):
        for channel in self.wave_state.channels:
            sample_width = self.wave_state.sample_width
            frame_rate = self.wave_state.frame_rate
            yield ChannelModel(channel, sample_width, frame_rate, self)

    def update_channel_models(self):
        self.channel_models = list(self.build_channel_models())
        # if len(self.channel_models) != len(self.wave_state.channels):
        #     raise Exception("Number of channels changed for the track. Was {} but found {}"
        #                     .format(len(self.channel_models),
        #                             len(self.wave_state.channels)))
        # for i, model in zip(range(len(self.channel_models)), self.build_channel_models()):
        #     self.channel_models[i] = model

    def drop_other_captures(self):
        self.view_model.drop_capture_from_other_tracks(self)

    def get_selected_part(self):
        if self.captured_area_container.is_released:
            start = self.captured_area_container.start
            finish = self.captured_area_container.finish
            return self.wave_state.get_part(start, finish)

    def set_wave_state(self, new_wave_state):
        self.wave_state = new_wave_state
        self.update_channel_models()

    def insert_part(self, part_wave_state):
        if self.captured_area_container.is_released:
            start = self.captured_area_container.start
            self.set_wave_state(self.wave_state.get_inserted(part_wave_state,
                                                             start))
            self.captured_area_container.drop()
            self.captured_area_container.capture(start)
            self.captured_area_container.move(start + len(part_wave_state))
            self.captured_area_container.release()

            self._wave_state_changed()
