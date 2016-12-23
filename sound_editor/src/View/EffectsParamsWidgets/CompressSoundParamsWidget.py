from View.EffectsParamsWidgets.TimeAndRatioParamsWidget import TimeAndRatioParamsWidget


class CompressSoundParamsWidget(TimeAndRatioParamsWidget):
    def apply_effect(self):
        self.max_possible_ratio = 1
        return self.apply_effect_by_func(self.track_model.compress_sound)