import numpy as np


class TestingUtils:
    @staticmethod
    def to_numpy_array(numbers):
        return np.array(list(map(np.int64, numbers)))