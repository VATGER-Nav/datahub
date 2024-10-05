from unittest import TestCase

from validators.icao import icao_validator


class TestICAOType(TestCase):
    def test_normal(self):
        icao_validator(icao="EDDB")
        icao_validator(icao="EDDL")
        icao_validator(icao="EDDF")

    def test_lowercase(self):
        test = icao_validator(icao="eddl")

        self.assertEqual(test, "EDDL")

    def test_expections(self):
        # ValidationError due to numbers in ICAO
        with self.assertRaises(ValueError):
            icao_validator(icao="1ADW")

        # ValidationError due to <4 letters
        with self.assertRaises(ValueError):
            icao_validator(icao="EDD")

        # ValidationError due to >4 letters
        with self.assertRaises(ValueError):
            icao_validator(icao="EDDTT")
