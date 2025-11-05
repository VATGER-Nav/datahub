from unittest import TestCase

from datahub.classes.datahub import Datahub


class TestDatahub(TestCase):
    def test_sort_data(self):
        """read the data and sort it, export it sorted"""
        Datahub().sort_data()

    def test_check_data(self):
        """only check the data for validity"""
        Datahub().check_data()

    def test_combine_data(self):
        """test the data combination"""
        Datahub().combine_data()
