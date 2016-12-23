from PyQt4 import QtGui
from View.EffectsParamsWidgets.EffectParamsWidget import EffectParamsWidget
from View.EffectsParamsWidgets.TimeAndRatioParamsWidget import TimeAndRatioParamsWidget
from View.Utils.NamedLineEdit import NamedLineEdit
from View.Utils.TimeInputWidget import TimeInputWidget


class ChangeSpeedParamsWidget(TimeAndRatioParamsWidget):
    def apply_effect(self):
        return self.apply_effect_by_func(self.track_model.change_speed)