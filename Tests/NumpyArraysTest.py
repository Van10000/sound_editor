import numpy as np
import unittest


class NumpyArraysTest(unittest.TestCase):
    def assert_numpy_array_equal(self, array1, array2):
        self.assertTrue(np.array_equal(array1, array2))

    @staticmethod
    def to_numpy_array(numbers):
        return np.array(list(map(np.int64, numbers)))