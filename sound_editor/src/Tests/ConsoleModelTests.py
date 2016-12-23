import unittest
from ConsoleSoundEditor.ConsoleModel import ConsoleModel


class ConsoleModelTests(unittest.TestCase):
    def test_parse_time_all_parts(self):
        time_str = "1:02:345"
        expected_result = 62.345

        time_in_seconds = ConsoleModel._parse_time_to_seconds(time_str)

        self.assertAlmostEqual(time_in_seconds, expected_result, delta=1e-3)

    def test_parse_time_only_minutes(self):
        time_str = "1"
        expected_result = 60

        time_in_seconds = ConsoleModel._parse_time_to_seconds(time_str)

        self.assertAlmostEqual(time_in_seconds, expected_result, delta=1e-3)