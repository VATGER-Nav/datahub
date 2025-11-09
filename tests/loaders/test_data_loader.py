import json
import tempfile
import unittest
from pathlib import Path

import toml

from datahub.loaders.data_loader import DataLoader
from datahub.views.data_source import DataSource
from datahub.views.station import Station


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory structure with test files"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)

        self._create_test_files()

    def tearDown(self):
        """Clean up temporary directory"""
        self.temp_dir.cleanup()

    def test_on_data(self):
        DataLoader.load("data/", exclude_folders={"event_schedules", "topsky"})

    def _create_test_files(self):
        """Create test JSON and TOML files"""
        # Create folders
        folder1 = self.data_dir / "edgg"
        folder2 = self.data_dir / "edww"
        excluded_folder = self.data_dir / "temp"

        folder1.mkdir()
        folder2.mkdir()
        excluded_folder.mkdir()

        # Sample station data
        station1_data = {
            "logon": "EDDF_TWR",
            "frequency": "118.500",
            "abbreviation": "TWR",
            "description": "Frankfurt Tower",
        }

        station2_data = {
            "logon": "EDDS_APP",
            "frequency": "119.850",
            "abbreviation": "APP",
            "description": "Stuttgart Approach",
        }

        station3_data = {
            "logon": "EDGG_CTR",
            "frequency": "135.725",
            "abbreviation": "CTR",
            "description": "Langen Control",
        }

        # Create JSON file with single station
        with Path.open(folder1 / "station1.json", "w") as f:
            json.dump(station1_data, f)

        # Create JSON file with list of stations
        with Path.open(folder1 / "stations_list.json", "w") as f:
            json.dump([station2_data, station3_data], f)

        # Create TOML file
        with Path.open(folder2 / "station2.toml", "w") as f:
            toml.dump(station1_data, f)

        # Create file in excluded folder
        with Path.open(excluded_folder / "excluded.json", "w") as f:
            json.dump(station1_data, f)

        # Create a non-JSON/TOML file (should be ignored)
        with Path.open(folder1 / "readme.txt", "w") as f:
            f.write("This should be ignored")

    def test_load_returns_list_of_data(self):
        """Test that load returns a list of Data objects"""
        result = DataLoader.load(self.data_dir)

        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, DataSource) for item in result))

    def test_load_finds_all_files(self):
        """Test that all valid files are loaded"""
        result = DataLoader.load(self.data_dir, exclude_folders={"temp"})

        # Should find 3 files (station1.json, stations_list.json, station2.toml)
        # but not excluded.json or readme.txt
        self.assertEqual(len(result), 3)

    def test_load_parses_json_single_station(self):
        """Test parsing JSON file with single station"""
        result = DataLoader.load(self.data_dir)

        # Find the station1.json result
        station1_result = next((item for item in result if "station1.json" in item.source), None)

        self.assertIsNotNone(station1_result)
        self.assertEqual(len(station1_result.data), 1)
        self.assertEqual(station1_result.data[0].logon, "EDDF_TWR")

    def test_load_parses_json_list_of_stations(self):
        """Test parsing JSON file with list of stations"""
        result = DataLoader.load(self.data_dir)

        # Find the stations_list.json result
        list_result = next((item for item in result if "stations_list.json" in item.source), None)

        self.assertIsNotNone(list_result)
        self.assertEqual(len(list_result.data), 2)
        self.assertEqual(list_result.data[0].logon, "EDDS_APP")
        self.assertEqual(list_result.data[1].logon, "EDGG_CTR")

    def test_load_parses_toml(self):
        """Test parsing TOML file"""
        result = DataLoader.load(self.data_dir)

        # Find the station2.toml result
        toml_result = next((item for item in result if "station2.toml" in item.source), None)

        self.assertIsNotNone(toml_result)
        self.assertEqual(len(toml_result.data), 1)
        self.assertEqual(toml_result.data[0].logon, "EDDF_TWR")

    def test_load_excludes_folders(self):
        """Test that excluded folders are skipped"""
        result = DataLoader.load(self.data_dir, exclude_folders={"temp"})

        # Should not find excluded.json
        excluded_found = any("excluded.json" in item.source for item in result)
        self.assertFalse(excluded_found)

    def test_load_with_multiple_excluded_folders(self):
        """Test excluding multiple folders"""
        result = DataLoader.load(self.data_dir, exclude_folders={"temp", "edww"})

        # Should only find files from edgg folder
        self.assertTrue(all("edgg" in item.source for item in result))

    def test_load_ignores_non_json_toml_files(self):
        """Test that non-JSON/TOML files are ignored"""
        result = DataLoader.load(self.data_dir)

        # Should not find readme.txt
        txt_found = any("readme.txt" in item.source for item in result)
        self.assertFalse(txt_found)

    def test_load_relative_path_correct(self):
        """Test that source paths are relative to data_dir"""
        result = DataLoader.load(self.data_dir, exclude_folders={"temp"})

        for item in result:
            # Path should not be absolute
            self.assertFalse(Path(item.source).is_absolute())
            # Path should start with folder name
            self.assertTrue(item.source.startswith("edgg") or item.source.startswith("edww"))

    def test_load_with_empty_directory(self):
        """Test loading from empty directory"""
        empty_dir = self.data_dir / "empty"
        empty_dir.mkdir()

        result = DataLoader.load(empty_dir)

        self.assertEqual(len(result), 0)

    def test_parse_file_with_unsupported_extension(self):
        """Test _parse_file with unsupported file extension"""
        txt_file = self.data_dir / "edgg" / "test.txt"
        with Path.open(txt_file, "w") as f:
            f.write("some text")

        result = DataLoader._parse_file(txt_file)

        self.assertEqual(result, [])

    def test_load_accepts_string_path(self):
        """Test that load accepts string paths"""
        result = DataLoader.load(str(self.data_dir))

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_load_accepts_path_object(self):
        """Test that load accepts Path objects"""
        result = DataLoader.load(Path(self.data_dir))

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_data_contains_station_objects(self):
        """Test that Data objects contain Station instances"""
        result = DataLoader.load(self.data_dir)

        for data_item in result:
            self.assertTrue(all(isinstance(s, Station) for s in data_item.data))


if __name__ == "__main__":
    unittest.main()
