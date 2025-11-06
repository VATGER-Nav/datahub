import json
from pathlib import Path
from unittest import TestCase

from datahub.views.station import Station


class TestStation(TestCase):
    def test_on_data(self):
        """testing by creating objects from the current data"""

        base_dir = Path("data")
        folders = ["edgg", "edww", "edmm"]

        for folder in folders:
            folder_path = base_dir / folder
            if Path(folder_path).exists():
                read_json_files_in_folder(folder_path)
            else:
                print(f"Folder does not exist: {folder_path}")

    def test_dict(self):
        dct = {"logon": "EDDL_TWR", "frequency": "118.305", "abbreviation": "DLT"}

        Station(**dct)


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
