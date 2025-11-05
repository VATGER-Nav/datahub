from unittest import TestCase

from datahub.validators.logon import logon_validator


class TestLogonValidator(TestCase):
    def test_normal(self):
        logon = "EDMM_FUL_CTR"
        self.assertEqual(logon.upper(), logon_validator(logon))

        logon = "edmm_ful_ctr"
        self.assertEqual(logon.upper(), logon_validator(logon))

        logon = "EDDL_TWR"
        self.assertEqual(logon.upper(), logon_validator(logon))

        logon = "eddb_twr"
        self.assertEqual(logon.upper(), logon_validator(logon))

    def test_exceptions(self):
        with self.assertRaises(ValueError):
            logon = "EDMM_INVALIDSUFFIX"
            logon_validator(logon)
