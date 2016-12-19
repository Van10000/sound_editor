from Core.WaveState.Loudness import Loudness
from Tests.NumpyArraysTests import NumpyArraysTest


class LoudnessTests(NumpyArraysTest):
    def test_fade_in(self):
        length = 10
        fade_length = 5

        loudness = Loudness.get_fade_in(fade_length, length)

        self.assertEqual(len(loudness), length)
        self.assert_all_less(loudness[:fade_length], 1)
        self.assert_all_almost_equal(loudness[fade_length:], 1)

    def test_fade_out(self):
        length = 13
        fade_length = 7

        loudness = Loudness.get_fade_out(fade_length, length)

        self.assertEqual(len(loudness), length)
        self.assert_all_less(loudness[-fade_length:], 1)
        self.assert_all_almost_equal(loudness[:-fade_length], 1)

    def assert_all_less(self, sequence, value):
        for elem in sequence:
            self.assertLess(elem, value)

    def assert_all_almost_equal(self, sequence, value, delta=1e-6):
        for elem in sequence:
            self.assertAlmostEqual(elem, value, delta=delta)