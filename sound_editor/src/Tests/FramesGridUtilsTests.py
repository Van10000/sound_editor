import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
from ViewModel.ViewUtils.FramesGridUtils import FramesGridUtils
from Tests.NumpyArraysTestCase import NumpyArraysTest
import unittest


class FramesGridUtilsTests(NumpyArraysTest):
    def test_get_steps_coordinates_all_points(self):
        steps = FramesGridUtils.get_steps_coordinates(5, 10, 5)
        self.assert_numpy_array_equal(steps,
                                      self.to_numpy_array(range(5, 10, 1)))

    def test_get_steps_coordinates_alignment(self):
        steps = FramesGridUtils.get_steps_coordinates(5, 11, 3)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([6, 8, 10]))

    def test_get_steps_coordinates_big_alignment(self):
        steps = FramesGridUtils.get_steps_coordinates(9, 30, 2)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([16, 24]))

    def test_get_steps_coordinate_half_interval(self):
        steps = FramesGridUtils.get_steps_coordinates(4, 12, 2)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([4, 8]))

    def test_get_steps_coordinates_not_maximal_points_count(self):
        steps = FramesGridUtils.get_steps_coordinates(4, 12, 3)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([4, 8]))

if __name__ == '__main__':
    unittest.main()
