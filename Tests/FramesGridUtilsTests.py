import unittest
from Core.FramesGridUtils import FramesGridUtils
import numpy as np
from Tests.NumpyArraysTest import NumpyArraysTest


class FramesGridUtilsTests(NumpyArraysTest):
    def test_get_steps_coordinates_all_points(self):
        steps = FramesGridUtils.get_steps_coordinates(5, 10, 10)
        self.assert_numpy_array_equal(steps, self.to_numpy_array(range(5, 11, 1)))

    def test_get_steps_coordinates_alignment(self):
        steps = FramesGridUtils.get_steps_coordinates(5, 11, 3)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([6, 8, 10]))

    def test_get_steps_coordinates_big_alignment(self):
        steps = FramesGridUtils.get_steps_coordinates(9, 30, 2)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([16, 24]))

    def test_get_steps_coordinates_bounds_inclusive(self):
        steps = FramesGridUtils.get_steps_coordinates(4, 12, 3)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([4, 8, 12]))

    def test_get_steps_coordinates_not_maximal_points_count(self):
        steps = FramesGridUtils.get_steps_coordinates(4, 12, 4)
        self.assert_numpy_array_equal(steps, self.to_numpy_array([4, 8, 12]))