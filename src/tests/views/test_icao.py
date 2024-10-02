from unittest import TestCase

from pydantic import ValidationError
from views.icao import ICAO


class TestICAOType(TestCase):
    def test_normal(self):
        ICAO(icao="EDDB")
        ICAO(icao="EDDL")
        ICAO(icao="EDDF")

    def test_lowercase(self):
        test = ICAO(icao="eddl")

        self.assertEqual(test.icao, "EDDL")

    def test_expections(self):
        # ValidationError due to numbers in ICAO
        with self.assertRaises(ValidationError):
            ICAO(icao="1ADW")

        # ValidationError due to <4 letters
        with self.assertRaises(ValidationError):
            ICAO(icao="EDD")

        # ValidationError due to >4 letters
        with self.assertRaises(ValidationError):
            ICAO(icao="EDDTT")
