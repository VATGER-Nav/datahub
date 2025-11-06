import json
import unittest
from pathlib import Path

from datahub.views.station import Station


class TestStation(unittest.TestCase):
    def setUp(self):
        self.valid_station_data = {
            "logon": "EDDF_TWR",
            "frequency": "118.500",
            "abbreviation": "DFT",
        }

    def test_from_dict_valid_data(self):
        station = Station(**self.valid_station_data)

        self.assertEqual(station.logon, "EDDF_TWR")
        self.assertEqual(station.frequency, "118.500")
        self.assertEqual(station.abbreviation, "DFT")

    def test_required_fields_missing(self):
        """Test that missing required fields raise ValidationError"""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            Station(frequency="118.500", abbreviation="DFT")

    def test_on_data(self):
        """testing by creating objects from the current data"""

        def parse_json(data):
            test = []
            for element in data:
                station = Station(**element)
                test.append(station)

            for element in test:
                element.model_dump(exclude_none=True)

        def read_json_files_in_folder(folder_path):
            folder = Path(folder_path)

            for file_path in folder.rglob("*.json"):
                # print(f"Reading file: {file_path}")
                with file_path.open("r") as json_file:
                    data = json.load(json_file)

                    parse_json(data)

        base_dir = Path("data")
        folders = ["edgg", "edww", "edmm"]

        for folder in folders:
            folder_path = base_dir / folder
            if Path(folder_path).exists():
                read_json_files_in_folder(folder_path)
            else:
                print(f"Folder does not exist: {folder_path}")

    def test_to_dict_excludes_none_values(self):
        """Test that to_dict excludes None values"""
        data = {
            "logon": "EDDF_TWR",
            "frequency": "118.500",
            "abbreviation": "DFT",
            "description": None,
        }
        station = Station(**data)
        result = station.to_dict()

        self.assertNotIn("description", result)
        self.assertIn("logon", result)

    def test_to_dict_excludes_empty_lists(self):
        """Test that to_dict excludes empty lists"""
        data = {
            "logon": "EDDF_TWR",
            "frequency": "118.500",
            "abbreviation": "DFT",
            "relevant_airports": [],
        }
        station = Station(**data)
        result = station.to_dict()

        self.assertNotIn("relevant_airports", result)

    def test_validate_relevant_airports_empty_list(self):
        """Test that empty relevant_airports list is handled correctly"""
        station = Station(
            logon="EDDF_TWR", frequency="118.500", abbreviation="DFT", relevant_airports=[]
        )

        self.assertEqual(station.relevant_airports, None)

    def test_validate_relevant_airports_none(self):
        """Test that None relevant_airports is handled correctly"""
        station = Station(
            logon="EDDF_TWR", frequency="118.500", abbreviation="DFT", relevant_airports=None
        )

        self.assertIsNone(station.relevant_airports)

    def test_filter_schedule_show_booked_removes_duplicates(self):
        """Test that schedule_show_booked filters out entries from schedule_show_always"""
        station = Station(
            logon="EDDF_TWR",
            frequency="118.500",
            abbreviation="DFT",
            schedule_show_always=["EDGG"],
            schedule_show_booked=["EDWW", "EDGG"],
        )

        self.assertNotIn("EDGG", station.schedule_show_booked)
        self.assertIn("EDWW", station.schedule_show_booked)

    def test_validate_cpdlc_login_valid(self):
        """Test that valid 4-character cpdlc_login is accepted"""
        station = Station(
            logon="EDDF_TWR", frequency="118.500", abbreviation="DFT", cpdlc_login="EDDF"
        )

        self.assertEqual(station.cpdlc_login, "EDDF")

    def test_validate_cpdlc_login_invalid_length(self):
        """Test that invalid cpdlc_login length raises ValueError"""
        with self.assertRaises(ValueError):
            Station(logon="EDDF_TWR", frequency="118.500", abbreviation="DFT", cpdlc_login="EDD")

    def test_gcap_status_invalid_value(self):
        """Test that invalid gcap_status value raises ValidationError"""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            Station(logon="EDDF_TWR", frequency="118.500", abbreviation="DFT", gcap_status="3")

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None"""
        station = Station(logon="EDDF_TWR", frequency="118.500", abbreviation="DFT")

        self.assertIsNone(station.description)
        self.assertIsNone(station.schedule_show_always)
        self.assertIsNone(station.relevant_airports)
        self.assertIsNone(station.gcap_status)


if __name__ == "__main__":
    unittest.main()
