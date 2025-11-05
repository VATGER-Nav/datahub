import os
import json
import toml
from unittest import TestCase

from datahub.views.station import Station


class TestStation(TestCase):
    def test_on_data(self):
        """testing by creating objects from the current data"""

        base_dir = "data"
        folders = ["edgg", "edww", "edmm"]

        for folder in folders:
            folder_path = os.path.join(base_dir, folder)
            if os.path.exists(folder_path):
                # print(f"Reading JSON files from folder: {folder_path}")
                read_json_files_in_folder(folder_path)
            else:
                print(f"Folder does not exist: {folder_path}")


def parse_json(data):
    test = []
    for element in data:
        station = Station.from_dict(element)
        test.append(station)

    for element in test:
        station_dict = station.model_dump(exclude_none=True)
        # print(station_dict)
        # print(
        #     toml.dumps(
        #         station_dict,
        #     )
        # )


def read_json_files_in_folder(folder_path):
    # Walk through the directory tree
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                # print(f"Reading file: {file_path}")
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)

                    parse_json(data)
