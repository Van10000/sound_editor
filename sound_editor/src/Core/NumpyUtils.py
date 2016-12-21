import numpy as np


class NumpyUtils:
    @staticmethod
    def to_numpy_array(numbers):
        return np.array(list(map(np.int64, numbers)))

    @staticmethod
    def get_filled(arr, required_length):
        zeros = np.zeros(required_length - len(arr))
        return np.append(arr, zeros)

    @staticmethod
    def numpy_sum(arr1, arr2):
        if len(arr1) == len(arr2):
            return arr1 + arr2
        if len(arr1) < len(arr2):
            arr1, arr2 = arr2, arr1
        arr2 = NumpyUtils.get_filled(arr2, len(arr1))
        return arr1 + arr2