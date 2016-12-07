from ViewModel.AbstractModel import AbstractModel
from ViewModel.TrackModel import TrackModel


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