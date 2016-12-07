import threading


class CapturedAreaContainer:
    def __init__(self):
        self.captured_coord = 0
        self.current_coord = 0
        self.is_released = False
        self.is_captured = False
        self.call_after_change = []
        self.call_after_capture = []
        self.lock = threading.Lock()

    def _after_change(self):
        for func in self.call_after_change:
            func()

    def _after_capture(self):
        for func in self.call_after_capture:
            func()

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
        self._after_capture()
        self._after_change()

    def move(self, x_coord):
        if not self.is_released:
            self.current_coord = x_coord
            self._after_change()
        else:
            raise Exception("Container is released at the moment.")

    def release(self):
        self.is_released = True

    def drop(self):
        if self.is_captured:
            self.captured_coord = 0
            self.current_coord = 0
            self.is_released = False
            self.is_captured = False
            self._after_change()