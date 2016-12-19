from View.EffectsParamsWidgets.FadeParamsWidget import FadeParamsWidget


class FadeOutParamsWidget(FadeParamsWidget):
    def apply_effect(self):
        self.apply_fade(self.track_model.fade_out)