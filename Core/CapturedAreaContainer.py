

class CapturedAreaContainer:
    def __init__(self):
        self.captured_coord = 0
        self.current_coord = 0
        self.is_released = False
        self.is_captured = False
        self.on_change = None

    def _changed(self):
        if self.on_change is not None:
            self.on_change()

    @property
    def start(self):
        return min(self.captured_coord, self.current_coord)

    @property
    def finish(self):
        return max(self.captured_coord, self.current_coord)

    def capture(self, coord):
        self.captured_coord = coord
        self.current_coord = coord
        self.is_captured = True
        self._changed()

    def move(self, x_coord):
        if not self.is_released:
            self.current_coord = x_coord
            self._changed()
        else:
            raise Exception("Container is released at the moment.")

    def release(self):
        self.is_released = True

    def drop(self):
        self.captured_coord = 0
        self.current_coord = 0
        self.is_released = False  # TODO: maybe just run __init__? Will it work?
        self.is_captured = False
        self._changed()