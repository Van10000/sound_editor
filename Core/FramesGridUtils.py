import math
import numpy as np


class FramesGridUtils:
    POWERS_OF_TWO = [1 << i for i in range(100)]

    @staticmethod
    def to_low_power_of_two(number):
        if number <= 0:
            raise IndexError("number should be positive, your input:" + str(number))
        for power in FramesGridUtils.POWERS_OF_TWO:
            if power > number:
                return power // 2

    @staticmethod
    def get_low_step_value(length, maximal_steps_number):
        approximate_step = length // maximal_steps_number + 1
        return FramesGridUtils.to_low_power_of_two(approximate_step)

    @staticmethod
    def get_start_aligned(start, step):
        return start if start % step == 0 else start // step * step + step

    @staticmethod
    def get_precise_step_value(start_frame, finish_frame, maximal_steps_number):
        for power in FramesGridUtils.POWERS_OF_TWO:
            if FramesGridUtils.step_fits(start_frame, finish_frame, power, maximal_steps_number):
                return power

    @staticmethod
    def step_fits(start_frame, finish_frame, step, maximal_steps_number):
        return FramesGridUtils.steps_count(step, start_frame, finish_frame) <= maximal_steps_number

    @staticmethod
    def steps_count(step, start_frame, finish_frame):
        start_aligned = FramesGridUtils.get_start_aligned(start_frame, step)
        length_aligned = finish_frame - start_aligned
        return length_aligned // step + 1

    @staticmethod
    def get_steps_coordinates(start_frame, finish_frame, maximal_steps_number):
        step = FramesGridUtils.get_precise_step_value(start_frame, finish_frame, maximal_steps_number)
        start_aligned = FramesGridUtils.get_start_aligned(start_frame, step)
        return np.arange(start_aligned, finish_frame + 1, step, dtype=np.int64)