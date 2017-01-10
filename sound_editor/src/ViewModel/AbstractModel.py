
class AbstractModel:
    def __init__(self):
        self.call_after_change = []

    def _after_change(self):
        for func in self.call_after_change:
            func()
