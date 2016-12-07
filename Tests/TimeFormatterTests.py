import unittest

from ViewModel.ViewUtils.TimeFormatter import TimeFormatter


class TimeFormatterTests(unittest.TestCase):
    def assert_time_parsed_correct(self, parsed, expected_time_m, expected_time_s, expected_time_ms):
        time_m, time_s, time_ms = parsed
        self.assertEqual(time_m, expected_time_m)
        self.assertEqual(time_s, expected_time_s)
        self.assertEqual(time_ms, expected_time_ms)

    def test_get_time_parsed(self):
        parsed = TimeFormatter.get_time_parsed(123.1234, 3)
        self.assert_time_parsed_correct(parsed, 2, 3, 123)

    def test_get_time_parsed_milliseconds(self):
        parsed = TimeFormatter.get_time_parsed(1.5286, 4)
        self.assert_time_parsed_correct(parsed, 0, 1, 5286)

    def test_format_add_leading_zeros(self):
        formatted = TimeFormatter.format(302.041, 3)
        self.assertEqual(formatted, "5:02:041")

    def test_format_zero_precision(self):
        formatted = TimeFormatter.format(101.345, 0)
        self.assertEqual(formatted, "1:41")

    def test_format_add_leading_zeros_with_zero_precision(self):
        formatted = TimeFormatter.format(182, 0)
        self.assertEqual(formatted, "3:02")