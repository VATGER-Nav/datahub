from unittest import TestCase

from datahub.functions.sort_station import sort_stations
from datahub.views.station import Station


class TestDatahub(TestCase):
    def test_sort_station(self):
        stations = [
            Station(
                logon="EDDL_CTR",
                frequency="123",
                abbreviation="ABC",
                description=None,
                schedule_show_always=None,
                schedule_show_booked=None,
                relevant_airports=None,
                gcap_status="1",
                s1_twr=True,
            ),
            Station(
                logon="EDDL_B_TWR",
                frequency="124",
                abbreviation="DEF",
                description=None,
                schedule_show_always=None,
                schedule_show_booked=None,
                relevant_airports=None,
                gcap_status="AFIS",
                s1_twr=True,
            ),
            Station(
                logon="EDDL_A_TWR",
                frequency="125",
                abbreviation="XYZ",
                description=None,
                schedule_show_always=None,
                schedule_show_booked=None,
                relevant_airports=None,
                gcap_status=None,
                s1_twr=False,
            ),
            Station(
                logon="EDDL_RMP",
                frequency="126",
                abbreviation="ABC",
                description=None,
                schedule_show_always=None,
                schedule_show_booked=None,
                relevant_airports=None,
                gcap_status="2",
                s1_twr=False,
            ),
        ]

        sorted_stations = sort_stations(stations)

        self.assertEqual(sorted_stations[0].logon, stations[3].logon)
        self.assertEqual(sorted_stations[1].logon, stations[2].logon)
        self.assertEqual(sorted_stations[2].logon, stations[1].logon)
        self.assertEqual(sorted_stations[3].logon, stations[0].logon)
