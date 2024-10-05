from unittest import TestCase

from validators.frequency import frequency_validator


class TestFrequencyValidator(TestCase):
    def _test_case(self, value, expected_value=None):
        if not expected_value:
            expected_value = value

        self.assertEqual(frequency_validator(value), expected_value)

    def test_valid_frequencies(self):
        self._test_case("118.000")
        self._test_case("119.005")
        self._test_case("120.010")
        self._test_case("121.015")
        self._test_case("122.025")
        self._test_case("123.030")
        self._test_case("124.035")
        self._test_case("125.040")
        self._test_case("126.050")
        self._test_case("127.055")
        self._test_case("128.060")
        self._test_case("129.065")
        self._test_case("130.075")
        self._test_case("131.080")
        self._test_case("132.085")
        self._test_case("134.090")
        self._test_case("137.100")

    def test_shortened_frequences(self):
        self._test_case("118", "118.000")
        self._test_case("137", "137.000")
        self._test_case("120.5", "120.500")
        self._test_case("120.50", "120.500")
        self._test_case("120.55", "120.550")
        self._test_case("120.05", "120.050")

    def test_exceptions(self):
        # test invalid frequencies
        with self.assertRaises(ValueError):
            self._test_case("118.001")

        with self.assertRaises(ValueError):
            self._test_case("117")

        with self.assertRaises(ValueError):
            self._test_case("138")

        with self.assertRaises(ValueError):
            self._test_case("137.999")
