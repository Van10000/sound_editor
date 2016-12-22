from View.EffectsParamsWidgets.TimeParamsWidget import TimeParamsWidget


class FadeInParamsWidget(TimeParamsWidget):
    def apply_effect(self):
        return self.apply_effect_by_func(self.track_model.fade_in)
