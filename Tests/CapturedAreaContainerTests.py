import unittest
from Core.CapturedAreaContainer import CapturedAreaContainer


class CapturedAreaContainerTests(unittest.TestCase):
    def setUp(self):
        self.container = CapturedAreaContainer()

    def move_all(self, *coordinates):
        self.container.capture(coordinates[0])
        for coord in coordinates:
            self.container.move(coord)
        self.container.release()

    def assert_start_and_finish(self, start, finish):
        self.assertEqual(self.container.start, start)
        self.assertEqual(self.container.finish, finish)

    def test_move(self):
        self.move_all(5, 10, 20, 15, 50, 30)
        self.assert_start_and_finish(5, 30)

    def test_start_after_finish(self):
        self.move_all(0, 5, -5)
        self.assert_start_and_finish(-5, 0)

    def test_drop(self):
        self.move_all(0, 20)
        self.container.drop()
        self.move_all(5, 10)
        self.assert_start_and_finish(5, 10)

    def test_capture_and_release(self):
        self.assertFalse(self.container.is_captured)
        self.container.capture(5)
        self.assertTrue(self.container.is_captured)
        self.assertFalse(self.container.is_released)
        self.container.release()
        self.assertTrue(self.container.is_released)