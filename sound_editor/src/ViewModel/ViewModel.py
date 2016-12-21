from ViewModel.AbstractModel import AbstractModel
from ViewModel.TrackModel import TrackModel
from Core import Utils


class ViewModel(AbstractModel):
    def __init__(self):
        super().__init__()
        self.track_models = []
        self.clipboard = None

    def add_track_model(self, track_model):
        self.track_models.append(track_model)

    def delete_track_model(self, track_model):
        self.track_models.remove(track_model)

    def drop_capture_from_other_tracks(self, track_model_to_save_capture):
        for track_model in self.track_models:
            if track_model != track_model_to_save_capture:
                track_model.captured_area_container.drop()

    def get_selected_track(self):
        for track_model in self.track_models:
            if track_model.captured_area_container.is_released:
                return track_model
        return None

    def copy(self):
        selected_track = self.get_selected_track()
        self.clipboard = selected_track.get_selected_part()

    def paste(self):
        if self.clipboard is not None:
            selected_track = self.get_selected_track()
            if selected_track is not None:
                selected_track.insert_part(self.clipboard)

    def delete(self):
        selected_track = self.get_selected_track()
        if selected_track is not None:
            selected_track.delete_selected_part()

    def reverse(self):
        selected_track = self.get_selected_track()
        if selected_track is not None:
            selected_track.reverse_selected_part()

    def select_all(self):
        selected_track = self.get_selected_track()
        if selected_track is not None:
            container = selected_track.captured_area_container
            container.capture_segment(0, len(selected_track.wave_state))

    def get_pasted_to_new_track_model(self):
        selected_track = self.get_selected_track()
        if selected_track is not None:
            selected_part = selected_track.get_selected_part()
            new_track_model = TrackModel(selected_part, self)
            return new_track_model

    def get_sum(self):
        active_tracks = filter(lambda model: model.is_active,
                               self.track_models)
        active_wave_states = list(map(lambda model: model.wave_state,
                                      active_tracks))
        return Utils.get_wave_states_sum(*active_wave_states)